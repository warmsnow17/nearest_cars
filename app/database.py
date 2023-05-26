"""Файл содержит подключение к базе данных."""
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def create_pool(
    pool_size: int = 20, uri: str = 'postgresql+asyncpg://postgres:postgres@db:5432/postgres',
) -> sessionmaker:

    """
    Функция принимает адрес поключение к базе данных и количество пулов.

    :param pool_size: количество пулов
    :param uri: адрес подключения к БД
    :return: Готовое подключение
    """
    engine = create_async_engine(url=make_url(uri), pool_size=pool_size, max_overflow=0)
    pool = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
    return pool


pool = None


async def get_db():
    global pool
    if pool is None:
        pool = create_pool()
    try:
        async with pool() as session:
            yield session
    finally:
        if session:
            await session.close()
