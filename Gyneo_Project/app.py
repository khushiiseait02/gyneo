# app.py
import os
from flask import Flask, redirect, url_for, session
from flask_pymongo import PyMongo

from app.auth_routes import create_auth_blueprint
from app.routes import bp as routes_bp

mongo = None

def create_app():
    app = Flask(__name__, static_folder='app/static', template_folder='app/templates')
    app.secret_key = os.environ.get("SECRET_KEY", "super-secret-dev-key")
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/gynae_db")

    global mongo
    mongo = PyMongo(app)

    # Attach mongo to blueprints (auth uses factory param, routes can access via routes_bp.mongo)
    routes_bp.mongo = mongo

    # Register blueprints
    app.register_blueprint(create_auth_blueprint(mongo))
    app.register_blueprint(routes_bp)

    # Home redirect convenience
    @app.route("/")
    def home():
        if "username" in session:
            return redirect(url_for("routes.dashboard"))
        return redirect(url_for("auth.login"))

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
