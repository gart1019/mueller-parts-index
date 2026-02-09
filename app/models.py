from sqlalchemy import String
from datetime import datetime, UTC
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash
from app import loginManager
from flask_login import UserMixin
from typing import Optional
from app import db

@loginManager.user_loader
def load_user(userId):
    return db.session.get(User, int(userId))

# ---------------- Database Models ----------------
#Everything is non-nullable by default


class Role(db.Model):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(50))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(str(self.password_hash), password)
    
    def __repr__(self) -> str:
        return str(self.email)

class Product(db.Model):
    __tablename__ = "prodcut"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    desc: Mapped[str] = mapped_column(String(300))
    # created_by: Mapped[Optional[User]] = relationship(back_populates="product")
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))