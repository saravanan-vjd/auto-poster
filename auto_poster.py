import os
import requests
import tweepy
import google.generativeai as genai
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo
import random
import time

# ==================== ENVIRONMENT VARIABLES ====================

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET,
    wait_on_rate_limit=True
)

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)


# ==================== LOGGING ====================
def log(msg):
    now = datetime.now(ZoneInfo("UTC")).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{now}] {msg}")


# ==================== TREND SCRAPER ====================
def get_trends():
    """Fetch ~20 raw trending hashtags from Trends24."""
    try:
        now_ist = datetime.now(ZoneInfo("Asia/Kolkata"))
        hour = now_ist.hour

        if 6 <= hour < 22:
            url = "https://trends24.in/india/"
        else:
            url = "https://trends24.in/united-states/"

        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        raw = []
        for a in soup.select(".trend-card__list li a"):
            text = a.get_text(strip=True)
            if text and len(text) > 1 and not text.startswith("http"):
                raw.append("#" + text.replace(" ", "").replace("#", ""))

        raw = list(dict.fromkeys(raw))[:20]  # first 20 trends
        log("RAW TRENDS → " + ", ".join(raw))
        return raw

    except Exception as e:
        log("Trend fetch failed → fallback used.")
        return ["#DailyLife", "#GoodVibes", "#Fun", "#LOL", "#RandomThings"]


# ==================== AI COMBINED PROMPT ====================

def build_prompt(trends):
    return f"""
You will generate a final Twitter post using the rules below.

----------------------------------------------------
PART 1 — TREND FILTERING
----------------------------------------------------
Here are ~20 trending hashtags:
{trends}

Your job:
- Filter only FUN, ENTERTAINMENT, POSITIVE, MEME-RELEVANT hashtags
- Must be ENGLISH topic (remove Hindi/regional if found)
- Remove politics, war, elections, death, RIP, crime, scandals, serious topics
- Keep only the FIRST 5 safe hashtags in the same original order

----------------------------------------------------
PART 2 — TWEET STYLE
----------------------------------------------------
Create ONE viral tweet with:
- meme + trend-bait energy
- chaotic gen-z sarcasm
- lowercase preferred
- very short (max 2 lines)
- feels like a random intrusive thought
- no motivation, no advice
- no hashtags inside tweet

Allowed personality ROTATION (pick one RANDOMLY):
A) Low battery humor / lazy energy
B) Indian daily struggle (chai, auto, parents)
C) Tech/App memes (instagram, whatsapp, netflix, UPI)
D) Random chaotic thought (wtf how is this trending??)

Optional emojis: 😂😭😌 but only 0–2 max

Examples of tone:
- “why is monday trending again?? we already hate it 😭”
- “phone at 5% and somehow my life decisions also at 5%”
- “every app wants premium except my salary”
- “is google judging me or what”

----------------------------------------------------
FINAL OUTPUT FORMAT
----------------------------------------------------
Line 1 → the tweet (1-2 lines)
Line 2 → empty line
Line 3 → EXACT 5 filtered safe hashtags, space-separated

Return ONLY that final output.
"""


# ==================== AI POST GENERATOR ====================
def make_final_post(trends):
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = build_prompt(trends)
    return model.generate_content(prompt).text.strip()


# ==================== MAIN POSTER ====================
def post_now():
    log("BOT STARTED")

    # RANDOM WAIT TIME (1 to 5 minutes)
    wait_seconds = random.randint(60, 300)
    log(f"Waiting for {wait_seconds} seconds before posting...")
    time.sleep(wait_seconds)

    trends = get_trends()
    final_post = make_final_post(trends)

    # basic safety check
    if final_post.count("\n") < 2:
        log("❌ AI formatting error")
        log(final_post)
        return

    try:
        client.create_tweet(text=final_post)
        log("✅ POSTED → " + final_post.replace("\n", " ")[:140] + " ...")
    except Exception as e:
        log("❌ ERROR → " + str(e))

# ==================== ENTRY ====================
if __name__ == "__main__":
    post_now()
