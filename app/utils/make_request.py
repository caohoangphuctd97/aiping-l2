import requests
import logging
from app.config import config
from app.exceptions.configure_exceptions import ServerErrorException
from app.schemas import TravelRecommendationReq

logger = logging.getLogger("__main__")


async def make_request_with_retries(
    method: str, url: str, headers: dict, params: dict = None,
    data: dict = None, retries: int = 5, timeout: int = 30
):
    """
    Make an HTTP request with retries.

    Args:
        method (str): HTTP method (e.g., 'GET', 'POST').
        url (str): The URL to send the request to.
        headers (dict): HTTP headers to include in the request.
        params (dict, optional): URL parameters to include in the request. Defaults to None.
        data (dict, optional): JSON data to include in the request body. Defaults to None.
        retries (int, optional): Number of retry attempts. Defaults to 5.
        timeout (int, optional): Timeout for the request in seconds. Defaults to 30.

    Returns:
        tuple: A tuple containing the JSON response and the status code.

    Raises:
        ServerErrorException: If the request fails after all retry attempts.
    """

    for attempt in range(retries):
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                timeout=timeout,
            )
            if response.status_code == 200:
                response_json = response.json()
                return response_json, response.status_code
            elif response.status_code in [502, 503, 429]:
                logger.warning(
                    f"Request failed with status code {response.status_code}."
                    f"Retrying... (Attempt {attempt + 1}/{retries})"
                )
                logger.warning(f"Response content: {response.text}")
            else:
                raise ServerErrorException(
                    f"Request failed with status code {response.status_code}"
                    f" and contain: {response.text}"
                )
        except (
            requests.exceptions.RequestException, requests.exceptions.Timeout
        ) as e:
            logger.error(
                f"Request failed: {e}. Retrying... "
                f"(Attempt {attempt + 1}/{retries})"
            )

    raise ServerErrorException(
        f"Request failed with status code {response.status_code}"
        f" and contain: {response.text}"
    )


async def render_payload_for_travel_recommendation(
    data: TravelRecommendationReq, **kwargs
) -> dict:
    """
    Render the payload for the travel recommendation request.

    Args:
        data (TravelRecommendationReq): The request data containing country and season.
        **kwargs: Additional keyword arguments for the OpenAI API.

    Returns:
        dict: The payload to be sent in the request.
    """
    return {
        "model": config.OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert travel advisor."
            },
            {
                "role": "user",
                "content": (
                    "Can you recommend some travel destinations in "
                    f"{data.country} during the {data.season}?"
                )
            },
            {
                "role": "user",
                "content": (
                    """
                    return data to list in python like this
                    [
                        "Go skiing in Whistler.",
                        "Experience the Northern Lights in Yukon.",
                        "Visit the Quebec Winter Carnival."
                    ]
                    """
                )
            }
        ],
        **kwargs
    }
