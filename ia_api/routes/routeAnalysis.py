from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from controllers.controllerAnalysis import analyze_deck
from services.cache import cached_matches, cached_cards

router = APIRouter()

class DeckRequest(BaseModel):
    deck: list[str]

@router.post("/analyze")
def analyze_deck_route(data: DeckRequest):
    if not cached_matches or not cached_cards:
        raise HTTPException(status_code=503, detail="Les données ne sont pas encore chargées depuis le backend.")
    result = analyze_deck(data.deck, cached_matches, cached_cards)
    return result
