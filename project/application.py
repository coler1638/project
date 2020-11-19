import os
import selenium
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from bs4 import BeautifulSoup
import requests

from helpers import apology, login_required, lookup

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///diarycards.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")

@app.route("/")
@login_required
def index():
    user_module = db.execute("SELECT module FROM users WHERE id = :user_id", user_id=session["user_id"])
    user_module = user_module[0]["module"]
    if user_module == 1:
        user_module = "Core Mindfulness"
    elif user_module == 2:
        user_module = "Emotion Regulation"
    elif user_module == 3:
        user_module = "Distress Tolerance"
    elif user_module == 4:
        user_module = "Interpersonal Effectiveness"
    else:
        user_module = "No module selected"

    return render_template("index.html", user_module = user_module)

@app.route("/dashboard")
@login_required
def dashboard():
    user_module = db.execute("SELECT module FROM users WHERE id = :user_id", user_id=session["user_id"])
    user_module = user_module[0]["module"]
    if user_module == 1:
        user_module = "Core Mindfulness"
    elif user_module == 2:
        user_module = "Emotion Regulation"
    elif user_module == 3:
        user_module = "Distress Tolerance"
    elif user_module == 4:
        user_module = "Interpersonal Effectiveness"
    else:
        user_module = "No module selected"
    flash(f"the user module is {user_module}")
    return render_template("index.html", user_module = user_module)


@app.route("/diarycard", methods=["GET", "POST"])
@login_required
def diarycard():
    """ Diary Cards home """
    # todo
    return apology("todo", 400)

@app.route("/diarycardhistory")
@login_required
def diarycardhistory():
    """Show history of Diary Card entries"""
     # todo
    return apology("todo", 400)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology")

        # Query database for username, returns a row with that username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/selectmodule", methods=["GET", "POST"])
@login_required
def selectmodule():
    """Select a module"""
    if request.method == "GET":
        return render_template("selectmodule.html")
    else:
        url = "http://3874baab-551e-4198-bc56-330b2e92422f-ide.cs50.xyz/selectmodule"
        req = requests.get(url)
        soup = BeautifulSoup(req, "html.parser")
        print(soup.prettify())
        flash(f"Successfully changed module")
        return redirect("/")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    # If request method was GET
    if request.method == "GET":
        return render_template("signup.html")
    # If request method was POST
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # check if username exists
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)
        # check if password exists
        elif not password:
                return apology("invalid password", 403)
        # check if confirmation exists
        elif not confirmation:
                return apology("invalid password", 403)
        # check passwords match
        elif password != confirmation:
            return apology("passwords must match", 403)
        # check if username taken
        rows = db.execute("SELECT username FROM users WHERE username = :username", username=username)
        if (len(rows) != 0):
            return apology("username taken", 403)
        else:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=username, password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8))
            if new_user:
                # Keep newly registered user logged in
                session["user_id"] = new_user
                # Flash info for the user
                flash(f"Registered as {username}")
                # Redirect user to homepage
                return redirect("/")

@app.route("/skills", methods=["GET", "POST"])
@login_required
def skills():
    """Display DBT Skills"""
     # todo
    return apology("todo", 400)


@app.route("/skillshistory", methods=["GET", "POST"])
@login_required
def skillshistory():
    """Display DBT Skills History"""
     # todo
    return apology("todo", 400)


@app.route("/tips", methods=["GET", "POST"])
@login_required
def tips():
    """Display  Tips & Tricks"""
     # todo
    return apology("todo", 400)

@app.route("/updatecard", methods=["GET", "POST"])
@login_required
def updatecard():
    """update diary card"""
     # todo
    return apology("todo", 400)

@app.route("/updateskills", methods=["GET", "POST"])
@login_required
def updateskills():
    """update skills"""
     # todo
    return apology("todo", 400)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)