import httpx
from services.cache import cached_matches, cached_cards

BACKEND_URL = "http://localhost:8000/api"

async def fetch_matches_and_cards():
    global cached_matches, cached_cards
    async with httpx.AsyncClient() as client:
        matches_resp = await client.get(f"{BACKEND_URL}/matches")
        cards_resp = await client.get(f"{BACKEND_URL}/cards")

    cached_matches.clear()
    cached_matches.extend(matches_resp.json())

    cached_cards.clear()
    cached_cards.extend(cards_resp.json())

    print(f'{len(cached_matches)} matchs et {len(cached_cards)} cartes récupérés depuis le backend.')
    # on affiche les match format json
    # print(f"Matchs récupérés : {(cached_matches)}")
    print(f"Cartes récupérées : {(cached_cards)}")
    print("✅ Données mises en cache avec succès.")
