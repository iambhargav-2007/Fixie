"""Deterministic Matching Engine."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from backend.app.services.discovery_service import DiscoveredProvider, DiscoveryRequirement
import logging

logger = logging.getLogger(__name__)

class ScoreBreakdown(BaseModel):
    problem_compatibility: float
    specialization: float
    availability: float
    distance: float
    rating: float
    price: float

class RankedProvider(BaseModel):
    provider_id: str
    name: str
    services: List[str]
    specializations: List[str]
    distance_km: float
    rating: float
    price_min: float
    price_max: float
    availability_status: str
    availability_slots: List[str]
    verified: bool
    fit_score: float
    score_breakdown: ScoreBreakdown

class MatchingResult(BaseModel):
    providers: List[RankedProvider]
    match_status: str
    reason: str

class MatchingEngine:
    # Weights defined by requirements
    WEIGHTS = {
        "problem_compatibility": 0.35,
        "specialization": 0.20,
        "availability": 0.15,
        "distance": 0.15,
        "rating": 0.10,
        "price": 0.05
    }

    def match(self, req: DiscoveryRequirement, candidates: List[DiscoveredProvider]) -> MatchingResult:
        if not candidates:
            return MatchingResult(
                providers=[],
                match_status="no_match",
                reason="No providers currently match the requested service and location."
            )

        # Pre-calculate prices for normalization
        avg_prices = []
        for c in candidates:
            p = c.provider.pricing
            avg_prices.append((p.min + p.max) / 2.0)
            
        min_price = min(avg_prices) if avg_prices else 0
        max_price = max(avg_prices) if avg_prices else 0

        ranked_candidates = []
        for c in candidates:
            breakdown = self._calculate_scores(c, req, min_price, max_price)
            
            fit_score = (
                breakdown.problem_compatibility * self.WEIGHTS["problem_compatibility"] +
                breakdown.specialization * self.WEIGHTS["specialization"] +
                breakdown.availability * self.WEIGHTS["availability"] +
                breakdown.distance * self.WEIGHTS["distance"] +
                breakdown.rating * self.WEIGHTS["rating"] +
                breakdown.price * self.WEIGHTS["price"]
            )

            rp = RankedProvider(
                provider_id=c.provider.id,
                name=c.provider.name,
                services=c.provider.services,
                specializations=c.provider.specializations,
                distance_km=c.distance_km,
                rating=c.provider.rating,
                price_min=c.provider.pricing.min,
                price_max=c.provider.pricing.max,
                availability_status=c.provider.availability.status,
                availability_slots=c.provider.availability.slots,
                verified=c.provider.verified,
                fit_score=round(fit_score, 2),
                score_breakdown=breakdown
            )
            ranked_candidates.append(rp)

        # Sort by fit_score descending, then distance ascending, then provider_id ascending
        ranked_candidates.sort(key=lambda x: (-x.fit_score, x.distance_km, x.provider_id))

        return MatchingResult(
            providers=ranked_candidates,
            match_status="success",
            reason=f"Found {len(ranked_candidates)} matched providers."
        )

    def _calculate_scores(self, candidate: DiscoveredProvider, req: DiscoveryRequirement, min_price: float, max_price: float) -> ScoreBreakdown:
        p = candidate.provider
        
        # 1. Problem Compatibility
        # Service is guaranteed to match due to discovery.
        # If specialization requested and matched, 100. Else 80.
        has_spec = req.specialization in p.specializations if req.specialization else True
        problem_score = 100.0 if has_spec else 80.0
        
        # 2. Specialization
        if req.specialization:
            spec_score = 100.0 if req.specialization in p.specializations else 50.0
        else:
            spec_score = 100.0
            
        # 3. Availability
        if req.preferred_time:
            avail_score = 100.0 if req.preferred_time in p.availability.slots else 50.0
        else:
            avail_score = 100.0
            
        # 4. Distance
        max_dist = req.max_distance_km
        if max_dist <= 0:
            dist_score = 100.0 if candidate.distance_km == 0 else 0.0
        else:
            dist_score = max(0.0, 100.0 - (candidate.distance_km / max_dist) * 100.0)
            
        # 5. Rating
        # Normalize rating from 0-5 to 0-100
        rating_score = (p.rating / 5.0) * 100.0 if p.rating > 0 else 0.0
        
        # 6. Price
        avg_price = (p.pricing.min + p.pricing.max) / 2.0
        if max_price == min_price:
            price_score = 100.0
        else:
            # lower price = higher score
            price_score = 100.0 - ((avg_price - min_price) / (max_price - min_price) * 100.0)
            
        return ScoreBreakdown(
            problem_compatibility=round(problem_score, 2),
            specialization=round(spec_score, 2),
            availability=round(avail_score, 2),
            distance=round(dist_score, 2),
            rating=round(rating_score, 2),
            price=round(price_score, 2)
        )
