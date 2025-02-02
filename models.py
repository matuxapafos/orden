from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import String, Boolean, Integer, DateTime, Text, ForeignKey, Column
from datetime import datetime
from database import db


association_table = db.Table(
    "user_items",
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("item_id", ForeignKey("items.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    password: Mapped[str] = mapped_column(Text(), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    items: Mapped["Item"] = relationship(
        "Item", secondary="user_items", back_populates="users"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "is_admin": self.is_admin,
            "items": self.items,
        }


class Item(db.Model):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    count: Mapped[int] = mapped_column(Integer(), nullable=False)
    price: Mapped[int] = mapped_column(Integer(), nullable=False)
    users: Mapped["User"] = relationship(
        "User", secondary="user_items", back_populates="items"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "state": self.state,
            "name": self.name,
            "count": self.count,
            "price": self.price,
            "users": self.users,
        }


class BuyOrder(db.Model):
    __tablename__ = "buy_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    count: Mapped[int] = mapped_column(Integer(), nullable=False)
    price: Mapped[int] = mapped_column(Integer(), nullable=False)
    provider_name: Mapped[str] = mapped_column(String(50), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "count": self.count,
            "price": self.price,
            "provider_name": self.provider_name,
        }


class ClaimOrder(db.Model):
    __tablename__ = "claim_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer(), ForeignKey("items.id"))
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "item_id": self.item_id,
            "user_id": self.user_id,
            "status": self.status,
            "created_at": self.created_at,
        }
