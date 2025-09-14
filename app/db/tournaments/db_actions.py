from typing import Optional, List
from datetime import date, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.associative import Result, Role, RoleUserByTeam
from app.db.tournaments.models import Tournament
from app.pydantic_models.tournaments import TournamentModel, TeamTournamentModel, ResultModel
from app.db.users.db_actions import get_user
from app.db.teams.models import Team
from app.db.users.models import User



async def add_tournament(user_id: str, db: AsyncSession, tournament_model: TournamentModel):
    user: Optional[User] = await get_user(user_id=user_id, db=db)
    if user.role != Role.organizator:
        return False

    tournament = Tournament(**tournament_model.model_dump())
    db.add(tournament)
    await db.commit()
    return True


async def get_tournaments(db: AsyncSession) -> List[Tournament]:
    return await db.scalars(select(Tournament).filter(Tournament.start_day > date.today()))


async def add_team_by_tournament(
    user_id: str,
    team_tournament_model:
    TeamTournamentModel,
    db: AsyncSession) -> bool:
    role_user_by_team: Optional[RoleUserByTeam] = await db.scalar(select(RoleUserByTeam)
        .filter_by(user=user_id, team_id=team_tournament_model.team_id, role=Role.teamlead)) # перевірка на тім ліда


    tournament: Optional[Tournament] = await db.scalar(select(Tournament).filter(Tournament.start_day > date.today(), Tournament.id==team_tournament_model.tournament_id))
    if not role_user_by_team or not tournament:
        return False


    result = Result(
        team_id = team_tournament_model.team_id,
        tornament_id=team_tournament_model.tournament_id
    )
    db.add(result)
    await db.commit()
    return True


async def add_result_by_team(user_id: str, result_model: ResultModel, db: AsyncSession) -> bool:
    result: Optional[Result] = await db.scalar(select(Result)
        .filter_by(team_id=result_model.team_id, tournament_id=result_model.tournament_id, result=None))
    user: Optional[User] = await get_user(user_id=user_id, db=db)

    if user.role != Role.organizator or not result or result.tournament.start_day >= date.today():
        return False

    result.result = result_model.result
    await db.commit()
    return True


async def change_result_by_team(user_id: str, result_model: ResultModel, db: AsyncSession) -> bool:
    result: Optional[Result] = await db.scalar(select(Result)
        .filter_by(team_id=result_model.team_id, tournament_id=result_model.tournament_id))
    user: Optional[User] = await get_user(user_id=user_id, db=db)

    if user.role != Role.organizator or not result or result.tournament.start_day <= date.today():
        return False

    result.result = result_model.result
    await db.commit()
    return True


async def get_results(db: AsyncSession):
    return await db.scalars(select(Result))