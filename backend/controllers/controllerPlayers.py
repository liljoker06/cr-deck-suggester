from typing import List
from database import get_database
from models.modelPlayer import Player

class PlayersController:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["players"]

    async def get_all_players(self, limit: int = 100) -> List[Player]:
        try:
            cursor = self.collection.find({}, {"_id": 0}).limit(limit).sort("trophies", -1)
            players_data = await cursor.to_list(length=None)
            return [Player(**player) for player in players_data]
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des joueurs : {e}")
            return []

    async def search_players_by_name(self, pattern: str, limit: int = 50) -> List[Player]:
        try:
            cursor = self.collection.find(
                {"name": {"$regex": pattern, "$options": "i"}},
                {"_id": 0}
            ).limit(limit).sort("trophies", -1)
            players_data = await cursor.to_list(length=None)
            return [Player(**player) for player in players_data]
        except Exception as e:
            print(f"❌ Erreur lors de la recherche de joueurs avec le motif '{pattern}' : {e}")
            return []

    async def get_players_count(self) -> int:
        try:
            return await self.collection.count_documents({})
        except Exception as e:
            print(f"❌ Erreur lors du comptage des joueurs : {e}")
            return 0

    async def get_players_stats(self) -> dict:
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
            cursor = self.collection.aggregate(pipeline)
            result = await cursor.to_list(length=1)
            if result:
                stats = result[0]
                stats.pop("_id", None)
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

    async def get_players_count_by_country(self) -> dict:
        try:
            pipeline = [
                {"$group": {"_id": "$pays", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 20}
            ]
            cursor = self.collection.aggregate(pipeline)
            result = await cursor.to_list(length=None)
            return {item["_id"]: item["count"] for item in result if item["_id"]}
        except Exception as e:
            print(f"❌ Erreur lors du comptage des joueurs par pays : {e}")
            return {}

    async def get_players_count_by_level(self) -> dict:
        try:
            pipeline = [
                {"$group": {"_id": "$level", "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}}
            ]
            cursor = self.collection.aggregate(pipeline)
            result = await cursor.to_list(length=None)
            return {item["_id"]: item["count"] for item in result if item["_id"]}
        except Exception as e:
            print(f"❌ Erreur lors du comptage des joueurs par niveau : {e}")
            return {}

    async def get_players_by_country(self, country: str, limit: int = 100) -> List[Player]:
        try:
            cursor = self.collection.find(
                {"pays": country}, {"_id": 0}
            ).limit(limit).sort("trophies", -1)
            players_data = await cursor.to_list(length=None)
            return [Player(**player) for player in players_data]
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des joueurs de '{country}' : {e}")
            return []

    async def get_players_by_clan(self, clan: str, limit: int = 100) -> List[Player]:
        try:
            cursor = self.collection.find(
                {"clan": clan}, {"_id": 0}
            ).limit(limit).sort("trophies", -1)
            players_data = await cursor.to_list(length=None)
            return [Player(**player) for player in players_data]
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des joueurs du clan '{clan}' : {e}")
            return []

    async def get_players_by_level(self, level: int, limit: int = 100) -> List[Player]:
        try:
            cursor = self.collection.find(
                {"level": level}, {"_id": 0}
            ).limit(limit).sort("trophies", -1)
            players_data = await cursor.to_list(length=None)
            return [Player(**player) for player in players_data]
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des joueurs de niveau {level} : {e}")
            return []

    async def get_players_by_trophy_range(self, min_trophies: int, max_trophies: int, limit: int = 100) -> List[Player]:
        try:
            cursor = self.collection.find(
                {"trophies": {"$gte": min_trophies, "$lte": max_trophies}}, {"_id": 0}
            ).limit(limit).sort("trophies", -1)
            players_data = await cursor.to_list(length=None)
            return [Player(**player) for player in players_data]
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des joueurs entre {min_trophies} et {max_trophies} trophées : {e}")
            return []
