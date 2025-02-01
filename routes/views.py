from flask import Blueprint, redirect, render_template, url_for
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User
from flask_jwt_extended import (
    get_jwt_identity,
)

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
    with Session() as session:
        statement = select(User).where(User.username == current_username)
        user = session.execute(statement).scalar_one_or_none()
    if user.is_admin:
        return render_template("admin.html")
    return render_template("user.html")
