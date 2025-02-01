from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, select
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from models import Base, User, Item, BuyOrder, ClaimOrder
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
import os
from dotenv import load_dotenv


load_dotenv()


DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
jwt = JWTManager(app)


engine = create_engine(DB_CONNECTION_STRING, echo=True)
Session = sessionmaker(engine)


@app.route("/auth/sign-in", methods=["POST"])
def sign_in():
    data = request.json
    with Session() as session:
        statement = select(User).where(User.username == data["username"])
        user = session.execute(statement).scalar_one_or_none()
    if user is None:
        return jsonify({"message": "User does not exists"}), 401
    if check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/auth/sign-up", methods=["POST"])
def sign_up():
    data = request.json
    new_user = User(
        username=data["username"],
        email="",
        name="",
        surname="",
        password=generate_password_hash(data["password"]),
        is_admin=False,
    )
    with Session() as session:
        try:
            session.add(new_user)
        except:
            session.rollback()
            raise
        else:
            session.commit()
    return jsonify({"message": "User  created successfully"}), 201


@app.route("/user", methods=["GET"])
@jwt_required()
def current_user():
    current_username = get_jwt_identity()
    return jsonify({"username": current_username}), 200


# @app.route("/user", methods=["PUT"])
# @jwt_required()
# def update_user():
# return UpdateUser()


# @app.route("/user/requests", methods=["GET"])
# @jwt_required()
# def get_user_requests():
# return GetUserRequests()


# @app.route("/user/requests", methods=["POST"])
# @jwt_required()
# def create_user_request():
# return CreateUserRequest()


# @app.route("/user/requests/repair", methods=["POST"])
# @jwt_required()
# def create_repair_request():
# return CreateRepairRequest()


# @app.route("/user/requests/repair/<id>", methods=["GET"])
# @jwt_required()
# def get_repair_request(id):
# return GetRepairRequest(id)


# @app.route("/inventory", methods=["GET"])
# def get_inventories():
# return GetInventories()


# @app.route("/inventory/<id>", methods=["GET"])
# def read_inventory(id):
# return ReadInventory(id)


# @app.route("/admin/inventory", methods=["POST"])
# @jwt_required()
# def create_inventory():
# return CreateInventory()


# @app.route("/admin/inventory/<id>", methods=["PUT"])
# @jwt_required()
# def update_inventory(id):
# return UpdateInventory(id)


# @app.route("/admin/inventory/<id>", methods=["DELETE"])
# @jwt_required()
# def delete_inventory(id):
# return DeleteInventory(id)


# @app.route("/admin/purchase", methods=["GET"])
# @jwt_required()
# def get_purchase_list():
# return GetPurchaseList()


# @app.route("/admin/purchase", methods=["POST"])
# @jwt_required()
# def create_purchase():
# return CreatePurchase()


# @app.route("/admin/purchase/<id>", methods=["GET"])
# @jwt_required()
# def get_purchase(id):
# return GetPurchase(id)


# @app.route("/admin/requests", methods=["GET"])
# @jwt_required()
# def get_all_user_requests():
# return GetAllUserRequests()


# @app.route("/admin/requests/<id>", methods=["PUT"])
# @jwt_required()
# def update_user_request(id):
# return UpdateUserRequest(id)


# @app.route("/admin/requests/repair", methods=["GET"])
# @jwt_required()
# def get_all_repair_requests():
# return GetAllRepairRequests()


# @app.route("/admin/assign", methods=["PUT"])
# @jwt_required()
# def assign_user():
# return AssignUser()


# @app.route("/admin/user", methods=["GET"])
# @jwt_required()
# def get_all_users():
# return GetAllUsers()


def create_db_and_tables() -> None:
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
    app.run(host="0.0.0.0", port=5000)
