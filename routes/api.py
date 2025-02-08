from flask import request, jsonify, Blueprint
from models import User, ClaimOrder, Item, BuyOrder
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from sqlalchemy import or_, and_
from database import db


api_bp = Blueprint("api", __name__)


@api_bp.route("/auth/sign-in", methods=["POST"])
def sign_in():
    data = request.json

    user = (
        db.session.execute(db.select(User).filter_by(username=data["username"]))
        .scalars()
        .one_or_none()
    )

    if user is None:
        return jsonify(
            {"message": f"User with username {data['username']} not found"}
        ), 404

    if check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user.username)
        return jsonify({"message": "Success", "access_token": access_token}), 200

    return jsonify({"message": "Invalid credentials"}), 401


@api_bp.route("/auth/sign-up", methods=["POST"])
def sign_up():
    data = request.json

    if "username" not in data or "password" not in data:
        return jsonify({"message": "Username and password are required"}), 400

    existing_username = (
        db.session.execute(db.select(User).where(User.username == data["username"]))
        .scalars()
        .one_or_none()
    )

    if existing_username:
        return jsonify(
            {"message": f"User with username {data['username']} already exists"}
        ), 409

    existing_email = (
        db.session.execute(db.select(User).where(User.email == data["email"]))
        .scalars()
        .one_or_none()
    )

    if existing_email:
        return jsonify(
            {"message": f"User with email {data['email']} already exists"}
        ), 409

    new_user = User(
        username=data["username"],
        email=data.get("email", ""),
        name=data.get("name", ""),
        surname=data.get("surname", ""),
        password=generate_password_hash(data["password"]),
        is_admin=data.get("is_admin", False),  
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(
        {"message": "User  created successfully", "user": new_user.to_dict()}
    ), 201


@api_bp.route("/user", methods=["GET"])
@jwt_required()
def current_user():
    current_username = get_jwt_identity()

    user = (
        db.session.execute(db.select(User).filter_by(username=current_username))
        .scalars()
        .one_or_none()
    )

    if user is None:
        return jsonify(
            {"message": f"User with username {current_username} not found"}
        ), 404

    return jsonify({"message": "Success", "user": user.to_dict()}), 200


@api_bp.route("/user", methods=["PUT"])
@jwt_required()
def update_user():
    current_username = get_jwt_identity()
    data = request.json

    user = (
        db.session.execute(db.select(User).filter_by(username=current_username))
        .scalars()
        .one_or_none()
    )

    if user is None:
        return jsonify({"message": f"User  with username {current_username} not found"}), 404

    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "name" in data:
        user.name = data["name"]
    if "surname" in data:
        user.surname = data["surname"]
    if "password" in data:
        user.password = generate_password_hash(data["password"])

    db.session.commit()

    return jsonify({"message": "User  updated successfully", "user": user.to_dict()}), 200


@api_bp.route("/user/orders", methods=["GET"])
@jwt_required()
def get_user_orders():
    current_username = get_jwt_identity()

    user = (
        db.session.execute(db.select(User).filter_by(username=current_username))
        .scalars()
        .one_or_none()
    )

    if user is None:
        return jsonify(
            {"message": f"User with username {current_username} not found"}
        ), 404

    claim_orders = (
        db.session.execute(db.select(ClaimOrder).filter_by(user_id=user.id))
        .scalars()
        .all()
    )

    return jsonify(
        {"message": "Success", "orders": [order.to_dict() for order in claim_orders]}
    ), 200


# @api_bp.route("/user/requests", methods=["POST"])
# @jwt_required()
# def create_user_request():
#     current_username = get_jwt_identity()
#     data = request.json

#     user = (
#         db.session.execute(db.select(User).filter_by(username=current_username))
#         .scalars()
#         .one_or_none()
#     )

#     if user is None:
#         return jsonify({"message": f"User  with username {current_username} not found"}), 404

#     new_request = (
#         user_id=user.id,
#         description=data["description"],
#         status="Pending"  
#     )

#     db.session.add(new_request)
#     db.session.commit()

#     return jsonify({"message": "Request created successfully", "request": new_request.to_dict()}), 201


# @api_bp.route("/user/requests/repair", methods=["POST"])
# @jwt_required()
# def create_repair_request():
#     current_username = get_jwt_identity()
#     data = request.json

#     user = (
#         db.session.execute(db.select(User).filter_by(username=current_username))
#         .scalars()
#         .one_or_none()
#     )

#     if user is None:
#         return jsonify({"message": f"User  with username {current_username} not found"}), 404

#     new_repair_request = RepairOrder(
#         user_id=user.id,
#         item_id=data["item_id"],
#         description=data["description"],
#         status="Pending"  # Default status
#     )

#     db.session.add(new_repair_request)
#     db.session.commit()

#     return jsonify({"message": "Repair request created successfully", "request": new_repair_request.to_dict()}), 201


# @api_bp.route("/user/requests/repair/<id>", methods=["GET"])
# @jwt_required()
# def get_repair_request(id):
#     current_username = get_jwt_identity()

#     user = (
#         db.session.execute(db.select(User).filter_by(username=current_username))
#         .scalars()
#         .one_or_none()
#     )

#     if user is None:
#         return jsonify({"message": f"User  with username {current_username} not found"}), 404

#     repair_request = (
#         db.session.execute(db.select(RepairOrder).filter_by(id=id, user_id=user.id))
#         .scalars()
#         .one_or_none()
#     )

#     if repair_request is None:
#         return jsonify({"message": f"Repair request with id {id} not found"}), 404

#     return jsonify({"message": "Success", "request": repair_request.to_dict()}), 200


@api_bp.route("/items", methods=["GET"])
@jwt_required()
def get_items():
    current_username = get_jwt_identity()

    user = (
        db.session.execute(db.select(User).filter_by(username=current_username))
        .scalars()
        .one_or_none()
    )

    if user is None:
        return jsonify(
            {"message": f"User with username {current_username} not found"}
        ), 404

    if user.is_admin:
        items = db.session.execute(db.select(Item)).scalars().all()
        return jsonify(
            {"message": "Success", "items": [item.to_dict() for item in items]}
        ), 200

    if user.items is None:
        return jsonify({"message": "Success", "items": []}), 200

    return jsonify(
        {"message": "Success", "items": [item.to_dict() for item in user.items]}
    ), 200


@api_bp.route("/items/<id>", methods=["GET"])
@jwt_required()
def read_inventory(id):
    current_username = get_jwt_identity()

    user = (
        db.session.execute(db.select(User).filter_by(username=current_username))
        .scalars()
        .one_or_none()
    )

    if user is None:
        return jsonify(
            {"message": f"User with username {current_username} not found"}
        ), 404

    item = db.select(Item).filter_by(id=id).scalars().one_or_none()

    if item is None:
        return jsonify({"message": f"Item with id {id} not found"}), 404

    if user.is_admin or any(user.username == current_username for user in item.users):
        return jsonify({"message": "Success", "item": item.to_dict()}), 200

    return jsonify({"message": "Forbidden", "item": None}), 403


@api_bp.route("/admin/items", methods=["POST"])
@jwt_required()
def create_item():
    current_username = get_jwt_identity()
    data = request.json

    user = (
        db.session.execute(db.select(User).filter_by(username=current_username))
        .scalars()
        .one_or_none()
    )

    if user is None or not user.is_admin:
        return jsonify({"message": "Forbidden"}), 403

    new_item = Item(
        state=data["state"],
        name=data["name"],
        count=data["count"],
        price=data["price"]
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "Item created successfully", "item": new_item.to_dict()}), 201


