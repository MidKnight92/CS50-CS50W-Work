import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Create purchases table if nonexistent
    db.execute("CREATE TABLE IF NOT EXISTS purchases ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'stock' TEXT NOT NULL, 'purchase_price' INTEGER NOT NULL, 'shares' INTEGER NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, user_id INTEGER FOREGIN KEY REFERENCES users (id) );")

    # Create portfolio table if nonexistent
    db.execute("CREATE TABLE IF NOT EXISTS portfolio ('id'INTEGER PRIMARY KEY AUTOINCREMENT, 'stock' TEXT NOT NULL, 'price' INTEGER NOT NULL, 'shares' INTEGER NOT NULL, user_id INTEGER FOREGIN KEY REFERENCES users (id) );")

    # Query users portfolio
    portfolio = db.execute("SELECT stock, price, shares FROM portfolio WHERE user_id=:userID GROUP BY stock", userID=session.get("user_id"))
    print(portfolio)

    if not portfolio:
            return render_template("index.html", cash=10000, total=10000)
    else:
            # Query database for users current cash balance
            cash = db.execute("SELECT cash FROM users WHERE id=:userID", userID=session.get("user_id"))
            cash = cash[0]["cash"]

            # Create a Temporary Table
            db.execute("CREATE TEMPORARY TABLE current_portfolio ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'symbol' TEXT NOT NULL, 'name' TEXT NOT NULL, 'current_price' INTEGER NOT NULL, 'shares' INTEGER NOT NULL, 'current_worth' INTEGER NOT NULL);")

            for p in portfolio:

                # Query current data on stock
                c = lookup(p["stock"])

                #  Insert Values into current_portfolio table
                db.execute("INSERT INTO current_portfolio (symbol, name, current_price, shares, current_worth) VALUES(?,?,?,?,?)", c["symbol"], c["name"], c["price"], p["shares"], (c["price"] * p["shares"]))

            # Query Users current holdings
            holdings = db.execute("SELECT symbol, name, current_price, SUM(shares), Sum(current_worth) FROM current_portfolio GROUP BY symbol")

            print(holdings)
            # Query Users total stock value
            total = db.execute("SELECT SUM(current_worth) FROM current_portfolio")

            # Calculate total of current stock value plus cash on hand
            grand_total = total[0]["SUM(current_worth)"] + cash

            print(grand_total)

            return render_template("index.html", holdings=holdings, total=grand_total, cash=cash), db.execute("DROP TABLE current_portfolio;")

@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    """Increase Cash"""
    # Query database for current cash value
    cash = db.execute("SELECT cash FROM users WHERE id=:user", user=session.get("user_id"))
    cash = cash[0]["cash"]

    if request.method == "POST":

        contribution = float(request.form.get("contribution"))

        # Ensure cash value was submitted
        if not request.form.get("contribution"):
            return apology("must provide cash value", 403)

        # Ensure nonzero positve value
        if contribution <= 0:
            return apology("must provide positive nonzero cash value", 403)

        # Ensure values are floats
        if not isinstance(contribution, float):
            return apology("need intergers")

        cash = float(cash)

        tmp = db.execute("UPDATE users SET cash = ? WHERE id = ?", (cash + contribution), session.get("user_id"))
        print(tmp)
        return redirect("/")
    else:
        return render_template("cash.html", cash=cash)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        stock = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        ticker = lookup(stock)

        # Ensure user inputed stock symbol
        if not stock:
            return apology("must provide stock symbol", 403)

        # Ensure user inputed valid stock symbol
        if stock != ticker["symbol"]:
            return apology("invalid ticker symbol", 403)
        else:
            price = ticker["price"]
            symbol = ticker["symbol"]

            # Query database for users current cash balance
            cash = db.execute("SELECT cash FROM users WHERE id=:userID", userID=session.get("user_id"))
            cash = cash[0]["cash"]

            # Ensure user has sufficient funds
            if (price * shares) > cash:
                return apology("insufficient funds", 403)
            else:
                difference = cash - (price * shares)

                # Insert values into purchases table
                db.execute("INSERT INTO purchases (user_id, stock, purchase_price, shares) VALUES(?,?,?,?)", session.get("user_id"), symbol, price, shares)

                # Query database for username
                rows = db.execute("SELECT stock FROM portfolio WHERE user_id =:user AND stock=:stock GROUP BY stock", user=session.get("user_id"), stock=stock)

                # Check for stock holdings
                if len(rows) == 0:

                    # Insert values into portfolio table
                    db.execute("INSERT INTO portfolio (user_id, stock, price, shares) VALUES(?,?,?,?)", session.get("user_id"), symbol, price, shares)
                else:

                    qty = db.execute("SELECT SUM(shares) from portfolio WHERE user_id=:user GROUP BY stock", user=session.get("user_id"))
                    qty = int(qty[0]["SUM(shares)"]) + shares

                    db.execute("UPDATE portfolio set shares = ?, price = ? WHERE stock = ? AND user_id = ?", qty, price, symbol, session.get("user_id"))

                # Update cash value in users table
                db.execute("UPDATE users SET cash = ? WHERE id = ?", difference, session.get("user_id"))

                return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


