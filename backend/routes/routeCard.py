from fastapi import APIRouter
from controllers.controllerCard import get_all_cards, get_card_by_name

router = APIRouter()

@router.get("/cards")
async def fetch_cards():
    return await get_all_cards()

@router.get("/cards/{name}")
async def fetch_card_by_name(name: str):
    return await get_card_by_name(name)
