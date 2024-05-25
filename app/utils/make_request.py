import requests
import logging
from app.config import config

logger = logging.getLogger("__main__")


async def make_request_with_retries(
    method: str, url: str, headers: dict, params: dict = None,
    data: dict = None, retries: int = 5, timeout: int = 30
):
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
            else:
                logger.warning(
                    f"Request failed with status code {response.status_code}."
                    f"Retrying... (Attempt {attempt + 1}/{retries})"
                )
                logger.warning(f"Response content: {response.text}")
        except (
            requests.exceptions.RequestException, requests.exceptions.Timeout
        ) as e:
            logger.error(
                f"Request failed: {e}. Retrying... "
                f"(Attempt {attempt + 1}/{retries})"
            )

    logger.error(f"Request failed after {retries} attempts.")
    return response.json(), response.status_code


def post_stream(url: str, headers: dict, data: dict = None):
    s = requests.Session()
    chunks = []
    token_info = None
    with s.post(
        url, json=data, headers=headers, stream=True,
        proxies={"http": config.PROXY_URL, "https": config.PROXY_URL}
    ) as resp:
        for line in resp.iter_content():
            if line:
                chunks.append(line)

    pending = None
    for chunk in chunks:
        if pending is not None:
            chunk = pending + chunk
        lines = chunk.splitlines()

        if lines and lines[-1] and chunk and lines[-1][-1] == chunk[-1]:
            pending = lines.pop()
        else:
            pending = None
        if len(lines) != 0:
            token_chunk = lines[0].decode("utf-8")
            if "completion_tokens" in token_chunk:
                token_info = lines[0].decode("utf-8")[6:]
    return chunks, token_info


def data_generator(response: str):
    for chunk in response:
        yield "{}".format(chunk.decode('utf-8'))
