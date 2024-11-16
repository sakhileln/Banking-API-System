from decimal import Decimal
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Enum, CheckConstraint
from enum import Enum as PyEnum


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///BankAPI.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Accounts(db.Model):
    __tablename__ = "accounts"

    account_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    balance = db.Column(db.Float(15, 2), default=0.00, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    # Define relationship with 'Transaction', using back_ppopulates
    transactions = db.relationship("Transactions", back_populates="account")

# Define Enum for transaction types
class TransactionType(PyEnum):
    deposit = "deposit"
    withdraw = "withdraw"


class Transactions(db.Model):
    __tablename__ = "transactions"

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey("accounts.account_id"), nullable=False
    )
    amount = db.Column(db.Float(15, 2), nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    # Define 'type' column as Enum type
    type = db.Column(Enum(TransactionType), nullable=False)
    # Add check constraint to ensure valid enum values
    __table_args__ = (
        CheckConstraint(
            "type IN ('deposit', 'withdraw')", name="check_transaction_type"
        ),
    )

    # Define relationship with 'Accounts', using back_populates
    account = db.relationship("Accounts", back_populates="transactions")


with app.app_context():
    db.create_all() # Create all tabkes in database [if they do not exist]


# Test: create a new account
with app.app_context():
    # Create new account
    # account = Accounts(
    #     first_name="Zethe", 
    #     last_name="Ndlazi", 
    #     email="zethe@orbital.stars", 
    #     balance=3.47
    # )
    # db.session.add(account)
    # db.session.commit()

    # Query and check if the account was added
    account = Accounts.query.filter_by(email="zethe@orbital.stars").first()

    # Simulate a deposit
    deposit_amount = Decimal('50.0')
    account.balance += deposit_amount

    # Create transaction record for deposit
    transaction = Transactions(
        account_id=account.account_id, 
        amount=deposit_amount, 
        type=TransactionType.deposit
    )
    db.session.add(transaction)
    db.session.commit()

    # Output the result
    print(f"Account : {account.first_name} {account.last_name}, Balance: ZAR {account.balance:.2f}")
    print(f"Deposit of: ZAR {deposit_amount} successful. New balance: ZAR {account.balance:.2f}")


# @app.route("/accounts", methods=["POST"])
# def create_account():
#     data = request.get_json()
#     new_account = Accounts(name=data["name"])
#     db.session.add(new_account)
#     db.session.commit()
#     return jsonify({"message": "Account created!"}), 201


# @app.route("/accounts/<int:account_id>", methods=["GET"])
# def view_account(account_id):
#     accounts = Accounts.query.get(account_id)
#     if not accounts:
#         return jsonify({"error": "Account not found"}), 404
#     return jsonify(
#         {
#             "account_id": accounts.account_id,
#             "first_name": accounts.first_name,
#             "last_name": accounts.last_name,
#             "email": accounts.email,
#             "balance": accounts.balance,
#             "created_at": accounts.created_at,
#         }
#     )


# @app.route("/accounts/<int:account_id>", methods=["PUT"])
# def update_account(account_id):
#     accounts = Accounts.query.get(account_id)
#     if not accounts:
#         return jsonify({"error": "Account not found"}), 404
#     data = request.get_json()
#     accounts.name = data["name"]
#     db.session.commit()
#     return jsonify({"message": "Account Updated!"})


# @app.route("/accounts/<int:account_id>", methods=["DELETE"])
# def delete_account(account_id):
#     accounts = Accounts.query.get(account_id)
#     if not accounts:
#         return jsonify({"error": "Account not found"}), 404
#     db.session.delete(accounts)
#     db.session.commit()
#     return jsonify({"message": "Account Deleted!"})


# @app.route("/accounts/<int:account_id>/deposit", methods=["POST"])
# def deposit(account_id):
#     accounts = Accounts.query.get(account_id)
#     if not accounts:
#         return jsonify({"error": "Account not found"}), 404
#     data = request.get_json()
#     amount = data["amount"]
#     accounts.balance += amount
#     new_transaction = Transactions(account_id=account_id, type="deposit", amount=amount)
#     db.session.add(new_transaction)
#     db.session.commit()
#     return jsonify({"message": f"Deposited {amount} !"})


# @app.route("/accounts/<int:account_id>/withdraw", methods=["POST"])
# def withdraw(account_id):
#     accounts = Accounts.query.get(account_id)
#     if not accounts:
#         return jsonify({"error": "Account not found"}), 404
#     data = request.get_json()
#     amount = data["amount"]
#     if amount > accounts.balance:
#         return jsonify({"error": "Insufficient funds! "}), 400
#     accounts.balance -= amount
#     new_transaction = Transactions(
#         account_id=account_id, type="withdraw", amount=amount
#     )
#     db.session.add(new_transaction)
#     db.session.commit()
#     return jsonify({"message": f"Withdrew {amount} !"})


# if __name__ == "__main__":
#     app.run(debug=True)
