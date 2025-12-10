# scraper.py
import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def extract_price_from_text(text: str):
    """Convert ₹23,999 to float 23999.0"""
    digits = re.sub(r"[^\d.]", "", text)
    try:
        return float(digits)
    except:
        return None


def get_flipkart_price(url: str):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print("[SCRAPER] Error fetching URL:", e)
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Try multiple selectors in order
    selectors = [
        "div._30jeq3._16Jk6d",      # primary price
        "div._25b18c span._30jeq3", # deal price
        ".Nx9bqj._4b5DiR",          # some products use this class
        ".UOcHJ0",                  # mobile/non-standard display
    ]

    for selector in selectors:
        el = soup.select_one(selector)
        if el and el.text.strip():
            price = extract_price_from_text(el.text.strip())
            if price:
                return price

    # Fallback: search any number starting with ₹
    text = soup.get_text()
    match = re.search(r"₹\s?([\d,]+)", text)
    if match:
        return extract_price_from_text(match.group())

    print("[SCRAPER] Could not detect price. HTML changed.")
    return None
