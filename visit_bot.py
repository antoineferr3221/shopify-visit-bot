import asyncio
from playwright.async_api import async_playwright
import random
import time
from datetime import datetime

SHOP_URL = "https://ton-shop.myshopify.com"  # Remplace par ton lien Shopify

# Choisit un proxy aléatoire dans le fichier proxies.txt
def get_random_proxy():
    try:
        with open("proxies.txt", "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        return random.choice(proxies) if proxies else None
    except FileNotFoundError:
        return None

# Fonction de visite
async def visit_site():
    proxy = get_random_proxy()
    print(f"🌐 Proxy utilisé : {proxy if proxy else 'aucun (connexion directe)'}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            proxy={"server": f"http://{proxy}"} if proxy else None,
            slow_mo=80
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = await context.new_page()
        await page.goto(SHOP_URL, timeout=60000)

        # Simule du scroll
        for _ in range(random.randint(3, 6)):
            await page.mouse.wheel(0, random.randint(300, 800))
            await asyncio.sleep(random.uniform(0.5, 1.5))

        # Attend sur le site
        await asyncio.sleep(random.uniform(5.0, 10.0))
        await browser.close()

# Génère des délais répartis sur une heure
def get_delays_for_visits(visits_per_hour):
    return sorted([random.randint(0, 3600) for _ in range(visits_per_hour)])

# Boucle principale (24h/24)
async def main_loop():
    print("🚀 Bot Shopify lancé 24h/24")

    while True:
        visits_this_hour = random.randint(100, 200)
        now = datetime.now()
        print(f"\n🕘 {now.strftime('%H:%M:%S')} - {visits_this_hour} visites prévues cette heure")

        delays = get_delays_for_visits(visits_this_hour)
        start_time = time.time()

        for i, delay in enumerate(delays):
            sleep_duration = max(0, delay - (time.time() - start_time))
            if sleep_duration > 0:
                time.sleep(sleep_duration)

            print(f"👤 Visite {i+1}/{visits_this_hour} - {datetime.now().strftime('%H:%M:%S')}")
            try:
                await visit_site()
            except Exception as e:
                print(f"⚠️ Erreur lors de la visite : {e}")

if __name__ == "__main__":
    asyncio.run(main_loop())
