from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Enum


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

from app import db

db_name = 'database.db'


class Accounts(db.Model):
    __tablename__  =  "Accounts"
    account_id = db.Column(db.Integer, increment=True, primary_key=True)
    first_name = db.Column(db.String(100),null=False)
    last_name = db.Column(db.String(100), null=False)
    email = db.Column(db.String(200), unique=True, null=False)
    balance = db.Column(db.Float(15,2), default=0.00, null=False)
    created_at = db.Column(db.Datetime, default=datetime, null=False)
    transactions = db.relationship("Accounts", backref='accounts')

class Transactions(db.Model):
    __tablename__ = "Transactions"
    transaction_id = db.Column(db.Integer(increment=True, primary_key=True))
    account_id = db.Column(db.Integer,db.foreign_key('accounts.account_id'))
    amount = db.Column(db.Float((15,2), null=False))
    type = db.Column.Check(Enum('deposit', 'withdraw'))
    transaction_date = db.Column(db.DateTime, default=datetime, null=False)

with app.app_context():
    db.create_all

@app.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    new_account = Accounts(name=data['name'])
    db.session.add(new_account)
    db.session.commit()
    return jsonify({"message": "Account created!"}), 201

@app.route('/accounts/<int:account_id>', methods=['GET'])
def  view_account(account_id):
    accounts = Accounts.query.get(account_id)
    if not accounts:
        return jsonify({"error": "Account not found"}),404
    return jsonify({"account_id": accounts.account_id, "first_name": accounts.first_name, "last_name": accounts.last_name, "email": accounts.email, "balance":accounts.balance,"created_at":accounts.created_at })

@app.route('/accounts/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    accounts = Accounts.query.get(account_id)
    if not accounts:
        return jsonify({"error": "Account not found"}),404
    data = request.get_json()
    accounts.name=data['name']
    db.session.commit()
    return jsonify({"message": "Account Updated!"})

@app.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    accounts = Accounts.query.get(account_id)
    if not accounts:
        return jsonify({"error": "Account not found"}),404
    db.session.delete(accounts)
    db.session.commit()
    return jsonify({"message": "Account Deleted!"})

@app.route('/accounts/<int:account_id>/deposit', methods=['POST'])
def deposit(account_id):
    accounts = Accounts.query.get(account_id)
    if not accounts:
        return jsonify({"error": "Account not found"}),404
    data = request.get_json()
    amount = data['amount']
    accounts.balance += amount
    new_transaction = Transactions(account_id=account_id,type = 'deposit', amount = amount)
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": f"Deposited {amount} !"})

@app.route('/accounts/<int:account_id>/withdraw', methods=['POST'])
def withdraw(account_id):
    accounts = Accounts.query.get(account_id)
    if not accounts:
        return jsonify({"error": "Account not found"}),404
    data = request.get_json()
    amount = data['amount']
    if amount > accounts.balance:
        return jsonify({"error": "Insufficient funds! "}),400
    accounts.balance -= amount
    new_transaction = Transactions(account_id=account_id,type = 'withdraw', amount = amount)
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": f"Withdrew {amount} !"})

if __name__ == '__main__':
    app.run(debug=True)