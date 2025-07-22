from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import get_database
from routes.routeData import router as update_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_database()
    print("✅ Connexion MongoDB prête.")
    yield
    print("🛑 Arrêt de l'app.")

app = FastAPI(lifespan=lifespan)


app.include_router(update_router.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "ClashDeck API opérationnelle 🚀"}
