from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from controllers.controllerArenas import ArenasController
from models.modelArena import Arena
import logging

router = APIRouter()
arenas_controller = ArenasController()

@router.get("/arenas", response_model=List[Arena])
async def get_all_arenas():
    """
    Récupère toutes les arènes
    """
    try:
        arenas = arenas_controller.get_all_arenas()
        return arenas
        
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des arènes: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@router.get("/arenas/search", response_model=List[Arena])
async def search_arenas_by_name(
    pattern: str = Query(..., description="Motif de recherche pour le nom de l'arène")
):
    """
    Recherche des arènes par nom (insensible à la casse)
    """
    try:
        arenas = arenas_controller.get_arenas_by_name_pattern(pattern)
        return arenas
        
    except Exception as e:
        logging.error(f"Erreur lors de la recherche d'arènes avec '{pattern}': {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
