from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.users.models import User
from app.config import settings

from app.pydantic_models.users import UserModel


async def get_user(user_id: str, db: AsyncSession)-> Optional[User]:
    return await db.scalar(select(User).filter_by(id=user_id))


async def sign_up(user_model: UserModel, db: AsyncSession) -> bool:
    user: Optional[User] = await db.scalar(select(User).filter_by(username=user_model.username))
    if user:
        return False

    user = User(**user_model.model_dump())
    db.add(user)
    await db.commit()
    return True


async def sign_in(username: str, password: str, db: AsyncSession) -> Optional[str]:
    user: Optional[User] = await db.scalar(select(User).filter_by(username=username))
    if not user:
        return

    return user.get_token(pwd=password)