from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from Models import db
import os
from celery_worker import celery_initilization
from init_data import init_data
from flask_caching import Cache



# Initialize Flask app
app = Flask(__name__)
cache = Cache()
# Initialize extensions
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
# CORS(app, origins=['http://localhost:8080'])

CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
            "supports_credentials": True,
            "headers": "Authorization",
        }
    },
)


# # Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///IIT_project.sqlite3'
app.config.timezone = 'UTC'
app.secret_key = 'uxkr75derd5e54xw3e67rc674i56ex65ei6xry6'
app.config["UPLOAD_FOLDER"] = "static"



app.config.update(
    broker_url='redis://localhost:6379/1',
    result_backend='redis://localhost:6379/2',
    CACHE_TYPE='RedisCache',
    CACHE_REDIS_URL='redis://localhost:6379/3',
    broker_connection_retry_on_startup=True
)



# Initialize the app context and database
with app.app_context():
    db.init_app(app)

# Initialize Celery
cache.init_app(app)
celery = celery_initilization(app)

# Import the routes




if __name__ == '__main__':

    path = './instance/IIT_project.sqlite3'
    if not os.path.exists('./instance/IIT_project.sqlite3'):
        print("Database not found. Creating a new one...")
        init_data(app,db)
    else :
        print("Database found. Using it...")
        pass
    from routes import *
    app.run(debug=True)