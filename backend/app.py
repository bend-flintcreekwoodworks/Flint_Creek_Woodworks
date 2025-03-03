from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from routes import setup_routes

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "your_secret_key_here"

db.init_app(app)

setup_routes(app)  # Register routes

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database if not exists
    app.run(debug=True)
