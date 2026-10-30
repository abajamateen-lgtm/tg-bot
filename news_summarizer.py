import os
import sys
import requests
import feedparser

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("Error: Missing Telegram credentials!")
    sys.exit(1)

FEEDS = [
    "https://cointelegraph.com/rss/tag/airdrop",
    "https://decrypt.co/feed"
]

KEYWORDS = ["mainnet", "snapshot", "airdrop", "claim", "testnet", "tge"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram dispatch error: {e}")

matches = []
headers = {'User-Agent': 'Mozilla/5.0'}

for feed_url in FEEDS:
    try:
        response = requests.get(feed_url, headers=headers, timeout=10)
        feed = feedparser.parse(response.content)
        for entry in feed.entries[:10]:
            title = entry.title
            link = entry.link
            if any(keyword in title.lower() for keyword in KEYWORDS):
                matches.append(f"• [{title}]({link})")
    except Exception as e:
        print(f"Failed to fetch {feed_url}: {e}")

if matches:
    summary = "🚨 *Airdrop & Snapshot News Digest* 🚨\n\n" + "\n".join(matches)
    send_telegram(summary)
    print("Telegram alert sent successfully!")
else:
    print("No relevant news matches found today.")
