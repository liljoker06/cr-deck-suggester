from pydantic import BaseModel
from typing import List, Optional
from models.modelArena import Arena
from models.modelCard import Card

class Deck(BaseModel):
    name: str
    arena: Arena
    cards: List[Card]
    rating: Optional[float] = None
