from typing import Optional, List
from uuid4 import uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.associative import Result


class Tournament(Base):
    __tablename__ = "tournaments"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(), nullable=True, default=None)
    teams: Mapped[List["User"]] = relationship(secondary=Result.__tablename__, lazy="selectin", back_populates="tournaments")
    tournaments: Mapped[List["Tournament"]] = relationship(secondary=Result.__tablename__, lazy="selectin", back_populates="teams")

    def __init__(self, *args, **kwargs):
        self.id = uuid4().hex
        super().__init__(*args, **kwargs)