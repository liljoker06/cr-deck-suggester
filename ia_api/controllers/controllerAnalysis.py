from database import db
cards_collection = db.cards
matches_collection = db.matches


def parse_elixir_cost(cost_str):
    try:
        return float(cost_str.split()[0])
    except Exception:
        return 0.0

def parse_int_with_commas(s):
    try:
        return int(s.replace(",", ""))
    except Exception:
        return 0

def parse_float_or_zero(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

async def analyze_deck(deck: list[str], db) -> dict:
    # 1) Récupérer les cartes dans MongoDB
    query = {
        "$or": [{"name": {"$regex": f"^{name}$", "$options": "i"}} for name in deck]
    }
    cards_cursor = db.cards.find(query)
    cards_list = await cards_cursor.to_list(length=None)

    print(f"Cartes trouvées dans la base de données : {len(cards_list)}")
    print(f"Détails des cartes : {cards_list}")

    # Préparer dict cartes pour accès rapide
    cards_dict = {}
    for card in cards_list:
        # Parsing simple des valeurs numériques
        def parse_float_or_zero(value):
            try:
                return float(str(value).split()[0].replace(",", ""))
            except:
                return 0.0

        def parse_int_or_zero(value):
            try:
                return int(str(value).replace(",", ""))
            except:
                return 0

        name = card["name"].lower()
        cards_dict[name] = {
            "elixir_cost": parse_float_or_zero(card.get("elixir_cost", 0)),
            "dps": parse_float_or_zero(card.get("dps", 0)),
            "hitpoints": parse_int_or_zero(card.get("hitpoints", 0)),
            "range": card.get("range", "N/A"),
            "description": card.get("description", ""),
            "category": card.get("category", ""),
            "image": card.get("image", ""),
        }

    # 2) Récupérer les matchs dans MongoDB (optionnel: filtrer par deck si tu veux)
    matches_cursor = db.matches.find()  # tu peux filtrer si besoin
    matches = await matches_cursor.to_list(length=100)  # limite 100 pour la perf

    # Calcul stats globales deck
    total_elixir = 0.0
    total_dps = 0.0
    total_hp = 0
    for card_name in deck:
        c = cards_dict.get(card_name.lower())
        if c:
            total_elixir += c["elixir_cost"]
            total_dps += c["dps"]
            total_hp += c["hitpoints"]
    count = len(deck) if deck else 1
    avg_elixir = total_elixir / count

    # Exemple de win_rate_estimation simple (à améliorer)
    win_rate_estimation = 0
    matches_found = len(matches)

    # Analyse cartes
    cards_analysis = []
    for card_name in deck:
        c = cards_dict.get(card_name.lower())
        if c:
            insight = ""
            if c["elixir_cost"] > 5:
                insight = "Carte coûteuse, attention à la gestion de l'élixir."
            elif c["dps"] > 100:
                insight = "Carte à fort DPS, bonne capacité offensive."
            else:
                insight = "Carte équilibrée ou soutien."
            cards_analysis.append({
                "name": card_name,
                "elixir": c["elixir_cost"],
                "dps": c["dps"],
                "hitpoints": c["hitpoints"],
                "range": c["range"],
                "description": c["description"],
                "insight": insight,
            })
        else:
            cards_analysis.append({
                "name": card_name,
                "elixir": 0,
                "dps": 0,
                "hitpoints": 0,
                "range": "N/A",
                "description": "",
                "insight": "Carte inconnue dans la base de données.",
            })

    # Position moyenne des cartes dans les actions des matchs (team seulement)
    positions = []
    for match in matches:
        for action in match.get("team", {}).get("actions", []):
            pos = action.get("position")
            if pos and pos.get("x") != "None" and pos.get("y") != "None":
                try:
                    x = int(pos["x"])
                    y = int(pos["y"])
                    positions.append((x, y))
                except:
                    pass

    if positions:
        avg_x = sum(x for x, y in positions) / len(positions)
        avg_y = sum(y for x, y in positions) / len(positions)
        positioning_summary = f"Position moyenne des cartes jouées : x={avg_x:.1f}, y={avg_y:.1f}."
    else:
        positioning_summary = "Pas de données de positionnement valides."

    result = {
        "deck": deck,
        "win_rate_estimation": win_rate_estimation,
        "matches_found": matches_found,
        "global_stats": {
            "average_elixir": avg_elixir,
            "total_dps": total_dps,
            "total_hitpoints": total_hp,
        },
        "positioning_insights": [positioning_summary],
        "cards_analysis": cards_analysis,
        "positioning_summary": positioning_summary,
        "analysis": "Analyse sommaire réalisée avec données MongoDB en temps réel.",
        "cards_info": [cards_dict.get(c.lower(), {}) for c in deck],
        "top_positioned_cards": [],  # À développer si besoin
    }

    return result