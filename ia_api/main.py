from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import get_database
from routes.routeAnalysis import router as analysis_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_database()
    app.state.db = db
    print("✅ Connexion MongoDB prête.")
    yield
    print("🛑 Arrêt de l'app.")

app = FastAPI(lifespan=lifespan)

app.include_router(analysis_router, prefix="/api")
# include les autres routers aussi

@app.get("/")
def root():
    return {"message": "ClashDeck API opérationnelle 🚀"}


# @app.on_event("startup")
# async def on_startup():
#     print("🔁 Chargement initial des données depuis le backend...")
#     await fetch_matches_and_cards()

#     async def update_loop():
#         while True:
#             print("🔄 Mise à jour automatique des données...")
#             await fetch_matches_and_cards()
#             await asyncio.sleep(2 * 60 * 60)  # toutes les 2 heures

#     # Lancer en tâche de fond
#     asyncio.create_task(update_loop())
