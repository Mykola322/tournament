from pydantic import BaseModel, Field


class TokenModel(BaseModel):
    access_token: str = Field(..., description="Bearer token")
    token_type: str = Field("Bearer")