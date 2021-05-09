from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import builtins

app = Flask(__name__)

db = SQLAlchemy()

POSTGRES = {
    'user': 'postgres',
    'pw': 'Ea$1ano01',
    'db': 'postgres',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'welcome'
db.init_app(app)

class Bank(db.Model):
    __tablename__ = 'users'
    _id = db.Column("id", db.Integer, primary_key=True)
    user = db.Column("user_name", db.String(30))
    password = db.Column("password", db.String(30))
    email = db.Column("email_address", db.String(40))
    balance = db.Column("balance", db.String(10))
    
    def __init__(self, user, password, email, balance):
        self.user = user
        self.password = password
        self.email = email
        self.balance = balance

@app.route("/")
def index():
    return "Flask App!"

@app.route("/bank/Lewis/login/", methods=["POST", "GET"])
def login():  
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_login = username + password
        session.permanent = True
        found_user = Bank.query.filter_by(user=username, password=password).first()

        while user_login != "" and found_user:
            session["user"] = username
            session["password"] = password
            return redirect(url_for("homepage"))
        
        if not found_user or user_login == "":
            invalid_login = "Invalid input. Try again"
    else:
        if "user" in session:
            return redirect(url_for("homepage"))
        
    return render_template('login-template.html', **locals())

#the template will be displayed when the app route is added to the URL
@app.route("/bank/Lewis/account/", methods=["POST", "GET"])
def account():
    if request.method == "POST":
        balance = ""
        username = request.form["newusername"]
        email = request.form["newemail"]
        password = request.form["newpassword"]
        confirm_password = request.form["confirmpassword"]
        session.permanent = True
        user_account = username + email + password + confirm_password

        found_user = Bank.query.filter_by(user=username).first()
        found_email = Bank.query.filter_by(email=email).first()
        while user_account != "" and password == confirm_password and len(password) >= 7 and not found_user and not found_email:
            session["user"] = username
            session["email"] = email
            session["password"] = password
            session["balance"] = balance
            new_user = Bank(username, password, email, balance)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("homepage"))

        if username == "":
            new_username_error = "  Username required"
        if email == "":
            new_email_error = "  Email required"
        if password == "":
            new_password_error = "  Password Required"
        if found_user:
            new_username_error = "  Username already exists"
        if found_email:
            new_email_error = "  Email already exists"
        if password != confirm_password and user_account != "":
            new_password_error = "  Your passwords do NOT match"
            confirm_password_error = "  Your passwords do NOT match"
        if len(password) < 7 and password != "":
            new_password_error = "  Your password must be at least 7 characters long"
            
    else:
        if "user" in session:
            return redirect(url_for("homepage"))
    
    return render_template('account-template.html', **locals())

@app.route("/bank/Lewis/manage/", methods=["POST", "GET"])
def manage():
    if "user" in session:
        username = session["user"]

        if request.method == "POST":
            deposit = request.form["deposit"]
            withdraw = request.form["withdraw"]
            balance = session["balance"]

            if request.form['deposit'] == "":
                deposit_error = "You must enter a number"
            else:
                balance += str(deposit)
                update_balance = Bank.query.filter_by(user=username).update(dict(balance=balance))
                db.session.commit()
                dp_bal = "Your current balance is £" + balance
        
            if request.form['withdraw'] == "":
                withdraw_error = "You must enter a number"
            else:
                wd_bal = "Your current balance is £" + withdraw
        # else:
        #     curr_bal = "Your current balance is"    
    else:
        return redirect(url_for("login"))
    
    return render_template('manage-template.html', **locals())

@app.route("/bank/Lewis/homepage/", methods=["POST", "GET"])
def homepage():
    if "user" in session:
        username = session["user"]
    else:
        return redirect(url_for("login"))

    return render_template('homepage-template.html', **locals())

@app.route("/bank/Lewis/information/", methods=["POST", "GET"])
def personal_info():
    if "user" in session:
        username = session["user"]
        email = session["email"]
        password = session["password"]

        if request.method == "POST":
            upd_un = request.form["updusername"]
            upd_em = request.form["updemail"]
            upd_pw = request.form["updpassword"]
            conf_upd_pw = request.form["confupdpassword"]
            session.permanent = True
            user_account = upd_un + upd_em + upd_pw + conf_upd_pw

            found_user = Bank.query.filter_by(user=upd_un).first()
            found_email = Bank.query.filter_by(email=upd_em).first()

            while user_account != "" and not found_user and not found_email and upd_pw == conf_upd_pw and len(upd_pw) >= 7:
                update_user = Bank.query.filter_by(user=username).update(dict(user=upd_un, email=upd_em, password=upd_pw))
                db.session.commit()
                session["user"] = upd_un
                session["email"] = upd_em
                session["password"] = "*" * len(upd_pw)
                flash("Your information has been updated")
                return redirect(url_for("personal_info"))
        
            if upd_un == "":
                upd_username_error = "  Username required"
            if upd_em == "":
                upd_email_error = "  Email required"
            if upd_pw == "":
                upd_password_error = "  Password required"
            if found_user:
                upd_username_error = "  Username already exists"
            if found_email:
                upd_email_error = "  Email already exists"
            if upd_pw != conf_upd_pw and user_account != "":
                upd_password_error = "  Your passwords do NOT match"
                upd_conf_password_error = "  Your passwords do NOT match"
            if len(upd_pw) < 7 and upd_pw != "":
                upd_password_error = "  Your password must be at least 7 characters long"
    
    else:
        return redirect(url_for("login"))
    
    return render_template('personal_info-template.html', **locals())


@app.route("/bank/Lewis/settings/", methods=["POST", "GET"])
def settings():
    if "user" in session:
        username = session["user"]
        email = session["email"]
        password = session["password"]
    else:
        return redirect(url_for("login"))
    return render_template('settings-template.html', **locals())


@app.route("/bank/Lewis/logout/", methods=["POST", "GET"])
def logout():
    session.pop("user", None)
    session.pop("password", None)
    flash("You have been successfully logged out")
    return redirect(url_for("login"))

@app.route("/bank/Lewis/delete/", methods=["POST", "GET"])
def delete():
    username = session["user"]
    found_user = Bank.query.filter_by(user=username).delete()
    session.pop("user", None)
    session.pop("password", None)
    session.pop("email", None)
    db.session.commit()
    flash("Your account has been deleted")
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(host='127.0.0.1', port=8001)