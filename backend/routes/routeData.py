from fastapi import FastAPI

from controllers.controllerData import run_update



router = FastAPI()


# Met à jour les données des arènes et cartes en les scrapant depuis le Wiki.
@router.get("/update-data")
async def update_data():
    await run_update()
    return {"message": "Données mises à jour avec succès."}


