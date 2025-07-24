from fastapi import FastAPI

from controllers.controllerData import run_update
from controllers.controllerGamedata import fetch_and_store_battles_for_all_players


router = FastAPI()


# Met à jour les données des arènes et cartes en les scrapant depuis le Wiki.
@router.get("/update-data")
async def update_data():
    await run_update()
    return {"message": "Données mises à jour avec succès."}


# Récupère et stocke les batailles pour tous les joueurs, avec une pause aléatoire entre chaque joueur.
@router.get("/fetch-battles")
async def fetch_battles():
    fetch_and_store_battles_for_all_players(limit=2)
    return {"message": "Batailles récupérées et stockées avec succès."}


