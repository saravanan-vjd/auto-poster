import os
import requests
import tweepy
import google.generativeai as genai
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo

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
Here are 20 trending hashtags:
{trends}

Your job:
- Analyze all 20 hashtags.
- Keep ONLY hashtags that are positive, neutral, fun, harmless, or entertainment-related.
- REMOVE anything involving:
  • death, rip, tragedy, sadness, accidents
  • justice for…, missing persons
  • politics, elections, protests
  • violence, crime, scandals, lawsuits
  • disasters, sickness, global events
  • drama, hate, fights, negativity
- Do NOT invent new hashtags.
- After filtering, return ONLY the first **5 safe hashtags** in the same order they appeared.

----------------------------------------------------
PART 2 — TWEET GENERATION
----------------------------------------------------
Create 1 tweet in the exact style of extremely viral relatable Twitter humor.

Tone & Personality:
- casual, chaotic, very human
- slightly unhinged, slightly dramatic
- dry humor, light sarcasm
- lowercase preferred unless necessary
- feels like an intrusive thought
- relatable, self-aware, not serious
- modern internet voice
- Gen Z energy but universal

Content Rules:
- talk about something simple, everyday, painfully relatable
- nothing deep, nothing wise, nothing poetic
- no advice, no motivation, no inspiration
- write like you're texting a friend
- can be a statement, complaint, question, or tiny chaotic story
- conversational, not structured
- optional emojis ONLY if they add comedic chaos (😭😂)
- one paragraph or one clean line

Do NOT:
- no hashtags (in the tweet itself)
- no formal language
- no deep quotes
- no metaphors
- no long explanations
- no lists
- no inspirational tone

----------------------------------------------------
FINAL OUTPUT FORMAT
----------------------------------------------------
Line 1 → the tweet  
Line 2 → (empty line)  
Line 3 → the FIVE filtered safe hashtags, space-separated.

Example FORMAT ONLY (not content):
i hate when my brain loads slower than my wifi

#fun #omg #relatable #daily #lol

Return ONLY the final post in exactly this 3-line format.
"""


# ==================== AI POST GENERATOR ====================
def make_final_post(trends):
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = build_prompt(trends)
    return model.generate_content(prompt).text.strip()


# ==================== MAIN POSTER ====================
def post_now():
    log("BOT STARTED")

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
