from datetime import timedelta,timezone
from app import celery, app
from app import db
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from Models import Users,CompletedBook,UserFeedback,Cart,Section
from datetime import datetime, timedelta
from flask import render_template
from celery.schedules import crontab
from collections import defaultdict
from collections import defaultdict
from operator import itemgetter


SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_EMAIL = "sender@gmail.com"
SENDER_PASSWORD = "password"



def send_mail(to, subject, msg_body):
    msg = MIMEMultipart()
    msg["To"] = to
    msg["From"] = SENDER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(msg_body, "html"))
    server = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    server.login(user=SENDER_EMAIL, password=SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()



def get_inactive_users():
    inactive_users = Users.query.filter(Users.last_login < (datetime.now().date())).all()
    return inactive_users


def generate_monthly_report(user):
    # Define the start and end of the period
    end = datetime.today().date()
    start = (datetime.today() - timedelta(days=30)).date()


    book_completed = CompletedBook.query.filter(
        CompletedBook.user_id == user.user_id,
        CompletedBook.return_date >= start,
        CompletedBook.return_date <= end,
        CompletedBook.revoked == False
    ).all()

    feedbacks = UserFeedback.query.filter(
        UserFeedback.user_id == user.user_id,
        UserFeedback.feedback_date >= start,
        UserFeedback.feedback_date <= end
    ).all()

    book_completed_data = [
        {
            'book_name': book.book_name,
            'return_date': book.return_date,
            'section_name': book.section_name,
            'issued_for': (book.return_date - book.date_issued).days,
            'user_name': user.user_name
        }
        for book in book_completed
    ]

    # print(book_issued_data , 'book_issued_data')
   
    feedbacks_data = [
        {
            'feedback_text': feedback.feedback,
            'feedback_date': feedback.feedback_date,
            'rating': feedback.rating
        }
        for feedback in feedbacks
    ]

    # print(book_completed_data, 'book_completed_data')
    # print(feedbacks, 'feedbacks')
    # Format the report content

    report_content = {
        # 'book_issued': book_issued_data,
        'book_completed': book_completed_data,
        'feedbacks': feedbacks_data,
        'report_period': f"{start.strftime('%B %d, %Y')} - {end.strftime('%B %d, %Y')}"
    }

    # Render the report template (this would be an HTML template)
    return render_template('monthly_report.html', **report_content)



@celery.task(name='send_daily_reminder')
def send_daily_reminder():
    with app.app_context():
        users = get_inactive_users()
        for user in users:
            print(user.email, 'email')
            if user.in_role('user') :
                sub = "Forgot to read book!!!"
                body = "Never forget to read newbooks. Have a great day."
                send_mail(user.email, sub, body)
        return 'Daily reminders sent'
    

@celery.task(name='revoke book acess')
def revoke_book_access():
    with app.app_context():
        now = datetime.now(timezone.utc).date()
        carts = Cart.query.filter(Cart.approved == 1 , Cart.date_end < now ).all()
        # carts = Cart.query.filter(Cart.approved == 1 ).all()
        books_delted = []
        for cart in carts:
            print("......................")
            print(cart.cart_user.user_name , cart.date_end , datetime.now() ,cart.book_info.name)
            books_delted.append({'book_name':cart.book_info.name ,"end_date":cart.date_end , 'today':now })
            print("............................")
            completed_book = CompletedBook(
                user_id=cart.cart_user.user_id,
                book_name=cart.book_info.name,
                section_name=cart.book_info.section.name,
                date_issued=cart.date_issued,
                return_date=cart.date_end,
                revoked=True,
                content=cart.book_info.content,
                author=cart.book_info.author,
            )
            db.session.add(completed_book)
            db.session.delete(cart)
            db.session.commit()
    return books_delted



@celery.task(name='send_monthly_report')
def send_monthly_report():
    with app.app_context():
        users = Users.query.all()
        for user in users:
            print('Sending monthly report to', user.email)
            if user.in_role('user'):
                sub = "MONTHLY REPORT"
                body = generate_monthly_report(user)
                send_mail(user.email, sub, body)
        # send_mail("rksnsneno@gmail.com", "Monthly Report", "hello we have bought two harry potter books")
        return 'Monthly reports sent'



@celery.task(name='books_issued_per_day')
def book_issued_per_day():
    with app.app_context():
        completed_books = CompletedBook.query.all()
        approved_carts = Cart.query.filter(Cart.approved == 1).all()
        data = []
        
        for book in completed_books:
            data.append({
                'book_name': book.book_name,
                'date_issued': book.date_issued
            })

        for cart in approved_carts:
            data.append({
                'book_name': cart.book_info.name,
                'date_issued': cart.date_issued
            })

        books_issued_per_day = defaultdict(int)
        for entry in data:
            issued_date = entry['date_issued']
            books_issued_per_day[issued_date] += 1

        sorted_data = sorted(books_issued_per_day.items(), key=itemgetter(0))
                
            # Print the sorted data
        data = {
            'date':[],
            'books_issued':[]
        }

        for date, count in sorted_data:
            data['date'].append(date)
            data['books_issued'].append(count)

        return data
    


@celery.task(name='top_popular_books')
def top_five_books():
    with app.app_context():
        feedbacks = UserFeedback.query.all()

        # Dictionary to accumulate ratings and counts for each book
        book_ratings = defaultdict(lambda: {'total_rating': 0, 'count': 0})

        # Collecting data from feedbacks
        for feedback in feedbacks:
            book_name = feedback.book_feedbacks.name
            book_ratings[book_name]['total_rating'] += feedback.rating
            book_ratings[book_name]['count'] += 1


        result = []

        # Calculating average ratings
        for book_name, rating_data in book_ratings.items():
            avg_rating = rating_data['total_rating'] / rating_data['count']
            result.append((book_name, avg_rating))

        return sorted(result, key=lambda x: x[1], reverse=True)[:5]



@celery.task(name='top_selling_books')
def top_selling_books() : 
    with app.app_context() : 
        book_issued = CompletedBook.query.all()

        data = {} ## book name and the count for book issued 

        for book in book_issued:
            if book.book_name not in data:
                data[book.book_name] = 1
            else:
                data[book.book_name] += 1

        book_issued = Cart.query.filter(Cart.approved == 1).all()

        for book in book_issued : 
            if book.book_info.name not in data:
                data[book.book_info.name] = 1
            else:
                data[book.book_info.name] += 1

        book = []
        count = []

        for key, value in data.items():
            book.append(key)
            count.append(value)
        
        data = sorted(list(zip(book, count)), key=lambda x: x[1], reverse=True)[:5]

    return data



        
@celery.task(name='Genres Distribution')
def genre_distribution():
    with app.app_context():
        data = {}
        Sections = Section.query.all()
        for section in Sections:
            if section.name not in data:
                data[section.name] = len(section.books)
            else:
                data[section.name] += len(section.books)
    
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

        store = {'section': [], 'count': []}

        for i in sorted_data:
            store['section'].append(i[0])
            store['count'].append(i[1])

        return store  # No need to sort again since it's already sorted



# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     print("Setting up periodic tasks...")
#     sender.add_periodic_task(
#         60.0,  # Interval in seconds for testing
#         send_daily_reminder.s(),
#         name='send_daily_reminder every 30 seconds'
#     )

#     sender.add_periodic_task(
#         60.0,  # Interval in seconds for testing
#         send_monthly_report.s(),
#         name='send_monthly_report every 60 seconds'
#     )

#     sender.add_periodic_task(
#         120.0,
#         revoke_book_access.s(),
#         name='revoke_book_access in every 5 mins'
#     )
#     print("Periodic tasks have been set up.")



@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("Setting up periodic tasks...")
    sender.add_periodic_task(
        crontab(hour=18, minute=0),
        send_daily_reminder.s(),
        name='send_daily_reminder every 6pm '
    )

    sender.add_periodic_task(
        crontab(day_of_month=1 ,hour=0, minute=0),
        send_monthly_report.s(),
        name='send_monthly_report every monthly'
    )

    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        revoke_book_access.s(),
        name='revoke_book_access at midnight'
    )
    print("Periodic tasks have been set up.")