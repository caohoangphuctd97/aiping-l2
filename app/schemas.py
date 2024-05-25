from typing import List, Dict

from pydantic import BaseModel, field_validator, ValidationError


class TravelRecommendationReq(BaseModel):
    country: str
    season: str

    class Config:
        schema_extra = {
            "example": {
                "country": "France",
                "season": "summer"
            }
        }

    @field_validator('season')
    def season_must_be_valid(cls, v):
        valid_seasons = ["spring", "summer", "autumn", "winter"]
        if v not in valid_seasons:
            raise ValidationError(f'Season must be one of {valid_seasons}')
        return v


class TravelRecommendationRes(BaseModel):
    country: str
    season: str
    recommendations: List[str]

    class Config:
        schema_extra = {
            "example": {
                "country": "Canada",
                "season": "winter",
                "recommendations": [
                    "Go skiing in Whistler.",
                    "Experience the Northern Lights in Yukon.",
                    "Visit the Quebec Winter Carnival."
                ]
            }
        }


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionReq(BaseModel):
    model: str = "gpt-4o"
    messages: List[Message]
