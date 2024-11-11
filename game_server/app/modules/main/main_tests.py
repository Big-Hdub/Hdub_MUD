import pytest
from quart import Quart
from quart.testing import QuartClient
from app.app import create_app

@pytest.fixture
async def app() -> Quart:
    app = await create_app('testing')
    return app

@pytest.fixture
async def client(app: Quart) -> QuartClient:
    return app.test_client()

@pytest.mark.asyncio
async def test_index(client: QuartClient):
    response = await client.get('/')
    assert response.status_code == 200
    data = await response.get_json()
    assert data == {'data': {'message': 'Hello, World!'}}
