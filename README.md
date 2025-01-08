# Library Management System

## Overview

This project is a **Library Management System** developed with **Vue 3** for the frontend and **Flask** for the backend API. The system is designed to manage books, users, and librarian functionalities efficiently. It offers features like book borrowing, returning, role-based access, user management, book genre management, and analytics. The system is intended for both regular users (who can borrow and return books) and librarians (who can manage books and monitor user activities).

---

## Features

### User Features:
- **Signup/Login**: User registration and authentication using JWT tokens.
- **Browse Books**: View a list of available books.
- **Borrow/Return Books**: Add books to the cart and return them.
- **User Dashboard**: View books borrowed, reading status, and completed books.
- **View Single Book Info**: Get detailed information about books.
- **Track Borrowing Status**: Monitor the status of borrowed books (reading, requested, completed).

### Librarian Features:
- **Login**: Librarians can log in and access restricted features.
- **Book Management**: Add, edit, and delete books in the library.
- **User Management**: Manage user requests, and track users who are reading or have finished books.
- **Genre Management**: Add or edit book genres.
- **Analytics**: Access analytics dashboards to view user activity, book popularity, and more.
- **Book Requests**: Manage book requests and track user borrowing history.

---

## Tech Stack

- **Frontend**: 
  - **Vue 3**: JavaScript framework for building the user interface.
  - **Vue Router**: For routing and navigation in the app.
  - **Axios**: For making HTTP requests to the backend.
  - **JWT**: For secure user authentication and token storage in session.
  
- **Backend**: 
  - **Flask**: Python web framework to build the API.
  - **Flask-JWT-Extended**: For JWT authentication.
  - **Flask-SQLAlchemy**: ORM for managing the database.
  - **Flask-Caching**: Caching mechanism for improving API performance.
  - **Celery**: Task scheduling (for reminders, monthly reports, etc.).
  - **Redis**: For caching and task queue management with Celery.

- **Database**: 
  - **SQLite** (or another RDBMS, e.g., PostgreSQL, MySQL) for persistent storage of users, books, and transactions.

---

## Installation

### Prerequisites
Make sure you have the following installed:
- **Node.js** (for the frontend)
- **Python 3** (for the backend)
- **pip** (for Python dependencies)

## Backend Setup

1. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Flask app:

    ```bash
    python app.py
    ```

---

## Frontend Setup

1. Navigate to the frontend folder:

    ```bash
    cd frontend
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Run the Vue app:

    ```bash
    npm run serve
    ```

The application will be available at:
- **Vue frontend**: [http://localhost:8080](http://localhost:8080)
- **Flask backend**: [http://localhost:5000](http://localhost:5000)


# API Reference

## Authentication API

- **POST /login**: Login endpoint for user authentication, returns JWT token.
- **POST /signup**: Signup endpoint for new user registration.
- **GET /user**: Fetch authenticated user details.
- **POST /logout**: Logout and invalidate the JWT token.

## Book Management API

- **GET /books**: Get the list of books available in the library.
- **POST /books**: Add a new book to the library (Admin only).
- **PUT /books/{bookId}**: Edit book details (Admin only).
- **DELETE /books/{bookId}**: Delete a book from the library (Admin only).

## User and Librarian Endpoints

- **GET /users**: List all users (Admin only).
- **GET /user/{id}**: Get details of a specific user (Admin only).
- **POST /book-request**: Request a book (User).
- **PUT /book-return**: Return a borrowed book (User).


### Authentication Endpoints

#### **POST /login**
- **Description**: Authenticates a user and returns a JWT token.
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }

## Tech

- **Backend**: Flask, Python
- **Frontend**: Vue 3, JavaScript
- **Database**: SQLite, PostgreSQL, MySQL
- **Task Queue**: Celery
- **Caching**: Redis
- **Authentication**: JWT

## Folder Structure

### `/backend`
- **app.py**: Flask application entry point.
- **models.py**: Database models, including definitions for users, books, and transactions.
- **requirements.txt**: Python dependencies required for the backend.
- **utils.py**: Helper functions for various tasks like JWT handling, caching, etc.

### `/frontend`
- **public/**: Contains static files like icons, and fonts.
- **src/**: Contains the source code for the Vue application.
  - **assets/**: Images, styles, and other static assets.
  - **components/**: Reusable Vue components like headers, footers, and buttons.
  - **views/**: Different page views that represent specific sections of the application.
  - **App.vue**: The main Vue component that serves as the root of the app.
  - **router.js**: Vue Router configuration for handling application routing.
  - **store.js**: Vuex store for state management (if used).
  - **main.js**: Entry point for the Vue app, where the app is initialized and mounted.

## Support

For any issues or questions, please open an issue in the repository or contact rksnsneno@gmail.com.

## Authors

[Rohit Sen] - Initial work - [GitHub Profile](https://github.com/Mrsenjiii)

## FAQ

- **Q: How do I get a JWT token?**  
  **A:** The token is provided when you log in with your credentials. It can be stored in session storage for future use.

- **Q: How can I add new books as a librarian?**  
  **A:** After logging in as a librarian, navigate to the "Manage Books" section and use the "Add Book" functionality.

## Environment Variables

Make sure to set the following environment variables for local development:

- **FLASK_APP**: The main Flask application file.
- **FLASK_ENV**: Set to development for local development.
- **JWT_SECRET_KEY**: Secret key for signing JWT tokens.



## Error Codes

- **400 Bad Request**: Invalid request data.
- **401 Unauthorized**: Authentication required (missing or invalid JWT token).
- **403 Forbidden**: Access denied (Admin privileges required).
- **404 Not Found**: The requested resource could not be found.
- **500 Internal Server Error**: An unexpected error occurred on the server.



## Demo


https://drive.google.com/file/d/1qLJ1FaMKFI1FEzuU7JrM1rnYDZi1cZ6t/view?usp=sharing
