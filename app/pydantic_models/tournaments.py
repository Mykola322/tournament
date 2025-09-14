from typing import Optional, List

from pydantic import BaseModel, Field
from app.pydantic_models.teams import TeamModelResponse, TeamModel


class TournamentModel(BaseModel):
    name: str = Field(..., description="Назва турніру")
    descriptoin: Optional[str] = Field(None, description="Опис турніру")
    reg_days: int = Field(7, description="Кількість днів для реєстрації на турнір")


class TournamentModelResponse(TournamentModel):
    id: str = Field(..., description="ID турніру")
    teams: List[TeamModelResponse] = Field([], description="Список команд учасників у турнірі")


class TeamTournamentModel(BaseModel):
    team_id: str = Field(..., description="ID команди")
    tournament_id: str = Field(..., description="ID турніру")


class ResultModel(TeamTournamentModel):
    result: float = Field(..., description="Результат команди у турнірі")


class ResultModelResponse(BaseModel):
    id: str
    team: TeamModelResponse
    tournament: TournamentModelResponse
    result: float