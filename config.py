import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/uatas-api'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["UPLOAD_FOLDER_IMAGES"] = "uploads/images"
    app.config["UPLOAD_FOLDER_PDF"] = "uploads/pdf"

    os.makedirs(app.config["UPLOAD_FOLDER_IMAGES"], exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER_PDF"], exist_ok=True)

    db.init_app(app)
    return app
