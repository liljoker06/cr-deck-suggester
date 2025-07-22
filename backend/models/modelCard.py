from pydantic import BaseModel
from typing import Optional

class Card(BaseModel):
    name: str
    category: str  # Catégorie générale (ex: "Troupe", "Sort", "Bâtiment")
    description: Optional[str] = None
    image: Optional[str] = None

    # Statistiques principales
    elixir_cost: Optional[int] = None
    hitpoints: Optional[int] = None
    damage: Optional[int] = None  # Dégâts classiques
    special_damage: Optional[int] = None  # Dégâts spéciaux (ex: death damage, tower damage)
    hit_speed: Optional[float] = None
    damage_per_second: Optional[int] = None
    range: Optional[str] = None
    count: Optional[int] = None

    # Champs supplémentaires selon la carte
    rarity: Optional[str] = None  # Rare, Épique, Légendaire, etc.
    card_type: Optional[str] = None  # Champion, Sort, Troupe, etc.
    lifetime: Optional[str] = None  # Durée de vie (ex: bâtiments)
    radius: Optional[str] = None  # Rayon d'effet (ex: sorts)
    spawn_speed: Optional[str] = None  # Vitesse d'apparition
    maximum_spawned: Optional[int] = None  # Nb max d'unités générées
