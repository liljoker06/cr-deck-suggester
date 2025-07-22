import requests
from bs4 import BeautifulSoup
from database import get_database

BASE_URL = "https://clashroyale.fandom.com"

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

            # Image
            img_tag = None
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



def update_cards(db):
    print("🔄 Mise à jour des cartes...")

    url = f"{BASE_URL}/wiki/Cards"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    card_collection = db["cards"]

    current_category = None
    content = soup.select("h2, h3, table.wikitable")

    for element in content:
        if element.name in ["h2", "h3"]:
            headline = element.find("span", class_="mw-headline")
            if headline:
                current_category = headline.text.strip()

        elif element.name == "table":
            rows = element.find_all("tr")[1:]  # Ignorer l'en-tête

            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 9:
                    continue

                link_tag = cols[0].find("a")
                if not link_tag or not link_tag.get("href"):
                    continue

                name = link_tag.get("title").strip()
                card_url = BASE_URL + link_tag["href"]

                # Page individuelle de la carte
                card_page = requests.get(card_url)
                card_soup = BeautifulSoup(card_page.text, "html.parser")

                # Description
                description = ""
                quote_block = card_soup.select_one(".quote-block")
                if quote_block:
                    desc_p = quote_block.find_next("p")
                    if desc_p:
                        description = desc_p.text.strip()

                # Image haute qualité
                image_url = None
                image_link = card_soup.select_one(".image.image-thumbnail a.image")
                if image_link and image_link.get("href"):
                    image_url = "https:" + image_link["href"]

                card_data = {
                    "name": name,
                    "category": current_category,
                    "elixir_cost": cols[1].text.strip(),
                    "hitpoints": cols[2].text.strip(),
                    "damage": cols[3].text.strip(),
                    "hit_speed": cols[4].text.strip(),
                    "dps": cols[5].text.strip(),
                    "special_damage": cols[6].text.strip(),
                    "range": cols[7].text.strip(),
                    "count": cols[8].text.strip(),
                    "description": description,
                    "image": image_url
                }

                card_collection.update_one(
                    {"name": name},
                    {"$set": card_data},
                    upsert=True
                )
                print(f"✅ Carte mise à jour : {name} ({current_category})")

    print("✅ Toutes les cartes ont été mises à jour.")

def run_update():
    db = get_database()
    update_arenas(db)
    update_cards(db)
    print("Mise à jour terminée.")

