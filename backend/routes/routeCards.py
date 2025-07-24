from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
# from controllers.controllerCards import CardsController
# from models.modelCard import Card
import logging

router = FastAPI()
# cards_controller = CardsController()

# Routes temporaires sans contrôleur pour éviter les erreurs
@router.get("/cards")
async def get_all_cards():
    """
    Récupère toutes les cartes - route temporaire
    """
    return {"message": "Route cards temporairement désactivée"}

@router.get("/cards/stats/count")
async def get_cards_count():
    """
    Récupère le nombre total de cartes - route temporaire
    """
    return {
        "total_cards": 0,
        "by_category": {},
        "by_rarity": {}
    }

@router.get("/cards/{card_name}")
async def get_card_by_name(card_name: str):
    """
    Récupère une carte spécifique par son nom - route temporaire
    """
    return {"message": f"Route pour la carte {card_name} temporairement désactivée"}

# @router.get("/cards", response_model=List[Card])
# async def get_all_cards(
#     category: Optional[str] = Query(None, description="Filtrer par catégorie"),
#     rarity: Optional[str] = Query(None, description="Filtrer par rareté"),
#     elixir_cost: Optional[str] = Query(None, description="Filtrer par coût en élixir"),
#     limit: Optional[int] = Query(None, description="Limiter le nombre de résultats")
# ):
#     """
#     Récupère toutes les cartes avec filtres optionnels
#     """
#     try:
#         if category and rarity:
#             # Si les deux filtres sont présents, on récupère par catégorie puis on filtre par rareté
#             cards = cards_controller.get_cards_by_category(category)
#             cards = [card for card in cards if card.rarity and card.rarity.lower() == rarity.lower()]
#         elif category:
#             cards = cards_controller.get_cards_by_category(category)
#         elif rarity:
#             cards = cards_controller.get_cards_by_rarity(rarity)
#         elif elixir_cost:
#             cards = cards_controller.get_cards_by_elixir_cost(elixir_cost)
#         else:
#             cards = cards_controller.get_all_cards()
        
#         # Appliquer la limite si spécifiée
#         if limit:
#             cards = cards[:limit]
            
#         return cards
        
#     except Exception as e:
#         logging.error(f"Erreur lors de la récupération des cartes: {e}")
#         raise HTTPException(status_code=500, detail="Erreur serveur")

# @router.get("/cards/search", response_model=List[Card])
# async def search_cards_by_name(
#     pattern: str = Query(..., description="Motif de recherche pour le nom de la carte"),
#     limit: Optional[int] = Query(50, description="Limiter le nombre de résultats")
# ):
#     """
#     Recherche des cartes par nom (insensible à la casse)
#     """
#     try:
#         cards = cards_controller.search_cards_by_name(pattern)
        
#         if limit:
#             cards = cards[:limit]
            
#         return cards
        
#     except Exception as e:
#         logging.error(f"Erreur lors de la recherche de cartes avec '{pattern}': {e}")
#         raise HTTPException(status_code=500, detail="Erreur serveur")

# @router.get("/cards/category/{category}", response_model=List[Card])
# async def get_cards_by_category(category: str):
#     """
#     Récupère toutes les cartes d'une catégorie donnée
#     """
#     try:
#         cards = cards_controller.get_cards_by_category(category)
        
#         if not cards:
#             raise HTTPException(status_code=404, detail=f"Aucune carte trouvée pour la catégorie '{category}'")
            
#         return cards
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         logging.error(f"Erreur lors de la récupération des cartes de catégorie '{category}': {e}")
#         raise HTTPException(status_code=500, detail="Erreur serveur")

# @router.get("/cards/rarity/{rarity}", response_model=List[Card])
# async def get_cards_by_rarity(rarity: str):
#     """
#     Récupère toutes les cartes d'une rareté donnée
#     """
#     try:
#         cards = cards_controller.get_cards_by_rarity(rarity)
        
#         if not cards:
#             raise HTTPException(status_code=404, detail=f"Aucune carte trouvée pour la rareté '{rarity}'")
            
#         return cards
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         logging.error(f"Erreur lors de la récupération des cartes de rareté '{rarity}': {e}")
#         raise HTTPException(status_code=500, detail="Erreur serveur")

# @router.get("/cards/elixir/{elixir_cost}", response_model=List[Card])
# async def get_cards_by_elixir_cost(elixir_cost: str):
#     """
#     Récupère toutes les cartes avec un coût en élixir donné
#     """
#     try:
#         cards = cards_controller.get_cards_by_elixir_cost(elixir_cost)
        
#         if not cards:
#             raise HTTPException(status_code=404, detail=f"Aucune carte trouvée coûtant {elixir_cost} élixir")
            
#         return cards
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         logging.error(f"Erreur lors de la récupération des cartes coûtant {elixir_cost} élixir: {e}")
#         raise HTTPException(status_code=500, detail="Erreur serveur")

# @router.get("/cards/evolutions", response_model=List[Card])
# async def get_cards_with_evolution():
#     """
#     Récupère toutes les cartes qui ont une évolution disponible
#     """
#     try:
#         cards = cards_controller.get_cards_with_evolution()
#         return cards
        
#     except Exception as e:
#         logging.error(f"Erreur lors de la récupération des cartes avec évolution: {e}")
#         raise HTTPException(status_code=500, detail="Erreur serveur")

# @router.get("/cards/categories")
# async def get_available_categories():
#     """
#     Récupère la liste des catégories disponibles
#     """
#     try:
#         categories = cards_controller.get_available_categories()
#         return {"categories": categories}
        
#     except Exception as e:
#         logging.error(f"Erreur lors de la récupération des catégories: {e}")
#         raise HTTPException(status_code=500, detail="Erreur serveur")

# @router.get("/cards/rarities")
# async def get_available_rarities():
#     """
#     Récupère la liste des raretés disponibles
#     """
#     try:
#         rarities = cards_controller.get_available_rarities()
#         return {"rarities": rarities}
        
#     except Exception as e:
#         logging.error(f"Erreur lors de la récupération des raretés: {e}")
#         raise HTTPException(status_code=500, detail="Erreur serveur")

# @router.get("/cards/{card_name}", response_model=Card)
# async def get_card_by_name(card_name: str):
#     """
#     Récupère une carte spécifique par son nom
#     """
#     try:
#         card = cards_controller.get_card_by_name(card_name)
        
#         if not card:
#             raise HTTPException(status_code=404, detail="Carte non trouvée")
            
#         return card
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         logging.error(f"Erreur lors de la récupération de la carte {card_name}: {e}")
#         raise HTTPException(status_code=500, detail="Erreur serveur")

# @router.get("/cards/stats/count")
# async def get_cards_count():
#     """
#     Récupère le nombre total de cartes et statistiques détaillées
#     """
#     try:
#         total_cards = cards_controller.get_cards_count()
#         by_category = cards_controller.get_cards_count_by_category()
#         by_rarity = cards_controller.get_cards_count_by_rarity()
        
#         return {
#             "total_cards": total_cards,
#             "by_category": by_category,
#             "by_rarity": by_rarity
#         }
        
#     except Exception as e:
#         logging.error(f"Erreur lors du calcul des statistiques: {e}")
#         raise HTTPException(status_code=500, detail="Erreur serveur")
