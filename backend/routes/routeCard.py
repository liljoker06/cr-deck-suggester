from fastapi import APIRouter
from controllers.controllerCard import get_all_cards

router = APIRouter()

@router.get("/cards")
def fetch_cards():
    return get_all_cards()