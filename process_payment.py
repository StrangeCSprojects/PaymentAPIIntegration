from flask import Flask, request, jsonify, Response  # Flask web framework and tools for JSON handling
from transaction import db, Transaction    # Import the database instance and Transaction model
import sys  # Used for flushing logs (optional)

# Initialize the Flask app
app = Flask(__name__)

# Configure connection to the cloud MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Clstrange:Ihatethis@database2.crm4oyaco2kc.us-west-2.rds.amazonaws.com:3306/testme'

# Uncomment this line to use a local database instead
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:SQLrootpassword@localhost:3306/payment_api'

# Disable SQLAlchemy modification tracking (improves performance)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

# Create all tables from models within app context
with app.app_context():
    db.create_all()

# Validate payment input data for required fields and correct types
def validate_payment(data: dict) -> tuple[bool, str]:
    """
    Validates incoming payment data.

    Args:
        data (dict): The payment data to validate.

    Returns:
        tuple: (is_valid: bool, error_message: str)
    """

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

# Default route to confirm the API is running
@app.route('/')
def index() -> str:
    """
    Root endpoint for health check.

    Returns:
        str: Confirmation message.
    """

    return "Zappa is alive!"

# POST endpoint to process a payment and store it in the database
@app.route('/process-payment', methods=['POST'])
def process_payment() -> tuple:
    """
    Processes a new payment from a JSON payload.

    Returns:
        tuple: (JSON response, HTTP status code)
    """

    data = request.json  # Get incoming JSON data
    is_valid, message = validate_payment(data)  # Validate input
    if not is_valid:
        return jsonify({"error": message}), 400  # Return 400 Bad Request if invalid
    
    # Create a new transaction record
    transaction = Transaction(
        amount=data['amount'],
        currency=data['currency'],
        payment_method=data['payment_method']
    )

    # Save the transaction to the database
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Payment processed"}), 201  # Return success message

# GET endpoint to retrieve paginated transaction history
@app.route('/transaction-history', methods=['GET'])
def transaction_history() -> Response:
    """
    Returns a paginated list of transactions.

    Query Params:
        page (int): Page number (default = 1)
        limit (int): Items per page (default = 10)

    Returns:
        Response: JSON with paginated transaction data
    """

    # Get pagination parameters from query string
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', 10, type=int)

    # Query transactions with pagination
    transactions = Transaction.query.paginate(page=page, per_page=per_page, error_out=False)

    # Serialize results into a JSON-ready list
    result = []
    for tx in transactions.items:
        result.append({
            "id": tx.id,
            "amount": tx.amount,
            "currency": tx.currency,
            "payment_method": tx.payment_method,
            "timestamp": tx.timestamp.isoformat()
        })

    # Return paginated response
    return jsonify({
        "transactions": result,
        "page": page,
        "total_pages": transactions.pages,
        "total_items": transactions.total
    })


