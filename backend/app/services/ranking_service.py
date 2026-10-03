from typing import List
from app.schemas.recommendation import RecommendationRequest, RankedProviderResponse, ScoreBreakdown
from app.services import discovery_service

PROBLEM_COMPATIBILITY_WEIGHT = 0.35
SPECIALIZATION_WEIGHT = 0.20
AVAILABILITY_WEIGHT = 0.15
DISTANCE_WEIGHT = 0.15
RATING_WEIGHT = 0.10
PRICE_WEIGHT = 0.05

def rank_providers(req: RecommendationRequest) -> List[RankedProviderResponse]:
    radius_meters = (req.requirements.max_distance_km or 5) * 1000
    
    # 1. Discover and Filter (Phase 3)
    eligible_list = discovery_service.discover_nearby_providers(
        service=req.requirements.service,
        lat=req.location.latitude,
        lon=req.location.longitude,
        radius=radius_meters,
        specialization=req.requirements.specialization,
        minimum_rating=req.requirements.minimum_rating,
        max_budget=req.requirements.max_budget,
        preferred_time=req.requirements.preferred_time,
        preferred_date=req.requirements.preferred_date
    )
    
    ranked = []
    for provider in eligible_list.providers:
        # 2. Score Calculation
        problem_score = 1.0  # Phase 3 filtered out incompatible
        specialization_score = 1.0  # Phase 3 filtered out incompatible
        availability_score = 1.0  # Phase 3 filtered out incompatible
        
        # Distance
        dist_km = provider.distance_km
        max_dist_km = float(req.requirements.max_distance_km or 5.0)
        if max_dist_km <= 0:
            distance_score = 1.0
        else:
            distance_score = max(0.0, 1.0 - (dist_km / max_dist_km))
            
        # Rating
        rating_score = max(0.0, min(1.0, provider.rating / 5.0))
        
        # Price
        if not req.requirements.max_budget:
            price_score = 1.0
        else:
            min_price = max(1, provider.pricing.get("min", 1))
            price_score = min(1.0, req.requirements.max_budget / float(min_price))
            price_score = max(0.0, price_score)
            
        # 3. Weighted Fit Score
        weighted_score = (
            problem_score * PROBLEM_COMPATIBILITY_WEIGHT
            + specialization_score * SPECIALIZATION_WEIGHT
            + availability_score * AVAILABILITY_WEIGHT
            + distance_score * DISTANCE_WEIGHT
            + rating_score * RATING_WEIGHT
            + price_score * PRICE_WEIGHT
        )
        
        fit_score = min(100.0, max(0.0, weighted_score * 100.0))
        fit_score = round(fit_score, 2)
        
        breakdown = ScoreBreakdown(
            problem_compatibility=problem_score,
            specialization=specialization_score,
            availability=availability_score,
            distance=round(distance_score, 2),
            rating=round(rating_score, 2),
            price=round(price_score, 2)
        )
        
        p_dict = provider.model_dump()
        ranked.append({
            **p_dict,
            "fit_score": fit_score,
            "score_breakdown": breakdown
        })
        
    # 4. Sort and Tie-breaking
    ranked_sorted = sorted(
        ranked,
        key=lambda x: (
            -x["fit_score"],
            x["distance_km"],
            -x["rating"],
            x["provider_id"]
        )
    )
    
    # 5. Assign Rank
    results = []
    for i, r in enumerate(ranked_sorted):
        r["rank"] = i + 1
        results.append(RankedProviderResponse(**r))
        
    return results
