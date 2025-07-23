import requests
import json
import os

#Crée le dossier "replays" si besoin
os.makedirs("replays", exist_ok=True)

# URL de l'API RoyaleAPI
url = "https://royaleapi.com/data/replay?tag=00GPQ2VCUR0L&team_tags=U2LYQJQVY&opponent_tags=P8LRG9UP&team_crowns=1&opponent_crowns=0&referrer_path=https://royaleapi.com/player/U2LYQJQVY/battles"

# Headers copiés depuis le navigateur f12 network (adapte les cookies si besoin)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Referer": "https://royaleapi.com/player/U2LYQJQVY/battles",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "fr-FR,fr;q=0.7",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": "__royaleapi_session_v2=f042666c90364d2984f951a8112ad809; NB_SRVID=srv2086659299; cf_clearance=pd.uBDkQ5c8.4A2uEXOX9Ak9lO8LYlEssy_T26UjZag-1753309437-1.2.1.1-CCuu4wnJhYJmGlR.UvgmSSjAqgdZwvjVZEfUnr.pCn0qKBxevu1uuNFytRG7iXTCeisuWHtWeg4ftHkX.ij4Q4SN8EmGd.IhomFmD1OEwKn2WQZJX1h_ibJGVkZ7p8dquOazVrtOHpoFkJPpxyXSHTuH35BrtkXpX7SEjra1bhLv1d_Ry7lH4YKYarQhARsheL0WBLJTcn3zHUFbwoEZcOiZb5xs_19hSZqYx7DO.oE"
}

# 📥 Requête
response = requests.get(url, headers=headers)

# 📤 Analyse de la réponse
if response.status_code == 200:
    try:
        data = response.json()
        with open("replays/replay_00GPQ2VCUR0L.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("✅ JSON sauvegardé dans replays/replay_00GPQ2VCUR0L.json")
    except Exception as e:
        print("⚠️ Erreur de parsing JSON :", e)
else:
    print(f"❌ Erreur HTTP {response.status_code}")
