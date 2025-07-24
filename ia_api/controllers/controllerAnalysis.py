from collections import Counter, defaultdict
from services.cache import cached_matches, cached_cards


def analyze_deck(deck, matches, cards_list):
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

    # Prépare dict cartes pour accès rapide
    cards_dict = {}
    for card in cards_list:
        name = card["name"].lower()
        cards_dict[name] = {
            "elixir_cost": parse_elixir_cost(card.get("elixir_cost", "0")),
            "dps": parse_float_or_zero(card.get("dps", "0")),
            "hitpoints": parse_int_with_commas(card.get("hitpoints", "0")),
            "range": card.get("range", "N/A"),
            "description": card.get("description", ""),
            "category": card.get("category", ""),
            "image": card.get("image", ""),
        }

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

    # Exemple de win_rate_estimation simple (à remplacer par modèle ML)
    win_rate_estimation = 0  # placeholder
    matches_found = len(matches)

    # Analyse cartes avec insight simple
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
        "analysis": "Analyse sommaire réalisée avec données disponibles.",
        "cards_info": [cards_dict.get(c.lower(), {}) for c in deck],
        "top_positioned_cards": [],  # À développer si besoin
    }

    return result


def extract_float(value):
    """Extrait un float en supprimant les virgules, parenthèses, etc."""
    if isinstance(value, (int, float)):
        return float(value)
    if not value:
        return 0.0
    value = str(value).split(" ")[0].replace(",", "").replace("(", "").replace(")", "")
    try:
        return float(value)
    except ValueError:
        return 0.0
    
def parse_float_or_zero(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0
