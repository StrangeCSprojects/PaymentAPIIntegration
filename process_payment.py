from flask import Flask, request, jsonify
from transaction import db, Transaction
import sys


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Clstrange:Ihatethis@database2.crm4oyaco2kc.us-west-2.rds.amazonaws.com:3306/testme'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

def validate_payment(data):
    required_fields = ['amount', 'currency', 'payment_method']
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"
    if not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
        return False, "Amount must be a positive number."
    if not isinstance(data['currency'], str) or len(data['currency']) != 3:
        return False, "Currency must be a 3-letter code (e.g., USD)."
    if not isinstance(data['payment_method'], str):
        return False, "Payment method must be a string."
    return True, ""

@app.route('/')
def index():
    return "Zappa is alive!"

@app.route('/process-payment', methods=['POST'])
def process_payment():
    data = request.json
    print("📦 Received payload:", data)
    sys.stdout.flush()
    is_valid, message = validate_payment(data)
    if not is_valid:
        return jsonify({"error": message}), 400
    
    transaction = Transaction(
        amount=data['amount'],
        currency=data['currency'],
        payment_method=data['payment_method']
    )

    db.session.add(transaction)
    db.session.commit()


    return jsonify({"message": "Payment processed"}), 201


@app.route('/transaction-history', methods=['GET'])
def transaction_history():
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', 10, type=int)

    # Query transactions from DB with pagination
    transactions = Transaction.query.paginate(page=page, per_page=per_page, error_out=False)

    # Serialize results
    result = []
    for tx in transactions.items:
        result.append({
            "id": tx.id,
            "amount": tx.amount,
            "currency": tx.currency,
            "payment_method": tx.payment_method,
            "timestamp": tx.timestamp.isoformat()
        })

    return jsonify({
        "transactions": result,
        "page": page,
        "total_pages": transactions.pages,
        "total_items": transactions.total
    })
