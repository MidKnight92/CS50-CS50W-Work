import os
import requests 
import xmltodict
import xmljson
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from flask import Flask, session, request, render_template, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import  generate_password_hash, check_password_hash

from helpers import login_required
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Set api key
KEY = "DEefVRmv7vuvBfgulzzN9A"

@app.route("/")
def index():

    # Create users table if nonexistent
    db.execute('CREATE TABLE IF NOT EXISTS users ("id" SERIAL PRIMARY KEY, "username" TEXT NOT NULL, "hash" TEXT NOT NULL)')

    # Create books table if nonexistent
    db.execute('CREATE TABLE IF NOT EXISTS books ("id" serial PRIMARY KEY, "author" text NOT NULL,"title" text NOT NULL, "isbn" Varchar(13), "year" Varchar(4) NOT NULL)')

    # Create reviews table if nonexistent
    db.execute(' CREATE TABLE IF NOT EXISTS reviews ("id" serial PRIMARY KEY,"rating" integer NOT NULL, "review" Varchar(200), "timestamp" timestamp, "book_id" INTEGER REFERENCES books(id),"user_id" INTEGER REFERENCES users(id))')

    db.commit()

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user """

    if request.method == "GET":

        return render_template("register.html")
    else:
        # Clear user from session
        session.clear()

        # Get data from form
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        rows = db.execute("SELECT username FROM users WHERE username = :username",
            {"username": username}).fetchone()
        
        if rows == None:
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", {"username": username, "hash": password})
            db.commit()
            return redirect("/login")
        else:
            return render_template("register.html", message="Username Taken")

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log in User """
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        rows = db.execute("SELECT * FROM users WHERE username = :username",
            {"username": username}).fetchone()
        
        
        if rows == None or not check_password_hash(rows[2], password):    
            return render_template("login.html", message="Invalid Username or Password")
        else:
            session["user_id"] = rows[0]
            return redirect("/search")
    else:
        session.clear()
        return render_template("login.html")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():  
    """ Search book by (ISBN, title, author) Display a list of possible matching results or message if there were no matches """ 
    if request.method == "POST":
        try:   
            query = request.form.get("query")

            resp = requests.get("https://www.goodreads.com/search/index.xml", params={"q": query, "key": KEY})  

            root = ET.fromstring(resp.content)

            xmlArr = []
            xmlDict = {}

            # Loop through all the nodes (id, title, author, image_url, and small_image_url) in best book XML response
            for child in root.findall("search/results/work/best_book/*"):
                # xmlDict[child.tag] = child.text
                
                # Assign the tag value to a variable
                key = child.tag

                # Assign the text value to a variable
                value = child.text

                # Author nodes need to go into name to assign author's name to the value variable
                if child.tag == "author":
                    name = child.findall("name")
                    for n in name:
                        value = n.text
                
                # Create dictonary with respective key value pairs   
                dict = {key:value} 

                # Update xmlDict with all the key value pairs
                xmlDict.update(dict)

                # Append the xmlDict to xmlArr at the last node then clear xmlDict
                if child.tag == "small_image_url":
                    xmlArr.append(xmlDict)
                    xmlDict = {}

            print(len(xmlArr))
            if len(xmlArr) == 0:
                return render_template("message.html", status="Books - No Matches", message="No Matches", image="./../static/open.jpg")
            else:
                return render_template("books.html", message=xmlArr)
        except ValueError:
            
            return render_template("message.html", status="Error", message="Sorry, an Error Occured", image="./../static/b.jpg")
    else:
        return render_template("search.html")          

