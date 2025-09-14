from typing import Optional, List
from uuid import uuid4
from datetime import date, timedelta

from sqlalchemy import String, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.associative import Result


class Tournament(Base):
    __tablename__ = "tournaments"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text(), nullable=True, default=None)
    start_day: Mapped[date] = mapped_column(Date())
    teams: Mapped[List["Team"]] = relationship(secondary=Result.__tablename__, lazy="selectin", back_populates="tournaments")


    def __init__(self, *args, reg_days: int = 7, **kwargs):
        self.id = uuid4().hex
        self.start_day = date.today() + timedelta(days=reg_days)
        super().__init__(*args, **kwargs)