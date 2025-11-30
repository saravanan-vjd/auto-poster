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
    prompt = """Create 1 tweet in the style of extremely viral, simple, relatable humor.

Writing rules:

Tone: casual, dry, mildly unhinged, extremely human

Style: short, simple, universal, everyday observations

No fancy words, no philosophy, no deep wisdom

Feels like someone thinking out loud

Should be something everyone experiences but never says

Slight sarcasm, light self-roast, a bit dramatic

Never inspirational, never motivational

No emojis unless naturally funny

No hashtags

No line breaks — one single paragraph unless it’s a two-part joke

It should feel like a tweet that gets 50k+ likes

Allowed formats:

A simple observation (“eating a meal without watching something feels illegal”)

A chaotic thought (“i’m such a fake idgaf’er because everything bothers me”)

A conversational joke (“ hacker: i have your passwords / me: finally what are they ”)

A relatable complaint (“i suck at hiding gifts”)

A simple question (“if you could master one skill instantly what would it be?”)

Do NOT:

Do not be poetic.

Do not be wise.

Do not be formal.

Do not explain anything.

Do not add hashtags.

Do not use big words.

Output: only the tweet. Nothing else."""
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
