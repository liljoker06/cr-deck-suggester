import os
import sys
import glob
import json
import asyncio
import time
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_database

def convert_tick_to_time(tick):
    seconds = tick / 60
    minutes = int(seconds // 60)
    remaining = int(seconds % 60)
    return f"{minutes}:{remaining:02}"

async def process_replay(path, matches_collection):
    match_id = os.path.basename(path).split("_")[-1].replace(".json", "")

    # Vérifie si déjà en base
    if await matches_collection.find_one({"match_id": match_id}):
        print(f"⏭Match {match_id} déjà analysé. Ignoré.")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data.get("success") or not data.get("html"):
            print(f"❌ JSON invalide ou sans HTML pour {match_id}.")
            return

        soup = BeautifulSoup(data["html"], "html.parser")

        link = soup.select_one("a.item")
        if not link:
            print(f"❌ Lien de score introuvable pour {match_id}")
            return

        href = link.get("href", "")
        query = parse_qs(urlparse(href).query)
        team_tag = query.get("team_tags", ["unknown"])[0]
        opponent_tag = query.get("opponent_tags", ["unknown"])[0]
        score_team = int(query.get("team_crowns", [0])[0])
        score_opponent = int(query.get("opponent_crowns", [0])[0])
        winner = team_tag if score_team > score_opponent else opponent_tag

        players_columns = soup.select("div.column.pad0topbottom")
        team_cards = [img["data-card"] for img in players_columns[0].select("img.replay_card")] if len(players_columns) >= 2 else []
        opponent_cards = [img["data-card"] for img in players_columns[1].select("img.replay_card")] if len(players_columns) >= 2 else []

        replay_time_div = soup.select_one("div.replay_time")
        end_time = None
        if replay_time_div:
            markers = replay_time_div.select("div.marker")
            if markers:
                end_time = markers[-1].get_text(strip=True)

        def extract_actions(selector, marker_map):
            div = soup.select_one(selector)
            actions = []
            if div:
                for card in div.select("img.replay_card"):
                    name = card.get("data-card")
                    time = card.get("data-t")
                    if name and time:
                        t = int(time)
                        actions.append({
                            "card": name,
                            "time": t,
                            "time_human": convert_tick_to_time(t),
                            "position": marker_map.get((name, t))
                        })
            return actions

        map_div = soup.select_one("div.map_stats_container div.map div.replay_map_container div.replay_map div.markers")
        blue_positions = {
            (m.get("data-c"), int(m.get("data-t"))): {"x": m.get("data-x"), "y": m.get("data-y")}
            for m in map_div.select("div.blue")
        } if map_div else {}

        red_positions = {
            (m.get("data-c"), int(m.get("data-t"))): {"x": m.get("data-x"), "y": m.get("data-y")}
            for m in map_div.select("div.red")
        } if map_div else {}

        team_actions = extract_actions("div.replay_team.team", blue_positions)
        opponent_actions = extract_actions("div.replay_team.opponent", red_positions)

        output_data = {
            "match_id": match_id,
            "team": {
                "tag": team_tag,
                "score": score_team,
                "deck": team_cards,
                "actions": team_actions
            },
            "opponent": {
                "tag": opponent_tag,
                "score": score_opponent,
                "deck": opponent_cards,
                "actions": opponent_actions
            },
            "winner": winner,
            "duration": end_time,
            "processed_at": datetime.utcnow()
        }

        await matches_collection.insert_one(output_data)
        print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Match {match_id} inséré en base.")
        
    except Exception as e:
        print(f"❌ Erreur lors du traitement de {match_id}: {str(e)}")

async def watch_folder():
    """Surveille en continu le dossier pour de nouveaux fichiers"""
    db = get_database()
    matches = db["matches"]
    
    processed_files = set()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Démarrage de la surveillance...")
    
    while True:
        try:
            # Scan des fichiers JSON
            json_files = set(glob.glob("replays/replay_*.json"))
            new_files = json_files - processed_files
            
            if new_files:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {len(new_files)} nouveau(x) fichier(s) détecté(s)")
                
                for file in new_files:
                    await process_replay(file, matches)
                    processed_files.add(file)
                    
            else:
                # Afficher un message toutes les 60 secondes pour confirmer que le script tourne
                current_time = datetime.now()
                if current_time.second == 0:  # Toutes les minutes pile
                    print(f"[{current_time.strftime('%H:%M:%S')}] En attente de nouveaux fichiers...")
            
            # Attendre 5 secondes avant la prochaine vérification
            await asyncio.sleep(5)
            
        except KeyboardInterrupt:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Arrêt demandé par l'utilisateur")
            break
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Erreur dans la surveillance: {str(e)}")
            await asyncio.sleep(10)  # Attendre plus longtemps en cas d'erreur

async def main():
    """Point d'entrée principal"""
    await watch_folder()

if __name__ == "__main__":
    asyncio.run(main())