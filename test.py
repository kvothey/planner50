from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import sqlite3

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response






# from bs4 import BeautifulSoup
# from urllib import request

# webpage = request.urlopen('https://courses.cs50.net/course/125186')
# soup = BeautifulSoup(webpage,'html.parser')

# file = open("courses.cs50.txt", "w")
# file.write(soup.prettify())

# #print(soup.prettify())