@app.route("/books/<int:book_id>", methods=["GET", "POST"])
def book(book_id):
    """ Display title, author, publication year, and reviews (from my site) for specific book """
    
    xmlArr = []
    xmlDict = {}

    if request.method == "GET" or request.method == "POST":
        resp = requests.get("https://www.goodreads.com/book/show.xml", params={"key": KEY, "id":book_id})

        root = ET.fromstring(resp.content)

        # Loop through all the nodes in book show XML response
        for child in root.findall("book/*"):
        
            # Assign the tag value to a variable
            key = child.tag

            # Assign the text value to a variable
            value = child.text

            # Create dictonary with respective key value pairs   
            dict = {key:value} 

            # Update xmlDict with all the key value pairs
            xmlDict.update(dict)

            if child.tag == "work":
                work = child.find("original_publication_year")
                # Assign the tag value to a variable
                key = work.tag

                # Assign the text value to a variable
                value = work.text

                # Create dictonary with respective key value pairs   
                dict = {key: value}

                # Update xmlDict with all the key value pairs
                xmlDict.update(dict)

            # Author nodes need to go into name to assign author's name to the value variable
            if child.tag == "authors":
            
                author = child.findall("author/*")
 
                # Loop through
                for a in author:
                    # Assign the tag value to a variable
                    key = a.tag

                    # Assign the text value to a variable
                    value = a.text

                    # Create dictonary with respective key value pairs   
                    dict = {key:value} 

                    # Update xmlDict with all the key value pairs
                    xmlDict.update(dict)

                    # print(xmlDict)
                    if a.tag == "average_rating":
                        # print(xmlDict)
                        xmlArr.append(xmlDict)
                        xmlDict = {}
    
        # Query db for reviews on my site and display them. 
        reviews = db.execute("SELECT * FROM reviews JOIN books on reviews.book_id = books.id WHERE books.title IN (SELECT title FROM books WHERE title = :title)", {"title":xmlArr[0]["title"]})
        
        print(reviews)
        if request.method == "GET":
            return render_template("book.html", book=xmlArr, reviews=reviews)
        else:

            # Query database for reviews of selected book by user in session
            rows = db.execute("SELECT reviews.id FROM reviews JOIN books ON reviews.book_id = books.id WHERE books.title IN (SELECT title FROM books WHERE title =:title) AND reviews.user_id =:user", {"user":int(session.get("user_id")), "title":xmlArr[0]['title']}).rowcount

            # Query returned a review ask user to review a different book
            if rows != 0:
                return render_template("message.html", status="Failed", message="Sorry, you have already reviewed this book. Please review a different book.", image="./../static/bk.jpg")
            else:
                # Get users review
                text = request.form.get("text")
                rating = int(request.form.get("rating"))

                # Insert Book into db and return id
                bk_id = db.execute("INSERT INTO books (author, title, isbn, year) VALUES (:author, :title, :isbn,:year) RETURNING id", {"author":xmlArr[0]['name'], "title":xmlArr[0]['title'], "isbn":xmlArr[0]['isbn'],"year":xmlArr[0]['original_publication_year']})
                
                book_id = None

                # Get the book id
                for bk in bk_id:
                    book_id = bk[0]
                        
                timestamp = datetime.now()

                # Insert Review
                db.execute("INSERT INTO reviews (rating, review, book_id, user_id, timestamp) VALUES (:rating, :review, :book_id, :user_id, :timestamp)", {"rating":rating, "review":text,"book_id":book_id, "user_id":int(session.get("user_id")), "timestamp": timestamp})

                db.commit()

                return render_template("message.html", status="Success", message="Thank You for your review!", image="./../static/typewriter.jpg")

@app.route("/logout")
def logout():
    """ Log User Out of Session """
    # session.pop("username", None)
    session.clear()
    return redirect("/")

