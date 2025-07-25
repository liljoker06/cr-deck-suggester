from fastapi import APIRouter
from controllers.controllerCard import get_all_cards

router = APIRouter()

@router.get("/cards")
async def fetch_cards():
    return await get_all_cards()
