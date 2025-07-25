from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List
from controllers.controllerAnalysis import analyze_deck
from services.ollama_service import query_llm
import json  

router = APIRouter()

class DeckRequest(BaseModel):
    deck: List[str]

@router.post("/analyze-deck")
async def analyze_deck_ai(data: DeckRequest, request: Request):
    db = request.app.state.db
    analysis = await analyze_deck(data.deck, db)
    if not analysis:
        return {"error": "Aucune donnée d'analyse trouvée pour ce deck."}
    
    print("Analyse du deck :", analysis)

    formatted_stats = json.dumps(analysis, indent=2, ensure_ascii=False)
    prompt = f"""
    Tu es un expert en stratégie Clash Royale.
    Voici un deck aléatoire composé de 8 cartes, et pour chacune, des statistiques issues de parties **gagnées par des joueurs du top 250 mondial** :{formatted_stats}

    Ces données contiennent  :
        - Le nom de la carte (en anglais)
        - Son coût en élixir
        - Sa fréquence d'apparition dans les matchs du top 250 (`presence_count`)
        - Sa position moyenne sur le terrain
        - Une carte souvent jouée après elle (`support_analysis`)

    Ta mission :
        1. Pour chaque carte, explique si elle est plutôt populaire ou peu utilisée chez les meilleurs joueurs, et ce que ses statistiques laissent deviner sur son rôle dans le deck.
        2. Ensuite, fais une **analyse stratégique du deck** :
        - Forces globales
        - Faiblesses potentielles
        - Idées de remplacements pour l’optimiser selon la méta actuelle

    Règles :
        - Réponds **en français**
        - Garde les **noms de cartes en anglais**
        - Bats-toi uniquement avec les stats (tu n’as pas de description complète)
        - Sois clair, stratégique, et concis (pas plus de 3 lignes par carte)

        Le but est d’aider un joueur intermédiaire à comprendre si ce deck est viable dans le contexte du top 250.
    """



    response = await query_llm(prompt)
    return {"summary": response}


@router.get("/test-ollama")
async def test_ollama():
    response = await query_llm("Parle-moi de Clash Royale.")
    return {"response": response}
