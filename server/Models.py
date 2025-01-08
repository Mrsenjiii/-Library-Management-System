from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy import and_
from datetime import datetime,timezone

db = SQLAlchemy()


user_role_association = db.Table('user_role_association',
                                 db.Column('user_id', db.Integer(),
                                           db.ForeignKey('users.user_id')),
                                 db.Column('role_id', db.String(10),
                                           db.ForeignKey('role.role_id'))
                                 )


class Users(db.Model):
    user_id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    user_password = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    active = db.Column(db.Boolean(), nullable=False)
    last_login = db.Column(db.Date(), nullable=True)
    Users_in_carts = db.relationship('Cart', backref='cart_user')
    user_feedbacks = db.relationship('UserFeedback', backref='user_feedbacks')

    def __repr__(self):
        return f"( id : {self.user_id}, name : {self.user_name} )"

    def roles_name(self):
        return [role.name for role in self.roles]
    
    def in_role(self, role):
        if role in self.roles_name():
            return True
        else:
            return False



class Role(db.Model):
    role_id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String())

    users_under_role = db.relationship(
        'Users', secondary=user_role_association, backref='roles')

    def __repr__(self):
        return f"Role(role_id={self.role_id}, name={self.name})"


class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publish_date = db.Column(db.Date(), nullable=True, default=None)
    book_loc_url = db.Column(db.Text(), nullable=False)
    book_pdf_loc_url = db.Column(db.Text(), nullable=False)
    # Automatically set the current date for book_date
    book_date = db.Column(db.Date(), nullable=False, default=lambda: datetime.now(timezone.utc).date())
    section_id = db.Column(db.Integer(), ForeignKey('section.id'), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    users_under_role = db.relationship('Cart', backref='book_info')
    book_feedbacks = db.relationship('UserFeedback', backref='book_feedbacks')
    def __repr__(self):
        return f"<Book {self.name} by {self.author} (Published: {self.publish_date})>"


class Section(db.Model):
    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    books = db.relationship('Book', backref='section', lazy=True)


class Cart(db.Model):
    """
            user --- one to many --- Cart  # a cart can be created by only one user   
            book -- one to many --- Cart # every cart row has only one product   
    """
    cart_id = db.Column(db.Integer(), primary_key=True)
    cart_user_id = db.Column(db.Integer(), ForeignKey(
        'users.user_id'), nullable=False)
    book_id = db.Column(db.Integer(), ForeignKey('book.id'), nullable=False)
    date_issued = db.Column(db.Date(), nullable=False) 
    date_end = db.Column(db.Date(), nullable=False)
    approved = db.Column(db.Boolean(), nullable=False) # 0 = not approved, 1 = approved
    def __repr__(self):
        return f"( id : {self.cart_id}, user_id : {self.cart_user_id}, book_id : {self.book_id} )"


class UserFeedback(db.Model):
    feedback_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), ForeignKey(
        'users.user_id'), nullable=False)
    book_id = db.Column(db.Integer(), ForeignKey('book.id'), nullable=False)
    rating = db.Column(db.Integer(), nullable=False)
    feedback = db.Column(db.Text(), nullable=False)
    feedback_date = db.Column(db.Date(), nullable=False , default=lambda: datetime.now(timezone.utc).date())
    def __repr__(self):
        return f"( id : {self.feedback_id}, user_id : {self.user_id}, book_id : {self.book_id} )"


class CompletedBook(db.Model):
    """"""
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), ForeignKey(
        'users.user_id'), nullable=False)
    book_name = db.Column(db.String(100), nullable=False)
    section_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date_issued = db.Column(db.Date(), nullable=False)# start of reading.
    return_date = db.Column(db.Date(), nullable=False) # end of reading or revoked date. if revoked is true then return_date = revoked_date
    revoked = db.Column(db.Boolean(), nullable=False , default=False)


    def __repr__(self):
        return f"( id : {self.id}, user_id : {self.user_id}, book_name : {self.book_name} )"