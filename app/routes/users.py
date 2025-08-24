from typing import Optional, List, Annotated, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.users import db_actions
from app.pydantic_models.users import UserModel, UserModelResponse
from app.config import settings
from app.db.base import get_db
from app.pydantic_models.token import TokenModel


users_route = APIRouter(prefix="/users", tags=["User"])


def get_user_id(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/users/token"))]) -> str:
    try:
        payload = jwt.decode(token, key=settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return user_id
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@users_route.post("/", status_code=status.HTTP_201_CREATED, summary="Реєсрація нового користувача")
async def sign_up(user_model: UserModel, db: Annotated[AsyncSession, Depends(get_db)]) -> None:
    result = await db_actions.sign_up(user_model=user_model, db=db)
    if not result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ім'я зайняте, спробуйте інше")


@users_route.post("/token/", status_code=status.HTTP_200_OK, response_model=TokenModel, summary="Вхід у застосунок")
async def sign_in(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession,Depends(get_db)]):
    token = await db_actions.sign_in(username=form.username, password=form.password, db=db)
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return dict(access_token=token)


@users_route.get("/me/", status_code=status.HTTP_202_ACCEPTED, response_model=UserModelResponse, summary="Інформація про поточного користувача")
async def get_user(user_id: Annotated[str, Depends(get_user_id)], db: Annotated[AsyncSession, Depends(get_db)]):
    return await db_actions.get_user(user_id=user_id, db=db)