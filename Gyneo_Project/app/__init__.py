from flask import Flask
from flask_pymongo import PyMongo

from app.auth_routes import create_auth_blueprint   # Import auth blueprint
from app.routes import bp                           # Import main/routes blueprint

mongo = None

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    app.secret_key = "your_secret_key"
    app.config["MONGO_URI"] = "mongodb://localhost:27017/gynae_db"
    
    global mongo
    mongo = PyMongo(app)

    # Attach mongo to routes blueprint (if needed)
    bp.mongo = mongo

    # Register Blueprints (THIS MUST COME BEFORE return)
    app.register_blueprint(create_auth_blueprint(mongo))
    app.register_blueprint(bp)

    return app
