from collections.abc import AsyncIterator

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_sessionmaker
from app.models import State
from app.schemas import StateOut

app = FastAPI()


async def get_session() -> AsyncIterator[AsyncSession]:
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as session:
        yield session


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/states")
async def list_states(session: AsyncSession = Depends(get_session)) -> list[StateOut]:
    result = await session.execute(select(State).order_by(State.sort_order, State.id))
    return [StateOut(id=state.id, code=state.code) for state in result.scalars()]
