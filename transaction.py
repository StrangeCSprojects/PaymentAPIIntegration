# Import necessary modules for database modeling and timestamping
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from . import db  # Assumes 'db = SQLAlchemy()' is initialized in __init__.py


# Define the Transaction database model
class Transaction(db.Model):
    # Declare all model fields (columns)
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
