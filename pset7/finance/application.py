import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
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


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == 'POST':
        if request.form.get("amount"):
            # handle negative and non-numeric input
            try:
                float(request.form.get("amount"))
            except ValueError:
                return apology("must provide valid amount", 400)

            if float(request.form.get("amount")) <= 0:
                return apology("must provide valid amount", 400)
            elif float(request.form.get("amount")) >= 1000:
                flash("Wow, that's quite much! ")
            elif float(request.form.get("amount")) < 1000 and float(request.form.get("amount")) >= 100:
                flash("Cash added! ")
            else:
                flash("That little? Poor fella...")

            # update amount of cash
            cash_left = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])[0]["cash"]
            db.execute('UPDATE users SET cash = :cash WHERE id = :id', cash=cash_left + float(request.form.get("amount")), id=session["user_id"])
            return redirect("/")

        elif request.form.get("shares"):
            # buy shares
            symbol = request.form.get("symbol")
            shares = request.form.get("shares")
            # handle fractional, negative, and non-numeric share number
            if not symbol or lookup(symbol) == None:
                return apology("must provide valid symbol and share number", 400)
            elif shares.isdigit() == False or int(shares) <= 0:
                return apology("must provide valid share number", 400)

            # calculate total price for the buy request
            curr_price = lookup(symbol)["price"]
            total_price = curr_price * int(shares)

            # db.execute returns list of dicts (one dict, actually), where key == "cash" and value - cash left in user's account
            cash_left = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])[0]["cash"]

            # ensure user has enough money to buy the shares
            if total_price > cash_left:
                return apology("not enough cash left")

            # add stock to the users portfolio
            db.execute("INSERT INTO portfolio (id, Symbol, Company, Shares, Price, Total) VALUES(:id, :Symbol, :Company, :Shares, :Price, :Total)",
                        id=session["user_id"], Symbol=symbol.upper(), Company=lookup(symbol)["name"],
                        Shares=shares, Price=curr_price, Total=total_price)

            # update cash
            db.execute('UPDATE users SET cash = :cash WHERE id = :id', cash=cash_left - total_price, id=session["user_id"])

            flash("Bought!")

            return redirect("/")

        elif request.form.get("shares_sell"):
            # sell shares
            symbol = request.form.get("symbol_sell")
            shares = request.form.get("shares_sell")

            # calculate total price for the sell request
            company_name = lookup(request.form.get("symbol_sell"))["name"]
            curr_price = lookup(request.form.get("symbol_sell"))["price"]
            total_price = curr_price * -int(request.form.get("shares_sell"))

            # db.execute returns list of dicts (one dict, actually), where key == "cash" and value - cash left in user's account
            cash_left = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])[0]["cash"]

            # calculate if user has enough shares for operation to be made
            shares = db.execute("SELECT SUM(Shares) FROM portfolio WHERE id = :id AND Company = :company GROUP BY Company", id = session["user_id"], company=company_name)

            if shares[0]["SUM(Shares)"] < int(request.form.get("shares_sell")):
                return apology("you do not have enough shares for this operation to be completed")

            # add operation to users portfolio
            exe = db.execute("INSERT INTO portfolio (id, Symbol, Company, Shares, Price, Total) VALUES(:id, :Symbol, :Company, :Shares, :Price, :Total)",
                        id=session["user_id"], Symbol=request.form.get("symbol_sell").upper(), Company=lookup(request.form.get("symbol_sell"))["name"],
                        Shares=-int(request.form.get("shares_sell")), Price=curr_price, Total=total_price)

             # update cash
            db.execute('UPDATE users SET cash = :cash WHERE id = :id', cash=cash_left - total_price, id=session["user_id"])

            return redirect("/")

    else:
        """Show portfolio of stocks"""
        cash_left = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])[0]["cash"]
        historical_data = db.execute("SELECT Symbol, Company, SUM(Shares), Price, Total FROM portfolio WHERE id = :id GROUP BY Company", id=session["user_id"])

        # lookup current share prices and calculate current each share's total value
        curr_prices = []
        total_prices = []
        curr_prices = [ lookup(purchase["Symbol"])["price"] for purchase in historical_data ]
        total_prices = [ lookup(purchase["Symbol"])["price"] * purchase["SUM(Shares)"] for purchase in historical_data ]

        # calculate current net portfolio value
        total = cash_left + sum(total_prices)

        # transfer current share prices and total share value to historical_data (so that it can be accesed by index.html)
        for i in range(len(curr_prices)):
            historical_data[i]["Price"] = usd(curr_prices[i])
            historical_data[i]["Total"] = usd(total_prices[i])

        companies = db.execute("SELECT Symbol FROM portfolio WHERE id = :id GROUP BY Symbol", id = session["user_id"])

        return render_template("index.html", historical=historical_data, cash_left = usd(cash_left), total=usd(total), companies = companies)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        # handle fractional, negative, and non-numeric share number
        if not symbol or lookup(symbol) == None:
            return apology("must provide valid symbol and share number", 400)
        elif shares.isdigit() == False or int(shares) <= 0:
            return apology("must provide valid share number", 400)

        # calculate total price for the buy request
        curr_price = lookup(symbol)["price"]
        total_price = curr_price * int(shares)

        # db.execute returns list of dicts (one dict, actually), where key == "cash" and value - cash left in user's account
        cash_left = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])[0]["cash"]

        #ensure user has enough money to buy the shares
        if total_price > cash_left:
            return apology("not enough cash left")

        # add stock to the users portfolio
        db.execute("INSERT INTO portfolio (id, Symbol, Company, Shares, Price, Total) VALUES(:id, :Symbol, :Company, :Shares, :Price, :Total)",
                    id=session["user_id"], Symbol=symbol.upper(), Company=lookup(symbol)["name"],
                    Shares=shares, Price=curr_price, Total=total_price)

        # update cash
        db.execute('UPDATE users SET cash = :cash WHERE id = :id', cash=cash_left - total_price, id=session["user_id"])

        flash("Bought!")

        return redirect("/")

    else:
        return render_template("buy.html")

