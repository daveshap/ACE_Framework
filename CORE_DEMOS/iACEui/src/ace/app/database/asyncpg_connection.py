import asyncpg
from .settings import settings


async def get_asyncpg_db():
    conn = await asyncpg.connect(settings.database_uri)
    try:
        yield conn
    finally:
        await conn.close()


