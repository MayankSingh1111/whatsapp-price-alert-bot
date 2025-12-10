# Flipkart Price Tracker + WhatsApp Alert Bot

A real-time automation tool built using Python that monitors prices of Flipkart products and sends WhatsApp alerts when the price drops below a target value.

---

## 🚀 Features

### Tracking & Automation
- Track any product from Flipkart using product URL
- Set your own **target price**
- Automatically check prices using:
  - Manual CLI command
  - Windows Task Scheduler (auto-run daily)

### Price Alerts & Data Storage
- WhatsApp notification when price drops below target
- Saves every price check to **SQLite database**
- Tracks product status (active / inactive)

### CLI Operations Supported
- Add new product to track
- List tracked products
- Check price for **one** product manually
- Check prices for **all** active products
- Deactivate products anytime

---

## 🛠 Tech Stack

| Module | Technology |
|--------|------------|
| Language | Python 3 |
| Web Scraping | Requests + BeautifulSoup |
| Database | SQLite3 |
| CLI Output | Tabulate |
| Notification | pywhatkit (WhatsApp Web API) |
| Automation | Windows Task Scheduler |

---

## 📂 Folder Structure

- price_tracker/
  - db.py → Database + price history functions  
  - scraper.py → Flipkart price fetching logic  
  - notifier.py → WhatsApp messaging automation  
  - main.py → CLI app for user actions  
  - auto_check.py → Script for daily auto price monitoring  

---

## ▶️ How To Run

### Install requirements
```bash
pip install requests beautifulsoup4 tabulate pywhatkit

```

### Run manually (CLI)

python main.py


- Menu options:
  - Add product
  - List products
  - Check price for one
  - Check prices for all
  - Deactivate
  - Exit

---

## ⚙️ Auto Price Check (Daily)

Use Windows Task Scheduler:

- Trigger: Daily (e.g., 9:00 AM)
- Action:
  - Program: `python`
  - Arguments: `auto_check.py`
  - Start in: project folder path

- Requirements:
  - Laptop ON
  - Logged into WhatsApp Web

---

## 🔐 WhatsApp Configuration

- Update your number in `notifier.py`
WHATSAPP_NUMBER = "+91XXXXXXXXXX"

- Login to **WhatsApp Web** in default browser

---

## 📊 Example Output

- === Auto Price Check Started ===
 - Checking: Trimer
 - Current Price: 899.0 INR
 - No alert needed.
- === Auto Price Check Ended ===



---

## 🌟 Future Enhancements

- Support Amazon India, Myntra, Meesho
- GUI Dashboard for product monitoring
- Email + Telegram alerts support
- Price trend graph visualization
- Cloud hosted deployment

---

## 👨‍💻 Author

- Name: **Mayank Singh**  
- Role: Python Developer | Automation Enthusiast  
- LinkedIn: https://www.linkedin.com/in/mayank-singh-0162a920a/
- GitHub: https://github.com/MayankSingh1111/  

---

### ⭐ If you like this project, please give it a Star on GitHub!
