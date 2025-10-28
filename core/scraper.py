import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://keysoutline.com"
BOT_URL = "t.me/kunafa_vpn_bot"  


async def fetch_html(url):

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def get_keys_by_country(limit=16):

    url = f"{BASE_URL}"
    html = await fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    keys_by_country = {}
    cards = soup.find_all("div", class_="card", limit=limit)

    for card in cards:
        country = card.find("h3").get_text(strip=True)
        country=country.replace("United Arab Emirates", "UAE")
        country=country.replace("United States", "US")
        country=country.replace("United Kingdom", "UK")
        

        link = card.find("a")["href"]
        key_url = f"{BASE_URL}{link}"


        key_html = await fetch_html(key_url)
        key_soup = BeautifulSoup(key_html, "html.parser")
        key = key_soup.find("textarea", {"id": "accessKey"}).get_text(strip=True)


        if key.startswith("ss://"):

            key = key.replace("%20KeysOutline.com%20/", "")
            key = key.replace("t.me/KeysOutlineFree", BOT_URL)  


            if country not in keys_by_country:
                keys_by_country[country] = []
            keys_by_country[country].append(key)

    return keys_by_country