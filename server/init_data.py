# from app import db, app
from Models import Users, Role, Book, Section, Cart, CompletedBook, UserFeedback
from datetime import date,timedelta
from random import randint
from sqlalchemy.orm.exc import NoResultFound


content1 = """A special 25th anniversary edition of the extraordinary international bestseller, including a new Foreword by Paulo Coelho.

Combining magic, mysticism, wisdom and wonder into an inspiring tale of self-discovery, The Alchemist has become a modern classic, selling millions of copies around the world and transforming the lives of countless readers across generations.

Paulo Coelho's masterpiece tells the mystical story of Santiago, an Andalusian shepherd boy who yearns to travel in search of a worldly treasure. His quest will lead him to riches far different—and far more satisfying—than he ever imagined. Santiago's journey teaches us about the essential wisdom of listening to our hearts, of recognizing opportunity and learning to read the omens strewn along life's path, and, most importantly, to follow our dreams.

"""

content2= """Newlyweds Tricia and Ethan are searching for the house of their dreams.

But when they visit the remote manor that once belonged to Dr. Adrienne Hale, a renowned psychiatrist who vanished without a trace four years earlier, a violent winter storm traps them at the estate… with no chance of escape until the blizzard comes to an end.

In search of a book to keep her entertained until the snow abates, Tricia happens upon a secret room. One that contains audio transcripts from every single patient Dr. Hale has ever interviewed. As Tricia listens to the cassette tapes, she learns about the terrifying chain of events leading up to Dr. Hale’s mysterious disappearance.

Tricia plays the tapes one by one, late into the night. With each one, another shocking piece of the puzzle falls into place, and Dr. Adrienne Hale’s web of lies slowly unravels.

And then Tricia reaches the final cassette.
"""

content3 = """
Journalist Ben Harper is on his way home when he sees the flames in the churchyard. The derelict community centre is on fire. And somebody is trapped inside.

With Ben's help the person escapes, only to flee the scene before they can be identified. Now the small town of Haddley is abuzz with rumours. Was this an accident, or arson?

Then a skeleton is found in the burnt-out foundations.

And when the identity of the victim is revealed, Ben is confronted with a crime that is terrifyingly close to home. As he uncovers a web of deceit and destruction that goes back decades, Ben quickly learns that in this small town, everybody has something to hide.
"""


