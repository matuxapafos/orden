from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column
from datetime import datetime


class Base(DeclarativeBase):
    pass


association_table = Table(
    "user_items",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("item_id", ForeignKey("items.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    items: Mapped["Item"] = relationship("Item", secondary="user_items")


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    count: Mapped[int] = mapped_column(Integer(), nullable=False)
    price: Mapped[int] = mapped_column(Integer(), nullable=False)
    users: Mapped["User"] = relationship("User", secondary="user_items")


class BuyOrder(Base):
    __tablename__ = "buy_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    count: Mapped[int] = mapped_column(Integer(), nullable=False)
    price: Mapped[int] = mapped_column(Integer(), nullable=False)
    provider_name: Mapped[str] = mapped_column(String(50), nullable=True)


class ClaimOrder(Base):
    __tablename__ = "claim_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer(), ForeignKey("items.id"))
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
