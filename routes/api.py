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
    user = db.one_or_404(db.select(User).filter_by(username=data["username"]))
    print(type(user))
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
    try:
        db.session.add(new_user)
    except:
        db.session.rollback()
        raise
    else:
        db.session.commit()
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


@api_bp.route("/user/orders", methods=["GET"])
@jwt_required()
def get_user_requests():
    current_username = get_jwt_identity()

    current_user = db.session.execute(
        db.select(User).where(User.username == current_username)
    ).scalar_one_or_none()
    if current_user is None:
        return jsonify({"error": "No user with such username"}), 404
    statement = db.select(ClaimOrder).where(ClaimOrder.user_id == current_user.id)
    claim_orders = db.session.execute(statement).scalars().all()

    return jsonify(
        [
            {
                "id": order.id,
                "item_id": order.item_id,
                "user_id": order.user_id,
                "status": order.status,
                "created_at": order.created_at,
            }
            for order in claim_orders
        ]
    )


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
def get_inventories():
    statement = db.select(Item)
    items = db.session.execute(statement).scalars().all()
    return jsonify(
        [
            {
                "id": item.id,
                "state": item.state,
                "name": item.name,
                "count": item.count,
                "price": item.count,
            }
            for item in items
        ]
    )


@api_bp.route("/items/<id>", methods=["GET"])
def read_inventory(id):
    statement = db.select(Item).where(Item.id == id)
    item = db.session.execute(statement).scalar_one_or_none()
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(
        {
            "id": item.id,
            "state": item.state,
            "name": item.name,
            "count": item.count,
            "price": item.count,
        }
    )


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
