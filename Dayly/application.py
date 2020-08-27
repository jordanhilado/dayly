import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final.db")


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    text = db.execute("SELECT text FROM tasks WHERE user_id = :id", id=session["user_id"])
    title = db.execute("SELECT title FROM list_titles WHERE user_id = :id", id=session["user_id"])
    if len(title) > 0:
        return render_template("tasks.html", text=text, title=title)
    else:
        return render_template("newlist.html")


@app.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    text = db.execute("SELECT text FROM notes WHERE user_id = :id", id=session["user_id"])
    title = db.execute("SELECT title FROM note_titles WHERE user_id = :id", id=session["user_id"])
    if len(text) > 0:
        return render_template("notes.html", text=text, title=title)
    else:
        return render_template("newnote.html")


@app.route("/addnote", methods=["GET", "POST"])
@login_required
def addnote():
    if request.method =="POST":
        notetext = request.form.get("notetext")
        title = request.form.get("title")
        db.execute("INSERT INTO notes (user_id, text, list) VALUES (:id, :notetext, :title)", id=session["user_id"], notetext=notetext, title=title)
        db.execute("INSERT INTO note_titles (user_id, title) VALUES (:id, :title)", id=session["user_id"], title=title)
        flash("Note Created.")
        return redirect("/notes")


@app.route("/addlist", methods=["GET", "POST"])
@login_required
def addlist():
    if request.method =="POST":
        todo = request.form.get("task")
        title = request.form.get("title")
        db.execute("INSERT INTO tasks (user_id, text, list) VALUES (:id, :todo, :title)", id=session["user_id"], todo=todo, title=title)
        db.execute("INSERT INTO list_titles (user_id, title) VALUES (:id, :title)", id=session["user_id"], title=title)
        flash("List Created.")
        return redirect("/tasks")


@app.route("/changepass", methods=["GET", "POST"])
@login_required
def changepass():
    if request.method =="POST":
        nonhash = request.form.get("newpw")
        firstpw = request.form.get("password1")
        if nonhash != firstpw:
            flash("Passwords do not match - Try again.")
            return redirect("/settings")
        else:
            newnew = generate_password_hash(nonhash)
            db.execute("UPDATE users SET hash = :newnew WHERE id = 1", newnew=newnew)
            flash("Password Changed.")
            return redirect("/settings")


@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    if request.method =="POST":
        task = request.form.get("task")
        if not task:
            return apology("please select a task", 403)
        else:
            db.execute("DELETE FROM tasks WHERE text = :task AND user_id = :id", task=task, id=session["user_id"])
            flash("Task removed.")
            return redirect("/tasks")


@app.route("/deletelist", methods=["GET", "POST"])
@login_required
def deletelist():
    tasks = db.execute("SELECT text FROM tasks WHERE user_id = :id", id=session["user_id"])
    if request.method =="POST":
        title = request.form.get("title")
        if not title:
            return apology("please select a list", 403)
        else:
            if len(tasks) > 0:
                db.execute("DELETE FROM tasks WHERE list = :title AND user_id = :id", title=title, id=session["user_id"])
                db.execute("DELETE FROM list_titles WHERE title = :title AND user_id = :id", title=title, id=session["user_id"])
                flash("List removed.")
                return redirect("/tasks")
            else:
                db.execute("DELETE FROM list_titles WHERE title = :title AND user_id = :id", title=title, id=session["user_id"])
                flash("List removed.")
                return redirect("/tasks")


@app.route("/deletenote", methods=["GET", "POST"])
@login_required
def deletenote():
    notetext = db.execute("SELECT text FROM notes WHERE user_id = :id", id=session["user_id"])
    if request.method =="POST":
        title = request.form.get("title")
        if not title:
            return apology("please select a list", 403)
        else:
            if len(notetext) > 0:
                db.execute("DELETE FROM notes WHERE list = :title AND user_id = :id", title=title, id=session["user_id"])
                db.execute("DELETE FROM note_titles WHERE title = :title AND user_id = :id", title=title, id=session["user_id"])
                flash("Note removed.")
                return redirect("/notes")
            else:
                db.execute("DELETE FROM note_titles WHERE title = :title AND user_id = :id", title=title, id=session["user_id"])
                flash("Note removed.")
                return redirect("/notes")


@app.route("/additem", methods=["GET", "POST"])
@login_required
def additem():
    title = db.execute("SELECT title FROM list_titles WHERE user_id = :id", id=session["user_id"])
    if request.method =="POST":
        todo = request.form.get("task")
        for i in title:
            db.execute("INSERT INTO tasks (user_id, text, list) VALUES (:id, :todo, :title)", id=session["user_id"], todo=todo, title=i["title"])
        flash("Task added.")
        return redirect("/tasks")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    title = db.execute("SELECT title FROM list_titles WHERE user_id = :id", id=session["user_id"])
    if request.method =="POST":
        text = request.form.get("task")
        new = request.form.get("new")
        db.execute("DELETE FROM tasks WHERE text = :text AND user_id = :id", text=text, id=session["user_id"])
        for i in title:
            db.execute("INSERT INTO tasks (user_id, text, list) VALUES (:id, :new, :title)", id=session["user_id"], new=new, title=i["title"])
        flash("Task edited.")
        return redirect("/tasks")
    


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    return render_template("settings.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username.")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password.")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Incorrect username/password.")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Successfully logged in.")
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


@app.route("/calendar", methods=["GET", "POST"])
@login_required
def calendar():
    return render_template("calendar.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return apology("must provide username", 403)
        elif not password:
            return apology("must provide password", 403)
        elif password != confirmation:
            return apology("passwords don't match", 403)
        elif db.execute("SELECT username FROM users WHERE username = ?", (username)):
            return apology("username taken", 403)
        pw = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :oof)", username=username, oof=pw)
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
