#from cs50 import SQL
import os
from flask_sqlalchemy import SQLALCHEMY
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology, gened

# Configure application
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE"]
db = SQLALCHEMY(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable)
	def __init__(self, name):
		self.name = name


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
#db = SQL("sqlite:///courses50.db")

# List out GenEd Requirements
gen = ["Aesthetic and Interpretive Understanding", "Culture and Belief", "Societies of the World", "United States in the World", "Ethical Reasoning", "Empirical and Mathematical Reasoning", "Science of the Physical Universe", "Science of Living Systems"]

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#Index route
@app.route("/")
@login_required
def index():
	#List of semesters and data for each
	semesters = ["1st Freshman", "2nd Freshman", "1st Sophmore", "2nd Sophmore", "1st Junior", "2nd Junior", "1st Senior", "2nd Senior"]
	selected = [[],[],[],[],[],[],[],[]]
	filled = {}

	#Select user's courses
	courses = db.execute("SELECT cat_num, sem FROM user_courses WHERE user_id = :id", id=session["user_id"])

	#Find all data for each course
	for row in courses:
		search = db.execute("SELECT number, CourseOverall FROM Qcourses WHERE cat_num=:q LIMIT 1", q=row["cat_num"])
		if search:
			row["abbrev"] = search[0]["number"]
			row["score"] = search[0]["CourseOverall"]
		search = db.execute("SELECT title, notes, cat_num FROM courses WHERE (cat_num LIKE :q)", q=row["cat_num"])
		if search:
			row["title"] = search[0]["title"]
			row["notes"] = search[0]["notes"]
		if row["notes"]:
			row["gened"] = gened(row["notes"])

		#Determine what semester the course should be in
		if row["sem"]:
			selected[row["sem"] - 1].append(row)

	#Check if each requirment is filled
	for req in gen:
		temp = db.execute("SELECT cat_num FROM user_courses WHERE (gened=:req) AND (user_id = :id) LIMIT 1", req=req, id=session["user_id"])
		if temp:
			filled[req] = db.execute("SELECT title FROM courses WHERE (cat_num=:num)", num=int(temp[0]["cat_num"]))

	return render_template("index.html", courses=courses, select=selected, sem=semesters, gened=gen, fill=filled)

#Search route - looks for courses in the database
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
	if request.method == "POST":
		query = request.form.get("courses")
		semester = request.form.get("semester")
		temp = []
		course = []

		#Check for query string
		if not query:
			return apology("give a query, or %", 400)

		#Write query
		rows = "SELECT courses.title, courses.notes, Qcourses.cat_num, Qcourses.number, courses.fall, courses.spring FROM courses INNER JOIN Qcourses ON courses.cat_num=Qcourses.cat_num "
		params = ["WHERE (Qcourses.number LIKE :q) ", "WHERE (courses.title LIKE :q) ", ""]

		if semester == "fall":
			params[2] = "AND (courses.fall = 'Y') "
		elif semester == "spring":
			params[2] = "AND (courses.spring = 'Y') "

		query = "%" + query + "%"
		course = db.execute(rows + params[0] + params[2] + "UNION " + rows + params[1] + params[2] + "ORDER BY Qcourses.number ASC", q=query)

		#Get GenEd requirements
		for row in course:
			if row["notes"]:
				row["gened"] = gened(row["notes"])
		return render_template("search.html", results=course, gen=gen)
	else:
		return render_template("search.html", gen=gen)

#Adds courses from search to user
@app.route("/add", methods=["POST"])
@login_required
def add():
	num = request.form.get("saved")

	#Check if the course has already been added
	out = db.execute("SELECT * FROM user_courses WHERE (cat_num=:num) AND (user_id=:id)", num=num, id=session["user_id"])
	if out:
		return apology("already selected", 400)

	db.execute("INSERT INTO user_courses (user_id, cat_num, sem) VALUES (:id, :num, :sem)", id=session["user_id"], num=num, sem="0")
	return redirect("/")

#Allows user to add listed courses to planner
@app.route("/semester", methods=["POST"])
@login_required
def semester():
	if not request.form.get("semester"):
		return apology("select a semester", 400)

	if not request.form.get("year"):
		return apology("select a year", 400)

	sem = int(request.form.get("semester"))
	year = int(request.form.get("year"))
	num = request.form.get("saved")

	#Check if possible to take class that semester
	possible = db.execute("SELECT fall, spring FROM courses WHERE cat_num=:num", num=num)
	if not possible:
		return apology("not this semester", 400)
	if sem == 1 and possible[0]["fall"] != "Y":
		return apology("not this semester", 400)
	elif sem == 2 and possible[0]["spring"] != "Y":
		return apology("not this semester", 400)
	
	#Update info on what semester
	db.execute("UPDATE user_courses SET sem = :sem WHERE (cat_num = :num) AND (user_id=:id)", sem=sem+year, num=num, id=session["user_id"])

	return redirect("/")

#Remove course from user list
@app.route("/remove", methods=["POST"])
@login_required
def remove():
	num = request.form.get("remove")
	db.execute("DELETE FROM user_courses WHERE (cat_num=:q) AND (user_id=:id)", q=num, id=session["user_id"])

	return redirect("/")

#Remove course from user's planner
@app.route("/reset", methods=["POST"])
@login_required
def reset():
	num = request.form.get("reset")
	db.execute("UPDATE user_courses SET sem=:sem, gened='None' WHERE (cat_num=:num) AND (user_id=:id)", sem=0, num=num, id=session["user_id"])

	return redirect("/")

#Set course as a GenEd Requirement
@app.route("/requirements", methods=["POST"])
@login_required
def requirements():

	if not request.form.get("requirements"):
		apology("select course", 400)

	course = request.form.get("requirements")
	req = request.form.get("saved")

	db.execute("UPDATE user_courses SET gened=:gen WHERE (cat_num=:num) AND (user_id=:id)", gen=req, num=course, id=session["user_id"])

	return redirect("/")

#Remove course from requirement
@app.route("/remreq", methods=["POST"])
@login_required
def remreq():
	req = request.form.get("remreq")
	db.execute("UPDATE user_courses SET gened='None' WHERE (gened=:gen) AND (user_id=:id)", gen=req, id=session["user_id"])
	return redirect("/")


####FUNCTIONS FOR LOGGING IN####
#Loging route
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("provide a username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("provide a password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("wrong password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

#Lougout route
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

#Registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
           # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        elif db.execute("SELECT * FROM users WHERE username = :username",
                        username=request.form.get("username")):
            return apology("username taken", 400)

        # Input username and password to database
        has = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO 'users' ('username', 'hash') VALUES(:username, :has)",
                   username=request.form.get("username"), has=has)

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("register.html", error="")