from sqlalchemy import String, Integer
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash
from flask_admin.contrib.sqla import ModelView
from app import loginManager
from flask_login import UserMixin
from typing import Optional
from app import db

@loginManager.user_loader
def load_user(userId):
    return db.session.get(User, int(userId))

# ---------------- Database Models ----------------
#Everything is non-nullable by default

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(150))
    created_at: Mapped[datetime] = mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(str(self.password_hash), password)
    
    def __repr__(self) -> str:
        return str(self.full_name)

class Product(db.Model):
    __tablename__ = "prodcut"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(75))
    identifier: Mapped[str] = mapped_column(String(50))
    brand: Mapped[str] = mapped_column(String(50))
    stock_count: Mapped[int] = mapped_column(Integer, default=0)
    # created_by: Mapped[Optional[User]] = relationship(back_populates="product")
    # created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

class Role(db.Model):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)

class UserView(ModelView):
    #modals instead of redirecting to new page to edit information
    create_modal = True
    edit_modal = True
    column_editable_list = ['full_name', 'email']
    column_exclude_list = ['password_hash']
    column_searchable_list = ['full_name', 'email']