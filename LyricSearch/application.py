import os

from cs50 import SQL
import datetime
from flask import Flask, flash, redirect, render_template, request, session,jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
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

# Custom filter


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ls.db")


@app.route("/")
@login_required
def index():
    songs=db.execute("SELECT song FROM songs ")

    return render_template("index.html",selects=songs)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():



    return redirect("/")



@app.route("/history")
@login_required
def history():

    return


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM login WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
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





@app.route("/register", methods=["GET", "POST"])
def register():


    if request.method == "POST":
        session.clear()
        rows=db.execute("SELECT * from login")
        user=request.form.get("username")
        password=request.form.get("password")
        cpassword=request.form.get("confirmation")
        for row in rows:
            if row["username"]==user:
                return apology("Username already exists",400)
        if password != cpassword:
            return apology("password did not match",400)
        if request.form.get("password") =="" or request.form.get("username")=="":
            return apology("invalid username or password",400)
        a=db.execute("INSERT INTO login (username,password) VALUES(:username,:hash)",username=user,hash= generate_password_hash(str(password)))
        """Register user"""

        session["user_id"] = a
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    return

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    q = request.args.get("q")
    f=q.replace(" ", "")
    info=db.execute("SELECT * FROM songs WHERE song=:q",
                q=f)


    return jsonify(info)




def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
