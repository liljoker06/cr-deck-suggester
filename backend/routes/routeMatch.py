from fastapi import APIRouter
from controllers.controllerMatch import get_all_matches

router = APIRouter()

@router.get("/matches")
async def fetch_all_matches():
    return await get_all_matches()
