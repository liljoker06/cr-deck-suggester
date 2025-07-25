import re
from math import sqrt
from collections import defaultdict
from motor.motor_asyncio import AsyncIOMotorDatabase

def normalize_card_name(name: str) -> str:
    return name.lower().replace("-", " ").strip()

async def analyze_deck(deck_names: list[str], db: AsyncIOMotorDatabase):
    normalized_deck = [normalize_card_name(name) for name in deck_names]
    card_stats = {name: {"count": 0, "positions": [], "supports": defaultdict(int)} for name in normalized_deck}

    async for match in db.matches.find():
        winner_tag = match.get("winner")
        if not winner_tag:
            continue

        for side in ["team", "opponent"]:
            player = match.get(side, {})
            if player.get("tag") != winner_tag:
                continue

            match_deck = [normalize_card_name(c) for c in player.get("deck", [])]
            actions = player.get("actions", [])

            for idx, action in enumerate(actions):
                current_card = normalize_card_name(action.get("card", ""))
                if current_card not in normalized_deck:
                    continue

                card_stats[current_card]["count"] += 1

                # Position moyenne
                pos = action.get("position", {})
                try:
                    x, y = float(pos.get("x", 0)), float(pos.get("y", 0))
                    if x and y:
                        card_stats[current_card]["positions"].append((x, y))
                except:
                    pass

                # Support analysis
                t1 = action.get("time", 0)
                for other in actions[idx+1:]:
                    t2 = other.get("time", 0)
                    if 0 < (t2 - t1) <= 2:
                        other_card = normalize_card_name(other.get("card", ""))
                        if other_card != current_card:
                            card_stats[current_card]["supports"][other_card] += 1
                    elif (t2 - t1) > 3:
                        break

    # Format des résultats
    results = []
    for card_name, data in card_stats.items():
        pos_list = data["positions"]
        avg_pos = {
            "x": round(sum(p[0] for p in pos_list) / len(pos_list), 2) if pos_list else None,
            "y": round(sum(p[1] for p in pos_list) / len(pos_list), 2) if pos_list else None,
        }

        # support_analysis
        if data["supports"]:
            top_support = max(data["supports"].items(), key=lambda i: i[1])
            support_analysis = {
                "most_supported_card": top_support[0],
                "times_played_after": top_support[1]
            }
        else:
            support_analysis = None

        # 💡 Récupérer le coût en élixir depuis la collection "cards"
        card_doc = await db.cards.find_one({"name": {"$regex": f"^{re.escape(card_name)}$", "$options": "i"}})
        elixir_cost = card_doc.get("elixir_cost") if card_doc else None

        results.append({
            "name": card_name,
            "presence_count": data["count"],
            "elixir_cost": elixir_cost,
            "average_position": avg_pos,
            "support_analysis": support_analysis
        })

    return results
