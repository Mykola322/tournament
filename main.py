import asyncio

from fastapi import FastAPI
import uvicorn

from app.routes.users import users_route
from app.routes.teams import teams_route
from app.routes.tournaments import tournaments_route
from app.db.base import create_db


app = FastAPI()
app.include_router(users_route)
app.include_router(teams_route)
app.include_router(tournaments_route)


if __name__ == "__main__":
   # asyncio.run(create_db())
    uvicorn.run("main:app", reload=True)