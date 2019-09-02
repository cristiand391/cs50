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

    rows = db.execute(
        'SELECT symbol, SUM(CASE WHEN operation = "SELL" THEN -shares ELSE shares END) shares FROM transactions WHERE id = :id GROUP BY symbol;', id=session['user_id'])

    cash = db.execute('SELECT cash FROM users WHERE id = :id', id=session['user_id'])[0]['cash']

    grand_total = cash

    for row in rows:
        stock = lookup(row['symbol'])

        row['name'] = stock['name']
        row['price'] = stock['price']
        row['total'] = row['shares'] * stock['price']

        grand_total += row['shares'] * stock['price']

    rows.append({
        'symbol': 'CASH',
        'cash': cash,
        'total': grand_total
    })

    return render_template('index.html', stocks=rows)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST
    if request.method == 'POST':

        # Ensure shares is a positive integer:
        try:
            if int(request.form.get('shares')) < 1:
                return apology("input isn't a positive integer", 400)
        except ValueError:
            return apology("input isn't an integer", 400)

        # Ensure symbol was provided
        if not request.form.get('symbol'):
            return apology('must provide symbol', 403)

        # Ensure symbol exists
        if lookup(request.form.get('symbol')) == None:
            return apology("symbol doens't exist")

        shares = int(request.form.get('shares'))

        stock_price = lookup(request.form.get('symbol'))['price']

        cash = db.execute('SELECT cash FROM users WHERE id = :id', id=session['user_id'])[0]['cash']

        # Check if the user can afford the stock
        if stock_price * shares > cash:
            return apology(f"You don't have enough cash to buy {shares} shares.", 403)

        db.execute('INSERT INTO transactions (id, operation, symbol, shares, price) VALUES(:id, :operation, :symbol, :shares, :stock_price)',
            id=session['user_id'],
            symbol=request.form.get('symbol').upper(),
            operation='BUY',
            shares=shares,
            stock_price=stock_price
            )

        db.execute('UPDATE users SET cash = :cash WHERE id = :id',
            cash=cash - shares * stock_price,
            id=session['user_id'])

        # Redirect user to home page
        return redirect('/')

    # User reached route via GET
    else:
        return render_template('buy.html')


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    users_rows = db.execute('SELECT username FROM users')

    users = [user['username'] for user in users_rows]

    if len(str(request.args.get('username'))) > 1 and request.args.get('username') not in users:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    rows = db.execute('SELECT operation, symbol, shares, price, date FROM transactions WHERE id = :id',
        id=session['user_id'])

    return render_template('history.html', stocks=rows[::-1])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':

        # Ensure username was submitted
        if not request.form.get('username'):
            return apology('must provide username', 400)

        # Ensure password was submitted
        elif not request.form.get('password'):
            return apology('must provide password', 400)

        # Query database for username
        user = db.execute('SELECT * FROM users WHERE username = :username', username=request.form.get('username'))

        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0]['hash'], request.form.get('password')):
            return apology('invalid username and/or password', 400)

        # Remember which user has logged in
        session['user_id'] = user[0]['id']

        # Redirect user to home page
        return redirect('/')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect('/')


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST
    if request.method == 'POST':

        # Ensure symbol was provided
        if not request.form.get('symbol'):
            return apology('must provide symbol', 400)

        # Get stock info
        stock = lookup(request.form.get('symbol'))

        # Check symbol exists
        if stock == None:
            return apology("symbol doesn't exists", 400)

        return render_template('quoted.html', stock=stock)

    # User reached route via GET
    else:
        return render_template('quote.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST
    if request.method == 'POST':

        # Ensure username was provided
        if not request.form.get('username'):
            return apology('must provide username', 400)

        # Ensure passwords were provided
        elif not request.form.get('password') or not request.form.get('confirmation'):
            return apology('must provide password', 400)

        # Ensure passwords match
        elif request.form.get('password') != request.form.get('confirmation'):
            return apology("passwords doesn't match", 400)

        users_rows = db.execute('SELECT username FROM users')

        users = [user['username'] for user in users_rows]

        if request.form.get('username') in users:
            return apology('username already taken', 400)

        # Insert user and password's hash in the database
        user_id = db.execute('INSERT INTO users(username, hash) VALUES(:username, :hash)',
            username=request.form.get('username'),
            hash=generate_password_hash(request.form.get('password'))
            )

        # Log in new user
        session['user_id'] = user_id

        # Redirect user to home page
        return redirect('/')

    # User reached route via GET
    else:
        return render_template('register.html')


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    rows = db.execute('SELECT symbol, shares FROM transactions WHERE id = :id', id=session['user_id'])

    # Generate a list of stock's symbols owned by the current user
    stocks = {stock["symbol"]: stock["shares"] for stock in rows}

    # User reached route via POST
    if request.method == 'POST':

        if not request.form.get('symbol'):
            return apology('must provide symbol', 403)

        elif request.form.get('symbol') not in stocks:
            return apology("you don't own any stock of this company")

        try:
            if int(request.form.get('shares')) < 1:
                return apology('must prove a positive number of stocks')

            elif int(request.form.get('shares')) > stocks[request.form.get('symbol')]:
                return apology("you don't own that shares")
        except ValueError:
            return apology("input isn't an integer", 403)

        stock_price = lookup(request.form.get('symbol'))['price']

        db.execute('INSERT INTO transactions (id, operation, symbol, shares, price) VALUES(:id, :operation, :symbol, :shares, :price)',
            id=session['user_id'],
            operation='SELL',
            symbol=request.form.get('symbol'),
            shares=request.form.get('shares'),
            price=stock_price
            )

        db.execute('UPDATE users SET cash = cash + :y WHERE id = :id',
            y=stock_price * int(request.form.get('shares')),
            id=session['user_id']
            )

        return redirect('/')

    # User reached route via GET
    else:
        return render_template('sell.html', stocks=stocks)


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Allow user to change his/her password"""

    # User reached route via POST
    if request.method == 'POST':

        # Ensure passwords that were submitted
        if not request.form.get('password'):
            return apology('must provide password', 400)

        elif not request.form.get('new_password') or not request.form.get('confirmation'):
            return apology('must provide a new password', 400)

        elif request.form.get('new_password') != request.form.get('confirmation'):
            return apology("passwords doesn't match")

        user = db.execute('SELECT * FROM users WHERE id = :id', id=session['user_id'])

        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0]['hash'], request.form.get('password')):
            return apology('invalid username and/or password', 400)

        db.execute('UPDATE users SET hash = :hash WHERE id = :id',
                hash=generate_password_hash(request.form.get('new_password')),
                id=session['user_id']
                )

        return redirect('/logout')
    else:
        return render_template('password.html')


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
