from flask import redirect
from sqlalchemy import String, Integer, ForeignKey, Boolean, UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash
from flask_admin.contrib.sqla import ModelView
from app import loginManager
from flask_login import UserMixin, current_user
from typing import Any, Optional
from app import db

@loginManager.user_loader
def load_user(userId):
    return db.session.get(User, int(userId))

# ---------------- Database Models ----------------
#Everything is non-nullable by default

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    verification_id: Mapped[UUID] = mapped_column(UUID(), unique=True, nullable=True) #UUID of email link
    full_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(unique=True)
    account_active: Mapped[Boolean] = mapped_column(Boolean(), default=False)
    email_verified: Mapped[Boolean] = mapped_column(Boolean(), default=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(150))
    created_at: Mapped[datetime] = mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(str(self.password_hash), password)
    
    def __init__(self, n, e) -> None:
        self.full_name = n
        self.email = e
        
    
    def __repr__(self) -> str:
        return str(self.full_name)

class Product(db.Model):
    __tablename__ = "prodcut"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(75))
    identifier: Mapped[str] = mapped_column(String(50))
    brand_id: Mapped[Optional[int]] = mapped_column(ForeignKey("brand.id"), nullable=True)
    brand: Mapped[Optional["Brand"]] = relationship()
    stock_count: Mapped[int] = mapped_column(Integer, default=0)
    machine_id: Mapped[Optional[int]] = mapped_column(ForeignKey("machine.id"), nullable=True)
    machine: Mapped[Optional["Machine"]] = relationship()
    created_by_id: Mapped[int] = mapped_column(ForeignKey("user.id"), default=lambda: current_user.id)
    created_by: Mapped["User"] = relationship()
    created_at: Mapped[datetime] = mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return str(self.identifier)
    
class Brand(db.Model):
    __tablename__ = "brand"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(75))
    created_by_id: Mapped[int] = mapped_column(ForeignKey("user.id"), default=lambda: current_user.id) 
    created_by: Mapped["User"] = relationship()
    created_at: Mapped[datetime] = mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    def __init__(self, name: str, user: User) -> None:
        self.name=name
        self.created_by=user

    def __repr__(self) -> str:
        return str(self.name)
    
class Machine(db.Model):
    __tablename__ = "machine"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(75))
    created_by_id: Mapped[int] = mapped_column(ForeignKey("user.id"), default=lambda: current_user.id) 
    created_by: Mapped["User"] = relationship()
    created_at: Mapped[datetime] = mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    def __init__(self, name: str, user: User) -> None:
        self.name=name
        self.created_by=user

    def __repr__(self) -> str:
        return str(self.name)

class Role(db.Model):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)


# ---------------- Administration ViewModels ----------------

class BaseView(ModelView):
    #modals instead of redirecting to new page to edit information
    create_modal = False
    edit_modal = True
    column_exclude_list = ['password_hash']
    form_excluded_columns = ['created_at', 'created_by']

    def on_model_change(self, model, form, is_created: bool) -> None:
        if is_created:
            model.created_by = current_user

    def is_accessible(self) -> bool:
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name: Any, **kwargs: Any) -> Any:
        return redirect('/login')

class UserView(BaseView, ModelView):
    can_create = False
    column_editable_list = ['full_name', 'email', 'account_active', 'email_verified']
    column_exclude_list = ['verification_id', 'password_hash']
    column_searchable_list = ['full_name', 'email']

class ProductView(BaseView, ModelView):
    column_editable_list = ['brand','name', 'machine', 'identifier','stock_count']

class BrandView(BaseView, ModelView):
    column_editable_list = ['name']

class MachineView(BaseView, ModelView):
    column_editable_list = ['name']