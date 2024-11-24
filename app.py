from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email
from models import db, Accounts, Transactions

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///BankAPI.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'mysecretkey'  # Change this to a secret key of your choice

# Initialize db
db.init_app(app)

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('Register')

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('Login')

@app.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    new_account = Accounts(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        balance=data["balance"],
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
    accounts.first_name = data["first_name"]
    accounts.last_name = data["last_name"]
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
        return jsonify({"error": "Insufficient funds!"}), 400
    accounts.balance -= amount
    new_transaction = Transactions(account_id=account_id, type="withdraw", amount=amount)
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": f"Withdrew {amount} !"})

@app.route("/html")
def test_html():
    return render_template("index.html")

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Here you can add code to save the user details to the database
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Here you can add authentication logic
        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

# Home route
@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
