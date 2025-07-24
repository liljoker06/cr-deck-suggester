from fastapi import FastAPI
from routes.routeAnalysis import router as analysis_router
from services.fetch_data import fetch_matches_and_cards
import asyncio

app = FastAPI(title="ClashDeck IA API 🤖")

app.include_router(analysis_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API IA 🤖"}

@app.on_event("startup")
async def on_startup():
    print("🔁 Chargement initial des données depuis le backend...")
    await fetch_matches_and_cards()

    async def update_loop():
        while True:
            print("🔄 Mise à jour automatique des données...")
            await fetch_matches_and_cards()
            await asyncio.sleep(2 * 60 * 60)  # toutes les 2 heures

    # Lancer en tâche de fond
    asyncio.create_task(update_loop())
