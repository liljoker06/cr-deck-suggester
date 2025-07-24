from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import List
from controllers.controllerAnalysis import analyze_deck

router = APIRouter()

class DeckRequest(BaseModel):
    deck: List[str]

@router.post("/analyze")
async def analyze_deck_route(data: DeckRequest, request: Request):
    db = request.app.state.db
    try:
        result = await analyze_deck(data.deck, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