@app.route("/api/<int:isbn>")
def api(isbn):
    """Returns a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score or a 404 error if not found"""

    # Create API Table if nonexistent
    db.execute('CREATE TABLE IF NOT EXISTS api_data ("id" serial PRIMARY KEY, "author" TEXT, "average_score" DECIMAL, "isbn" TEXT,"review_count" INTEGER, "title" TEXT, "year" TEXT)')

    db.commit()
    try:
    
        # Convert isbn int to string
        isbn = str(isbn) 
        # print(isbn)
        # Query api_data
        row = db.execute('SELECT * FROM api_data WHERE isbn=:isbn', {"isbn": isbn}).rowcount

        # print(row)

        # Query returned rows
        if row != 0:
            
            test = db.execute('SELECT SUM(rating), COUNT(reviews) FROM reviews JOIN books ON reviews.book_id=books.id WHERE books.isbn=:isbn', {"isbn": isbn})

            sum_rating = None
            count_total = None

            for k,v in test:
                sum_rating = k
                count_total = v

            obj = {}

            # None of my users have reviewed this book
            if sum_rating== None and count_total == 0:

                result = db.execute('SELECT author, ROUND(average_score, 2), isbn, review_count, title, year FROM api_data WHERE isbn=:isbn')

                for row in result:
                    obj["author"] = row[0]
                    obj["average_score"] = str(row[1])
                    obj["isbn"] = row[2]
                    obj["review_count"] = row[3]
                    obj["title"] = row[4]
                    obj["year"] = row[5]

                return jsonify(obj)
            else:
                result = db.execute('SELECT author, ROUND(AVG(average_score + :rating), 2), isbn, SUM(review_count + :count), title, year FROM api_data WHERE isbn=:isbn GROUP BY author, isbn, title, year', {"rating":sum_rating, "count":count_total, "isbn":isbn})


                for row in result:
                    obj["author"] = row[0]
                    obj["average_score"] = str(row[1])
                    obj["isbn"] = row[2]
                    obj["review_count"] = row[3]
                    obj["title"] = row[4]
                    obj["year"] = row[5]

                return jsonify(obj)

        # Query returned zero rows
        else:

            # Query for Review Counts for Average_Rating, Reviews_count, and ISBN
            res1 = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbn})

            # Convert Data to JSON
            data = json.loads(res1.text)
            data = data["books"][0]
            
            response = {}

            book_id = None
        
            for k, v in data.items():
                if k == "isbn": 
                    response[k] = v
                if k == "average_rating": 
                    response["average_score"] = v
                if k == "reviews_count":
                    response["review_count"] = v
                if k == "id":
                    book_id = v


            # Query Show using book_id need Title, Author, Publication date (year)
            res2 = requests.get("https://www.goodreads.com/book/show.xml", params={"key": KEY, "id": book_id})

            root = ET.fromstring(res2.content)

            # Loop through all the nodes in book show XML response
            for child in root.findall("book/*"):

                # Assign the tag value to a variable
                key = child.tag

                # Assign the text value to a variable
                value = child.text

                if child.tag == "title":
                    response[key] = value

                if child.tag == "work":
                        # Find publication year
                        year = child.find("original_publication_year")
                        
                        # Assign the text value to a variable
                        year_value = year.text  

                        response["year"] = year_value

                # Author nodes need to go into name to assign author's name to the value variable
                if child.tag == "authors":
                    
                    # Find author name
                    author = child.find("author/name")

                    # Assign the text value to a variable
                    author_value = author.text

                    response["author"] = author_value

            print(type(response["average_score"]))

            # Insert values into api_data table
            db.execute('INSERT INTO api_data (author, average_score, isbn, review_count, title, year) VALUES (:author, :average_score, :isbn, :review_count, :title, :year ) RETURNING author, average_score, isbn, review_count, title, year',{"author":response["author"], "average_score":float(response["average_score"]), "isbn": response["isbn"], "review_count":response["review_count"], "title":response["title"], "year":response["year"]})
            
            db.commit()
            
            return jsonify(response)
    except Exception:
        return jsonify({"Error":"Invalid ISBN"}), 404

# ==================================================================== Save =====================================================================
# SAVE: PSQL CLI 
# psql postgres://rsgtoygzkfrppw:4b31eadd39fc624e7665267ff4c5960c6e9543ebd3c8cf315316cd9bbd74d681@ec2-35-173-94-156.compute-1.amazonaws.com:5432/d6i0ph8aoih86u

# SAVE: Paste in terminal to run program
# export FLASK_APP=application.py
# export FLASK_DEBUG=1
# export DATABASE_URL=postgres://rsgtoygzkfrppw:4b31eadd39fc624e7665267ff4c5960c6e9543ebd3c8cf315316cd9bbd74d681@ec2-35-173-94-156.compute-1.amazonaws.com:5432/d6i0ph8aoih86u


# DB SCHEMAS: 
# CREATE TABLE "users" (
#   "id" serial PRIMARY KEY,
#   "username" text NOT NULL,
#   "hash" text NOT NULL
# );

# CREATE TABLE "books" (
#   "id" serial PRIMARY KEY,
#   "author" text NOT NULL,
#   "title" text NOT NULL,
#   "isbn" Varchar(13),
#   "year" Varchar(4) NOT NULL
# );

# CREATE TABLE "reviews" (
#   "id" serial PRIMARY KEY,
#   "rating" integer NOT NULL,
#   "review" Varchar(200), 
#   "timestamp" timestamp,
#   "book_id" INTEGER REFERENCES books(id),
#   "user_id" INTEGER REFERENCES users(id)
# );

# CREATE TABLE "api_data" (
#   'id' PRIMARY KEY SERIAL,
#   'author' VARCHAR, 
#   'average_score' VARCHAR, 
#   'isbn' TEXT,
#   'review_count' INTEGER, 
#   'title' VARCHAR, 
#   'year' VARCHAR
# );
