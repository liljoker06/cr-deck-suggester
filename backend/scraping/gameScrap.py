import requests
import json
import os

#Crée le dossier "replays" si besoin
os.makedirs("replays", exist_ok=True)

# URL de l'API RoyaleAPI à rendre dynamique avec le tag du joueur etc 
url = "https://royaleapi.com/data/replay?tag=00GPQ2VCUR0L&team_tags=U2LYQJQVY&opponent_tags=P8LRG9UP&team_crowns=1&opponent_crowns=0&referrer_path=https://royaleapi.com/player/U2LYQJQVY/battles"

# Headers copiés depuis le navigateur f12 network (adapte les cookies si besoin)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Referer": "https://royaleapi.com/player/U2LYQJQVY/battles",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "fr-FR,fr;q=0.7",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": "__royaleapi_session_v2=76fea327c6924735a3ef820da0b03869; NB_SRVID=srv743175; cf_clearance=5p0fAonKaYipdqZEnqm3dVXv7.dOO7IABADmB9tGYAE-1753340508-1.2.1.1-X37ax5Yhj9z3JtEOpTpRU9SRyv2EA7kkucdhrTC.2UB7Wrx07ICIL2DzSh.rhn2w3pNED1.dE9AGMV.T95qBby6zllRfqYjrWKXdBXj6WmUcxfZiippxZ9YpBsjCTJloVVnhu4isQx9ct_fyxDNlgqG6oQ5KEU2_Hk1lOnc_F47azZNGMrss8qkjOO_wdlmQ9q.aSdplSzroMEJaHNzc6nPgKR72t1EawOkniglqO4U"
}

# Requête
response = requests.get(url, headers=headers)

# Analyse de la réponse
if response.status_code == 200:
    try:
        data = response.json()
        with open("replays/replay_00GPQ2VCUR0L.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("JSON sauvegardé dans replays/replay_00GPQ2VCUR0L.json")
    except Exception as e:
        print("Erreur de parsing JSON :", e)
else:
    print(f"Erreur HTTP {response.status_code}")
