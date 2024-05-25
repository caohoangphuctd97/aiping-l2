import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
@patch("app.apis.travel.get_travel_recommendations", new_callable=AsyncMock)
async def test_travel_recommendation_api(mock_api):
    mock_api.return_value = {
        "country": "Canada",
        "season": "winter",
        "recommendations": [
            "Go skiing in Whistler.",
            "Experience the Northern Lights in Yukon.",
            "Visit the Quebec Winter Carnival.",
        ],
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        request_data = {"country": "Canada", "season": "winter"}
        response = await ac.post("/api/v1/travel_recommendation", json=request_data)

    assert response.status_code == 200
    assert response.json() == {
        "country": "Canada",
        "season": "winter",
        "recommendations": [
            "Go skiing in Whistler.",
            "Experience the Northern Lights in Yukon.",
            "Visit the Quebec Winter Carnival.",
        ],
    }
