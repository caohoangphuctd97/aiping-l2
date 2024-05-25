from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from app.schemas import TravelRecommendationReq, TravelRecommendationRes
from app.utils.make_request import make_request_with_retries

import logging
import json


router = APIRouter(prefix="", tags=["travel"])
logger = logging.getLogger("__main__")


@router.post(
    "/travel_recommendation", status_code=status.HTTP_200_OK,
    response_model=TravelRecommendationRes
)
async def chat_completions(
    data: TravelRecommendationReq
):
    return JSONResponse(content={})
