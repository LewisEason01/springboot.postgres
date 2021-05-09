from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import psycopg2

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
    user = db.Column("user_name", db.String(20))
    password = db.Column("password", db.String(30))
    email = db.Column("email_address", db.String(20))
    balance = db.Column("balance", db.Float(20))
    
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
        session.permanent = True
        found_user = Bank.query.filter_by(user=username, password=password).first()

        while username != "" and password != "":
            if found_user:
                session["user"] = username
                session["user"] = found_user.user
                return redirect(url_for("homepage"))
            else:
                invalid_login = "Invalid input. Try again"
                return redirect(url_for("login"))
        if username == "":
            username_error = "*  Username required"
        if password == "":
            password_error = "* Password required"
    else:
        if "user" in session:
            return redirect(url_for("homepage"))
        
    return render_template('login-template.html', **locals())

#the template will be displayed when the app route is added to the URL
@app.route("/bank/Lewis/account/", methods=["POST", "GET"])
def account():
    if request.method == "POST":
        username = request.form["newusername"]
        email = request.form["newemail"]
        password = request.form["newpassword"]
        confirm_password = request.form["confirmpassword"]
        session.permanent = True

        found_user = Bank.query.filter_by(user=username).first()
        while username != "" and password != "" and email != "" and confirm_password != "" and password == confirm_password:
            if found_user:
                flash(f"{username} already exists")
                return redirect(url_for("account"))
            elif len(password) > 7:
                new_password_error = "Your password is too short"
            else:
                usr = Bank(username, password, email, 0.00)
                db.session.add(usr)
                db.session.commit()
                return redirect(url_for("homepage"))

        if username == "":
            new_username_error = "*  Username required"
        if email == "":
            new_email_error = "*  Email required"
        if password == "":
            new_password_error  = "*  Password required"
        if password == "":
            confirm_password_error = "*  Password MUST be confirmed"
        if password != confirm_password:
            flash("Your passwords do not match.")
            
    else:
        if "user" in session:
            return redirect(url_for("homepage"))
    
    return render_template('account-template.html', **locals())

@app.route("/bank/Lewis/manage/", methods=["POST", "GET"])
def manage():
    return render_template('manage-template.html', **locals())


@app.route("/bank/Lewis/homepage/", methods=["POST", "GET"])
def homepage():
    # if "user" in session:
    #     username = session["user"]
    # else:
    #     return redirect(url_for("login"))

    return render_template('homepage-template.html', **locals())

@app.route("/bank/Lewis/logout/", methods=["POST", "GET"])
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/bank/Lewis/delete/", methods=["POST", "GET"])
def delete():
    # found_user = Bank.query.filter_by(user=username).delete()
    # session.pop("user", None)
    # db.session.delete(usr)
    # db.session.commit()
    return redirect(url_for("login"))

# @app.route("/bank/Lewis/deposit/", methods=["POST", "GET"])
# # def deposit():
# #     if request.method == "POST":
# #         deposit = request.form["deposit"]
# #         session.permanent = True
# #         balance = balance + deposit
# #         db.session.commit()
# #         user_balance = "Your current balance is " + balance
# #     return redirect(url_for("homepage"))

# @app.route("/bank/Lewis/withdraw/", methods=["POST", "GET"])
# def withdraw():
#     return redirect(url_for("homepage"))

# @app.route("/bank/Lewis/balance/", methods=["POST", "GET"])
# def current_balance():
#     return redirect(url_for("homepage"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(host='127.0.0.1', port=8001)