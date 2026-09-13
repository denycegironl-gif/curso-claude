import httpx
import pytest

from app.main import app


@pytest.mark.asyncio
async def test_states_returns_catalog_ordered() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/states")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "code": "PENDIENTE"},
        {"id": 2, "code": "EN_CURSO"},
        {"id": 3, "code": "BLOQUEADA"},
        {"id": 4, "code": "HECHA"},
    ]
