# main.py
from tabulate import tabulate

from db import init_db, add_product, list_products, save_price, deactivate_product
from scraper import get_flipkart_price
from notifier import send_whatsapp_alert


def prompt_add_product():
    print("\n=== Add New Product to Track ===")
    name = input("Product name: ").strip()
    url = input("Flipkart product URL: ").strip()
    target_price_str = input("Target price (INR): ").strip()

    try:
        target_price = float(target_price_str)
    except ValueError:
        print("❌ Invalid target price.")
        return

    if not name or not url:
        print("❌ Name and URL are required.")
        return

    add_product(name, url, target_price)
    print("✅ Product added for tracking!\n")


def show_products():
    print("\n=== Tracked Products ===")
    rows = list_products(active_only=False)
    if not rows:
        print("(No products tracked yet)\n")
        return

    # rows: id, name, url, target_price, last_price, currency, active
    table = []
    for r in rows:
        pid, name, url, target, last, curr, active = r
        status = "Active" if active == 1 else "Inactive"
        table.append([pid, name, target, last, curr, status])

    print(tabulate(table, headers=["ID", "Name", "Target", "Last Price", "Currency", "Status"], tablefmt="github"))
    print()


def check_price_for_product():
    print("\n=== Check Price for Single Product ===")
    pid_str = input("Enter Product ID: ").strip()
    if not pid_str.isdigit():
        print("❌ Invalid Product ID.")
        return
    pid = int(pid_str)

    # find product
    rows = list_products(active_only=False)
    product = None
    for r in rows:
        if r[0] == pid:
            product = r
            break

    if not product:
        print("❌ Product ID not found.")
        return

    pid, name, url, target_price, last_price, currency, active = product
    print(f"Fetching current price for: {name}")
    current_price = get_flipkart_price(url)

    if current_price is None:
        print("❌ Could not fetch price. Check URL or scraper selectors.")
        return

    print(f"Current price: {current_price} {currency}")
    save_price(pid, current_price, currency=currency)

    if current_price <= target_price:
        msg = (
            f"Price Drop Alert! 🎉\n"
            f"Product: {name}\n"
            f"Current price: {current_price} {currency}\n"
            f"Target price: {target_price} {currency}\n"
            f"URL: {url}"
        )
        print("✅ Current price is at or below target. Sending WhatsApp alert (if configured)...")
        send_whatsapp_alert(msg)
    else:
        diff = current_price - target_price
        print(f"ℹ️ Still {diff:.2f} {currency} above target price.")


def check_all_products():
    print("\n=== Check Prices for All Active Products ===")
    rows = list_products(active_only=True)
    if not rows:
        print("(No active products to check)\n")
        return

    for r in rows:
        pid, name, url, target_price, last_price, currency, active = r
        print(f"\n→ Checking: [{pid}] {name}")
        current_price = get_flipkart_price(url)

        if current_price is None:
            print("   ❌ Could not fetch price (selector/URL issue?)")
            continue

        print(f"   Current price: {current_price} {currency}")
        save_price(pid, current_price, currency=currency)

        if current_price <= target_price:
            msg = (
                f"Price Drop Alert! 🎉\n"
                f"Product: {name}\n"
                f"Current price: {current_price} {currency}\n"
                f"Target price: {target_price} {currency}\n"
                f"URL: {url}"
            )
            print("   ✅ Price is at/below target. Sending WhatsApp alert (if configured)...")
            send_whatsapp_alert(msg, delay_seconds=30)
        else:
            diff = current_price - target_price
            print(f"   ℹ️ Still {diff:.2f} {currency} above target price.")


def deactivate_menu():
    print("\n=== Deactivate Product ===")
    pid_str = input("Enter Product ID to deactivate: ").strip()
    if not pid_str.isdigit():
        print("❌ Invalid Product ID.")
        return
    pid = int(pid_str)
    deactivate_product(pid)
    print("✅ Product deactivated (if ID existed).\n")


def main_menu():
    init_db()
    while True:
        print("==== Flipkart Price Tracker (CLI) ====")
        print("1. Add new product to track")
        print("2. List all products")
        print("3. Check price for one product")
        print("4. Check prices for all active products")
        print("5. Deactivate a product")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            prompt_add_product()
        elif choice == "2":
            show_products()
        elif choice == "3":
            check_price_for_product()
        elif choice == "4":
            check_all_products()
        elif choice == "5":
            deactivate_menu()
        elif choice == "6":
            print("Bye! Happy tracking 👋")
            break
        else:
            print("❌ Invalid choice, try again.\n")


if __name__ == "__main__":
    main_menu()
