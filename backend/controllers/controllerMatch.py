from database import get_database

async def get_all_matches():
    db = get_database()
    cursor = db.matches.find({}, {"_id": 0})
    matches = await cursor.to_list(length=None)
    return matches
