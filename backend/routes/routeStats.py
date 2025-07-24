from fastapi import APIRouter, HTTPException
from controllers.controllerArenas import ArenasController
from controllers.controllerCard import get_all_cards
from controllers.controllerPlayers import PlayersController
from database import get_database
import logging

router = APIRouter()

# Initialisation des controllers
arenas_controller = ArenasController()
cards_controller = get_all_cards()
players_controller = PlayersController()

@router.get("/stats")
async def get_global_stats():
    """
    Récupère toutes les statistiques globales de l'application
    """
    try:
        # Utilisation des controllers pour récupérer les statistiques
        cards_count = cards_controller
        total_cards = len(cards_count)
        arenas_count = arenas_controller.get_arenas_count()
        players_count = players_controller.get_players_count()
        
        # Statistiques détaillées des cartes
        # cards_by_category = cards_controller.get_cards_count_by_category()
        # cards_by_rarity = cards_controller.get_cards_count_by_rarity()
        
        # Statistiques des joueurs
        players_stats = players_controller.get_players_stats()
        players_by_country = players_controller.get_players_count_by_country()
        players_by_level = players_controller.get_players_count_by_level()
        
        # Compter les decks (via base directe car pas de controller dédié)
        db = get_database()
        decks_count = db["decks"].count_documents({})
        
        return {
            "totals": {
                "cards": total_cards,
                "arenas": arenas_count,
                "players": players_count,
                "decks": decks_count
            },
            "cards": {
                # "by_category": cards_by_category,
                # "by_rarity": cards_by_rarity,
                # "total": cards_count
            },
            "players": {
                "general_stats": players_stats,
                "by_country": dict(list(players_by_country.items())[:10]),  # Top 10 pays
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
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@router.get("/stats/cards")
async def get_cards_stats():
    """
    Récupère les statistiques détaillées des cartes
    """
    try:
        # total_cards = cards_controller.get_cards_count()
        # by_category = cards_controller.get_cards_count_by_category()
        # by_rarity = cards_controller.get_cards_count_by_rarity()
        # categories = cards_controller.get_available_categories()
        # rarities = cards_controller.get_available_rarities()
        # evolution_cards = len(cards_controller.get_cards_with_evolution())
        
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

@router.get("/stats/players")
async def get_players_stats():
    """
    Récupère les statistiques détaillées des joueurs
    """
    try:
        general_stats = players_controller.get_players_stats()
        by_country = players_controller.get_players_count_by_country()
        by_level = players_controller.get_players_count_by_level()
        
        # Top 5 joueurs
        top_players = players_controller.get_top_players(5)
        
        return {
            "general": general_stats,
            "distribution": {
                "by_country": dict(list(by_country.items())[:15]),  # Top 15 pays
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
        total_arenas = arenas_controller.get_arenas_count()
        all_arenas = arenas_controller.get_all_arenas()
        
        # Calcul des statistiques des arènes
        if all_arenas:
            min_trophies = min(arena.min_trophies for arena in all_arenas)
            max_trophies = max(arena.min_trophies for arena in all_arenas)
            
            # Distribution par paliers de trophées
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
