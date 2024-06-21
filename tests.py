import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer, TestClient
from server import healthcheck, hash, get_hash_string




def get_test_client(app):
    server = TestServer(app)
    return TestClient(server)


@pytest.mark.asyncio
async def test_healthcheck():
    app = web.Application()
    app.router.add_get('/healthcheck', healthcheck)
    async with get_test_client(app) as client:
        resp = await client.get('/healthcheck')
        assert resp.status == 200
        data = await resp.json()
        assert data == {}


@pytest.mark.parametrize("input_string, expected_hash", [
    ("Hello!", "334d016f755cd6dc58c53a86e183882f8ec14f52fb05345887c8a5edd42c87b7"),
])
@pytest.mark.asyncio
async def test_hash(input_string, expected_hash):
    app = web.Application()
    app.router.add_post('/hash', hash)
    async with get_test_client(app) as client:
        resp = await client.post('/hash', json={"string": input_string})
        assert resp.status == 200
        data = await resp.json()
        assert data["hash_string"] == expected_hash


@pytest.mark.asyncio
async def test_hash_missing_string_field():
    app = web.Application()
    app.router.add_post('/hash', hash)
    async with get_test_client(app) as client:
        resp = await client.post('/hash', json={})
        assert resp.status == 400
        data = await resp.json()
        assert "validation_errors" in data
        assert data["validation_errors"] == "string field not found in json"
