import os
import tweepy
from google import genai  # Correct import for new SDK
from datetime import datetime
from zoneinfo import ZoneInfo
import random
import time

# ==================== ENVIRONMENT VARIABLES ====================
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Works automatically (or rename to GEMINI_API_KEY)

if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, GOOGLE_API_KEY]):
    raise ValueError("Missing required API keys in environment variables.")

# Gemini Client (auto-uses GOOGLE_API_KEY or GEMINI_API_KEY from env)
client_gemini = genai.Client()

# Tweepy Client
client_tweepy = tweepy.Client(
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
You will generate a final Twitter post using the rules below.

Create ONE viral tweet with:

meme + trend-bait energy
chaotic gen-z sarcasm
lowercase preferred
very short (max 2 lines)
feels like a random intrusive thought
no motivation, no advice
no hashtags inside tweet

Allowed personality ROTATION (pick one RANDOMLY):
A) Low battery humor / lazy energy
B) Indian daily struggle (chai, auto, parents)
C) Tech/App memes (instagram, whatsapp, netflix, UPI)
D) Random chaotic thought (wtf how is this trending??)

Optional emojis:  but only 0–2 max

Examples of tone:

“why is monday trending again?? we already hate it ”
“phone at 5% and somehow my life decisions also at 5%”
“every app wants premium except my salary”
“is google judging me or what”

----------------------------------------------------
FINAL OUTPUT FORMAT
----------------------------------------------------
Line 1 → the tweet (1-2 lines)Return ONLY that final output.
"""

# ==================== GENERATE TWEET ====================
def make_final_post() -> str | None:
    try:
        prompt = build_prompt()
        
        response = client_gemini.models.generate_content(
            model="gemini-2.5-flash",  # Use "gemini-1.5-flash" (stable) or "gemini-2.5-flash" if available
            contents=prompt
        )
        
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
        response = client_tweepy.create_tweet(text=clean_tweet)
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
