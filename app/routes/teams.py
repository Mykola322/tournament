from typing import Optional, List, Annotated

from fastapi import APIRouter, status, HTTPException, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.teams import db_actions
from app.pydantic_models.teams import TeamModel, TeamModelResponse, UserByTeamModel
from app.routes.users import get_user_id
from app.db.base import get_db


teams_route = APIRouter(prefix="/teams", tags=["Teams"])


@teams_route.post("/", status_code=status.HTTP_201_CREATED)
async def add_team(
    user_id: Annotated[str, Depends(get_user_id)],
    team_model: TeamModel,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db_actions.add_team(user_id=user_id, team_model=team_model, db=db)
    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Така команда вже існує")


@teams_route.get("/", status_code=status.HTTP_202_ACCEPTED, response_model=List[TeamModelResponse])
async def get_teams(
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[str, Depends(get_db)]
):
    return await db_actions.get_teams(db=db)


@teams_route.get("/{team_id}/", status_code=status.HTTP_202_ACCEPTED, response_model=TeamModelResponse, summary="Інформація про користувача")
async def get_team(
        user_id: Annotated[str, Depends(get_user_id)],
        db: Annotated[AsyncSession, Depends(get_db)],
        team_id: str = Path(..., description="ID команди")
):
    team = await db_actions.get_team(team_id=team_id, db=db)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такої команди не існує")

    return team


@teams_route.post("/member/", status_code=status.HTTP_202_ACCEPTED, summary="Додати учасника команди")
async def add_member_by_team(
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
    user_by_team_model: UserByTeamModel
):
    result = await db_actions.add_member_by_team(
        user_id=user_id,
        user_by_team_model=user_by_team_model,
        db=db
    )

    if not result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)