from database import get_database

async def get_all_cards():
    db = get_database()
    cursor = db.cards.find({}, {"_id": 0})
    cards = await cursor.to_list(length=None)
    return cards
