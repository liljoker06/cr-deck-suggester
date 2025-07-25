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

Voici les statistiques d’un deck :
{formatted_stats}

Analyse :
- Les points forts du deck
- Les faiblesses possibles
- Des suggestions de cartes à remplacer pour améliorer les performances

Ta réponse doit être claire et concise, destinée à un joueur débutant ou intermédiaire.
"""

    response = await query_llm(prompt)
    return {"summary": response}
