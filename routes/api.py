from flask import request, jsonify, Blueprint
from models import User, ClaimOrder, Item
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from database import db


api_bp = Blueprint("api", __name__)


@api_bp.route("/auth/sign-in", methods=["POST"])
def sign_in():
    data = request.json

    user = db.one_or_404(
        db.select(User).filter_by(username=data["username"]),
        description=f'User with username {data['username']} not found',
    )

    if check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token), 200

    return jsonify({"message": "Invalid credentials"}), 401


@api_bp.route("/auth/sign-up", methods=["POST"])
def sign_up():
    data = request.json

    new_user = User(
        username=data["username"],
        email=data.get("email", ""),
        name=data.get("name", ""),
        surname=data.get("surname", ""),
        password=generate_password_hash(data["password"]),
        is_admin=False,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User  created successfully"}), 201


@api_bp.route("/user", methods=["GET"])
@jwt_required()
def current_user():
    current_username = get_jwt_identity()

    user = db.one_or_404(
        db.select(User).filter_by(username=current_username),
        description=f"User with username {current_username} not found",
    )

    return jsonify(user.to_dict()), 200


# @api_bp.route("/user", methods=["PUT"])
# @jwt_required()
# def update_user():
# return UpdateUser()


@api_bp.route("/user/orders", methods=["GET"])
@jwt_required()
def get_user_orders():
    current_username = get_jwt_identity()

    current_user = db.one_or_404(
        db.select(User).filter_by(username=current_username),
        description=f"User with username {current_username} not found",
    )

    claim_orders = (
        db.session.execute(db.select(ClaimOrder).filter_by(user_id=current_user.id))
        .scalars()
        .all()
    )

    return jsonify([order.to_dict() for order in claim_orders]), 200


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


@api_bp.route("/items", methods=["GET"])
@jwt_required()
def get_items():
    current_username = get_jwt_identity()

    user = db.one_or_404(
        db.select(User).filter_by(username=current_username),
        description=f"User with username {current_username} not found",
    )

    if user.is_admin:
        items = db.session.execute(db.select(Item)).scalars().all()
        return jsonify([item.to_dict() for item in items]), 200

    if user.items is None:
        return jsonify([]), 200

    return jsonify([item.to_dict() for item in user.items]), 200


@api_bp.route("/items/<id>", methods=["GET"])
@jwt_required()
def read_inventory(id):
    current_username = get_jwt_identity()

    user = db.one_or_404(
        db.select(User).filter_by(username=current_username),
        description=f"User with username {current_username} not found",
    )

    item = db.one_or_404(
        db.select(Item).filter_by(id=id), description=f"Item with id {id} not found"
    )

    if user.is_admin or any(user.username == current_username for user in item.users):
        return jsonify(item.to_dict()), 200

    return jsonify({}), 403


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


@api_bp.route("/admin/user", methods=["GET"])
@jwt_required()
def get_all_users():
    statement = db.select(User)
    users = db.session.execute(statement).scalars().all()
    return jsonify(
        [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "surname": user.surname,
            }
            for user in users
        ]
    )
