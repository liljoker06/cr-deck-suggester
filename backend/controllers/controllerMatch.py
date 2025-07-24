from database import get_database

def get_all_matches():
    db = get_database()
    matches = db["matches"]
    return list(matches.find({}, {"_id": 0}))  # on exclut le champ MongoDB _id
