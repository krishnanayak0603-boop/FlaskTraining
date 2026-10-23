from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:your_password@localhost/flaskproject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
print("krishna")


# Database model
class User(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(12), nullable=True)
    msg = db.Column(db.String(80), nullable=True)


# Create table
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)