@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Let user change password for existing account"""
    if request.method == "POST":

        # Ensure password was submitted
        if not request.form.get("newpassword"):
            return apology("must provide password", 400)
        # Ensure passwords match
        elif request.form.get("newpassword") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        elif request.form.get("newpassword").isalpha() == True:
            return apology("password must contain at least one numeric symbol")

        # encrypt new password
        hash = generate_password_hash(request.form.get("newpassword"))
        print(hash)
        # update user's password in database
        result = db.execute("UPDATE users SET hash = :hash WHERE id = :id", hash=hash, id = session["user_id"])

        if not result:
            return apology("password not available", 400)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changepass.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # extract history of operation for a particular user
    historical_data = db.execute("SELECT Symbol, Company, Shares, Price, Total, Timestamp FROM portfolio WHERE id = :id", id=session["user_id"])

    return render_template("history.html", historical=historical_data)

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
    if request.method == "POST":
        # ensure user provides symbol
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        # ensure symbol is valid
        if lookup(request.form.get("symbol")) == None:
            return apology("invalid symbol", 400)

        # store return values of lookup(), so I can pass them to html files later easily
        quote_py = lookup(request.form.get("symbol"))

        return render_template("quoted.html", company=quote_py["name"], symbol=quote_py["symbol"], price=usd(quote_py["price"]))
    else:
        return render_template("quote.html")


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
        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        elif request.form.get("password").isalpha() == True:
            return apology("password must contain at least one numeric symbol")

        # protect the user - hash the password
        hash = generate_password_hash(request.form.get("password"))

        # store user's data in the database, so they can log in again later
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"), hash=hash)
        if not result:
            return apology("username or/and password not available", 400)

        # Log in user automatically
        session["user_id"] = result

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        
        # calculate total price for the sell request
        company_name = lookup(request.form.get("symbol"))["name"]
        curr_price = lookup(request.form.get("symbol"))["price"]
        total_price = curr_price * -int(request.form.get("shares"))

        # db.execute returns list of dicts (one dict, actually), where key == "cash" and value - cash left in user's account
        cash_left = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])[0]["cash"]

        # calculate if user has enough shares for operation to be made
        shares = db.execute("SELECT SUM(Shares) FROM portfolio WHERE id = :id AND Company = :company GROUP BY Company", id = session["user_id"], company=company_name)

        if shares[0]["SUM(Shares)"] < int(request.form.get("shares")):
            return apology("you do not have enough shares for this operation to be completed")

        # add operation to users portfolio
        exe = db.execute("INSERT INTO portfolio (id, Symbol, Company, Shares, Price, Total) VALUES(:id, :Symbol, :Company, :Shares, :Price, :Total)",
                    id=session["user_id"], Symbol=request.form.get("symbol").upper(), Company=lookup(request.form.get("symbol"))["name"],
                    Shares=-int(request.form.get("shares")), Price=curr_price, Total=total_price)

         # update cash
        db.execute('UPDATE users SET cash = :cash WHERE id = :id', cash=cash_left - total_price, id=session["user_id"])

        return redirect("/")

    else:
        # extract list of companies user has in portfolio
        companies = db.execute("SELECT Symbol FROM portfolio WHERE id = :id GROUP BY Symbol", id = session["user_id"])

        return render_template("sell.html", companies = companies)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
