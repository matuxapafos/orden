from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Boolean
from sqlalchemy import ForeignKey
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    surname: Mapped[str] = mapped_column(String(30), nullable=True)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean(), nullable=False)


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    repair_order_id: Mapped[int] = mapped_column(nullable=False)


class Buy_order(Base):
    __tablename__ = "Buy_order"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    count: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    provider_name: Mapped[str] = mapped_column(String(30), nullable=True)


class repair_order(Base):
    __tablename__ = "repair_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)


class Claim_order(Base):
    __tablename__ = "Claim_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    count: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)


class report(Base):
    __tablename__ = "reports"
    id: Mapped[int] = mapped_column(primary_key=True)
    devoted_by: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    date: Mapped[datetime] = mapped_column(nullable=False)
    contact: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
