from pydantic import BaseModel
from typing import List, Optional

class Player(BaseModel):
    name: str
    player_tag: str
    level: int
    trophies: int
    clan: str
    badge_clan: str
    pays: str
