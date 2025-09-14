from typing import Optional, List, Annotated

from fastapi import APIRouter, Depends, status, Query, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tournaments import db_actions
from app.db.tournaments.models import Tournament
from app.db.associative import Result
from app.pydantic_models.tournaments import TournamentModel, TeamModelResponse, TeamTournamentModel, ResultModel, TournamentModelResponse, ResultModelResponse
from app.routes.users import get_user_id
from app.db.base import get_db


tournaments_route = APIRouter(prefix="/tournaments", tags=["Tournaments"])


@tournaments_route.post("/", status_code=status.HTTP_201_CREATED)
async def add_tournament(
    user_id: Annotated[str, Depends(get_user_id)],
    tournament_model: TournamentModel,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db_actions.add_tournament(
        user_id=user_id,
        tournament_model=tournament_model,
        db=db
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Ви не можете створювати турніри")



@tournaments_route.get("/", status_code=status.HTTP_202_ACCEPTED, response_model=List[TournamentModelResponse])
async def get_tournaments(user_id: Annotated[str, Depends(get_user_id)], db: Annotated[AsyncSession, Depends(get_db)]):
    return await db_actions.get_tournaments(db=db)


@tournaments_route.put("/", status_code=status.HTTP_202_ACCEPTED)
async def add_team_by_tournament(
    user_id: Annotated[str, Depends(get_user_id)],
    team_tournament_model: TeamTournamentModel,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db_actions.add_team_by_tournament(
        user_id=user_id,
        team_tournament_model=team_tournament_model,
        db=db
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Цей користувач не може зареєструвати команду")


@tournaments_route.patch("/add_resut/", status_code=status.HTTP_202_ACCEPTED)
async def add_result_by_team(
    user_id: Annotated[str, Depends(get_user_id)],
    result_model: ResultModel,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db_actions.add_result_by_team(
        user_id=user_id,
        result_model=result_model,
        db=db
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)


@tournaments_route.patch("/change_result/", status_code=status.HTTP_202_ACCEPTED)
async def change_result(
    user_id: Annotated[str, Depends(get_user_id)],
    result_model: ResultModel,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db_actions.change_result_by_team(
        user_id=user_id,
        result_model=result_model,
        db=db
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Цей користувач не може змінювати результати турніру")


@tournaments_route.get("/results/", status_code=status.HTTP_202_ACCEPTED, response_model=List[ResultModelResponse])
async def get_results(user_id: Annotated[str, Depends(get_user_id)], db: Annotated[AsyncSession, Depends(get_db)]):
    return await db_actions.get_results(db=db)
