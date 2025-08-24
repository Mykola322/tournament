from typing import Optional, List
from datetime import date, timedelta, timezone, datetime
from uuid import uuid4
from enum import Enum
from sqlalchemy import String, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import jwt
import bcrypt

from app.db.base import Base
from app.config import settings
from app.db.associative import Role, RoleUserByTeam


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, default=None)
    last_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, default=None)
    bio: Mapped[Optional[str]] = mapped_column(Text(), nullable=True, default=None)
    role: Mapped[Role] = mapped_column(default=Role.user)
    teams: Mapped[List["Team"]] = relationship(secondary=RoleUserByTeam.__tablename__, back_populates="users", lazy="selectin")


    def __init__(self, *args, **kwargs):
        self.id = uuid4().hex
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self.password_

    @password.setter
    def password(self, pwd):
        self.password_ = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())

    def is_verify_password(self, pwd: str):
        return bcrypt.checkpw(pwd.encode(), self.password_.encode())

    def get_token(self, pwd: str, expire_time: int = 30):
        if not self.is_verify_password(pwd):
            return

        exp = datetime.now(timezone.utc) + timedelta(minutes=expire_time)
        payload = dict(sub=self.id, exp=exp)
        return jwt.encode(payload=payload, key=settings.secret_key, algorithm=settings.algorithm)
