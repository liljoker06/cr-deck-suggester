from database import get_database

async def get_all_cards():
    db = get_database()
    cursor = db.cards.find({}, {"_id": 0})
    cards = await cursor.to_list(length=None)
    return cards

async def get_card_by_name(name: str):
    db = get_database()
    card = await db.cards.find_one({"name": name}, {"_id": 0})
    return card if card else {}