import pytest
from unittest.mock import AsyncMock, patch
from app.schemas import TravelRecommendationReq, TravelRecommendationRes
from app.controllers.travel import get_travel_recommendations


@pytest.mark.asyncio
@patch("app.controllers.travel.make_request_with_retries", new_callable=AsyncMock)
async def test_get_travel_recommendations(mock_make_request):
    # Mock the make_request_with_retries function
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": (
                        "Sure! Here are some winter travel recommendations: "
                        '["Go skiing in Whistler.", "Experience the Northern Lights in Yukon.", '
                        '"Visit the Quebec Winter Carnival."]'
                    )
                }
            }
        ]
    }
    mock_make_request.return_value = (mock_response, 200)

    request_data = TravelRecommendationReq(country="Canada", season="winter")
    response = await get_travel_recommendations(request_data)

    expected_response = TravelRecommendationRes(
        country="Canada",
        season="winter",
        recommendations=[
            "Go skiing in Whistler.",
            "Experience the Northern Lights in Yukon.",
            "Visit the Quebec Winter Carnival.",
        ],
    )
    assert response == expected_response
