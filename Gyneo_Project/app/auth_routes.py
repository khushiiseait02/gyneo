# app/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import DuplicateKeyError
import traceback

def create_auth_blueprint(mongo):
    auth_bp = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

    @auth_bp.route("/register", methods=["GET", "POST"])
    def register():
        if not mongo or getattr(mongo, "db", None) is None:
            flash("❌ Database not available. Contact admin.", "danger")
            return render_template("register.html")

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            role = request.form.get("role", "patient")

            if not username or not password:
                flash("⚠ Provide a username and password.", "danger")
                return redirect(url_for("auth.register"))

            try:
                if mongo.db.users.find_one({"username": username}):
                    flash("⚠ Username already exists!", "danger")
                    return redirect(url_for("auth.register"))

                hashed_pw = generate_password_hash(password)
                mongo.db.users.insert_one({
                    "username": username,
                    "password": hashed_pw,
                    "role": role
                })
            except DuplicateKeyError:
                flash("⚠ Username already exists!", "danger")
                return redirect(url_for("auth.register"))
            except Exception:
                traceback.print_exc()
                flash("❌ Registration failed due to a server error.", "danger")
                return redirect(url_for("auth.register"))

            flash("✅ Registration successful! Please login.", "success")
            return redirect(url_for("auth.login"))

        return render_template("register.html")

    @auth_bp.route("/login", methods=["GET", "POST"])
    def login():
        if not mongo or getattr(mongo, "db", None) is None:
            flash("❌ Database not available. Contact admin.", "danger")
            return render_template("login.html")

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            if not username or not password:
                flash("❌ Enter username and password.", "danger")
                return render_template("login.html")

            try:
                user = mongo.db.users.find_one({"username": username})
            except Exception:
                traceback.print_exc()
                flash("❌ Login failed due to server error.", "danger")
                return render_template("login.html")

            if user and check_password_hash(user.get("password", ""), password):
                session["username"] = username
                session["role"] = user.get("role", "patient")
                flash("✅ Logged in successfully!", "success")
                return redirect(url_for("routes.dashboard"))
            else:
                flash("❌ Invalid username or password", "danger")

        return render_template("login.html")

    @auth_bp.route("/logout")
    def logout():
        session.clear()
        flash("✅ You have been logged out.", "info")
        return redirect(url_for("auth.login"))

    return auth_bp
