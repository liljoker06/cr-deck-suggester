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


@app.get("/")
def root():
    return {"message": "ClashDeck API opérationnelle 🚀"}

