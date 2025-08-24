from typing import Optional, List
from enum import Enum, IntEnum
from uuid import uuid4

from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Role(Enum):
    teamlead = "teamlead"
    member = "member"
    organizator = "organizator"
    admin = "admin"
    user = "user"


class AddVote(IntEnum):
    vote_up = 1
    vote_down = -1


class RoleUserByTeam(Base):
    __tablename__ = "role_user_by_team"

    id = Column(String(100), primary_key=True)
    user_id = Column(String(100), ForeignKey("users.id", ondelete="CASCADE"))
    team_id = Column(String(100), ForeignKey("teams.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship()
    team: Mapped["Team"] = relationship(lazy="selectin")
    role: Mapped[Role] = mapped_column(default=Role.member)

    def __init__(self, *args, **kwargs):
        self.id = uuid4().hex
        super().__init__(*args, **kwargs)


class VoteResult(Base):
    __tablename__ = "votes"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    team_id: Mapped[str]= mapped_column(ForeignKey("teams.id"), primary_key=True)
    team: Mapped["Team"] = relationship(lazy="selectin")
    tournament_id: Mapped[str] = mapped_column(String(100), ForeignKey("tournaments.id"), primary_key=True)
    tournament: Mapped["Tournament"] = relationship(lazy="selectin")
    vote_result: Mapped[int] = mapped_column()

    def __init__(self, *args, **kwargs):
        self.id = uuid4().hex
        super().__init__(*args, **kwargs)


class Result(Base):
    __tablename__ = "results"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    team_id: Mapped[str]= mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True)
    team: Mapped["Team"] = relationship(lazy="selectin")
    tournament_id = Column(String(100), ForeignKey("tournaments.id", ondelete="CASCADE"), primary_key=True)
    tournament: Mapped["Tournament"] = relationship(lazy="selectin")
    result: Mapped[float] = mapped_column()

    def __init__(self, *args, **kwargs):
        self.id = uuid4().hex
        super().__init__(*args, **kwargs)