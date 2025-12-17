import os
import tweepy
import google.generativeai as genai
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

if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, GOOGLE_API_KEY]):
    raise ValueError("Missing required API keys in environment variables.")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Tweepy Client
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET,
    wait_on_rate_limit=True
)

# ==================== LOGGING ====================
def log(msg: str):
    now = datetime.now(ZoneInfo("UTC")).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{now}] {msg}")

# ==================== AI PROMPT ====================
def build_prompt() -> str:
    return """
You are a chaotic Indian Gen-Z meme account posting random late-night intrusive thoughts.

Generate ONE short tweet:
- all lowercase
- sarcastic, lazy, tired energy
- very short (under 200 characters)
- feels like a random 2am thought
- no motivation, no advice, no questions
- optional 0–2 emojis only: 😂 😭 🙃 😔 😌 🫠 😩 🥲
- NO hashtags, NO mentions, NO links, NO questions

Randomly pick one vibe:
A) Exhausted low battery life
B) Indian chaos (mom, chai, traffic, parents, auto)
C) App/phone addiction (reels, WhatsApp, Netflix, UPI)
D) Pure existential dread

Examples:
- "phone at 5% and my life decisions also at 5% 😭"
- "mom calling for dinner but i'm busy existing"
- "every app wants premium except my salary"
- "why does breathing feel manual today"

Return ONLY the tweet text. No quotes, no extra text.
"""

# ==================== GENERATE TWEET ====================
def make_final_post() -> str | None:
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(build_prompt())
        
        if not response.text:
            log("⚠️ Gemini returned empty text")
            return None
        
        return response.text.strip()
    
    except Exception as e:
        log(f"⚠️ Gemini error: {str(e)}")
        return None

# ==================== MAIN FUNCTION ====================
def post_now():
    log("BOT STARTED – Generating chaotic 2am thought...")

    # Random delay: 3–18 minutes for natural jitter
    wait_seconds = random.randint(180, 1080)
    log(f"Waiting {wait_seconds // 60} minutes before posting...")
    time.sleep(wait_seconds)

    tweet_text = make_final_post()
    if not tweet_text:
        log("❌ No valid tweet generated – skipping run")
        return

    # Basic validation
    if len(tweet_text) < 10 or len(tweet_text) > 280:
        log(f"❌ Invalid length ({len(tweet_text)} chars)")
        return

    # Remove any accidental @ or #
    clean_tweet = ' '.join([
        word for word in tweet_text.split()
        if not word.startswith(('@', '#'))
    ]).strip()

    if len(clean_tweet) < 10:
        log("❌ Tweet too short after cleaning")
        return

    # Final post
    try:
        response = client.create_tweet(text=clean_tweet)
        tweet_id = response.data['id']
        url = f"https://x.com/i/status/{tweet_id}"
        
        log("✅ POSTED SUCCESSFULLY")
        log(f"→ {clean_tweet}")
        log(f"🔗 {url}")

    except tweepy.TooManyRequests:
        log("❌ RATE LIMIT HIT – Too many posts today (max 17/day)")
    except tweepy.Forbidden:
        log("❌ FORBIDDEN – Check app permissions or Free tier limits")
    except tweepy.Unauthorized:
        log("❌ UNAUTHORIZED – Invalid API keys?")
    except Exception as e:
        log(f"❌ POSTING ERROR: {str(e)}")

# ==================== RUN ====================
if __name__ == "__main__":
    post_now()