def init_data(app, db):
    with app.app_context():
        db.create_all()
        try:
            # Create roles if they don't already exist
            existing_roles = {role.role_id for role in Role.query.all()}
            
            if 'user' not in existing_roles:
                role1 = Role(role_id='user', name='user', description='User can only read and request books')
                db.session.add(role1)
            
            if 'librarian' not in existing_roles:
                role2 = Role(role_id='librarian', name='librarian', description='Librarian can add books and do management of library')
                db.session.add(role2)

            db.session.commit()

            # Create users if they don't already exist
            existing_users = {user.user_name for user in Users.query.all()}

            if 'zainab' not in existing_users:
                user1 = Users(user_name='zainab', user_password='$2b$12$jFZxmyNY8.W6u5Ir/DtlQOLYXicOsrGebZ53qQ4BILDuH0rtIwyt2',
                              email='rksnsneno@example.com', active=True, last_login=date.today())
                db.session.add(user1)
            

            if 'adminrohit' not in existing_users:
                user2 = Users(user_name='adminrohit', user_password='$2b$12$8f8H6KbXluk8FVFnfzLm3uNHgxMiURrXJT26ui5PZ/bYJ6Ndz9beS',
                              email='admin123@gmail.com', active=True, last_login=date.today())
                db.session.add(user2)


            if 'Neha' not in existing_users:
                user3 = Users(user_name='Neha', user_password='$2b$12$rtgvVBhKcMdz6YLj4iJxMu/9.7g5z5//gK5ldcIFy0wd6HTv2qrI2',
                              email='neha@gmail.com' , active=True, last_login=date.today()-timedelta(days=10))

            user4 = Users(user_name='maish_rider', user_password='$2b$12$N2oP6uhevbFVio4acEcGe.Wu.REx/SGtVYZGC8p88ShtnrIdz04yi',
                          email='manish@gmail.com', active=True, last_login=date.today()-timedelta(days=10))
            db.session.add(user3)
            db.session.add(user4)

            for i in range(1,100):
                user = Users(user_name=f'fake_user_{i}', user_password=f'$2b$12$jFZxmyNY8.W6u5Ir/DtlQOLYXicOsrGebZ53qQ4BILDuH0rtIwyt2{i}',
                              email=f'fake_user_{i}@example.com', active=True, last_login=date.today())
                db.session.add(user)

            db.session.commit()

            # Associate users with roles
            user1 = Users.query.filter_by(user_name='zainab').first()
            user2 = Users.query.filter_by(user_name='adminrohit').first()
            user3 = Users.query.filter_by(user_name='Neha').first()
            user4 = Users.query.filter_by(user_name='maish_rider').first()


            role1 = Role.query.filter_by(role_id='user').first()
            role2 = Role.query.filter_by(role_id='librarian').first()


            for i in range(1,100):
                user = Users.query.filter_by(user_name=f'fake_user_{i}').first()
                user.roles.append(role1)



            if role1 and user1:
                user1.roles.append(role1)
            
            if role2 and user2:
                user2.roles.append(role2)

            if role1 and user2:
                user2.roles.append(role1)

            if role1 and user3: 
                user3.roles.append(role1)

            if role1 and user4:
                user4.roles.append(role1)

            db.session.commit()

            # Creating sections
            section1 = Section(name='Self Help', description='Description of Section 1')
            section2 = Section(name='Thriller', description='Description of Section 2')
            section3 = Section(name='Romance', description='Description of Section 3')
            section4 = Section(name='Fiction', description='Description of Section 4')

            db.session.add(section1)
            db.session.add(section2)
            db.session.add(section3)
            db.session.add(section4)
            db.session.commit()

            
            book1 = Book(name='Alchemist', content=content1, author='Paulo Coelho', book_loc_url='alchemist.jpg',
                         section_id=section1.id, price=200, publish_date=date.today() - timedelta(days=100) , book_pdf_loc_url='The_alchemist.pdf')
            
            book2 = Book(name='Eleven Minutes', content=content2, author='John Cleese', book_loc_url='Eleven Minutes.jpg',
                         section_id=section2.id, price=5, publish_date=date.today() - timedelta(days=200) , book_pdf_loc_url='The_alchemist.pdf')
            
            book3 = Book(name='Shogun', content=content3, author='Hajime Isayama', book_loc_url='Shogun.jpg',
                         section_id=section1.id, price=5, publish_date=date.today() - timedelta(days=400) , book_pdf_loc_url='The_alchemist.pdf')
            

            db.session.add(book1)
            db.session.add(book2)
            db.session.add(book3)

            for section in [section1, section2, section3, section4]:
                section_name = section.name
                for i in range(1,6):
                    book_name = f'Book {section_name} {i}'
                    book_content = f'Content of {book_name}'
                    book = Book(name=book_name, content=content3, author=f'Hajime {i}', book_loc_url='Shogun.jpg',
                        section_id=section.id, price=i*20 , publish_date=date.today() - timedelta(days=i*100) , book_pdf_loc_url='The_alchemist.pdf')
                    db.session.add(book)


            db.session.commit()

            # Creating carts
            cart1 = Cart(cart_user_id=user1.user_id, book_id=book1.id, date_issued=date.today() - timedelta(days=8),
                         date_end=date.today() + timedelta(days=0), approved=True)
            cart2 = Cart(cart_user_id=user1.user_id, book_id=book2.id, date_issued=date.today() - timedelta(days=5),
                         date_end=date.today() + timedelta(days=1), approved=True)
            cart3 = Cart(cart_user_id=user1.user_id, book_id=book3.id, date_issued=date.today() - timedelta(days=3),
                         date_end=date.today() - timedelta(days=1), approved=True)

            db.session.add(cart1)
            db.session.add(cart2)
            db.session.add(cart3)
            db.session.commit()

            # Creating completed books
            completed_book1 = CompletedBook(user_id=user1.user_id, book_name='Seven Layers', section_name='Thriller',
                                            content='Content of Completed Book 1', author='Pico de Gallos',
                                            date_issued=date.today() - timedelta(days=10),
                                            return_date=date.today() - timedelta(days=3), revoked=False)
            
            completed_book2 = CompletedBook(user_id=user2.user_id, book_name='Ghost Diaries', section_name='Crime',
                                            content='Content of Completed Book 2', author='Taaki Suzuki',
                                            date_issued=date.today() - timedelta(days=11),
                                            return_date=date.today() - timedelta(days=2), revoked=False)


            db.session.add(completed_book1)
            db.session.add(completed_book2)

            today_date = date.today()

            for i in range(180, 8, -1):
                date_issued = today_date - timedelta(days=i)
                date_end = today_date - timedelta(days=i-8)

                book_to_issue_in_a_day = randint(5, 10)  # number of books to issue in a day
                book_ids = {randint(1, 20) for _ in range(book_to_issue_in_a_day)}  # unique book ids
                user_ids = {randint(5, 99) for _ in range(book_to_issue_in_a_day)}  # unique user ids

                user_book_combinations = set()

                while len(user_book_combinations) < len(book_ids):
                    user = randint(0, len(user_ids)-1)
                    book = randint(0, len(book_ids)-1)
                    if (user, book) not in user_book_combinations:
                        user_book_combinations.add((user, book))

                for user_index, book_index in user_book_combinations : 
                    try:
                        user = Users.query.filter_by(user_id=list(user_ids)[user_index]).one()
                        book = Book.query.filter_by(id=list(book_ids)[book_index]).one()

                        completed_book = CompletedBook(
                            user_id=user.user_id,
                            book_name=book.name,
                            section_name=book.section.name,
                            content=book.content,
                            author=book.author,
                            date_issued=date_issued,
                            return_date=date_end,
                            revoked=False
                        )

                        db.session.add(completed_book)

                    except NoResultFound:
                        print(f"User or Book not found for indices user_index={user_index}, book_index={book_index}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")
                        db.session.rollback()

            db.session.commit()

            # Creating feedbacks
            feedback1 = UserFeedback(user_id=user1.user_id, book_id=book1.id, rating=5, feedback="I love the book!",
                                     feedback_date=date.today() - timedelta(days=10))
            feedback2 = UserFeedback(user_id=user1.user_id, book_id=book1.id, rating=4, feedback="I enjoyed the book!",
                                     feedback_date=date.today() - timedelta(days=5))
            feedback3 = UserFeedback(user_id=user1.user_id, book_id=book1.id, rating=3, feedback="I didn't like the book!",
                                     feedback_date=date.today() - timedelta(days=3))
            feedback4 = UserFeedback(user_id=user1.user_id, book_id=book1.id, rating=5, feedback="I love the book!",
                                     feedback_date=date.today() - timedelta(days=2))
            feedback5 = UserFeedback(user_id=user1.user_id, book_id=book2.id, rating=4, feedback="I enjoyed the book!",
                                     feedback_date=date.today() - timedelta(days=1))
            
            db.session.add(feedback1)
            db.session.add(feedback2)
            db.session.add(feedback3)
            db.session.add(feedback4)
            db.session.add(feedback5)

            feedbacks = ['I love the book!', 'I enjoyed the book!', 'I didn\'t like the book!' , 'Good book!' , 'Bad book!']
            ratings = [5, 4, 2, 4, 1]

            

            for completed_book in CompletedBook.query.all():
                feed_index = randint(0, 4)  # Select a random feedback index
                
                book = Book.query.filter_by(name=completed_book.book_name).first()
                
                if book is None:
                    print(f"Book with name '{completed_book.book_name}' not found. Skipping feedback for this entry.")
                    continue 
                
                # Create a new UserFeedback entry
                feedback = UserFeedback(
                    user_id=completed_book.user_id,
                    book_id=book.id,
                    rating=ratings[feed_index],
                    feedback=feedbacks[feed_index],
                    feedback_date=completed_book.return_date
                )
                
                # Add the feedback to the session
                db.session.add(feedback)

            # Commit all changes to the database
            db.session.commit()

            print("Entries added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback()