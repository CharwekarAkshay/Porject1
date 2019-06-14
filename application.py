import os

from passlib.hash import pbkdf2_sha256

from flask import Flask, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# engine = create_engine(os.getenv("postgresql://postgres:root@localhost:5432/books"))
engine = create_engine("postgresql://postgres:root@localhost:5432/books")
db = scoped_session(sessionmaker(bind=engine))

""" 
    GoodReads API
    Key : qqEZWhks7b45cLgTHtmXg
    Secret:  5b0zPSNyzYStmV8P8GaMiQjZVNcMDC1Fs1VcGdYUxB4
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        #add testcase if data is not stored in the database then we have to render the registerpage with error
        #Get all the parameter from the request
        #Check password and repassword before storing the data
        # Encrypt the password before stroing

        username = request.form.get("username")
        userpassword = request.form.get("password")
        repassword = request.form.get("repassword")
        mobile = request.form.get("mobile")

        if userpassword == repassword:
            userpassword = pbkdf2_sha256.encrypt(userpassword,rounds=20000, salt_size=20)
            db.execute("INSERT into users(user_name,user_password,mobile) values (:username, :userpassword, :mobile)", {"username":username, "userpassword": userpassword,"mobile":mobile})
            db.commit()
        # Add validation if the password and repassword doesn't match
        return render_template("register.html")


@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/home")
def home():
    return render_template("home.html")