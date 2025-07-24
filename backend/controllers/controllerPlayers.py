from typing import List, Optional
from database import get_database
from models.modelPlayer import Player

class PlayersController:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["players"]

    def get_all_players(self, limit: int = 100) -> List[Player]:
        """
        Récupère tous les joueurs de la base de données (avec limite pour éviter la surcharge)
        """
        try:
            players_data = list(self.collection.find({}, {"_id": 0}).limit(limit).sort("trophies", -1))
            players = [Player(**player) for player in players_data]
            return players
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des joueurs : {e}")
            return []



    def search_players_by_name(self, pattern: str, limit: int = 50) -> List[Player]:
        """
        Recherche des joueurs dont le nom contient le motif donné (insensible à la casse)
        """
        try:
            players_data = list(self.collection.find(
                {"name": {"$regex": pattern, "$options": "i"}}, 
                {"_id": 0}
            ).limit(limit).sort("trophies", -1))
            
            players = [Player(**player) for player in players_data]
            return players
        except Exception as e:
            print(f"❌ Erreur lors de la recherche de joueurs avec le motif '{pattern}' : {e}")
            return []
# 
    def get_players_count(self) -> int:
        """
        Récupère le nombre total de joueurs
        """
        try:
            return self.collection.count_documents({})
        except Exception as e:
            print(f"❌ Erreur lors du comptage des joueurs : {e}")
            return 0

    def get_players_stats(self) -> dict:
        """
        Récupère des statistiques générales sur les joueurs
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total_players": {"$sum": 1},
                        "avg_trophies": {"$avg": "$trophies"},
                        "avg_level": {"$avg": "$level"},
                        "max_trophies": {"$max": "$trophies"},
                        "min_trophies": {"$min": "$trophies"},
                        "players_with_clan": {
                            "$sum": {
                                "$cond": [
                                    {"$and": [
                                        {"$ne": ["$clan", ""]},
                                        {"$ne": ["$clan", None]},
                                        {"$ne": ["$clan", "Sans clan"]}
                                    ]}, 1, 0
                                ]
                            }
                        }
                    }
                }
            ]
            
            result = list(self.collection.aggregate(pipeline))
            if result:
                stats = result[0]
                stats.pop("_id", None)  # Supprimer l'_id
                return stats
            else:
                return {
                    "total_players": 0,
                    "avg_trophies": 0,
                    "avg_level": 0,
                    "max_trophies": 0,
                    "min_trophies": 0,
                    "players_with_clan": 0
                }
        except Exception as e:
            print(f"❌ Erreur lors du calcul des statistiques des joueurs : {e}")
            return {}

    def get_players_count_by_country(self) -> dict:
        """
        Récupère le nombre de joueurs par pays
        """
        try:
            pipeline = [
                {"$group": {"_id": "$pays", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 20}  # Top 20 pays
            ]
            
            result = list(self.collection.aggregate(pipeline))
            return {item["_id"]: item["count"] for item in result if item["_id"]}
        except Exception as e:
            print(f"❌ Erreur lors du comptage des joueurs par pays : {e}")
            return {}

    def get_players_count_by_level(self) -> dict:
        """
        Récupère le nombre de joueurs par niveau
        """
        try:
            pipeline = [
                {"$group": {"_id": "$level", "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}}
            ]
            
            result = list(self.collection.aggregate(pipeline))
            return {item["_id"]: item["count"] for item in result if item["_id"]}
        except Exception as e:
            print(f"❌ Erreur lors du comptage des joueurs par niveau : {e}")
            return {}

    def get_players_by_country(self, country: str, limit: int = 100) -> List[Player]:
        """
        Récupère les joueurs d'un pays donné
        """
        try:
            players_data = list(self.collection.find(
                {"pays": country}, 
                {"_id": 0}
            ).limit(limit).sort("trophies", -1))
            
            players = [Player(**player) for player in players_data]
            return players
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des joueurs de '{country}' : {e}")
            return []

    def get_players_by_clan(self, clan: str, limit: int = 100) -> List[Player]:
        """
        Récupère les joueurs d'un clan donné
        """
        try:
            players_data = list(self.collection.find(
                {"clan": clan}, 
                {"_id": 0}
            ).limit(limit).sort("trophies", -1))
            
            players = [Player(**player) for player in players_data]
            return players
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des joueurs du clan '{clan}' : {e}")
            return []

    def get_players_by_level(self, level: int, limit: int = 100) -> List[Player]:
        """
        Récupère les joueurs d'un niveau donné
        """
        try:
            players_data = list(self.collection.find(
                {"level": level}, 
                {"_id": 0}
            ).limit(limit).sort("trophies", -1))
            
            players = [Player(**player) for player in players_data]
            return players
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des joueurs de niveau {level} : {e}")
            return []

    def get_players_by_trophy_range(self, min_trophies: int, max_trophies: int, limit: int = 100) -> List[Player]:
        """
        Récupère les joueurs dans une plage de trophées
        """
        try:
            players_data = list(self.collection.find(
                {"trophies": {"$gte": min_trophies, "$lte": max_trophies}}, 
                {"_id": 0}
            ).limit(limit).sort("trophies", -1))
            
            players = [Player(**player) for player in players_data]
            return players
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des joueurs entre {min_trophies} et {max_trophies} trophées : {e}")
            return []

