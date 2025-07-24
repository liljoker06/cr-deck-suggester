import os
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs





### CONVERTISSEUR DE TEMPS EN MINUTES ET SECONDES 
def convert_tick_to_time(tick):
    seconds = tick / 60
    minutes = int(seconds // 60)
    remaining = int(seconds % 60)
    return f"{minutes}:{remaining:02}"





RAW_REPLAY_PATH = "replays/replay_00GPQ2VCUR0L.json"
OUTPUT_DIR = "games_parsed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(RAW_REPLAY_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Vérifie si HTML présent
if not data.get("success") or not data.get("html"):
    print("❌ Erreur : fichier JSON invalide ou sans contenu HTML.")
    exit()

soup = BeautifulSoup(data["html"], "html.parser")

# === Extraction HTML ===

# TAG DU MATCH
match_id = os.path.basename(RAW_REPLAY_PATH).split("_")[-1].replace(".json", "")
print(f"🔍 Analyse du match {match_id}...")

# SCORE
link = soup.select_one("a.item")
if not link:
    print("❌ Erreur : lien de score introuvable.")
    exit()
href = link.get("href", "")
query = parse_qs(urlparse(href).query)

team_tag = query.get("team_tags", ["unknown"])[0]
opponent_tag = query.get("opponent_tags", ["unknown"])[0]
score_team = int(query.get("team_crowns", [0])[0])
score_opponent = int(query.get("opponent_crowns", [0])[0])
winner = team_tag if score_team > score_opponent else opponent_tag

print(f"Équipe : {team_tag} ({score_team} couronnes)")
print(f"Adversaire : {opponent_tag} ({score_opponent} couronnes)")
print(f'score_team: {score_team}, score_opponent: {score_opponent}')
print(f"Gagnant : {winner}")
print(f"Score : {score_team} - {score_opponent} ({winner})")

# DECKS
# Récupère tous les blocs de deck (team + opponent)
players_columns = soup.select("div.column.pad0topbottom")

# Vérifie qu'on a bien deux colonnes (team et opponent)
if len(players_columns) >= 2:
    team_cards = [img["data-card"] for img in players_columns[0].select("img.replay_card")]
    opponent_cards = [img["data-card"] for img in players_columns[1].select("img.replay_card")]

    print("🔵 Deck team :", team_cards)
    print("🔴 Deck opponent :", opponent_cards)
else:
    print("❌ Impossible de trouver les decks.")


# TEMPS TOTAL DE LA GAME 
replay_time_div = soup.select_one("div.replay_time")
if replay_time_div:
    all_markers = replay_time_div.select("div.marker")
    if all_markers:
        end_time = all_markers[-1].get_text(strip=True)
        print("Durée totale de la partie :", end_time)
    else:
        print("Aucun marqueur de temps trouvé.")
else:
    print("Bloc 'replay_time' introuvable.")


# DETAILS GAME  

# Récupère les actions de la team bleue
team_cards_div = soup.select_one("div.replay_team.team")
if team_cards_div:
    cards = team_cards_div.select("img.replay_card")
    team_actions = []

    for card in cards:
        name = card.get("data-card")
        time = card.get("data-t")
        if name and time:
            team_actions.append((name, int(time)))

    print("Cartes jouées par la team bleue :")
    for name, t in team_actions:
        print(f"- {name} à ({convert_tick_to_time(t)})")
else:
    print("Bloc 'replay_team team' introuvable.")

# Récupère les actions de l'adversaire
opponent_cards_div = soup.select_one("div.replay_team.opponent")
if opponent_cards_div:
    cards = opponent_cards_div.select("img.replay_card")
    opponent_actions = []

    for card in cards:
        name = card.get("data-card")
        time = card.get("data-t")
        if name and time:
            opponent_actions.append((name, int(time)))

    print("Cartes jouées par l'adversaire :")
    for name, t in opponent_actions:
        print(f"- {name} à ({convert_tick_to_time(t)})")
else:
    print("Bloc 'replay_team opponent' introuvable.")



# STRUCTURED OUTPUT

# Sauvegarde


print(f"Match {match_id} analysé avec succès.")
