from fastapi import FastAPI, APIRouter, HTTPException
from typing import List, Optional
from database import get_database
import logging

router = FastAPI()

@router.get("/decks")
async def get_all_decks(
    arena_number: Optional[int] = None,
    limit: Optional[int] = None
):
    """
    Récupère tous les decks avec filtres optionnels
    """
    try:
        db = get_database()
        collection = db["decks"]
        
        # Construction du filtre
        filter_query = {}
        if arena_number:
            filter_query["arena_number"] = arena_number
        
        # Exécution de la requête
        cursor = collection.find(filter_query)
        if limit:
            cursor = cursor.limit(limit)
            
        decks = list(cursor)
        
        # Conversion des ObjectId en string
        for deck in decks:
            if "_id" in deck:
                del deck["_id"]
        
        return decks
        
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des decks: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@router.get("/decks/{deck_id}")
async def get_deck_by_id(deck_id: str):
    """
    Récupère un deck spécifique par son ID
    """
    try:
        db = get_database()
        collection = db["decks"]
        
        deck = collection.find_one({"_id": deck_id})
        
        if not deck:
            raise HTTPException(status_code=404, detail="Deck non trouvé")
        
        # Suppression de l'ObjectId
        if "_id" in deck:
            del deck["_id"]
            
        return deck
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du deck {deck_id}: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@router.get("/decks/stats/count")
async def get_decks_count():
    """
    Récupère le nombre total de decks
    """
    try:
        db = get_database()
        collection = db["decks"]
        
        total_decks = collection.count_documents({})
        
        return {
            "total_decks": total_decks
        }
        
    except Exception as e:
        logging.error(f"Erreur lors du calcul des statistiques de decks: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
