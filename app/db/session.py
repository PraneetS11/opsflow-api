from collections.abc import AsyncIterator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    """One session per request; services own explicit transaction boundaries."""
    async with request.app.state.sessions() as session:
        yield session
