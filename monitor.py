import os
import json
import requests
import ssl
import socket
from datetime import datetime

# List of websites to check
URLS = [
    "url_1",
    "url_2",
    "url_3"
]

# Status file
STATUS_FILE = "website_status.json"

# Google Chat Webhook URL (Hardcoded here for direct use)
WEBHOOK_URL = "<WEBHOOK_URL>"

# Load or initialize website status
if os.path.exists(STATUS_FILE):
    try:
        with open(STATUS_FILE, "r") as f:
            website_status = json.load(f)
    except json.JSONDecodeError:
        website_status = {url: {"down_count": 0, "time_ranges": []} for url in URLS}
else:
    website_status = {url: {"down_count": 0, "time_ranges": []} for url in URLS}

# Send alert to Google Chat
def send_google_chat_message(message):
    if not WEBHOOK_URL:
        print("⚠ GOOGLE_CHAT_WEBHOOK_URL is missing. Skipping alert.")
        return
    
    payload = {"text": message}
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})
        if response.status_code != 200:
            print(f"⚠ Failed to send Google Chat alert (Status: {response.status_code})")
    except Exception as e:
        print(f"⚠ Exception while sending Google Chat alert: {e}")

# Check website uptime
def check_website(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        print(f"[✔] {url} is UP (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"[❌] {url} is DOWN! ({e})")
        message = f"⚠ ALERT: {url} is DOWN! ({e})"
        send_google_chat_message(message)

        # Track downtime details
        if url in website_status:
            website_status[url]["down_count"] += 1
            website_status[url]["time_ranges"].append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            website_status[url] = {"down_count": 1, "time_ranges": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]}

# Check SSL certificate expiry
def check_ssl_expiry(url):
    try:
        hostname = url.replace("https://", "").split("/")[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        if not cert:
            print(f"[❌] {url} SSL Certificate retrieval FAILED!")
            send_google_chat_message(f"⚠ ALERT: Could not retrieve SSL certificate for {url}.")
            return

        expiry_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y GMT")
        days_left = (expiry_date - datetime.utcnow()).days

        if days_left < 15:
            print(f"[❌] {url} SSL Certificate is EXPIRING SOON (Expires in {days_left} days)")
            send_google_chat_message(f"⚠ ALERT: {url} SSL Certificate expires in {days_left} days!")
        else:
            print(f"[✔] {url} SSL Certificate is valid (Expires in {days_left} days)")
    except Exception as e:
        print(f"[❌] {url} SSL Certificate Check FAILED ({e})")

# Save website status to file
def save_website_status():
    with open(STATUS_FILE, "w") as f:
        json.dump(website_status, f, indent=4)

# Main script
if __name__ == "__main__":
    for url in URLS:
        check_website(url)
        check_ssl_expiry(url)
        print("-" * 80)

    save_website_status()
