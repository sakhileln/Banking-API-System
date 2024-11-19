from decimal import Decimal
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Accounts, Transactions, TransactionType

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///BankAPI.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db
db.init_app(app)


# Test cases:
# with app.app_context():
#     db.create_all() # Create all tabkes in database [if they do not exist]
#     # Create new account
#     # account = Accounts(
#     #     first_name="Zethe", 
#     #     last_name="Ndlazi", 
#     #     email="zethe@orbital.stars", 
#     #     balance=3.47
#     # )
#     # db.session.add(account)
#     # db.session.commit()

#     # Query and check if the account was added
#     account = Accounts.query.filter_by(email="zethe@orbital.stars").first()

#     # Simulate a deposit
#     deposit_amount = Decimal('23.6')
#     account.balance += deposit_amount

#     # Create transaction record for deposit
#     transaction = Transactions(
#         account_id=account.account_id, 
#         amount=deposit_amount, 
#         type=TransactionType.deposit
#     )
#     db.session.add(transaction)
#     db.session.commit()

#     # Output the result
#     print(f"Account : {account.first_name} {account.last_name}, Balance: ZAR {account.balance:.2f}")
#     print(f"Deposit of: ZAR {deposit_amount} successful. New balance: ZAR {account.balance:.2f}")


@app.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    new_account = Accounts(
        first_name=data["first_name"], last_name=data["last_name"],
        email=data["email"], balance=data["balance"]
    )
    db.session.add(new_account)
    db.session.commit()
    return jsonify({"message": "Account created!"}), 201


@app.route("/accounts/<int:account_id>", methods=["GET"])
def view_account(account_id):
    accounts = Accounts.query.get(account_id)
    if not accounts:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(
        {
            "account_id": accounts.account_id,
            "first_name": accounts.first_name,
            "last_name": accounts.last_name,
            "email": accounts.email,
            "balance": accounts.balance,
            "created_at": accounts.created_at,
        }
    )


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    accounts = Accounts.query.get(account_id)
    if not accounts:
        return jsonify({"error": "Account not found"}), 404
    data = request.get_json()
    accounts.name = data["name"]
    db.session.commit()
    return jsonify({"message": "Account Updated!"})


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    accounts = Accounts.query.get(account_id)
    if not accounts:
        return jsonify({"error": "Account not found"}), 404
    db.session.delete(accounts)
    db.session.commit()
    return jsonify({"message": "Account Deleted!"})


@app.route("/accounts/<int:account_id>/deposit", methods=["POST"])
def deposit(account_id):
    accounts = Accounts.query.get(account_id)
    if not accounts:
        return jsonify({"error": "Account not found"}), 404
    data = request.get_json()
    amount = data["amount"]
    accounts.balance += amount
    new_transaction = Transactions(account_id=account_id, type="deposit", amount=amount)
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": f"Deposited {amount} !"})


@app.route("/accounts/<int:account_id>/withdraw", methods=["POST"])
def withdraw(account_id):
    accounts = Accounts.query.get(account_id)
    if not accounts:
        return jsonify({"error": "Account not found"}), 404
    data = request.get_json()
    amount = data["amount"]
    if amount > accounts.balance:
        return jsonify({"error": "Insufficient funds! "}), 400
    accounts.balance -= amount
    new_transaction = Transactions(
        account_id=account_id, type="withdraw", amount=amount
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": f"Withdrew {amount} !"})


if __name__ == "__main__":
    app.run(debug=True)
