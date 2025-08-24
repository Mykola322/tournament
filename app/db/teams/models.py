from typing import Optional, List
from uuid import uuid4
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.associative import RoleUserByTeam, Result




class Team(Base):
    __tablename__ = "teams"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text(), nullable=True, default=None)
    users: Mapped[List["User"]] = relationship(lazy="selectin", back_populates="teams", secondary=RoleUserByTeam.__tablename__)
    tournaments: Mapped[List["Tournament"]] = relationship(lazy="selectin", back_populates="teams", secondary=Result.__tablename__)

    def __init__(self, *args, **kwargs):
        self.id = uuid4().hex
        super().__init__(*args, **kwargs)