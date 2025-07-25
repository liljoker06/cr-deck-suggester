from fastapi import APIRouter, HTTPException
from controllers.controllerArenas import ArenasController
from controllers.controllerCard import get_all_cards
from controllers.controllerPlayers import PlayersController
from database import get_database
import logging

router = APIRouter()

arenas_controller = ArenasController()
players_controller = PlayersController()

@router.get("/stats")
async def get_global_stats():
    """
    Récupère toutes les statistiques globales de l'application
    """
    try:
        # Statistiques synchrones/asynchrones
        cards_data = await get_all_cards()
        total_cards = len(cards_data)

        arenas_count = await arenas_controller.get_arenas_count()
        players_count = await players_controller.get_players_count()

        players_stats = await players_controller.get_players_stats()
        players_by_country = await players_controller.get_players_count_by_country()
        players_by_level = await players_controller.get_players_count_by_level()

        db = get_database()
        decks_count = await db["decks"].count_documents({})

        return {
            "totals": {
                "cards": total_cards,
                "arenas": arenas_count,
                "players": players_count,
                "decks": decks_count
            },
            "players": {
                "general_stats": players_stats,
                "by_country": dict(list(players_by_country.items())[:10]),
                "by_level": players_by_level,
                "total": players_count
            },
            "arenas": {
                "total": arenas_count
            },
            "system": {
                "possible_combinations": "∞",
                "last_updated": "En temps réel"
            }
        }

    except Exception as e:
        logging.error(f"Erreur lors de la récupération des statistiques globales: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@router.get("/stats/players")
async def get_players_stats():
    """
    Récupère les statistiques détaillées des joueurs
    """
    try:
        general_stats = await players_controller.get_players_stats()
        by_country = await players_controller.get_players_count_by_country()
        by_level = await players_controller.get_players_count_by_level()

        # Supposons que tu as une méthode async `get_top_players`
        # Sinon commente ce bloc ou implémente la méthode
        if hasattr(players_controller, "get_top_players"):
            top_players = await players_controller.get_top_players(5)
        else:
            top_players = []

        return {
            "general": general_stats,
            "distribution": {
                "by_country": dict(list(by_country.items())[:15]),
                "by_level": by_level
            },
            "top_players": [
                {
                    "name": player.name,
                    "trophies": player.trophies,
                    "level": player.level,
                    "clan": player.clan,
                    "country": player.pays
                } for player in top_players
            ]
        }

    except Exception as e:
        logging.error(f"Erreur lors de la récupération des statistiques de joueurs: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@router.get("/stats/arenas")
async def get_arenas_stats():
    """
    Récupère les statistiques des arènes
    """
    try:
        total_arenas = await arenas_controller.get_arenas_count()
        all_arenas = await arenas_controller.get_all_arenas()

        if all_arenas:
            min_trophies = min(arena.min_trophies for arena in all_arenas)
            max_trophies = max(arena.min_trophies for arena in all_arenas)

            trophy_ranges = {
                "0-1000": len([a for a in all_arenas if a.min_trophies < 1000]),
                "1000-3000": len([a for a in all_arenas if 1000 <= a.min_trophies < 3000]),
                "3000-5000": len([a for a in all_arenas if 3000 <= a.min_trophies < 5000]),
                "5000+": len([a for a in all_arenas if a.min_trophies >= 5000])
            }
        else:
            min_trophies = max_trophies = 0
            trophy_ranges = {}

        return {
            "total_arenas": total_arenas,
            "trophy_range": {
                "min": min_trophies,
                "max": max_trophies
            },
            "distribution_by_trophy_range": trophy_ranges,
            "arenas_list": [
                {
                    "number": arena.number,
                    "name": arena.name,
                    "min_trophies": arena.min_trophies
                } for arena in all_arenas
            ]
        }

    except Exception as e:
        logging.error(f"Erreur lors de la récupération des statistiques d'arènes: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@router.get("/stats/cards")
async def get_cards_stats():
    """
    Récupère les statistiques détaillées des cartes
    """
    try:
        # À décommenter quand les méthodes existent
        # total_cards = await cards_controller.get_cards_count()
        # by_category = await cards_controller.get_cards_count_by_category()
        # by_rarity = await cards_controller.get_cards_count_by_rarity()
        # categories = await cards_controller.get_available_categories()
        # rarities = await cards_controller.get_available_rarities()
        # evolution_cards = len(await cards_controller.get_cards_with_evolution())

        return {
            # "total_cards": total_cards,
            # "cards_with_evolution": evolution_cards,
            # "available_categories": categories,
            # "available_rarities": rarities,
            # "distribution": {
            #     "by_category": by_category,
            #     "by_rarity": by_rarity
            # }
        }

    except Exception as e:
        logging.error(f"Erreur lors de la récupération des statistiques de cartes: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
