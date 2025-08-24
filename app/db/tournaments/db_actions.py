from typing import Optional, List
from datetime import date, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.associative import Result, Role
from app.db.tournaments.models import Tournament
from app.pydantic_models.tournaments import TournamentModel
from app.db.users.db_actions import get_user


async def add_tournament(user_id: str, db: AsyncSession, tournament_model: TournamentModel):
    user = await get_user(user_id=user_id, db=db)
    if user.role != Role.organizator:
        return False

    tournament = Tournament(**tournament_model.model_dump())
    db.add(tournament)
    await db.commit()
    return True


async def get_tournaments(db: AsyncSession) -> List[Tournament]:
    return await db.scalars(select(Tournament).filter(Tournament.start_day < date.today()))