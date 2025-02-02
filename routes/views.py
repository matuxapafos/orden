from flask import Blueprint, redirect, render_template, url_for
from models import User
from flask_jwt_extended import (
    get_jwt_identity,
)
from database import db

views_bp = Blueprint("views", __name__)


@views_bp.route("/")
def index():
    return redirect(url_for("views.login"))


@views_bp.route("/login")
def login():
    return render_template("index.html")


@views_bp.route("/register")
def register():
    return render_template("index.html")


@views_bp.route("/dashboard")
def dashboard():
    current_username = get_jwt_identity()
    statement = db.select(User).where(User.username == current_username)
    user = db.session.execute(statement).scalar_one_or_none()
    if user.is_admin:
        return render_template("admin.html")
    return render_template("user.html")
