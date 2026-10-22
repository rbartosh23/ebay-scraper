import argparse
import json
import time
import requests
from bs4 import BeautifulSoup
 
 
def price_to_cents(text):
    """Turn text like '$54.99' into the integer 5499. Return None if no price."""
    for word in text.split():
        if "$" in word:
            cleaned = word.replace("$", "").replace(",", "").replace("+", "")
            cleaned = cleaned.strip(".")
 
            parts = cleaned.split(".")
            dollars = int(parts[0])
            if len(parts) > 1:
                cents = int(parts[1].ljust(2, "0")[:2])
            else:
                cents = 0
 
            return dollars * 100 + cents
 
    return None
 
 
def shipping_to_cents(text):
    """'Free shipping' -> 0, '+$4.25 shipping' -> 425."""
    if "free" in text.lower():
        return 0
    return price_to_cents(text)
 
 
def get_items_sold(text):
    """'1,234 sold' -> 1234. Return None if there is no number."""
    for word in text.split():
        cleaned = word.replace(",", "").replace("+", "")
        if cleaned.isdigit():
            return int(cleaned)
    return None
 
 
def get_text(card, selector):
    """Find one thing inside a listing and return its text.
    If it is not there, return None."""
    tag = card.select_one(selector)
    if tag is None:
        return None
    return tag.get_text(strip=True)
 
 
def extract_items(html):
    """Take the HTML of one page and return a list of dictionaries."""
    soup = BeautifulSoup(html, "html.parser")
    items = []
 
    cards = soup.select("li.s-item")
 
    for card in cards:
        name_text = get_text(card, "div.s-item__title")
        price_text = get_text(card, "span.s-item__price")
        status_text = get_text(card, "span.SECONDARY_INFO")
        shipping_text = get_text(card, "span.s-item__shipping")
        returns_text = get_text(card, "span.s-item__free-returns")
        sold_text = get_text(card, "span.s-item__hotness")
 
        item = {
            "name": name_text,
            "price": None,
            "status": status_text,
            "shipping": None,
            "free_returns": None,
            "items_sold": None,
        }
 
        if price_text is not None:
            item["price"] = price_to_cents(price_text)
 
        if shipping_text is not None:
            item["shipping"] = shipping_to_cents(shipping_text)
 
        if returns_text is not None:
            item["free_returns"] = "free returns" in returns_text.lower()
 
        if sold_text is not None:
            item["items_sold"] = get_items_sold(sold_text)
 
        items.append(item)
 
    return items
 
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--search")
    parser.add_argument("--pages-dir")
    args = parser.parse_args()
 
    all_items = []
 
    for page_number in range(1, 11):
 
        if args.pages_dir is not None:
            filename = args.pages_dir + "/page-" + str(page_number) + ".html"
            with open(filename, encoding="utf-8") as file:
                html = file.read()
        else:
            response = requests.get(
                "https://www.ebay.com/sch/i.html",
                params={"_nkw": args.search, "_pgn": page_number},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10,
            )
            response.raise_for_status()
            html = response.text
            time.sleep(1)
 
        page_items = extract_items(html)
        all_items.extend(page_items)
 
    output_name = args.search + ".json"
    with open(output_name, "w", encoding="utf-8") as file:
        json.dump(all_items, file, indent=2)
 
    print("Saved", len(all_items), "items to", output_name)
 
 
if __name__ == "__main__":
    main()