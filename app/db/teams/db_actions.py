from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.associative import RoleUserByTeam, Role, VoteResult, Result
from app.db.teams.models import Team