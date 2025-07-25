from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import get_database
from routes.routeAnalysis import router as analysis_router
from fastapi.middleware.cors import CORSMiddleware




@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_database()
    app.state.db = db
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

app.include_router(analysis_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "ClashDeck API opérationnelle 🚀"}

