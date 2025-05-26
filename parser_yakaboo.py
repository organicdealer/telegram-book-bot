import requests
from bs4 import BeautifulSoup
import json
import os

CATEGORIES = {
    "Бізнес": "https://www.yakaboo.ua/ua/knigi/business-money-economy.html?dir=desc&order=discount&p={}",
    "Саморозвиток": "https://www.yakaboo.ua/ua/knigi/samorazvitie-motivacija.html?dir=desc&order=discount&p={}"
}

SENT_FILE = "sent_books.json"

def load_sent_ids():
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_sent_ids(sent_ids):
    with open(SENT_FILE, "w") as f:
        json.dump(list(sent_ids), f)

def get_discounts():
    sent_ids = load_sent_ids()
    new_sent_ids = set()
    books = []

    for name, url_template in CATEGORIES.items():
        page = 1

        while True:
            url = url_template.format(page)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.select("li.item.product.product-item")

            if not items:
                break

            for item in items:
                title_tag = item.select_one("a.product-item-link")
                if not title_tag:
                    continue

                title = title_tag.get_text(strip=True)
                link = title_tag["href"]
                book_id = link.split("/")[-1].split(".")[0]

                if book_id in sent_ids:
                    continue

                price_old = item.select_one("span.old-price")
                price_new = item.select_one("span.price")
                if not price_old or not price_new:
                    continue

                books.append({
                    "title": f"{title} ({name})",
                    "price": price_new.get_text(strip=True),
                    "link": link
                })
                new_sent_ids.add(book_id)

            page += 1

    save_sent_ids(sent_ids.union(new_sent_ids))
    return books
