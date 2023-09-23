from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from flask_session import Session


from helpers import login_required, apology, get_morrisons_items, get_waitrose_items

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        ### Morrisons and Waitrose shared key words
        key = request.form.get("item")
        session["key"] = key

        morrisons_items = get_morrisons_items(key)
        waitrose_items = get_waitrose_items(key)

        return render_template(
            "search.html",
            morrisons_items=morrisons_items,
            waitrose_items=waitrose_items,
        )
    else:
        return render_template("search.html")


@app.route("/searched")
@login_required
def searched():
    user_id = session["user_id"]

    # Getting temp item list again
    key = session["key"]
    morrisons_items = get_morrisons_items(key)
    waitrose_items = get_waitrose_items(key)

    # Adding items to the morrisons cart's database
    item_name_mor = request.args.get("item_name_mor")
    item_prc_mor = request.args.get("item_prc_mor")
    item_qty_mor = request.args.get("item_qty_mor")
    item_img_url_mor = request.args.get("item_img_url_mor")
    success_mor = ""
    try:
        if item_qty_mor:
            if item_prc_mor == "Out of stock":
                return apology("out of stock items cannot be added to the cart", 403)
            elif int(item_qty_mor) > 0:
                db.execute(
                    "INSERT INTO morrisons_cart (user_id,item_name_mor,item_prc_mor,item_qty_mor,item_img_url_mor) VALUES(?,?,?,?,?)",
                    user_id,
                    item_name_mor,
                    item_prc_mor,
                    item_qty_mor,
                    item_img_url_mor,
                )
                success_mor += f"{item_qty_mor} x {item_name_mor} succesfully added your morrisons cart!"
            else:
                return apology("invalid quantity", 403)
    except ValueError:
        return apology("invalid quantity", 403)

    # Adding items to the waitrose cart's database
    item_name_wait = request.args.get("item_name_wait")
    item_prc_wait = request.args.get("item_prc_wait")
    item_qty_wait = request.args.get("item_qty_wait")
    item_img_url_wait = request.args.get("item_img_url_wait")
    success_wait = ""
    try:
        if item_qty_wait:
            if int(item_qty_wait) > 0:
                db.execute(
                    "INSERT INTO waitrose_cart (user_id,item_name_wait,item_prc_wait,item_qty_wait,item_img_url_wait) VALUES(?,?,?,?,?)",
                    user_id,
                    item_name_wait,
                    item_prc_wait,
                    item_qty_wait,
                    item_img_url_wait,
                )
                success_wait += f"{item_qty_wait} x {item_name_wait} succesfully added your waitrose cart."
            else:
                return apology("invalid quantity", 403)
    except ValueError:
        return apology("invalid quantity", 403)

    return render_template(
        "search.html",
        morrisons_items=morrisons_items,
        waitrose_items=waitrose_items,
        success_wait=success_wait,
        success_mor=success_mor,
    )


