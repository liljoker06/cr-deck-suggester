from typing import List, Optional
from database import get_database
from models.modelArena import Arena

class ArenasController:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["arenas"]

    def get_all_arenas(self) -> List[Arena]:
        """
        Récupère toutes les arènes de la base de données
        """
        try:
            arenas_data = list(self.collection.find({}, {"_id": 0}).sort("number", 1))
            arenas = [Arena(**arena) for arena in arenas_data]
            return arenas
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des arènes : {e}")
            return []
# 
    def get_arenas_count(self) -> int:
        """
        Récupère le nombre total d'arènes
        """
        try:
            return self.collection.count_documents({})
        except Exception as e:
            print(f"❌ Erreur lors du comptage des arènes : {e}")
            return 0

    def get_arenas_by_name_pattern(self, pattern: str) -> List[Arena]:
        """
        Recherche des arènes par nom (insensible à la casse)
        """
        try:
            regex_pattern = {"$regex": pattern, "$options": "i"}
            arenas_data = list(self.collection.find(
                {"name": regex_pattern}, 
                {"_id": 0}
            ).sort("number", 1))
            arenas = [Arena(**arena) for arena in arenas_data]
            return arenas
        except Exception as e:
            print(f"❌ Erreur lors de la recherche d'arènes avec '{pattern}' : {e}")
            return []


   
