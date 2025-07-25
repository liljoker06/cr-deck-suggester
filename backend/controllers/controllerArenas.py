from typing import List
from database import get_database
from models.modelArena import Arena

class ArenasController:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["arenas"]

    async def get_all_arenas(self) -> List[Arena]:
        """
        Récupère toutes les arènes de la base de données (async)
        """
        try:
            cursor = self.collection.find({}, {"_id": 0}).sort("number", 1)
            arenas_data = await cursor.to_list(length=None)
            return [Arena(**arena) for arena in arenas_data]
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des arènes : {e}")
            return []

    async def get_arenas_count(self) -> int:
        """
        Récupère le nombre total d'arènes (async)
        """
        try:
            return await self.collection.count_documents({})
        except Exception as e:
            print(f"❌ Erreur lors du comptage des arènes : {e}")
            return 0

    async def get_arenas_by_name_pattern(self, pattern: str) -> List[Arena]:
        """
        Recherche des arènes par nom (insensible à la casse, async)
        """
        try:
            regex_pattern = {"$regex": pattern, "$options": "i"}
            cursor = self.collection.find({"name": regex_pattern}, {"_id": 0}).sort("number", 1)
            arenas_data = await cursor.to_list(length=None)
            return [Arena(**arena) for arena in arenas_data]
        except Exception as e:
            print(f"❌ Erreur lors de la recherche d'arènes avec '{pattern}' : {e}")
            return []