@app.route("/carts", methods=["POST", "GET"])
@login_required
def carts():
    user_id = session["user_id"]
    if request.method == "POST":
        # Morrisons item removal
        if request.form.get("item_name_mor"):
            removing_qty_mor = request.form.get("removing_qty_mor")
            current_item_qty = db.execute(
                "SELECT SUM(item_qty_mor) FROM morrisons_cart WHERE user_id=? AND item_name_mor=?",
                user_id,
                request.form.get("item_name_mor"),
            )[0]["SUM(item_qty_mor)"]
            try:
                if (
                    current_item_qty < int(removing_qty_mor)
                    or int(removing_qty_mor) < 1
                ):
                    return apology("invalid quantity", 403)
                else:
                    item_name_mor = request.form.get("item_name_mor")
                    item_img_url_mor = request.form.get("item_img_url_mor")
                    item_prc_mor = request.form.get("item_prc_mor")
                    neg_qty_mor = int(removing_qty_mor) * (-1)
                    db.execute(
                        "INSERT INTO morrisons_cart (user_id,item_name_mor,item_qty_mor,item_img_url_mor,item_prc_mor) VALUES(?,?,?,?,?)",
                        user_id,
                        item_name_mor,
                        neg_qty_mor,
                        item_img_url_mor,
                        item_prc_mor,
                    )

            except ValueError:
                return apology("invalid quantity", 403)

        # Waitrose item removal
        if request.form.get("item_name_wait"):
            removing_qty_wait = request.form.get("removing_qty_wait")
            current_item_qty = db.execute(
                "SELECT SUM(item_qty_wait) FROM waitrose_cart WHERE user_id=? AND item_name_wait=?",
                user_id,
                request.form.get("item_name_wait"),
            )[0]["SUM(item_qty_wait)"]
            try:
                if (
                    current_item_qty < int(removing_qty_wait)
                    or int(removing_qty_wait) < 1
                ):
                    return apology("invalid quantity", 403)
                else:
                    item_name_wait = request.form.get("item_name_wait")
                    item_img_url_wait = request.form.get("item_img_url_wait")
                    item_prc_wait = request.form.get("item_img_url_wait")
                    neg_qty_wait = int(removing_qty_wait) * (-1)
                    db.execute(
                        "INSERT INTO waitrose_cart (user_id,item_name_wait,item_qty_wait,item_img_url_wait,item_prc_wait) VALUES(?,?,?,?,?)",
                        user_id,
                        item_name_wait,
                        neg_qty_wait,
                        item_img_url_wait,
                        item_prc_wait,
                    )
            except ValueError:
                return apology("invalid quantity", 403)
        return redirect("/carts")

    else:
        morrisons_cart_items = db.execute(
            "SELECT item_name_mor, item_prc_mor, item_img_url_mor, SUM(item_qty_mor) AS item_total_qty_mor FROM morrisons_cart WHERE user_id=? GROUP BY item_name_mor",
            user_id,
        )

        waitrose_cart_items = db.execute(
            "SELECT item_name_wait, item_prc_wait, item_img_url_wait, SUM(item_qty_wait) AS item_total_qty_wait FROM waitrose_cart WHERE user_id=? GROUP BY item_name_wait",
            user_id,
        )

        total_mor = 0
        for row in morrisons_cart_items:
            raw_prc_mor = row["item_prc_mor"]
            if "p" in raw_prc_mor:
                float_prc_mor = float(raw_prc_mor.replace("p", "")) * 0.01
            if "£" in raw_prc_mor:
                float_prc_mor = float(raw_prc_mor.replace("£", ""))
            int_qty_mor = int(row["item_total_qty_mor"])
            full_prc_mor = float_prc_mor * int_qty_mor
            total_mor += full_prc_mor
        total_mor = round(total_mor, 2)

        total_wait = 0
        for row in waitrose_cart_items:
            raw_prc_wait = row["item_prc_wait"]
            if "p" in raw_prc_wait:
                float_prc_wait = float(raw_prc_wait.replace("p", "")) * 0.01
            if "£" in raw_prc_wait:
                float_prc_wait = float(raw_prc_wait.replace("£", ""))
            int_qty_wait = int(row["item_total_qty_wait"])
            full_prc_wait = float_prc_wait * int_qty_wait
            total_wait += full_prc_wait
        total_wait = round(total_wait, 2)

        return render_template(
            "carts.html",
            morrisons_cart_items=morrisons_cart_items,
            waitrose_cart_items=waitrose_cart_items,
            total_mor=total_mor,
            total_wait=total_wait,
        )


@app.route("/removed", methods=["POST"])
@login_required
def removed():
    # Emptying carts and database
    user_id = session["user_id"]
    if request.form.get("remover") == "1":
        db.execute("DELETE FROM morrisons_cart WHERE user_id=?", user_id)
    elif request.form.get("remover") == "2":
        db.execute("DELETE FROM waitrose_cart WHERE user_id=?", user_id)
    else:
        return apology("unexpected event", 403)
    return redirect("/carts")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE user_name = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return apology("please provide a user name!")
        elif not password:
            return apology("please provide a password!")
        elif confirmation != password:
            return apology("passwords do not match!")
        else:
            ### database check
            rows = db.execute("SELECT * FROM users")
            for row in rows:
                if username == row["user_name"]:
                    return apology(
                        "Sorry, this username is already taken. Please choose a different username."
                    )
            db.execute(
                "INSERT INTO users (user_name,hash) VALUES(?,?)",
                username,
                generate_password_hash(password),
            )
            return redirect("/")
    else:
        return render_template("/register.html")
