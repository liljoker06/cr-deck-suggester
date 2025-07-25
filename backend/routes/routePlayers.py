from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from controllers.controllerPlayers import PlayersController
from models.modelPlayer import Player
import logging

router = APIRouter()
players_controller = PlayersController()

@router.get("/players", response_model=List[Player])
async def get_all_players(
    limit: Optional[int] = Query(100, description="Limiter le nombre de résultats", le=500),
    clan: Optional[str] = Query(None, description="Filtrer par clan"),
    country: Optional[str] = Query(None, description="Filtrer par pays"),
    level: Optional[int] = Query(None, description="Filtrer par niveau"),
    min_trophies: Optional[int] = Query(None, description="Nombre minimum de trophées"),
    max_trophies: Optional[int] = Query(None, description="Nombre maximum de trophées")
):
    """
    Récupère tous les joueurs avec filtres optionnels
    """
    try:
        if min_trophies is not None and max_trophies is not None:
            if min_trophies > max_trophies:
                raise HTTPException(status_code=400, detail="Le minimum ne peut pas être supérieur au maximum")
            players = await players_controller.get_players_by_trophy_range(min_trophies, max_trophies, limit)

        elif country:
            players = await players_controller.get_players_by_country(country, limit)

        elif clan:
            players = await players_controller.get_players_by_clan(clan, limit)

        elif level is not None:
            players = await players_controller.get_players_by_level(level, limit)

        else:
            players = await players_controller.get_all_players(limit)

        return players

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des joueurs: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@router.get("/players/search", response_model=List[Player])
async def search_players_by_name(
    pattern: str = Query(..., description="Motif de recherche pour le nom du joueur"),
    limit: Optional[int] = Query(50, description="Limiter le nombre de résultats", le=100)
):
    """
    Recherche des joueurs par nom (insensible à la casse)
    """
    try:
        players = await players_controller.search_players_by_name(pattern, limit)
        return players

    except Exception as e:
        logging.error(f"Erreur lors de la recherche de joueurs avec '{pattern}': {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
