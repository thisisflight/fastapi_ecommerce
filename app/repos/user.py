from fastapi import Depends
from sqlalchemy import exists, insert, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend import get_db
from app.models import User
from app.schemas import CreateUserDB


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def create_user(self, user_schema: CreateUserDB) -> User:
        user_db = CreateUserDB(**user_schema.model_dump())
        stmt = insert(User).values(**user_db.model_dump()).returning(User)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def check_if_user_exists(self, username: str, email: str) -> bool:
        stmt = select(exists().where(or_(User.username == username, User.email == email)))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def activate_user(self, email):
        stmt = update(User).where(User.email == email).values(is_active=True).returning(User)
        result = await self.session.execute(stmt)
        return result.scalar()


def get_user_repo(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session)