# ORDER BY timestamp
@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    purchases = db.execute("SELECT * FROM purchases WHERE user_id=:user", user=session.get("user_id"))
    sales = db.execute("SELECT * FROM sales WHERE user_id=:user", user=session.get("user_id"))
    print(purchases)
    print(sales)

    # Create a Temporary History Table
    db.execute("CREATE TEMPORARY TABLE history ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'symbol' TEXT NOT NULL,  'price' INTEGER NOT NULL, 'shares' INTEGER NOT NULL, 'timestamp' DATETIME);")

    # Insert sales values into History Table
    for s in sales:
        shares = int(s["shares"])
        tmp = db.execute("INSERT INTO history(symbol, price, shares, timestamp) VALUES(?,?,?,?)", s["stock"], s["sold_for"], (-shares), s["timestamp"])

    # Insert purchase values into History Table
    for p in purchases:
        shares = int(p["shares"])
        tmp = db.execute("INSERT INTO history(symbol, price, shares, timestamp) VALUES(?,?,?,?)", p["stock"], p["purchase_price"], shares, p["timestamp"])

    # Query history table order data by timestamp
    tmp = db.execute("SELECT * FROM history ORDER BY timestamp")

    return render_template("history.html", holdings=tmp), db.execute("DROP TABLE history")


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbl = request.form.get("symbol")
        quote = lookup(symbl)

        # Ensure valid stock ticker
        if quote != None:
            return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])
        else:
            return apology("invalid ticker symbol", 403)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 403)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        # All fields are provided for now ensure user does not already exist
        else:

            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

            # Query returned a user - username is taken
            if len(rows) == 1:
                return apology("username taken", 403)

            # Add user to database
            else:
                username = request.form.get("username")
                password = generate_password_hash(request.form.get("password"))
                db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=username, password=password)
                return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Query database for users holdings
    holdings = db.execute("SELECT stock, Sum(shares) FROM portfolio WHERE user_id=:user GROUP BY stock", user=session.get("user_id"))

    # User reached route via POST (as by clicking a link or via redirect)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Ensure that user picked a ticker symbol
        if not symbol:
            return apology("must pick ticker symbol", 403)

        # Ensure that user picked valid amount of shares
        if shares <= 0:
            return apology("must pick a positive nonzero number", 403)

        for h in holdings:
            # Ensure that user picked valid amount of holdings on share
            if symbol == h["stock"]:
                if shares > h["Sum(shares)"]:
                    return apology("must pick a valid amount of shares", 403)
                else:

                    difference = h["Sum(shares)"] - shares
                    print("HERE IS DIFFERENCE",difference)
                    sale_price = lookup(symbol)
                    sale_price = sale_price["price"]

                    # Create a sales table
                    db.execute("CREATE TABLE IF NOT EXISTS sales ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'stock' TEXT NOT NULL, 'sold_for' INTEGER NOT NULL, 'shares' INTEGER NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, user_id INTEGER FOREGIN KEY REFERENCES users (id) );")

                    # Insert data into sales table
                    db.execute("INSERT INTO sales (stock, sold_for, shares, user_id) VALUES(?,?,?,?)", symbol, sale_price, shares, session.get("user_id"))

                    # Query users cash in users table
                    cash = db.execute("SELECT cash FROM users WHERE id=:user", user=session.get("user_id"))
                    cash = int(cash[0]["cash"])


                    # Update portfolio holdings (Remove stocks with 0 shares from portfolio table)
                    if difference <= 0:
                        db.execute("DELETE FROM portfolio WHERE stock=:stock AND user_id=:user", stock=symbol, user=session.get("user_id"))

                         # Update cash value in users table
                        db.execute("UPDATE users SET cash = ? WHERE id = ?", (cash + (sale_price * shares)), session.get("user_id"))
                    else:
                        current = db.execute("UPDATE portfolio SET shares = ? WHERE user_id = ? AND stock = ?", difference, session.get("user_id"), symbol)

                        # Update cash value in users table
                        db.execute("UPDATE users SET cash = ? WHERE id = ?", (cash +(sale_price * shares)), session.get("user_id"))

                    break


        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", holdings=holdings)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
