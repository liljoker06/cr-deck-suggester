from database import get_database

def get_all_cards():
    db = get_database()
    cards = list(db.cards.find({}, {"_id": 0}))  # exclude MongoDB _id
    return cards