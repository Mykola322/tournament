from typing import Optional, List

from pydantic import BaseModel, Field
from app.pydantic_models.teams import TeamModelResponse


class TournamentModel(BaseModel):
    name: str = Field(..., description="Назва турніру")
    descriptoin: Optional[str] = Field(None, description="Опис турніру")
    start_day: int = Field(7, description="Кількість днів для реєстрації на турнір")


class TournamentModelResponse(TournamentModel):
    id: str = Field(..., description="ID турніру")
    teams: List[TeamModelResponse] = Field([], description="Список команд учасників у турнірі")