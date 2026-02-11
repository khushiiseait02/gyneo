from flask_pymongo import PyMongo

mongo = None

def init_db(app):
    global mongo
    app.config["MONGO_URI"] = "mongodb://localhost:27017/gynae_db"
    mongo = PyMongo(app)
    return mongo

