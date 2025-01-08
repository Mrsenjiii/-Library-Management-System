# # 
# book = ['book1', 'book2', 'book3', 'book4', 'book5']
# count = [4,2,1,8,9]
from app import app
from Models import *

# data = sorted(list(zip(book, count)), key=lambda x: x[1], reverse=True)[:5]


# store = { 'book':[],'count':[]}

# for i in data:
#     store['book'].append(i[0])
#     store['count'].append(i[1])


# print(store)


# data = {'a':3, 'b':6, 'c':8, 'd':0, 'e':55, 'f':5, 'g':5, 'h':5, 'i':5, 'j':5, 'k':5, 'l':5, 'm':5, 'n':5, 'o':5, 'p':5, 'q':5, 'r':5, 's':5, 't':5, 'u':5, 'v':5, 'w':5, 'x':5, 'y':5, 'z':5}
# a = sorted(data.items(), key=lambda x: x[1], reverse=True)
# print(data.items())


# for i in range(100,1 ,-1):
#     print(i)
from random import randint
books_id = [randint(1, 10) for _ in range(10)]
books_id = list(set(books_id))
# books = Book.query.all()


user_id = [randint(3,99) for _ in range(20)  ] ### 
user_id = list(set(user_id))

li = []

# while len(li) < 10:
#     user = randint(0,len(user_id))
#     book = randint(0,len(books_id))
#     if (user,book) not in li:
#         li.append((user,book))

        

# print(li)

# li  = [(1,2)]

# if (1,2) not in li:
#     print('yes')
# else:
#     li.append((2,2))

# print(li)
# print(user_id)

from collections import defaultdict
from operator import itemgetter
def book_issed():
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

print(book_issed())






def popular_books():
    with app.app_context():
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

# print(popular_books())

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

        # Prepare the final output
        result = {
            'book': [],
            'avg_rating': []
        }

        # Calculating average ratings
        for book_name, rating_data in book_ratings.items():
            avg_rating = rating_data['total_rating'] / rating_data['count']
            result['book'].append(book_name)
            result['avg_rating'].append(avg_rating)

        return result

# print(top_five_books())




# @celery.task(name='Genres Distribution')
def genre_distribution():
    with app.app_context():
        data = {}

        Sections= Section.query.all()
        for section in Sections:
            if section.name not in data:
                data[section.name] = len(section.books)
            else:
                data[section.name] += len(section.books)
    

        data = sorted(data.items(), key=lambda x: x[1], reverse=True)

        store = { 'section':[],'count':[]} 

        for i in data : 
            store['section'].append(i[0])
            store['count'].append(i[1])

    return store

# print(genre_distribution())