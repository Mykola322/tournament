from typing import Optional, List
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.associative import RoleUserByTeam, Role, VoteResult, Message
from app.db.teams.models import Team
from app.pydantic_models.teams import TeamModel, UserByTeamModel, MessageModel, ChangeMessageModel
from app.db.users.db_actions import get_user
from app.pydantic_models.tournaments import TeamTournamentModel, TournamentModel
from app.db.tournaments.models import Tournament


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


async def add_vote_by_tournament(user_id: str, team_tournament_model: TeamTournamentModel, db: AsyncSession) -> bool:
    role_user_by_team: Optional[RoleUserByTeam] = await db.scalar(select(RoleUserByTeam)
        .filter_by(user_id=user_id, team_id=team_tournament_model.team_id))

    tournament: Optional[Tournament] = await db.scalar(select(Tournament)
        .filter(Tournament.id==team_tournament_model.tournament_id, Tournament.start_day > date.today()))
    if not role_user_by_team or not tournament:
        return False

    vote_result: Optional[VoteResult] = await db.scalar(select(VoteResult)
        .filter_by(team_id=team_tournament_model.team_id, tournament_id=team_tournament_model.tournament_id))
    if not vote_result:
        vote_result = VoteResult(
            team_id=team_tournament_model.team_id,
            tournament_id=team_tournament_model.tournament_id
        )
        db.add(vote_result)

    vote_result.vote_result += team_tournament_model.vote
    await db.commit()
    return True


async def create_message(user_id: str, message_model: MessageModel, db: AsyncSession) -> bool:
    message = await db.scalar(select(Message).filter_by(user_id=user_id, team_id=message_model.team_id))
    if message:
        return False

    message = Message(
        user_id=user_id,
        **message_model.model_dump()
    )
    db.add(message)
    await db.commit()
    return True


async def get_messages_teamlead(user_id: str, team_id: str, db: AsyncSession) -> List[Message]:
    role_user_by_team = await db.scalar(select(RoleUserByTeam).filter_by(
        user_id=user_id, team_id=team_id, role=Role.teamlead
    ))
    if not role_user_by_team:
        return []

    return await db.scalars(select(Message).filter_by(team_id=team_id, result=None))


async def change_result_message(
        user_id: str,
        change_message_model: ChangeMessageModel,
        db: AsyncSession
) -> bool:
    message: Optional[Message] = await db.scalar(select(Message).filter_by(id=change_message_model.message_id, result=None))
    if not message:
        return False


    role_user_by_team = await db.scalar(select(RoleUserByTeam)
        .filter_by(user_id=user_id, team_id=message.team_id, role=Role.teamlead)
    )
    if not role_user_by_team:
       return False


    message.answer = change_message_model.answer
    message.result = change_message_model.result

    if change_message_model.result:
        role_user_by_team = RoleUserByTeam(user_id=message.user_id, team_id=message.team_id)
        db.add(role_user_by_team)

    await db.commit()
    return True


async def get_messages(user_id: str, db: AsyncSession) -> List[Message]:
    return await db.scalars(select(Message).filter_by(user_id=user_id))