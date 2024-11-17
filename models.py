from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Enum, CheckConstraint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
