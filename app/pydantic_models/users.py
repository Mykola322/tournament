from typing import Optional

from pydantic import BaseModel, Field


class UserModelResponse(BaseModel):
    id: str = Field(..., description="ID користувача")
    username: str = Field(..., description="Логін користувача", min_length=5)
    first_name: Optional[str] = Field(None, description="Ім'я")
    last_name: Optional[str] = Field(None, description="Прізвище")
    bio: Optional[str] = Field(None, description="Коротка інформація про себе")


class UserModel(BaseModel):
    username: str = Field(..., description="Логін користувача", min_length=5)
    password: str = Field(..., description="Пароль", min_length=6)
    first_name: Optional[str] = Field(None, description="Ім'я")
    last_name: Optional[str] = Field(None, description="Прізвище")
    bio: Optional[str] = Field(None, description="Коротка інформація про себе")