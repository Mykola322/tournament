from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.associative import RoleUserByTeam, Role, VoteResult
from app.db.teams.models import Team
from app.pydantic_models.teams import TeamModel, UserByTeamModel
from app.db.users.db_actions import get_user


async def add_team(user_id: str, team_model: TeamModel, db: AsyncSession) -> None:
    team: Optional[Team] = await db.scalar(select(Team).filter_by(name=team_model.name))
    if team:
        return False

    team = Team(**team_model.model_dump())
    role_user_by_team = RoleUserByTeam(
        user_id=user_id,
        team=team,
        role=Role.teamlead
    )
    db.add(role_user_by_team)
    await db.commit()
    return True


async def get_teams(db: AsyncSession):
    return await db.scalars(select(Team))


async def get_team(team_id: str, db: AsyncSession) -> Optional[Team]:
    return await db.scalar(select(Team).filter_by(id=team_id))


async def add_member_by_team(user_id: str, user_by_team_model: UserByTeamModel, db: AsyncSession) -> bool:
    role_user_by_team: Optional[RoleUserByTeam] = await db.scalar(select(RoleUserByTeam).filter_by(user_id=user_id, team_id=user_by_team_model.team_id, role=Role.teamlead))
    if not role_user_by_team:
        return False

    user = await db.scalar(select(user_id=user_by_team_model.member_id, db=db))
    if not user:
        return False
    role_user_by_team = RoleUserByTeam(
        team_id=user_by_team_model.team_id,
        user_id=user_by_team_model.member_id
    )
    db.add(role_user_by_team)
    await db.commit()
    return True