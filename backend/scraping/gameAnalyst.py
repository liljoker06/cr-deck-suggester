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
print(f"Gagnant : {winner}")
print(f"Score : {score_team} - {score_opponent} ({winner})")

# DECKS
players_columns = soup.select("div.column.pad0topbottom")

if len(players_columns) >= 2:
    team_cards = [img["data-card"] for img in players_columns[0].select("img.replay_card")]
    opponent_cards = [img["data-card"] for img in players_columns[1].select("img.replay_card")]

    print("🔵 Deck team :", team_cards)
    print("🔴 Deck opponent :", opponent_cards)
else:
    print("❌ Impossible de trouver les decks.")
    team_cards = []
    opponent_cards = []

# TEMPS TOTAL DE LA GAME 
end_time = None
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

# ACTIONS TEAM
team_actions = []
team_cards_div = soup.select_one("div.replay_team.team")
if team_cards_div:
    for card in team_cards_div.select("img.replay_card"):
        name = card.get("data-card")
        time = card.get("data-t")
        if name and time:
            t = int(time)
            team_actions.append((name, t))
    print("Cartes jouées par la team bleue :")
    for name, t in team_actions:
        print(f"- {name} à ({convert_tick_to_time(t)})")
else:
    print("Bloc 'replay_team team' introuvable.")

# ACTIONS OPPONENT
opponent_actions = []
opponent_cards_div = soup.select_one("div.replay_team.opponent")
if opponent_cards_div:
    for card in opponent_cards_div.select("img.replay_card"):
        name = card.get("data-card")
        time = card.get("data-t")
        if name and time:
            t = int(time)
            opponent_actions.append((name, t))
    print("Cartes jouées par l'adversaire :")
    for name, t in opponent_actions:
        print(f"- {name} à ({convert_tick_to_time(t)})")
else:
    print("Bloc 'replay_team opponent' introuvable.")

# POSITIONS
map_div = soup.select_one("div.map_stats_container div.map div.replay_map_container div.replay_map div.markers")
if map_div:
    blue_markers = map_div.select("div.blue")
    red_markers = map_div.select("div.red")

    # Dictionnaires positions (clé = (card, time))
    blue_positions_map = {
        (m.get("data-c"), int(m.get("data-t"))): {
            "x": m.get("data-x"),
            "y": m.get("data-y")
        } for m in blue_markers
    }
    red_positions_map = {
        (m.get("data-c"), int(m.get("data-t"))): {
            "x": m.get("data-x"),
            "y": m.get("data-y")
        } for m in red_markers
    }

    print("📍 Positions des cartes jouées :")
    print("🔵 Team bleue :")
    for key, pos in blue_positions_map.items():
        print(f"- {key[0]} à {key[1]} → (x: {pos['x']}, y: {pos['y']})")
    print("🔴 Team adverse :")
    for key, pos in red_positions_map.items():
        print(f"- {key[0]} à {key[1]} → (x: {pos['x']}, y: {pos['y']})")
else:
    print("❌ Bloc 'markers' introuvable dans replay_map.")
    blue_positions_map = {}
    red_positions_map = {}

# Fusion actions + positions + temps humain
team_actions_with_pos = []
for name, t in team_actions:
    pos = blue_positions_map.get((name, t))
    team_actions_with_pos.append({
        "card": name,
        "time": t,
        "time_human": convert_tick_to_time(t),
        "position": pos
    })

opponent_actions_with_pos = []
for name, t in opponent_actions:
    pos = red_positions_map.get((name, t))
    opponent_actions_with_pos.append({
        "card": name,
        "time": t,
        "time_human": convert_tick_to_time(t),
        "position": pos
    })

# STRUCTURED OUTPUT
output_data = {
    "match_id": match_id,
    "team": {
        "tag": team_tag,
        "score": score_team,
        "deck": team_cards,
        "actions": team_actions_with_pos
    },
    "opponent": {
        "tag": opponent_tag,
        "score": score_opponent,
        "deck": opponent_cards,
        "actions": opponent_actions_with_pos
    },
    "winner": winner,
    "duration": end_time
}

# Sauvegarde
output_path = os.path.join(OUTPUT_DIR, f"{match_id}.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"✅ Match analysé avec succès et sauvegardé dans '{output_path}'")
