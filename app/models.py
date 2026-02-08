from sqlalchemy import select
from sqlalchemy import String
from datetime import datetime, UTC
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column(String(50))

class Product(Base):
    __tablename__ = "prodcut"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    desc: Mapped[str]
    created_by: Mapped[Optional[User]] = relationship(back_populates="user")
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))