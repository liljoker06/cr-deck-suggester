from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import get_database
from routes.routeData import router as update_router
from routes.routeArenas import router as arenas_router
from routes.routePlayers import router as players_controller
from routes.routeStats import router as stats_router
from routes.routeCards import router as cards_router
from routes.routeDecks import router as decks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_database()
    print("✅ Connexion MongoDB prête.")
    yield
    print("🛑 Arrêt de l'app.")

app = FastAPI(lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(update_router.router, prefix="/api")
app.mount("/api/cards", cards_router)
app.mount("/api/decks", decks_router)  
app.mount("/api/data", update_router)
app.include_router(arenas_router, prefix="/api")
app.include_router(players_controller, prefix="/api")
app.include_router(stats_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "ClashDeck API opérationnelle 🚀"}
