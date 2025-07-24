import requests, os, json, sys
from typing import List
from bs4 import BeautifulSoup
from database import get_database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.modelPlayer import Player

BASE_URL = "https://clashroyale.fandom.com"
PLAYERS_URL = "https://royaleapi.com/players/leaderboard/season/2025-06"
DEBUG_FILE = "debug_player.html"
OUTPUT_FILE = "players_data.json"
BACKEND_DIR = os.path.join(os.path.dirname(__file__), "..")

import re

def update_arenas(db):
    print("Mise à jour des arènes...")
    url = f"{BASE_URL}/wiki/Arenas"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    arena_collection = db["arenas"]
    tables = soup.find_all("table", {"class": "wikitable"})

    for table in tables:
        rows = table.find_all("tr")[1:]

        for row in rows:
            td = row.find("td", rowspan=True)
            if not td:
                continue

            
            a_tag = td.find("a", class_="image")
            if a_tag:
                image_url = a_tag.get("href")
                if image_url and not image_url.startswith("http"):
                    image_url = BASE_URL + image_url

            # Text brut
            raw_parts = [part for part in td.stripped_strings]
            if len(raw_parts) < 2:
                continue

            full_name = raw_parts[0] if "Arena" in raw_parts[0] else raw_parts[1]

            # Séparer "Goblin Stadium (Arena 1)"
            match = re.match(r"(.+?)\s+\(Arena\s+(\d+)\)", full_name)
            if not match:
                continue
            name, number = match.group(1).strip(), int(match.group(2))

            # Trophées : chercher le premier "xxx" ou "xxx+" ou "xxx-yyy"
            min_trophies = 0
            for part in raw_parts:
                match_troph = re.match(r"(\d+)", part)
                if match_troph:
                    min_trophies = int(match_troph.group(1))
                    break

            arena = {
                "number": number,
                "name": name,
                "image": image_url,
                "min_trophies": min_trophies
            }

            arena_collection.update_one(
                {"number": number},
                {"$set": arena},
                upsert=True
            )

    print("Arènes mises à jour.")



def get_card_images(card_name: str) -> dict:
    def fetch_image_from_url(url):
        try:
            res = requests.get(url)
            if res.status_code != 200:
                return None
            soup = BeautifulSoup(res.text, "html.parser")
            a_tag = soup.select_one('figure.pi-item.pi-image a.image-thumbnail')
            if a_tag and a_tag.get("href"):
                return a_tag["href"]
        except Exception as e:
            print(f"⚠️ Erreur récupération image depuis {url} : {e}")
        return None

    base_url = f"{BASE_URL}/wiki/{card_name.replace(' ', '_')}"
    evolution_url = f"{base_url}/Evolution"

    return {
        "base_image": fetch_image_from_url(base_url),
        "evolution_image": fetch_image_from_url(evolution_url)
    }


def update_cards(db):
    print("🔄 Mise à jour des cartes...")

    url = f"{BASE_URL}/wiki/Cards"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    card_collection = db["cards"]
    current_category = None
    content = soup.select("h2, h3, table.wikitable")

    # Mappage des en-têtes
    field_map = {
        "cost": "elixir_cost",
        "cost (ability)": "elixir_cost",
        "cost (+ability)": "elixir_cost",
        "hitpoints": "hitpoints",
        "hitpoints (+shield)": "hitpoints",
        "health": "hitpoints",
        "damage": "damage",
        "crown tower damage": "crown_tower_damage",
        "hit speed": "hit_speed",
        "hit speed (seconds)": "hit_speed",
        "damage per second": "dps",
        "special damage": "special_damage",
        "range": "range",
        "radius": "radius",
        "count": "count",
        "lifetime": "lifetime",
        "troop spawned": "troop_spawned",
        "spawn speed": "spawn_speed",
        "maximum spawned": "max_spawned",
        "rarity": "rarity",
        "type": "type"
    }

    def normalize(text):
        return text.strip().lower().replace("\xa0", " ")

    for element in content:
        if element.name in ["h2", "h3"]:
            headline = element.find("span", class_="mw-headline")
            if headline:
                current_category = headline.text.strip()

        elif element.name == "table":
            headers_raw = element.find_all("th")
            headers = [normalize(th.text) for th in headers_raw]
            rows = element.find_all("tr")[1:]

            for row in rows:
                cols = row.find_all("td")
                if not cols:
                    continue

                link_tag = row.find("a")
                if not link_tag or not link_tag.get("href"):
                    continue

                name = link_tag.text.strip()
                card_url = BASE_URL + link_tag["href"]

                # Charger la page individuelle
                try:
                    card_page = requests.get(card_url)
                    card_soup = BeautifulSoup(card_page.text, "html.parser")
                except Exception as e:
                    print(f"❌ Erreur chargement page {name} : {e}")
                    continue

                # Description
                description = ""
                quote_block = card_soup.select_one(".quote-block")
                if quote_block:
                    desc_p = quote_block.find_next("p")
                    if desc_p:
                        description = desc_p.text.strip()

                # Structure initiale
                card_data = {
                    "name": name,
                    "category": current_category,
                    "description": description
                }

                # Images
                image_url = get_card_images(name)

                card_data["image"] = image_url.get("base_image")
                if not card_data["image"]:
                    print(f"⚠️ Image non trouvée pour {name}, utilisation de l'URL de la carte.")
                    card_data["image"] = card_url

                card_data["evolution_image"] = image_url.get("evolution_image")
                if not card_data["evolution_image"]:
                    print(f"⚠️ Image d'évolution non trouvée pour {name}, aucune évolution associée.")

                # Extraction des colonnes
                for idx, header in enumerate(headers):
                    field = field_map.get(header)
                    if field and idx < len(cols):
                        value = cols[idx].text.strip()
                        if value:
                            card_data[field] = value

                # Insertion / update MongoDB
                card_collection.update_one(
                    {"name": name, "category": current_category},
                    {"$set": card_data},
                    upsert=True
                )
                print(f"✅ Carte mise à jour : {name} ({current_category})")

    print("📥 Mise à jour des évolutions...")

    # Table des évolutions (Cycles)
    evolution_table = soup.select_one("table.wikitable:has(th:contains('Cycles'))")
    if evolution_table:
        rows = evolution_table.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue

            name_tag = cols[0].find("a")
            if not name_tag:
                continue

            name = name_tag.text.strip()
            evolution_data = {
                "elixir_cost": cols[1].text.strip(),
                "cycles": cols[2].text.strip(),
                "overall_cost": cols[3].text.strip(),
                "stat_boost": cols[4].text.strip().replace("\n", " ")
            }

            result = card_collection.update_one(
                {"name": name},
                {"$set": {"evolution": evolution_data}}
            )
            if result.matched_count:
                print(f"🧬 Évolution ajoutée à {name}")
            else:
                print(f"⚠️ Évolution non associée (carte non trouvée) : {name}")

    print("✅ Mise à jour terminée pour toutes les cartes et évolutions.")

