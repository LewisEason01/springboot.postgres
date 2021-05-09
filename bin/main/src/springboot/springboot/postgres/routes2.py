from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import psycopg2


app = Flask(__name__)

db = SQLAlchemy()

connection = psycopg2.connect(
    user="postgres",
    password="Ea$1ano01",
    database="postgres",
    host="localhost",
    port="5432",
)

cursor = connection.cursor()

app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class Bank(db.Model):
    __tablename__ = 'users'
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("user_name", db.String(20))
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

@app.route("/bank/Lewis/login/", methods=['GET', 'POST'])
def login():  
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session["user"] = username

        found_user = Bank.query.filter_by(user=username).first()
        if found_user:
            session["user"] = found_user.user
            return redirect(url_for("homepage"))
        else:
            flash("Invalid login. Try again")
            return redirect(url_for("login"))
    else:
        if "user" in session:
            return redirect(url_for("homepage"))
        
        return render_template('login-template.html', **locals())

#the template will be displayed when the app route is added to the URL
@app.route("/bank/Lewis/account/", methods=['GET', 'POST'])
def account():
    if request.method == "POST":
        new_username = request.form["newusername"]
        new_email = request.form["newemail"]
        new_password = request.form["newpassword"]
        confirm_password = request.form["confirmpassword"]
        session["user"] = new_username

        found_user = Bank.query.filter_by(user=new_username).first()
        if found_user:
            flash("{{new_username}} already exists")
        else:
            postgres_insert_query = """ INSERT INTO users (user_name, email_address, password) VALUES (%s,%s,%s)"""
            record_to_insert = (new_username, new_email, new_password, 0.00)
            cursor.execute(postgres_insert_query, record_to_insert)
            return redirect(url_for("homepage"))
    else:
        if "user" in session:
            return redirect(url_for("homepage"))
    return render_template('account-template.html', **locals())

@app.route("/bank/Lewis/manage/", methods=['GET', 'POST'])
def manage():
    return render_template('manage-template.html', **locals())


@app.route("/bank/Lewis/homepage/", methods=['GET', 'POST'])
def homepage():
    # if "homepage" in session:
    #     username = session["homepage"]
    # else:
    #     return redirect(url_for("login"))

    return render_template('homepage-template.html', **locals())

@app.route("/bank/Lewis/logout/", methods=['GET', 'POST'])
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(host='127.0.0.1', port=8001)