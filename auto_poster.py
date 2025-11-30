import os
import io
import random
import requests
import tweepy
import google.generativeai as genai
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo

# ==================== ENV / SECRETS ====================
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
def log(m):
    now = datetime.now(ZoneInfo("UTC"))
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S UTC')}] {m}")

log("BOT STARTED")

def post_now():    

    # Generate a tweet via Gemini
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = """Create 1 Act like the most sarcastic, deadpan, minimalist Twitter poet who asks short questions just to judge the answers.

Generate exactly one post in this structure:

Line 1 — Bold Question

7–12 words

Designed to make people reply

Dry sarcasm, quiet judgment

Zero emojis, zero hashtags


Line 2 — Divider

Just a single em dash
Example: —


Line 3 — My Opinion

7–12 words

Unimpressed, self-aware sarcasm

Feels like I already know better


Tone Rules:

“Seen everything, shocked by nothing”

Inside-joke energy

Not wholesome, not rude — just cold honesty

Minimalist, cryptic, quietly superior


Examples: What’s the funniest thing you believed as a kid
—
I thought adults actually had a plan

One daily task you’d delete forever
—
Laundry should honestly learn to clean itself

Do not explain anything.
Do not add extra lines.
Deliver exactly this structure."""
    resp = model.generate_content(prompt).text.strip()

    # Clean numbering or bullets if any
    if resp and resp[0].isdigit():
        resp = resp.lstrip("0123456789").lstrip(".-) ").strip()

    # Validate length
    if len(resp) < 20 or len(resp) > 200:
        log("Generated tweet length invalid — skipping")
        return

    try:
        client.create_tweet(text=resp)
        log("✅ POSTED TEXT → " + resp[:100] + " ...")
    except Exception as e:
        log("❌ ERROR on tweet → " + str(e))

if __name__ == "__main__":
    post_now()