def save_html_file(content, filename):
    filepath = os.path.join(BACKEND_DIR, filename)
    if not os.path.exists(filepath):
        with open(filepath, "wb") as f:
            f.write(content)

def extract_json_from_html(html_content):
    start = html_content.find("initRoster(")
    if start == -1:
        return None
    
    end = html_content.find(");", start)
    if end == -1:
        return None
    
    bloc = html_content[start:end]
    array_match = re.search(r'\[\s*(\{[\s\S]*?\})\s*(,\s*\{[\s\S]*?\}\s*)*\]', bloc)
    
    if not array_match:
        return None
    
    try:
        data = json.loads(array_match.group(0))
        output_path = os.path.join(BACKEND_DIR, OUTPUT_FILE)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return data
    except:
        return None

def scrape_players():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    try:
        response = requests.get(PLAYERS_URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        save_html_file(response.content, DEBUG_FILE)
        
        json_data = extract_json_from_html(response.text)
        if json_data:
            print(f"✅ {len(json_data)} joueurs extraits du JSON")


    except requests.RequestException as e:
        print(f"❌ Erreur lors de la requête : {e}")
        return None

            
def get_data_json():
    output_path = os.path.join(BACKEND_DIR, OUTPUT_FILE)
    if not os.path.exists(output_path):
        print(f"❌ Le fichier {OUTPUT_FILE} n'existe pas.")
        return None
    
    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data

def parse_players_from_json(data: List[dict]) -> List[Player]:
    players = []

    for item in data:
        try:
            player = Player(
                name=item.get("name", ""),
                player_tag=item.get("tag", ""),
                level=item.get("expLevel", 0),
                trophies=item.get("trophies", 0),
                clan=item.get("clan", {}).get("name", "Sans clan") if not item.get("not_in_clan", False) else "Sans clan",
                badge_clan=item.get("clan", {}).get("badge", {}).get("name", "") if not item.get("not_in_clan", False) else "",
                pays=item.get("country_name", "Inconnu")
            )
            players.append(player)
        except Exception as e:
            print(f"Erreur lors de la création d'un joueur : {e}")
            continue

    return players

def insert_players(db, data):

    player_collection = db["players"]

    players = parse_players_from_json(data)

    for player in players:
        # On vérifie si le joueur existe déjà via son tag
        exists = player_collection.find_one({"player_tag": player.player_tag})
        if exists:
            print(f"⚠️ Joueur {player.name} déjà présent. Ignoré.")
            continue

        
        player_dict = {
            "name": player.name,
            "player_tag": player.player_tag,
            "level": player.level,
            "trophies": player.trophies,
            "clan": player.clan,
            "badge_clan": player.badge_clan,
            "pays": player.pays
        }

        player_collection.update_one(
            {"player_tag": player.player_tag},
            {"$set": player_dict},
            upsert=True
        )

    print(f"✅ {len(players)} joueurs insérés avec succès.")



def run_update():
    db = get_database()
    update_arenas(db)
    update_cards(db)
    scrape_players()
    data = get_data_json()
    if data:
        insert_players(db, data)
    print("Mise à jour terminée.")

