from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def overview():
    """Show overview of budget"""
    if request.method == "POST":
        category = request.form.get("category")
        notes = request.form.get("notes")
        
        # Check if fields are filled out correclty 
        if not category:
            return apology("Missing Category Name", 400)

        # Insert new category into budget_category table
        db.execute("INSERT INTO budget_categories (user_id, category, notes, amount) VALUES (?, ?, ?, ?)", session["user_id"], category, notes, 0) 
        
        return redirect("/")

    budgets = db.execute("SELECT * FROM budget_categories WHERE user_id = ?", session["user_id"])

    # Total from all categories amounts added together
    total_amount = db.execute("SELECT SUM(amount) AS amount FROM budget_categories WHERE user_id = ?", session["user_id"])
    total = total_amount[0]['amount']
    
    # If there is a new user, then budgets will be empty and total will be of NonType, which is not support for the usd function. So equal total to 0.
    if not budgets:
        total = 0

    return render_template("overview.html", budgets=budgets, total=total)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        usernames = db.execute("SELECT username FROM users WHERE username = ?", username)

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure username is not taken
        elif int(len(usernames)) > 0:
            return apology("username is already taken", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensures password matches confirmation
        elif password != confirmation:
            return apology("passwords don't match", 400)

        # If everything is inputed correctly then insert username and password hash into database, and redirect user to homepage and keep them logged in. 
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
        
        return redirect("/")

        # If using GET method, load registration page.
    else:
        return render_template("register.html")


@app.route("/expenses", methods=["GET", "POST"])
@login_required
def expenses():
    """File any new expenses"""
    if request.method == "POST":
        date = request.form.get("date")
        amount = request.form.get("amount")
        description = request.form.get("description")
        category = request.form.get("category")
        
        # Make sure fields are filled out correctly
        if not date:
            return apology("Missing Date", 400)
        elif not amount:
            return apology("Missing Amount", 400)
        elif amount.isdigit() == False:
            return apology("Amount Needs to Be a Number", 400)
        elif not category:
            return apology("Missing Category", 400)


        # Add items to summary table as a new expense transaction
        db.execute("INSERT INTO cash (transaction_date, expenses, description, category, user_id) VALUES (?, ?, ?, ?, ?)", date, amount, description, category, session["user_id"])
        
        # Subtract new amount to the specific category total
        db.execute("UPDATE budget_categories SET amount = amount - ? WHERE user_id = ? AND category = ?", amount, session["user_id"], category)
        
        return redirect("/expenses")

    budgets = db.execute("SELECT * FROM budget_categories WHERE user_id = ?", session["user_id"])

    # Income summary table
    # Used https://www.w3schools.com/sql/sql_null_values.asp to learn how to use the IS NOT NULL operator.
    transactions = db.execute("SELECT transaction_date, expenses, description, category FROM cash WHERE user_id = ? AND expenses IS NOT NULL", session["user_id"])
    
    return render_template("expenses.html", budgets=budgets, transactions=transactions)


@app.route("/income", methods=["GET", "POST"])
@login_required
def income():
    """File any new income transactions"""
    if request.method == "POST":
        date = request.form.get("date")
        amount = request.form.get("amount")
        description = request.form.get("description")
        category = request.form.get("category")
        
        # Make sure fields are filled out correctly
        if not date:
            return apology("Missing Date", 400)
        elif not amount:
            return apology("Missing Amount", 400)
        elif amount.isdigit() == False:
            return apology("Amount Needs to Be a Number", 400)
        elif not category:
            return apology("Missing Category", 400)


        # Add items to summary table as a new income transaction
        db.execute("INSERT INTO cash (transaction_date, income, description, category, user_id) VALUES (?, ?, ?, ?, ?)", date, amount, description, category, session["user_id"])
        
        # Add new amount to the specific category total
        db.execute("UPDATE budget_categories SET amount = amount + ? WHERE user_id = ? AND category = ?", amount, session["user_id"], category)
        
        return redirect("/income")

    budgets = db.execute("SELECT * FROM budget_categories WHERE user_id = ?", session["user_id"])

    # Income summary table
    transactions = db.execute("SELECT transaction_date, income, description, category FROM cash WHERE user_id = ? AND income IS NOT NULL", session["user_id"])
    return render_template("income.html", budgets=budgets, transactions=transactions)


@app.route("/distribution_tool", methods=["GET", "POST"])
@login_required
def distribution_tool():
    """Distribute any amount across your budget"""
    if request.method == "POST":
        amount = request.form.get("amount")
        if not amount:
            return apology("Missing Amount", 400)
        elif amount.isdigit() == False:
            return apology("Amount Is Not a Number", 400)
        # Takes each percentage that exists and divides the amount by those percentages
        percentages = db.execute("SELECT percentage, id FROM distribution WHERE user_id = ?", session["user_id"])
        for i in range(len(percentages)):
            percentage = percentages[i]['percentage']
            id = percentages[i]['id']
            # Used https://stackoverflow.com/questions/8362792/how-do-i-shift-the-decimal-place-in-python/8362821 to better understand how to make the integer percentages into decimals so I can multiply the amount to be distributed by the decimal to get an accurate answer.  
            new_amount = float(amount) * (percentage / 100.)
            db.execute("UPDATE distribution SET amount = ? WHERE id = ?", new_amount, id)

        return redirect("/distribution_tool")
        # For the visual table of categories that already exist
    distributions = db.execute("SELECT category, percentage, amount FROM distribution WHERE user_id = ?", session["user_id"])
    return render_template("distribution_tool.html", distributions=distributions)


@app.route("/create_tool", methods=["GET", "POST"])
@login_required
def create_tool():
    """Show portfolio of stocks"""

    if request.method == "POST":
        category = request.form.get("category")
        percentage = request.form.get("percentage")
        db.execute("INSERT INTO distribution (user_id, category, percentage) VALUES (?, ?, ?)", session["user_id"], category, percentage)
        return redirect("/create_tool")

    # For the drop down menu when adding a new tool
    categories = db.execute("SELECT category FROM budget_categories WHERE user_id = ?", session["user_id"])
    
    # For the visual table of categories that already exist
    distributions = db.execute("SELECT category, percentage, id FROM distribution WHERE user_id = ?", session["user_id"])
    return render_template("create_tool.html", categories=categories, distributions=distributions)

@app.route("/delete_distribution", methods=["POST"])
@login_required
def delete_distribution():
    """Delete distribution category"""
    id = request.form.get("id")
    if id: 
        db.execute("DELETE FROM distribution WHERE id = ?", id)
    return redirect("/create_tool")

@app.route("/delete_category", methods=["POST"])
@login_required
def delete_category():
    """Delete category"""
    id = request.form.get("id")
    if id: 
        db.execute("DELETE FROM budget_categories WHERE id = ?", id)
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)