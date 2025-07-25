from pydantic import BaseModel

class Battle(BaseModel):
    team_0_clan_tag: str | None  # Chaîne ou None si absent
    team_0_crowns: int | None
    replayTag: str | None
    opponent_0_crowns: int | None
    opponent_0_tag: str | None
    team_0_tag: str | None
    opponent_0_clan_tag: str | None

