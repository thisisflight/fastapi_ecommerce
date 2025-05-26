from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declared_attr

from app.backend import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ECHO,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    future=True
)
SessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            async with session.begin():
                yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
