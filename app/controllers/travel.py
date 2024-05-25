import logging
import ast

from app.config import config
from app.schemas import TravelRecommendationReq, TravelRecommendationRes
from app.utils.make_request import (
    make_request_with_retries,
    render_payload_for_travel_recommendation,
)

logger = logging.getLogger("__main__")


async def get_travel_recommendations(
    data: TravelRecommendationReq, **kwargs
) -> TravelRecommendationRes:
    """
    Fetch travel recommendations from OpenAI's API based on the provided data.

    Args:
        data (TravelRecommendationReq): The request data containing country and season.
        **kwargs: Additional keyword arguments of OpenAI API.

    Returns:
        TravelRecommendationRes: The response containing travel recommendations.
    """

    url = f"{config.OPENAI_API_URL}{config.OPENAI_CHAT_COMPLETIONS_ENPOINT}"
    headers = {
        "Authorization": f"Bearer {config.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = await render_payload_for_travel_recommendation(data=data, **kwargs)
    response_json, _ = await make_request_with_retries(
        method="POST", url=url, headers=headers, data=payload
    )

    contents = ""
    for content in response_json.get("choices", []):
        contents += content["message"]["content"]

    # Extract the list part from the content
    list_start = contents.find("[")
    list_end = contents.rfind("]") + 1
    list_str = contents[list_start:list_end]

    # Convert the string representation of the list to an actual list
    travel_destinations = ast.literal_eval(list_str)

    return TravelRecommendationRes(
        country=data.country, season=data.season, recommendations=travel_destinations
    )
