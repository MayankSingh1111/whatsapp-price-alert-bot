# notifier.py
import datetime

try:
    import pywhatkit
    PYWHATKIT_AVAILABLE = True
except ImportError:
    PYWHATKIT_AVAILABLE = False
    print("[NOTIFIER] pywhatkit not installed. WhatsApp sending will be disabled.")


# Set your WhatsApp number here, including country code (e.g. +91xxxxxxxxxx)
WHATSAPP_NUMBER = "+917906558332"  # TODO: replace with your number


def send_whatsapp_alert(message: str, delay_seconds: int = 20):
    """
    Send a WhatsApp message using pywhatkit.
    Opens WhatsApp Web in browser, so make sure you are logged in.

    delay_seconds: how many seconds from now to schedule sending.
    """
    if not PYWHATKIT_AVAILABLE:
        print("[NOTIFIER] WhatsApp message not sent (pywhatkit missing). Message would be:")
        print(message)
        return

    if "XXXXXXXXXX" in WHATSAPP_NUMBER:
        print("[NOTIFIER] Please set WHATSAPP_NUMBER in notifier.py first.")
        print("Message that would be sent:")
        print(message)
        return

    now = datetime.datetime.now()
    send_time = now + datetime.timedelta(seconds=delay_seconds)

    hour = send_time.hour
    minute = send_time.minute

    try:
        print(f"[NOTIFIER] Scheduling WhatsApp message at {hour}:{minute:02d} ...")
        pywhatkit.sendwhatmsg(
            WHATSAPP_NUMBER,
            message,
            hour,
            minute,
            wait_time=20,  # seconds to wait after opening browser
            tab_close=True,
            close_time=3,
        )
        print("[NOTIFIER] WhatsApp message scheduled/sent.")
    except Exception as e:
        print("[NOTIFIER] Error sending WhatsApp message:", e)
        print("Message was:")
        print(message)
