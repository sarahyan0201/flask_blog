from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from myblog.db import db
from myblog.auth.models import User
from . import auth



@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            session.permanent =True
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password")

    return render_template("login.html")

@auth.route("/logout")
def logout():
    logout_user()
    flash("帳號已成功登出Account successfully logged out.")
    return redirect(url_for("index"))
        
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("此帳號已被註冊，請使用其他名稱 This account has already been registered. Please use a different username.")
            return render_template("register.html")

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("註冊成功 Registration successful")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth.route("/admin/users")
@login_required
def manage_users():
    users = User.query.all()
    return render_template("manage_users.html", users=users)

@auth.route("/admin/users/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("使用者已成功刪除 User successfully deleted.")
    return redirect(url_for("auth.manage_users"))


