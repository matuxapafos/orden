from flask import request, jsonify, Blueprint
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
)


api_bp = Blueprint("api", __name__)


@api_bp.route("/auth/sign-in", methods=["POST"])
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


@api_bp.route("/auth/sign-up", methods=["POST"])
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


@api_bp.route("/user", methods=["GET"])
@jwt_required()
def current_user():
    current_username = get_jwt_identity()
    return jsonify({"username": current_username}), 200


# @api_bp.route("/user", methods=["PUT"])
# @jwt_required()
# def update_user():
# return UpdateUser()


# @api_bp.route("/user/requests", methods=["GET"])
# @jwt_required()
# def get_user_requests():
# return GetUserRequests()


# @api_bp.route("/user/requests", methods=["POST"])
# @jwt_required()
# def create_user_request():
# return CreateUserRequest()


# @api_bp.route("/user/requests/repair", methods=["POST"])
# @jwt_required()
# def create_repair_request():
# return CreateRepairRequest()


# @api_bp.route("/user/requests/repair/<id>", methods=["GET"])
# @jwt_required()
# def get_repair_request(id):
# return GetRepairRequest(id)


# @api_bp.route("/inventory", methods=["GET"])
# def get_inventories():
# return GetInventories()


# @api_bp.route("/inventory/<id>", methods=["GET"])
# def read_inventory(id):
# return ReadInventory(id)


# @api_bp.route("/admin/inventory", methods=["POST"])
# @jwt_required()
# def create_inventory():
# return CreateInventory()


# @api_bp.route("/admin/inventory/<id>", methods=["PUT"])
# @jwt_required()
# def update_inventory(id):
# return UpdateInventory(id)


# @api_bp.route("/admin/inventory/<id>", methods=["DELETE"])
# @jwt_required()
# def delete_inventory(id):
# return DeleteInventory(id)


# @api_bp.route("/admin/purchase", methods=["GET"])
# @jwt_required()
# def get_purchase_list():
# return GetPurchaseList()


# @api_bp.route("/admin/purchase", methods=["POST"])
# @jwt_required()
# def create_purchase():
# return CreatePurchase()


# @api_bp.route("/admin/purchase/<id>", methods=["GET"])
# @jwt_required()
# def get_purchase(id):
# return GetPurchase(id)


# @api_bp.route("/admin/requests", methods=["GET"])
# @jwt_required()
# def get_all_user_requests():
# return GetAllUserRequests()


# @api_bp.route("/admin/requests/<id>", methods=["PUT"])
# @jwt_required()
# def update_user_request(id):
# return UpdateUserRequest(id)


# @api_bp.route("/admin/requests/repair", methods=["GET"])
# @jwt_required()
# def get_all_repair_requests():
# return GetAllRepairRequests()


# @api_bp.route("/admin/assign", methods=["PUT"])
# @jwt_required()
# def assign_user():
# return AssignUser()


# @api_bp.route("/admin/user", methods=["GET"])
# @jwt_required()
# def get_all_users():
# return GetAllUsers()
