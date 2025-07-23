import asyncio
from playwright.async_api import async_playwright
import json
import os

async def run():
    # 🧭 Chemins à adapter
    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    user_data_dir = r"C:\Users\joker\AppData\Local\BraveSoftware\Brave-Browser\User Data"

    async with async_playwright() as p:
        # 💡 Lance Brave AVEC ton profil utilisateur
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            executable_path=brave_path,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        page = await browser.new_page()

        async def handle_response(response):
            if "/data/replay" in response.url and response.status == 200:
                try:
                    data = await response.json()
                    print("✅ JSON intercepté !")
                    with open("replay_data.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                except Exception as e:
                    print("⚠️ Erreur lors de la lecture du JSON :", e)

        page.on("response", handle_response)

        print("🟢 Brave est lancé AVEC ton compte connecté.")
        print("➡️ Va sur une page de replay pour déclencher le JSON.")
        await page.goto("https://royaleapi.com/player/U2LYQJQVY/battles")
        await page.wait_for_timeout(120000)  # 2 min pour interagir

        await browser.close()

asyncio.run(run())
