from fastapi import APIRouter, status
from app.schemas import TravelRecommendationReq, TravelRecommendationRes
from app.controllers.travel import get_travel_recommendations

import logging


router = APIRouter(prefix="", tags=["travel"])
logger = logging.getLogger("__main__")


@router.post(
    "/travel_recommendation",
    status_code=status.HTTP_200_OK,
    response_model=TravelRecommendationRes,
)
async def travel_recommendation(data: TravelRecommendationReq):
    res = await get_travel_recommendations(data)
    logger.info(res)
    return res
