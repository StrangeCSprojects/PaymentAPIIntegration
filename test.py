from flask import Flask, request, jsonify
from transaction import db, Transaction

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:SQLrootpassword@localhost/MYSQLPaymentAPIIntegration'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()