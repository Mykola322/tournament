from typing import Optional, List

from pydantic import BaseModel, Field

from app.pydantic_models.users import UserModelResponse


class TeamModel(BaseModel):
    name: str = Field(..., description="Назва команди")
    description: Optional[str] = Field(None, description="Опис команди")


class TeamModelResponse(TeamModel):
    id: str = Field(..., description="ID команди")
    users: List[UserModelResponse] = Field([], description="Список учасників")


class UserByTeamModel(BaseModel):
    member_id: str = Field(..., description="ID Користувача, якого додаємо до комнади")
    team_id: str = Field(..., description="ID Команди")
