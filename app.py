import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from math import floor

from helpers import apology, login_required

DISHMAX = 10
UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Configure application
app = Flask(__name__)

# Determine the upload folder used
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
db = SQL("sqlite:///split.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        # Get inputs from form
        if not request.form.get("count"):
            return apology("invalid input", 400)
        count = request.form.get("count")
        method = request.form.get("how")

        # Update user's count and method
        db.execute("UPDATE users SET method = :method, count = :count WHERE id = :id", id=session["user_id"],
                   count=count, method=method)
        return redirect("/method")


@app.route("/venmo", methods=["GET", "POST"])
@login_required
def venmo():
    if request.method == "POST":
        # Get user inputs and validate
        username = request.form.get("username")
        password = request.form.get("password")
        venmo = request.form.get("venmo")

        if not username or not password or not venmo:
            return apology("Missing username and/or password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        # Insert Venmo username
        db.execute("UPDATE users SET venmo = :venmo WHERE username = :username",
                   venmo=venmo, username=username)
        return redirect("/")
    else:
        return render_template("changevenmo.html")


@app.route("/method", methods=["GET"])
@login_required
def method():
    if request.method == "GET":
        # Decided to make /method its own page instead of simply rendering template from index so /method can be reached
        # independently of index
        return render_template("method.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No File Uploaded')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # Submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            return render_template("upload.html")
    else:
        return render_template("upload.html")


@app.route("/manual", methods=["GET", "POST"])
@login_required
def manual():
    if request.method == "GET":
        # Render manual with the user's stored method and count
        row = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        count = row[0]['count']
        method = row[0]['method']

        return render_template("manual.html", method=method, count=count)
    else:
        # Get user's stored method and count
        row = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        count = int(row[0]['count'])
        method = row[0]['method']
        venmo = row[0]['venmo']
        if not venmo:
            venmo = None
        # If evenly...
        if method == "evenly":
            # Validate inputs
            if not request.form.get("totalevenly") or not request.form.get("taxevenly") or not request.form.get("tipevenly"):
                return apology("Invalid Input", 400)

            # Redefine inputs in useful ways
            total = float(request.form.get("totalevenly"))
            tax = float(request.form.get("taxevenly"))
            tip = float(int(request.form.get("tipevenly"))/100)

            # Define Grandtotal all expenses
            grandtotal = total + tax + (total * tip)

            # Determine each person's equal share of the bill
            share = grandtotal / count * 100

            # Round each person's share down so as not to display fractions of cents
            share = floor(share) / 100

            # Correct for the rounding by adding a 0.01 to each person starting with person 1 until sum of shares equals grandtotal
            extra = 0
            correction = 0
            while round(share * count + correction, 2) != round(grandtotal,2):
                extra += 1
                correction += 0.01
            return render_template("evenly.html", count=count, extra=extra, share=share, venmo=venmo)

        else:
            # Validate inputs for tax and tip
            if not request.form["taxbydish"] or not request.form["tipbydish"]:
                return apology("Invalid Input", 400)

            # Initialize bill subtotal and shared as ints and initialize totals as a list of size count
            subtotal = 0
            totals = [0] * count
            shared = 0

            # For each dish in manual (subtracted one bc of zero indexing)
            for i in range(DISHMAX - 1):

                # If the dish input has a value...
                if request.form["dish" + str(i+1) + "value"]:

                    # Format dishvalue and dishbuyer in useful ways
                    dishvalue = float(request.form["dish"+ str(i+1) + "value"])
                    dishbuyer = request.form["dish" + str(i+1) + "buyer"]

                    # Add dishvalue to subtotal
                    subtotal += dishvalue

                    # If dishbuyer is shared, add dishvalue to shared
                    if dishbuyer == "shared":
                        shared = shared + dishvalue

                    # Else, iterate through each value in count
                    else:
                        for j in range(count):
                            # If dishbuyer's value is count, add dishvalue to appropriate index in list
                            if int(dishbuyer) == (j+1):
                                totals[j] = totals[j] + dishvalue

            # Convert html inputs to useful variables (and convert tip to a %)
            tax = float(request.form["taxbydish"])
            tip = float(int(request.form["tipbydish"])/100)

            # Find each person's share of the tax, tip and shared dishes and add to their total
            shares = [0] * count
            for i in range(count):
                totals[i] += shared / count
            temp = totals
            for i in range(count):
                shares[i] += (totals[i] * tip)
            for i in range(count):
                shares[i] += (totals[i] / subtotal) * tax
            for i in range(count):
                totals[i] += shares[i]


            # Calculate grandtotal
            grandtotal = round(tax + (tip * subtotal) + subtotal, 2)

            # Initialize extra and correctiontotal to ints 0
            extra = 0
            correctiontotal = 0

            # Round each entry in totals down so as not to display partial cents
            for i in range(count):
                totals[i] = round((floor(totals[i]*100) / 100), 2)

            # Sum all entries in totals
            for i in range(count):
                correctiontotal += round(totals[i],2)

            # Correct for rounding by adding a penny to each person (server side using extra) starting w/ person 1 until
            # correctiontotal equals grandtotal
            while round(correctiontotal, 2) != round(grandtotal, 2):
                extra += 1
                correctiontotal += 0.01
            return render_template("bydish.html", count=count, totals=totals, extra=extra, venmo=venmo)


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    # Validate username
    username = request.args.get("username")
    if not username:
        return jsonify(False)

    # Check if username is in database and validate
    rows = db.execute("SELECT * FROM users WHERE username = :username",
                      username=username)
    if rows:
        return jsonify(False)
    return jsonify(True)

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


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "POST":
        # Get user inputs and validate
        username = request.form.get("username")
        oldpassword = request.form.get("oldpassword")
        newpassword = request.form.get("newpassword")
        confirmation = request.form.get("confirmation")

        if not username or not oldpassword or not newpassword or not confirmation:
            return apology("Missing username and/or password", 400)

        if not confirmation == newpassword:
            return apology("New Password/Confimation mismatch", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], oldpassword):
            return apology("invalid username and/or password", 403)

        # Generate new hash and update database
        newhash = generate_password_hash(newpassword)
        db.execute("UPDATE users SET hash = :newhash WHERE username = :username",
                   newhash=newhash, username=username)
        return redirect("/")
    else:
        return render_template("password.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Get user inputs and validate
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        confirmation = request.form.get("confirmation")
        venmo = request.form.get("venmo")
        if not username:
            return apology("must provide username", 400)

        # Extract rows in database and validate proper inputs
        rows = db.execute("SELECT * FROM users")
        for row in rows:
            if username == row["username"]:
                return apology("invalid username", 400)
        if not password or not confirmation or request.form.get("password") != confirmation:
            return apology("invalid password/confirmation", 400)

        # Insert new user into database and alter session[]
        user_id = db.execute("INSERT INTO users ('username','hash', 'venmo') VALUES (:username, :password, :venmo)",
                             username=username, password=password, venmo=venmo)
        session['user_id'] = user_id
        return redirect('/')
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
