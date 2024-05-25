from typing import Literal
from pydantic_settings import BaseSettings

DEFAULT_API_PREFIX = "api"
DEFAULT_API_VERSION = "v1"


class Config(BaseSettings):
    APPLICATION_NAME: str = "AIPIPING L2 API"
    DESCRIPTION: str = "AIPIPING L2 API"

    ENVIRONMENT: Literal["dev", "qa", "prod"] = "dev"

    API_VERSION: str = DEFAULT_API_VERSION
    API_PREFIX: str = DEFAULT_API_PREFIX
    OPENAI_API_KEY: str
    OPENAI_API_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_CHAT_COMPLETIONS_ENPOINT: str = "/chat/completions"

    @property
    def OPENAPI_PREFIX(self):
        print(f"/{self.API_PREFIX}/{self.API_VERSION}")
        return f"/{self.API_PREFIX}/{self.API_VERSION}"


config = Config()
