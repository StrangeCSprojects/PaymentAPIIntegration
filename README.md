# Payment API (Serverless Flask Project)

A cloud-hosted, serverless payment processing API built with Flask, AWS Lambda (via Zappa), and MySQL on AWS RDS. Designed to handle secure transaction submissions and return paginated transaction histories, this project demonstrates full-stack deployment of a scalable backend using modern cloud infrastructure.

---

## 📦 Features

- RESTful API built with Flask
- Hosted using AWS Lambda + Zappa
- Connected to an AWS RDS MySQL instance
- POST endpoint to process payments
- GET endpoint with pagination to fetch transaction history
- Handles JSON input with validation
- Serverless, scalable, and secure

---

## API Endpoints

### `POST /process-payment`
- **Description**: Submits a payment
- **Body Parameters (JSON)**:
  ```json
  {
    "amount": 100.00,
    "currency": "USD",
    "payment_method": "credit_card"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Payment processed successfully"
  }
  ```

### `GET /transaction-history`
- **Query Params**:
  - `page` (default `1`)
  - `limit` (default `10`)
- **Response**:
  ```json
  {
    "page": 1,
    "total_items": 5,
    "total_pages": 1,
    "transactions": [ ... ]
  }
  ```

---

## 🔧 Technologies Used
- Python 3.11
- Flask
- Flask-SQLAlchemy
- PyMySQL
- MySQL (AWS RDS)
- Zappa
- AWS Lambda
- AWS API Gateway

---

## 🛠 Setup Instructions

### 🔹 Local Development
1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Add your `SQLALCHEMY_DATABASE_URI` config for a local instance
5. Run the app:
   ```bash
   flask run
   ```

### 🔹 Deploy to AWS Lambda
1. Configure `zappa_settings.json`
2. Deploy with:
   ```bash
   zappa deploy dev
   ```
3. Update with:
   ```bash
   zappa update dev
   ```

---

## Example `SQLALCHEMY_DATABASE_URI`
```python
mysql+pymysql://Cstrange:paymentapid@payment-api-db.c1iqiis249wk.us-west-1.rds.amazonaws.com:3306/paymentAPI
```

---

## Issues & Solutions (Selected)

| Issue | Solution |
|-------|----------|
| Lambda returned 502 / 403 | Fixed by defining route methods and redeploying with Zappa |
| Access denied for MySQL user | Recreated user `Cstrange@'%'` and granted all privileges |
| Lambda couldn't reach DB | Adjusted RDS security group to allow public access on port 3306 |
| `admin@ec2` errors | Updated Zappa/Flask config to use the correct MySQL user |

---

## License
MIT License

---

## Author
**Cody Strange**  
_BSc Software Engineering, Utah Valley University
