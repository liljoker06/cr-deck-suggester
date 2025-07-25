from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from math import sqrt
from motor.motor_asyncio import AsyncIOMotorDatabase

from controllers.controllerAnalysis import analyze_deck
from database import get_database

router = APIRouter()


# --- Modèle Pydantic ---
class DeckRequest(BaseModel):
    deck: List[str]


# --- Fonctions utilitaires ---
def normalize_card_name(name: str) -> str:
    return name.lower().replace("-", " ").strip()


def determine_playstyle(positions: List[dict]) -> str:
    offensive_count = 0
    for pos in positions:
        if pos["x"] is not None and pos["y"] is not None:
            distance = sqrt((16000 - pos["x"])**2 + (19000 - pos["y"])**2)
            if distance < 5000:
                offensive_count += 1
    ratio = offensive_count / len(positions) if positions else 0
    return "offensif" if ratio >= 0.5 else "défensif"


def describe_position(x: float, y: float) -> str:
    if x < 10000:
        horizontal = "à gauche"
    elif x > 22000:
        horizontal = "à droite"
    else:
        horizontal = "au centre"

    if y < 8000:
        vertical = "dans le fond de votre camp"
    elif y > 17000:
        vertical = "près du pont"
    else:
        vertical = "au milieu du terrain"

    return f"{horizontal}, {vertical}"


# --- Route principale ---
@router.post("/analyze-deck-route")
async def analyze_deck_route(data: DeckRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    deck = data.deck

    if len(deck) != 8:
        return {"error": "Le deck doit contenir exactement 8 cartes."}

    stats = await analyze_deck(deck, db)

    total_elixir = 0
    pos_list = []
    readable_cards = []
    popularite_cartes = []

    for card in stats:
        elixir_str = card["elixir_cost"]
        if isinstance(elixir_str, str) and "(" in elixir_str:
            elixir = int(elixir_str.split("(")[0].strip())
        else:
            try:
                elixir = int(elixir_str)
            except:
                elixir = 0
        total_elixir += elixir

        pos = card["average_position"]
        if pos["x"] and pos["y"]:
            pos_list.append(pos)
            position_desc = describe_position(pos["x"], pos["y"])
        else:
            position_desc = "Non déterminée"

        support = card["support_analysis"]
        support_desc = (
            f"{support['most_supported_card']} (souvent jouée juste après {card['name']}, {support['times_played_after']} fois)"
            if support else "Aucune donnée"
        )

        readable_cards.append({
            "nom": card["name"],
            "popularite": f"{card['presence_count']} apparitions dans les matchs du top 250" if card["presence_count"] > 0 else "Aucune apparition dans les matchs du top 250",
            "elixir": elixir_str,
            "position_moyenne": position_desc,
            "support": support_desc
        })

        # résumé lisible
        if card["presence_count"] > 0:
            popularite_cartes.append(
                f"✅ {card['name']} : utilisée {card['presence_count']} fois dans les matchs du top 250 mondial"
            )
        else:
            popularite_cartes.append(
                f"❌ {card['name']} : non utilisée dans les matchs du top 250 mondial"
            )

    playstyle = determine_playstyle(pos_list)
    avg_elixir = round(total_elixir / 8, 2)
    popularity = sum(c["presence_count"] for c in stats)
    popular_cards = [c["name"] for c in stats if c["presence_count"] >= 10]

    return {
        "summary": {
            "style_de_jeu": f"Ce deck a un style de jeu plutôt **{playstyle}**.",
            "elixir_moyen": f"Le coût moyen en élixir est de **{avg_elixir}**.",
            "popularite_globale": f"Les cartes du deck ont été jouées au total **{popularity} fois** par les joueurs du top 250.",
            "cartes_populaires": f"Cartes les plus utilisées (≥10 apparitions) : {', '.join(popular_cards) if popular_cards else 'Aucune'}",
            "popularite_cartes": popularite_cartes
        },
        "cartes_analysees": readable_cards
    }
