import re
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email, get_user_by_id, update_user, get_expense_stats

from routes.history import history_bp
from routes.stats import stats_bp
from routes.categories import categories_bp

app = Flask(__name__)
app.secret_key = "spendly-dev-secret"

app.register_blueprint(history_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(categories_bp)

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not name:
        return render_template("register.html", error="Full name is required.")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return render_template("register.html", error="Please enter a valid email address.")
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.")

    try:
        create_user(name, email, generate_password_hash(password))
    except sqlite3.IntegrityError:
        return render_template("register.html", error="An account with that email already exists.")

    return redirect(url_for("login", registered=1))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "GET":
        registered = request.args.get("registered")
        return render_template("login.html", registered=registered)

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    user = get_user_by_email(email)

    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.")

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("landing"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    if not session.get("user_id"):
        return redirect(url_for("landing"))
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = get_user_by_id(session["user_id"])
    stats = get_expense_stats(session["user_id"])

    if request.method == "GET":
        return render_template("profile.html", user=user, stats=stats)

    name = request.form.get("name", "").strip()
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name:
        return render_template("profile.html", user=user, stats=stats,
                               error="Name is required.")
    if new_password:
        if len(new_password) < 8:
            return render_template("profile.html", user=user, stats=stats,
                                   error="Password must be at least 8 characters.")
        if new_password != confirm_password:
            return render_template("profile.html", user=user, stats=stats,
                                   error="Passwords do not match.")

    password_hash = generate_password_hash(new_password) if new_password else None
    update_user(session["user_id"], name, password_hash)
    session["user_name"] = name

    user = get_user_by_id(session["user_id"])
    return render_template("profile.html", user=user, stats=stats,
                           success="Profile updated.")


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
