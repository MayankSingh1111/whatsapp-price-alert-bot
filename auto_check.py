# auto_check.py
from db import init_db, list_products, save_price
from scraper import get_flipkart_price
from notifier import send_whatsapp_alert


def run_automation():
    print("=== Auto Price Check Started ===")
    init_db()
    products = list_products(active_only=True)

    if not products:
        print("No active products.")
        return

    for p in products:
        pid, name, url, target, last, curr, active = p
        print(f"\nChecking: {name}")
        
        price = get_flipkart_price(url)
        if price is None:
            print("❌ Failed to fetch price.")
            continue

        print(f"Current Price: {price} {curr}")
        save_price(pid, price, curr)

        if price <= target:
            message = (
                f"Price Alert 🚀\n"
                f"{name}\nNow: {price} {curr}\nTarget: {target} {curr}\nURL: {url}"
            )
            print("Sending WhatsApp alert...")
            send_whatsapp_alert(message, delay_seconds=20)
        else:
            print("No alert needed.")

    print("\n=== Auto Price Check Ended ===")


if __name__ == "__main__":
    run_automation()
