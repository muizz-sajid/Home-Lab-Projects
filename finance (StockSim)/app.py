import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session["user_id"]

    track_rows = db.execute(
        "SELECT symbol, SUM(shares) AS tot_shares FROM tracking WHERE user_id = ? GROUP BY symbol HAVING tot_shares > 0", user_id)
    stock_info = []
    grand_total = 0

    for row in track_rows:
        sym = row["symbol"]
        shares = row["tot_shares"]

        stock = lookup(sym)
        price = stock["price"]
        total = shares * price
        grand_total = grand_total + total

        stock_info.append({
            "name": stock["name"],
            "shares": shares,
            "price": usd(price),
            "total": usd(total)
        })

    user_rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = user_rows[0]["cash"]

    grand_total = grand_total + cash

    return render_template("index.html", stock_info=stock_info, cash=usd(cash), grand_total=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":

        sym = request.form.get("symbol")
        shares = request.form.get("shares")

        if not sym:
            return apology("please provide stock symbol")
        if not shares or not shares.isdigit():
            return apology("please provide a positive integer")
        shares = int(shares)

        stock = lookup(sym)
        if stock is None:
            return apology("stock symbol is invalid")
        if shares <= 0:
            return apology("please provide a positive integer")

        rows = db.execute("SELECT cash from users WHERE id = ?", user_id)
        cash = rows[0]["cash"]

        total = shares * stock["price"]
        if total > cash:
            return apology("lack of funds to make that purchase")

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total, user_id)
        db.execute("INSERT INTO tracking (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, stock["symbol"], shares, stock["price"])

        return redirect("/")

    else:

        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    rows = db.execute(
        "SELECT symbol, shares, price, purchase_time FROM tracking WHERE user_id = ?", user_id)

    transactions = []

    for row in rows:
        if row["shares"] > 0:
            trans_type = "BOUGHT"
        else:
            trans_type = "SOLD"

        transactions.append({
            "Type": trans_type,
            "Symbol": row["symbol"],
            "Shares": abs(row["shares"]),
            "Price": usd(row["price"]),
            "Timestamp": row["purchase_time"],
        })

    return render_template("history.html", transactions=transactions)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
        sym = request.form.get("symbol")

        if not sym:
            return apology("please provide stock's symbol")

        stock = lookup(sym)
        if stock is None:
            return apology("stock symbol invalid")

        return render_template("quoted.html", name=stock["name"], price=usd(stock["price"]), symbol=stock["symbol"])

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("please provide username")
        if not password:
            return apology("please provide password")
        if not confirmation:
            return apology("please provide confirmation for password")
        if password != confirmation:
            return apology("passwords do not match")

        hs_password = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, hs_password)
        except ValueError:
            return apology("username already exists")

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":

        sym = request.form.get("symbol")
        shares = request.form.get("shares")

        if not sym:
            return apology("please provide stock symbol")
        if not shares or not shares.isdigit():
            return apology("please provide a positive integer")

        shares = int(shares)
        if shares <= 0:
            return apology("please provide a positive integer")

        rows = db.execute(
            "SELECT COALESCE(SUM(shares), 0) AS tot_shares FROM tracking WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, sym)

        if len(rows) != 1 or rows[0]["tot_shares"] < shares:
            return apology("shares not enough")

        stock = lookup(sym)
        if stock is None:
            return apology("Stock Symbol Invalid")

        per_share = stock["price"]
        owned_shares = shares * per_share

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", owned_shares, user_id)

        db.execute("INSERT INTO tracking (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, sym, -shares, per_share)

        return redirect("/")

    else:
        rows = db.execute(
            "SELECT symbol, SUM(shares) AS Shares FROM tracking WHERE user_id = ? GROUP BY symbol HAVING shares > 0", user_id)

        symbols = [row["symbol"] for row in rows]

        return render_template("sell.html", symbols=symbols)


@app.route("/cash_add", methods=["GET", "POST"])
@login_required
def cash_add():
    user_id = session["user_id"]

    if request.method == "POST":

        amount = request.form.get("amount")

        if not amount:
            return apology("please provide amount to add")

        try:
            amount = float(amount)
        except ValueError:
            return apology("invalid format")

        if amount <= 0:
            return apology("amount must be positive")

        db.execute("Update users SET cash = cash + ? WHERE id = ?", amount, user_id)

        return redirect("/")

    else:
        return render_template("cash_add.html")
