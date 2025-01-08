from flask import  request, jsonify, abort
from Models import *
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from dateutil.parser import isoparse
from functools import wraps
from app import app,cache
from app import bcrypt
from datetime import timedelta,date
import os
from werkzeug.utils import secure_filename
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from bcrypt import checkpw
from tasks import   top_five_books, book_issued_per_day, genre_distribution,top_selling_books



# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}



    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def save_file(file):
    # Implement file saving logic here
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return filename


def librarian_role(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        print(current_user, 'current user')
        user = Users.query.get(current_user)
        if not user or "librarian" not in [role.name for role in user.roles]:
            return jsonify({"error": "Librarian required for this route"}), 403
        return fn(*args, **kwargs)
    return wrapper


def user_role(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        print(current_user, 'current user')
        user = Users.query.get(current_user)
        if not user or "user" not in [role.name for role in user.roles]:
            return jsonify({"error": "User required for this route"}), 403
        return fn(*args, **kwargs)
    return wrapper

def user_or_librarian_req(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        print(current_user, 'current user')
        user = Users.query.get(current_user)
        if not user or ("librarian" not in [role.name for role in user.roles] and "user" not in [role.name for role in user.roles]):
            return jsonify({"error": "Librarian or user required for this route"}), 403
        return fn(*args, **kwargs)
    return wrapper




################################################################# signup and login ########################


@app.route('/api/signup', methods=['POST'])
def signup():
    print('hellow world , request body: ', request.json)
    try:
        data = request.json
        # Validate required fields
        required_fields = ['user_name', 'user_password', 'user_role', 'email', 'active']
        if not all(data.get(key) for key in required_fields):
            return jsonify({'error': 'All required fields must be provided'}), 400

        # Check if username or email already exists
        existing_user = Users.query.filter_by(user_name=data['user_name']).first()
        existing_email = Users.query.filter_by(email=data['email']).first()

        if existing_user:
            return jsonify({"error": "Username already exists"}), 409
        if existing_email:
            return jsonify({"error": "Email already exists"}), 409

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(data['user_password']).decode('utf-8')
        # Create a new user object
        new_user = Users(
            user_name=data['user_name'],
            user_password=hashed_password,
            email=data['email'],
            active=data['active'],
            last_login = datetime.strptime('1900-01-01', '%Y-%m-%d').date()

        )

        existing_role = Role.query.filter_by(name=data['user_role']).first()
        new_user.roles.append(existing_role)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400  # Bad Request
    except Exception as e:
        # Log the exception or handle it appropriately
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500



@app.route('/' , methods=['GET'])
def home():
    return 'Hello, World!'



@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        print('keys: ', data.keys())
        print(data)

        if not all(data.get(key) for key in ['user_name', 'user_password', 'role_type']):
            return jsonify({'error': 'All required fields must be provided'}), 400

        user_name = data['user_name']
        entered_password = data['user_password'].encode('utf-8') 
        requested_role = data['role_type']

        user = Users.query.filter_by(user_name=user_name).first()

        if not user:
            return jsonify({"error": "Username does not exist in the database"}), 404

        # Verify the password
        hashed_password = user.user_password.encode('utf-8')  
        if not checkpw(entered_password, hashed_password):
            return jsonify({'error': 'Invalid credentials'}), 401

        
        user_roles = [role.name for role in user.roles]
        if requested_role not in user_roles:
            print('User roles:', user_roles)
            return jsonify({'error': 'User does not have the required role'}), 403

        # Generate JWT token
        access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(hours=2))
        print(access_token)
        print('User roles:', user_roles)

        user.last_login = datetime.now().date()
        db.session.commit()
        print(user.last_login ,'new login date')
        return jsonify({
            "access_token": access_token,
            "user_id": user.user_id,
            "user_role": user_roles
        }), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400  # Bad Request

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500




@app.route('/api/section', methods=['GET'])
@cache.cached(timeout=300)
@jwt_required()
def get_all_sections():

    try:
        sections = Section.query.all()
        return jsonify([{'id': section.id, 'name': section.name, 'description': section.description ,'number_of_books':len(section.books)}
                        for section in sections]), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
   


@app.route('/api/section/<int:section_id>', methods=['GET'])
# @cache.cached(timeout=300, key_prefix='books_in_section')
@jwt_required()
def get_section(section_id):
    try:
        section = Section.query.get(section_id)
        if section:
            print('cache hit')
            return jsonify({'id': section.id, 'name': section.name, 'description': section.description}), 200
        else:
            return jsonify({'message': 'Section not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500



@app.route('/api/section', methods=['POST'])
@app.route('/api/section/<int:section_id>', methods=['PUT', 'DELETE'])
@jwt_required()
@librarian_role
def handle_section(section_id=None):
    try:
        if request.method == 'POST':
            data = request.json
            print(data)
            if not all(data.get(key) for key in ['name', 'description']):
                raise ValueError("All required fields must be provided.")

            new_section = Section(
                name=data['name'],
                description=data['description']
            )

            db.session.add(new_section)
            db.session.commit()

            return jsonify({'message': 'Section created successfully'}), 201



        elif request.method == 'PUT':
            data = request.json
            section = Section.query.get(section_id)
            if not section:
                return jsonify({'message': 'Section not found'}), 404
            section.name = data.get('name', section.name)
            section.description = data.get('description', section.description)
            db.session.commit()

            return jsonify({'message': 'Section updated successfully'}), 200

        elif request.method == 'DELETE':
            section = Section.query.get(section_id)
            if not section:
                return jsonify({'message': 'Section not found'}), 404

            for book in section.books:
                carts = Cart.query.filter_by(book_id=book.id).all()
                feedbacksforbook = UserFeedback.query.filter_by(book_id=book.id).all()

                for cart in carts:
                    db.session.delete(cart)

                for feedback in feedbacksforbook:
                    db.session.delete(feedback)
            

                db.session.delete(book)
            db.session.delete(section)
            db.session.commit()
            return jsonify({'message': 'Section deleted successfully'}), 200


    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400  # Bad Request
    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500
    finally:
        cache.clear()


    

@app.route('/api/section/<int:section_id>/books', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)
def get_books_by_section(section_id):
    print('lets see if the result is cached or not')
    try:
        section = Section.query.get(section_id)
        if not section:
            return jsonify({'message': 'Section not found'}), 404
        books = section.books
        books_data = []
        for book in books:
            book_data = {
                'id': book.id,
                'name': book.name,
                'content': book.content,
                'section_id': book.section_id,
                'author': book.author,
                'price': book.price,
                'book_loc_url': book.book_loc_url,
                'book_pdf_loc_url': book.book_pdf_loc_url,
                'publish_date': book.publish_date,
                'genre': book.section.name,
            }
            books_data.append(book_data)
        return jsonify({'books': books_data}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500




########################################################### API Books ##################################


@app.route('/api/book', methods=['POST'])
@jwt_required()
@librarian_role
def add_book():
    try:
        # Extract data from request
        data = request.form.to_dict()
        print(data.keys())
        # Validate required fields
        required_fields = ['name', 'content', 'author', 'price', 'section_id' , 'publish_date' ]
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Handle PDF upload
        pdf_file = request.files.get('book_pdf')
        if not pdf_file : 
            return jsonify({'error': 'PDF file is required'}), 400
        pdf_filename = save_file(pdf_file)
        print(pdf_filename , 'pdf filenamme')
        


        image_file = request.files.get('book_image')
        if not image_file : 
            return jsonify({'error': 'Image file is required'}), 400
        image_filename = save_file(image_file)

   
        print(image_filename , 'image filename')
        # static/Maktub.jpg
        
        publish_date = datetime.fromisoformat(data.get('publish_date'))
        # Create new book instance
        new_book = Book(
            name=data['name'],
            content=data['content'],
            author=data['author'],
            price=float(data['price']),
            section_id=int(data['section_id']),
            publish_date=publish_date,
            book_loc_url=image_filename,  # Save the image file path in book_loc_url
            book_pdf_loc_url=pdf_filename
        )
        # Add new book to the database
        db.session.add(new_book)
        db.session.commit()

        cache.clear()
    except IntegrityError as ie:
        db.session.rollback()
        return jsonify({'error': 'Integrity error occurred', 'details': str(ie)}), 400
    
    except SQLAlchemyError as sae:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(sae)}), 500
    
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
    


@app.route('/api/book/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id=None):
    if request.method == 'GET':
        try : 
            if book_id is not None:
                book = Book.query.get(book_id)
                if not book:
                    return jsonify({'message': 'Book not found'}), 404
                book_data = {
                    'id': book.id,
                    'name': book.name,
                    'content': book.content,
                    'author': book.author,
                    'price': book.price,
                    'section_id': book.section_id,
                    'book_loc_url': book.book_loc_url,
                    'book_pdf_loc_url': book.book_pdf_loc_url,
                    'genre': book.section.name,
                    'publish_date': book.publish_date
                }
                return jsonify(book_data), 200
        except Exception as e:
            print(e)
            return jsonify({'error': 'An unexpected error occurred'}), 500



@app.route('/api/book/<int:book_id>', methods=['PUT', 'DELETE'])
@jwt_required()
@librarian_role
def manage_book(book_id=None):
    if request.method == 'PUT':
        try:
            data = request.form

            # Validate required fields
            if 'name' not in data or not data['name'].strip():
                return jsonify({'error': 'Book name is required'}), 400
            if 'author' not in data or not data['author'].strip():
                return jsonify({'error': 'Author name is required'}), 400
            if 'section_id' not in data or not data['section_id'].isdigit():
                return jsonify({'error': 'Valid section ID is required'}), 400
            if 'price' not in data or not data['price'].replace('.', '', 1).isdigit() or float(data['price']) < 0:
                return jsonify({'error': 'Valid price is required'}), 400
            if 'content' not in data or not data['content'].strip():
                return jsonify({'error': 'Book content is required'}), 400
            if 'publish_date' not in data or not data['publish_date']:
                return jsonify({'error': 'Publish date is required'}), 400
            
            publish_date = datetime.fromisoformat(data.get('publish_date')).date()
            print(publish_date)
            
            # Additional validation
            today = datetime.today().date()
            if publish_date > today : 
                return jsonify({'error': 'Publish date cannot be in the future'}), 400

            book = Book.query.get(book_id)
            if not book : 
                return jsonify({'message': 'Book not found'}), 404

            # Update book details
            book.name = data['name']
            book.author = data['author']
            book.price = float(data['price'])
            book.section_id = int(data['section_id'])
            book.content = data['content']
            book.publish_date = publish_date
            
            # Handle file uploads if they are part of the request
            if 'book_image' in request.files:
                book_image = request.files['book_image']
                if book_image and allowed_file(book_image.filename):
                    # Save image file and update book.book_loc_url
                    book.book_loc_url = save_file(book_image)
                    print(book.book_loc_url)
            
            if 'book_pdf' in request.files:
                book_pdf = request.files['book_pdf']
                if book_pdf and allowed_file(book_pdf.filename):
                    # Save PDF file and update book.book_loc_url
                    book.book_pdf_loc_url = save_file(book_pdf)


            db.session.commit()
            cache.clear() ###################################################################cache clear
            return jsonify({'message': 'Book updated succsessfully'}), 200
        except Exception as e:
            print(e)
            return jsonify({'error': 'An unexpected error occurred'}), 500
        

    elif request.method == 'DELETE':
        try:
            book = Book.query.get(book_id)
            if not book:
                return jsonify({'message': 'Book not found'}), 404

            # Delete related carts and feedbacks
            Carts_for_books = Cart.query.filter_by(book_id=book_id).all()
            feedbacksforbook = UserFeedback.query.filter_by(book_id=book_id).all()

            for feedback in feedbacksforbook:
                db.session.delete(feedback)
            
            for cart in Carts_for_books:
                db.session.delete(cart)

            db.session.delete(book)
            db.session.commit()
            cache.clear()


            return jsonify({'message': 'Book deleted successfully'}), 200
        except Exception as e:
            print(e)
            return jsonify({'error': 'An unexpected error occurred'}), 500


#####################################################Cart Reqeuested bookes or reading books. #########################
@app.route('/requests/book', methods=['GET'])
@app.route('/users/book/<int:book_id>', methods=['GET'])
@jwt_required()
def get_users_by_book(book_id=None):
    try:
        print(book_id)
        if request.method == 'GET' : 
            if book_id:
                carts = Cart.query.filter(
                    and_(Cart.book_id == book_id, Cart.approved == True)).all()
                if not carts:
                    abort(404, description="No carts found for the given book ID.")
            else:
                carts = Cart.query.filter(Cart.approved == 0).all()
                if not carts:
                    abort(404, description="No carts found for the given book ID.")
            user_cart_info = []
            for cart in carts:
                user_info = {
                    'cart_id': cart.cart_id,
                    'date_issued': cart.date_issued,
                    'date_end': cart.date_end,
                    'user_name': cart.cart_user.user_name,
                    'user_id': cart.cart_user.user_id,
                    'book_name': cart.book_info.name
                }
                user_cart_info.append(user_info)
            return jsonify(user_cart_info), 200

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An error occurred: {str(e)}")
        # Return a generic error message to the client
        return jsonify({"error": "An unexpected error occurred.", "error": str(e)}), 500






@app.route('/api/users/<int:user_id>/carts/<int:book_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
# @user_or_librarian_req
def handle_user_cart(user_id, book_id):
    print(user_id, book_id)
    if request.method == 'GET':
        try:
            cart = Cart.query.filter(
                and_(Cart.book_id == book_id, Cart.cart_user_id == user_id)).first()
            if cart is None:
                print('hellow world')
                return jsonify(cart_info={}), 200
            cart_info = {
                'cart_id': cart.cart_id,
                'date_issued': cart.date_issued,
                'date_end': cart.date_end,
                'approved': cart.approved
            }
            return jsonify(cart_info), 200
        except Exception as e:
            print(e)
            return jsonify({"error": "An unexpected error occurred."}), 500

    elif request.method == 'POST':
        try:
            # Retrieve request data
            data = request.json
            print(data)
            # Example format: '2024-04-05T12:24:50.471Z'
            date_issued_str = data.get('date_issued')
            date_end_str = data.get('date_end')
            # print('date issued ' , '\n', date_issued_str, '\n', 'date end ', '\n', date_end_str)
            # Convert date strings to datetime objects
        
            date_issued = isoparse(date_issued_str)
            date_end = isoparse(date_end_str)

            print(date_issued, date_end)

            # Create a new cart
            new_cart = Cart(
                cart_user_id=user_id,
                book_id=book_id,
                date_issued=date_issued,
                date_end=date_end,
                approved=False
            )

            # Add the new cart to the database session
            db.session.add(new_cart)
            db.session.commit()

            # Return success response
            return jsonify({"message": "Cart created successfully.", "cart_id": new_cart.cart_id}), 201
        except Exception as e:
            print(e)
            return jsonify({"error": "An unexpected error occurred.", "error_message": str(e)}), 500

    elif request.method == 'DELETE':
        try:
            cart = Cart.query.filter(
                and_(Cart.book_id == book_id, Cart.cart_user_id == user_id)).first()
            if cart is None:
                return jsonify({"error": "Cart not found."}), 404

            # Delete the cart from the database session
            db.session.delete(cart)
            db.session.commit()

            # Return success response
            return jsonify({"message": "Cart deleted successfully."}), 200
        except Exception as e:
            print(e)
            return jsonify({"error": "An unexpected error occurred."}), 500


@app.route('/api/usercarts/<int:user_id>', methods=['GET'])
@jwt_required()
def user_carts(user_id):
    try:
        # Filter carts based on the approval status specified in the URL for a user with user_id = user_id
        approved = int(request.args.get('approved'))  # 'true' or 'false'
        carts = Cart.query.filter(
            and_(Cart.approved == approved, Cart.cart_user_id == user_id)).all()
        # Construct cart data
        carts_data = []
        for cart in carts:
            cart_data = {
                'cart_id': cart.cart_id,
                'date_issued': cart.date_issued,
                'date_end': cart.date_end,
                'approved': cart.approved,
                'book_name': cart.book_info.name
            }
            carts_data.append(cart_data)

        return jsonify({'carts': carts_data}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500


@app.route('/api/completedbooks/<int:user_id>', methods=['GET', 'DELETE'])
@jwt_required()
def completed_books(user_id):
    """Completed Books route for deleting""" 
    if request.method == 'GET':
        try:
            completed_books = CompletedBook.query.filter_by(
                user_id=user_id).all()
            completed_books_data = []
            for book in completed_books:
                book_data = {
                    'id': book.id,
                    'user_id': book.user_id,
                    'book_name': book.book_name,
                    'section_name': book.section_name,
                    'content': book.content,
                    'author': book.author,
                    'date_issued': book.date_issued,
                    'return_date': book.return_date
                }
                completed_books_data.append(book_data)
            return jsonify({'completed_books': completed_books_data}), 200
        except Exception as e:
            print(e)
            return jsonify({'error': 'An unexpected error occurred'}), 500
        
    elif request.method == 'DELETE':
        try:
            book_id = request.args.get('id')
            book_to_delete = CompletedBook.query.filter_by(
                id=book_id, user_id=user_id).first()
            if not book_to_delete:
                return jsonify({'message': 'Book not found'}), 404
            db.session.delete(book_to_delete)
            db.session.commit()
            return jsonify({'message': 'Book deleted successfully'}), 200
        except Exception as e:
            print(e)
            return jsonify({'error': 'An unexpected error occurred'}), 500



@app.route('/api/cart/<int:cart_id>', methods=['DELETE'])
@jwt_required()
def revoke_access(cart_id):
    """Revoke access or deny reques"""
    if request.method == 'DELETE':
        try:
            cart = Cart.query.get(cart_id)
            # cart = Cart.query.filter_by(cart_id=cart_id).first()
            if not cart:
                return jsonify({"message": "Cart not found"}), 404

            # Save completed book details

            db.session.delete(cart)
            db.session.commit()


            # Return success response
            return jsonify({"message": "Cart deleted successfully."}), 200
        except Exception as e:
            print(e)
            return jsonify({"error": "An unexpected error occurred."}), 500
        


### approve book or revoke book access not give feedback when revoke access
@app.route('/api/cart/<int:cart_id>', methods=['PATCH'])
@jwt_required()
@librarian_role
# user_role
# @user_or_librarian_req
def approve_book(cart_id):    
    if request.method == 'PATCH':
        try:
            days_to_approve = request.json.get('daysToApprove')
            cart = Cart.query.get(cart_id)
             
            print('hellow world')
            print(cart_id, 'cartid and taken for the days' , days_to_approve)
            if cart is None:
                return jsonify({"error": "Cart not found."}), 404
            elif not days_to_approve:
                return jsonify({"error": "daysToApprove is required."}), 400
            elif  int(days_to_approve) < 2 or int(days_to_approve) > 15 :
                print("daysToApprove must be between 2 and 15.")
                return jsonify({"error": "daysToApprove must be between 2 and 15."}) , 400
                

            started_reading = date.today()
            end_reading_date = started_reading + timedelta(days=int(days_to_approve))

            print('end_reading_date', end_reading_date)
            print('started_reading', started_reading)


            cart.date_issued = started_reading
            cart.date_end = end_reading_date
            cart.approved = 1
            db.session.commit()
    
            return jsonify({"message": "Cart approved successfully."}), 200

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({"error": "An unexpected error occurred.", "error_message": str(e)}), 500
        


@app.route('/api/completed_books', methods=['GET'])
@jwt_required()
def completed_book_users():
    try:
        book_name = request.args.get('book_name')
        print('book_name:', book_name)
        selected_data = select(
            Users.user_name, CompletedBook.book_name,
            CompletedBook.date_issued, CompletedBook.return_date,
            CompletedBook.id, CompletedBook.user_id
        ).join(CompletedBook, Users.user_id == CompletedBook.user_id)

        # if book_name:
        #     selected_data = selected_data.where(CompletedBook.book_name == book_name)

        selected_data = db.session.execute(selected_data).fetchall()
        completed_books_data = [
            {
                'id': book[4],
                'user_id': book[5],
                'book_name': book[1],
                'date_issued': book[2],
                'return_date': book[3],
                'user_name': book[0],
            }
            for book in selected_data
        ]
        return jsonify({'completed_books': completed_books_data}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500


@app.route('/api/delete_completed_books_users', methods=['DELETE'])
@jwt_required()
@librarian_role
def delete_completed_book_users():
    try:
        book_id = request.args.get('book_id')
        print('book_id:', book_id)
        
        book_to_delete = CompletedBook.query.filter_by(id=book_id).first()
        if not book_to_delete:
            return jsonify({'message': 'Book not found'}), 404

        db.session.delete(book_to_delete)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
    
@app.route('/api/carts', methods=['GET'])
@app.route('/api/carts/<int:book_id>', methods=['GET'])
@jwt_required()
def get_reading_books(book_id=None) :
    if request.method == 'GET':
        try:
            approved_str = request.args.get('approved')
            if approved_str is None:
                return jsonify({"error": "Approved status is required"}), 400
            try:
                approved = int(approved_str)
            except ValueError:
                return jsonify({"error": "Approved status must be an integer"}), 400

            if book_id:
                query = Cart.query.filter_by(approved=approved, book_id=book_id)
            else:
                query = Cart.query.filter_by(approved=approved)

            carts = query.all()
            if not carts:
                return jsonify({"message": "No carts found"}), 404

            carts_data = [{
                'book_name': cart.book_info.name,
                'user_name': cart.cart_user.user_name,
                'cart_id': cart.cart_id,
                'date_issued': cart.date_issued,
                'date_end': cart.date_end,
                'approved': cart.approved,
                'book_id': cart.book_id,
            } for cart in carts]

            return jsonify({"carts": carts_data}), 200

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({"error": "An unexpected error occurred.", "error_message": str(e)}), 500


@app.route('/api/return_book/<int:cart_id>', methods=['POST'])
@jwt_required()
@user_role
def return_book(cart_id):
    if request.method == 'POST':
        try:
            # Fetch the cart using cart_id
            cart = Cart.query.filter_by(cart_id=cart_id).first()
            if not cart:
                return jsonify({"message": "Cart not found"}), 404

            # Get the feedback and rating from the request body
            data = request.json
            feedback_text = data.get('feedback')
            rating = data.get('rating')


            # Validate the feedback and rating
            if not feedback_text or not isinstance(rating, int) or rating < 1 or rating > 5:
                return jsonify({"message": "Invalid feedback or rating"}), 400

            # Save feedback to the database
            feedback = UserFeedback(
                user_id=cart.cart_user_id,
                book_id=cart.book_info.id,
                rating=rating,
                feedback=feedback_text
            )

            db.session.add(feedback)
            # Save completed book details
            completed_book = CompletedBook(
                book_name=cart.book_info.name,
                date_issued=cart.date_issued,
                return_date=datetime.now(),
                user_id=cart.cart_user_id,
                content=cart.book_info.content,
                author=cart.book_info.author,
                section_name=cart.book_info.section.name,
                revoked=False
            )
            # Save completed book to the database
            db.session.add(completed_book)
            # Remove the cart entry
            db.session.delete(cart)
            db.session.commit()
            return jsonify({"message": "Book returned and feedback submitted successfully"}), 200

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({"error": "An unexpected error occurred.", "error_message": str(e)}), 500



@app.route('/api/feedback/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book_feedback(book_id):
    try:
        feedbacks = UserFeedback.query.filter_by(book_id=book_id).all()
        if not feedbacks:
            return jsonify({'message': 'No feedbacks found for this book'}), 404

        feedback_list = []
        for feedback in feedbacks:
            feedback_dict = {
                'id': feedback.feedback_id,
                'user_id': feedback.user_id,
                'book_id': feedback.book_id,
                'rating': feedback.rating,
                'feedback': feedback.feedback,
                'username': feedback.user_feedbacks.user_name,
            }
            feedback_list.append(feedback_dict)
        
        return jsonify({'feedbacks': feedback_list}), 200

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred.', 'error_message': str(e)}), 500



@app.route('/api/completedbook/<int:user_id>/<string:book_name>', methods=['GET'])
@jwt_required()
def get_completed_book(user_id, book_name):
    try:
        completed_book = CompletedBook.query.filter_by(user_id=user_id, book_name=book_name).all()

        if completed_book is None:
            return jsonify({'message': 'No completed book'}), 404
        completed_book = [ {
            'id': entry.id,
            'user_id': entry.user_id,
            'book_name': entry.book_name,
            'section_name': entry.section_name,
            'content': entry.content,
            'author': entry.author,
            'date_issued': entry.date_issued,
            'return_date': entry.return_date
        }  for entry in completed_book]

        return jsonify({'completed_book': completed_book}), 200

        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred.', 'error_message': str(e)}), 500



@app.route('/api/analytics', methods=['GET'])
@jwt_required()
@librarian_role
def analytics():
    try:
        book_issue_data = book_issued_per_day.apply_async()
        popular_book = top_five_books.apply_async()
        top_selling = top_selling_books.apply_async()
        genre_dist = genre_distribution.apply_async()

        analytics_data = {
            "book_issued_data": book_issue_data.get(timeout=10),
            "popular_book": popular_book.get(timeout=10),
            "top_selling_books": top_selling.get(timeout=10),
            "genre_distribution": genre_dist.get(timeout=10)
        }

        
        return jsonify(analytics_data), 200

    except Exception as e : 
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An error occurred", "details": str(e)}), 500
