from typing import Optional
from pydantic import BaseModel, Field

class Evolution(BaseModel):
    elixir_cost: Optional[str]  # Coût en élixir de l'évolution
    cycles: Optional[str]  # Nombre de cycles nécessaires pour déclencher l'évolution
    overall_cost: Optional[str]  # Coût total pour obtenir l'évolution
    stat_boost: Optional[str]  # Amélioration des statistiques apportée par l'évolution

class Card(BaseModel):
    name: str  # Nom de la carte
    category: str  # Catégorie de la carte (Troupe, Sort, Bâtiment)
    description: Optional[str]  # Description de la carte
    image: Optional[str]  # URL de l'image de la carte

    elixir_cost: Optional[str]  # Coût en élixir pour jouer la carte
    hitpoints: Optional[str]  # Points de vie de la carte
    damage: Optional[str]  # Dégâts infligés par la carte
    hit_speed: Optional[str]  # Vitesse d'attaque en secondes
    dps: Optional[str]  # Dégâts par seconde
    special_damage: Optional[str]  # Dégâts spéciaux (ex: dégâts de zone)
    crown_tower_damage: Optional[str]  # Dégâts infligés aux tours de couronne
    range: Optional[str]  # Portée d'attaque de la carte
    radius: Optional[str]  # Rayon d'effet (pour sorts de zone ou explosions)
    count: Optional[str]  # Nombre d'unités invoquées
    lifetime: Optional[str]  # Durée de vie de la carte (pour bâtiments)
    troop_spawned: Optional[str]  # Type de troupe générée (pour bâtiments générateurs)
    spawn_speed: Optional[str]  # Vitesse de génération des troupes
    max_spawned: Optional[str]  # Nombre maximum de troupes générées
    rarity: Optional[str]  # Rareté de la carte (Commune, Rare, Épique, Légendaire)
    type: Optional[str]  # Type spécifique de la carte

    evolution: Optional[Evolution]  # Données d'évolution de la carte (si disponible)