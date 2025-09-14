from typing import Optional, List

from pydantic import BaseModel, Field

from app.pydantic_models.users import UserModelResponse
from app.db.associative import AddVote

class TeamModel(BaseModel):
    name: str = Field(..., description="Назва команди")
    description: Optional[str] = Field(None, description="Опис команди")


class TeamModelResponse(TeamModel):
    id: str = Field(..., description="ID команди")
    users: List[UserModelResponse] = Field([], description="Список учасників")


class UserByTeamModel(BaseModel):
    member_id: str = Field(..., description="ID Користувача, якого додаємо до комнади")
    team_id: str = Field(..., description="ID Команди")


class TeamTournamentModel(BaseModel):
    team_id: str = Field(..., description="ID команди")
    tournament_id: str = Field(..., description="ID турніру")
    vote: AddVote = Field(AddVote.vote_up, description="+1 або -1 для голосування", examples=[-1, 1])


class MessageModel(BaseModel):
    team_id: str = Field(..., description="ID команди")
    message:  Optional[str] = Field(None, description="Повідомлення для тімліда")


class ChangeMessageModel(BaseModel):
    message_id: str = Field(...)
    answer: Optional[str] = Field(None)
    result: bool = Field(...)


class MessageModelResponse(BaseModel):
    id: str
    user_id: str
    team_id: str
    message: Optional[str]
    answer: Optional[str]
    result: Optional[bool]