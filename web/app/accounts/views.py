from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user

from app import db
from forms import RegisterForm, LoginForm
from models import User

accounts_bp = Blueprint("accounts", __name__)


@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("core.home"))

    form = RegisterForm(request.form)

    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Successfully registered!", "success")

        return redirect(url_for("core.home"))

    return render_template("register.html", form=form)

@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("core.home"))
    
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Successfully logged in!", "success")
            return redirect(url_for("core.home"))
        else:
            flash("Invalid credentials.", "danger")
        
    return render_template("login.html", form=form)


@accounts_bp.route("/logout")
def logout():
    logout_user()
    flash("Successfully logged out.", "success")
    return redirect(url_for("index"))