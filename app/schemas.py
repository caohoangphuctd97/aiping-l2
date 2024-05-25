from typing import List, Dict

from pydantic import BaseModel, field_validator
from countryinfo import CountryInfo


class TravelRecommendationReq(BaseModel):
    country: str
    season: str

    @field_validator("season")
    def season_must_be_valid(cls, v):
        valid_seasons = ["spring", "summer", "autumn", "winter"]
        if v not in valid_seasons:
            raise ValueError(f"Season must be one of {valid_seasons}")
        return v

    @field_validator("country")
    def country_must_be_valid(cls, v):
        try:
            _ = CountryInfo(v).info()
        except KeyError:
            raise ValueError("Invalid country name")
        return v


class TravelRecommendationRes(BaseModel):
    country: str
    season: str
    recommendations: List[str]
