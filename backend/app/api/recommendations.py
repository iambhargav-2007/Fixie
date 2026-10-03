from fastapi import APIRouter
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.services import ranking_service

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.post("", response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest):
    ranked_providers = ranking_service.rank_providers(request)
    return RecommendationResponse(
        providers=ranked_providers,
        count=len(ranked_providers)
    )