@api_bp.route("/admin/items/<int:id>", methods=["PUT"])
@jwt_required()
def update_item(id):
    current_username = get_jwt_identity()
    data = request.json

    user = (
        db.session.execute(db.select(User).filter_by(username=current_username))
        .scalars()
        .one_or_none()
    )

    if user is None or not user.is_admin:
        return jsonify({"message": "Forbidden"}), 403

    item = (
        db.session.execute(db.select(Item).filter_by(id=id))
        .scalars()
        .one_or_none()
    )

    if item is None:
        return jsonify({"message": f"Item with id {id} not found"}), 404

    if "name" in data:
        item.name = data["name"]
    if "state" in data:
        item.state = data["state"]
    if "count" in data:
        item.count = data["count"]
    if "price" in data:
        item.price = data["price"]

    db.session.commit()

    return jsonify({"message": "Item updated successfully", "item": item.to_dict()}), 200


@api_bp.route("/admin/inventory/<id>", methods=["DELETE"])
@jwt_required()
def delete_inventory(id):
    current_username = get_jwt_identity()
    user = (
        db.session.execute(db.select(User).filter_by(username=current_username))
        .scalars()
        .one_or_none()
    )

    if user is None or not user.is_admin:
        return jsonify({"message": "Forbidden"}), 403

    item = (
        db.session.execute(db.select(Item).filter_by(id=id))
        .scalars()
        .one_or_none()
    )

    if item is None:
        return jsonify({"message": f"Item with id {id} not found"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Inventory item deleted successfully"}), 200


@api_bp.route("/admin/purchase", methods=["GET"])
@jwt_required()
def get_purchase_list():
    current_username = get_jwt_identity()
    user = (
        db.session.execute(db.select(User).filter_by(username=current_username))
        .scalars()
        .one_or_none()
    )

    if user is None or not user.is_admin:
        return jsonify({"message": "Forbidden"}), 403

    purchases = db.session.execute(db.select(BuyOrder)).scalars().all()
    return jsonify({"message": "Success", "purchases": [purchase.to_dict() for purchase in purchases]}), 200


@api_bp.route("/admin/purchase", methods=["POST"])
@jwt_required()
def create_purchase():
    current_username = get_jwt_identity()
    data = request.json
    user = (
        db.session.execute(db.select(User).filter_by(username=current_username))
        .scalars()
        .one_or_none()
    )

    if user is None or not user.is_admin:
        return jsonify({"message": "Forbidden"}), 403

    new_purchase = BuyOrder(
        name=data["name"],
        count=data["count"],
        price=data["price"],
        provider_name=data["provider_name"]
    )

    db.session.add(new_purchase)
    db.session.commit()

    return jsonify({"message": "Purchase created successfully", "purchase": new_purchase.to_dict()}), 201


@api_bp.route("/admin/purchase/<int:id>", methods=["GET"])
@jwt_required()
def get_purchase(id):
    current_username = get_jwt_identity()
    user = (
        db.session.execute(db.select(User).filter_by(username=current_username))
        .scalars()
        .one_or_none()
    )

    if user is None or not user.is_admin:
        return jsonify({"message": "Forbidden"}), 403

    purchase = db.session.execute(db.select(BuyOrder).filter_by(id=id)).scalars().one_or_none()
    if purchase is None:
        return jsonify({"message": f"Purchase with id {id} not found"}), 404

    return jsonify({"message": "Success", "purchase": purchase.to_dict()}), 200


@api_bp.route("/admin/requests", methods=["GET"])
@jwt_required()
def get_all_user_requests():
    current_username = get_jwt_identity()
    user = (
        db.session.execute(db.select(User).filter_by(username=current_username))
        .scalars()
        .one_or_none()
    )

    if user is None or not user.is_admin:
        return jsonify({"message": "Forbidden"}), 403

    requests = db.session.execute(db.select(ClaimOrder)).scalars().all()
    return jsonify({"message": "Success", "requests": [request.to_dict() for request in requests]}), 200


@api_bp.route("/admin/requests/<int:id>", methods=["PUT"])
@jwt_required()
def update_user_request(id):
    current_username = get_jwt_identity()
    data = request.json
    user = (
        db.session.execute(db.select(User).filter_by(username=current_username))
        .scalars()
        .one_or_none()
    )

    if user is None or not user.is_admin:
        return jsonify({"message": "Forbidden"}), 403

    request_to_update = db.session.execute(db.select(ClaimOrder).filter_by(id=id)).scalars().one_or_none()
    if request_to_update is None:
        return jsonify({"message": f"Request with id {id} not found"}), 404

    if "item_id" in data:
        request_to_update.name = data["item_id"]
    if "user_id" in data:
        request_to_update.state = data["user_id"]
    if "status" in data:
        request_to_update.count = data["status"]
    if "created_at" in data:
        request_to_update.price = data["created_at"]

    db.session.commit()

    return jsonify({"message": "Request updated successfully", "request": request_to_update.to_dict()}), 200


# @api_bp.route("/admin/requests/repair", methods=["GET"])
# @jwt_required()
# def get_all_repair_requests():
#     current_username = get_jwt_identity()
#     user = (
#         db.session.execute(db.select(User).filter_by(username=current_username))
#         .scalars()
#         .one_or_none()
#     )

#     if user is None or not user.is_admin:
#         return jsonify({"message": "Forbidden"}), 403

#     repair_requests = db.session.execute(db.select(RepairOrder)).scalars().all()
#     return jsonify({"message": "Success", "repair_requests": [request.to_dict() for request in repair_requests]}), 200


@api_bp.route("/admin/assign", methods=["PUT"])
@jwt_required()
def assign_user():
    current_username = get_jwt_identity()
    data = request.json
    user = (
        db.session.execute(db.select(User).filter_by(username=current_username))
        .scalars()
        .one_or_none()
    )

    if user is None or not user.is_admin:
        return jsonify({"message": "Forbidden"}), 403

    user_to_assign = db.session.execute(db.select(User).filter_by(id=data["user_id"])).scalars().one_or_none()
    if user_to_assign is None:
        return jsonify({"message": f"User  with id {data['user_id']} not found"}), 404

    user_to_assign.is_admin = data.get


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
