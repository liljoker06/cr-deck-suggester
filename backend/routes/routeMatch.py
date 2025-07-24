# routes/routeMatch.py
from fastapi import APIRouter
from controllers.controllerMatch import get_all_matches

router = APIRouter()

@router.get("/matches")
def fetch_all_matches():
    return get_all_matches()
