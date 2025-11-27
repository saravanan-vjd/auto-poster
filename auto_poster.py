# ===================================================================
# FINAL EXPERT X/TWITTER BOT 2025 – 100% FREE 24/7 (Google Colab Ready)
# → India peak hours = India trends | USA peak hours = USA trends
# → Exactly 3 perfect trending hashtags per post
# → Images + Threads + Text | 10 posts/day | Never sleeps
# ===================================================================

# pip3 install tweepy schedule google-generativeai Pillow requests beautifulsoup4 lxml -q

import os
import time
import random
import io
import tempfile
import requests
import schedule
import tweepy
import google.generativeai as genai
from bs4 import BeautifulSoup
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# FORCE INDIA STANDARD TIME (IST)
os.environ['TZ'] = 'Asia/Kolkata'
time.tzset()

# ==================== LOGGING ====================
def log(m):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {m}")

log("FINAL EXPERT BOT STARTED – THE ONE AND ONLY VERSION")

# Load secrets from GitHub Actions ENV
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

# ==================== TIME-BASED TREND ENGINE (THE MAGIC) ====================
def get_trends():
    hour = datetime.now().hour
    if 6 <= hour < 22:  # 6 AM – 10 PM IST → INDIA PEAK
        url = "https://trends24.in/india/"
        country = "INDIA"
    else:               # 10 PM – 6 AM IST → USA PEAK
        url = "https://trends24.in/united-states/"
        country = "USA"

    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        raw = []
        for a in soup.select("a.trend-item"):
            text = a.get_text(strip=True)
            if text and len(text) > 1 and not text.startswith("http"):
                raw.append("#" + text.replace(" ", "").replace("#", ""))
        clean = list(dict.fromkeys(raw))[:3]  # Remove duplicates, take top 3
        log(f"{country} TRENDS → {' | '.join(clean)}")
        return clean
    except:
        log("Trend fetch failed → using safe hashtags")
        return ["#Motivation", "#Success", "#Growth"]

# ==================== IMAGE GENERATOR ====================
def make_image(text):
    try:
        img = Image.new("RGB", (1200, 630), "#0d0d26")
        d = ImageDraw.Draw(img)
        d.rectangle([(0,0),(1200,100)], fill="#1a1a40")
        d.rectangle([(0,530),(1200,630)], fill="#1a1a40")
        try:
            font = ImageFont.truetype("arial.ttf", 68)
        except:
            font = ImageFont.load_default()
        words = text.split()
        lines, line = [], []
        for word in words:
            test = " ".join(line + [word])
            if d.textlength(test, font=font) < 1100:
                line.append(word)
            else:
                lines.append(" ".join(line))
                line = [word]
        if line: lines.append(" ".join(line))
        y = (630 - len(lines)*95) // 2
        for l in lines:
            w = d.textlength(l, font=font)
            d.text(((1200 - w)/2, y), l, fill="#ffffff", font=font)
            y += 95
        buf = io.BytesIO()
        img.save(buf, "PNG")
        buf.seek(0)
        return buf
    except:
        return None

# ==================== CONTENT & QUEUE ====================
queue = []

def refill_queue():
    global queue
    queue.clear()
    trends = get_trends()
    tags = " " + " ".join(trends)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # 5 Text Posts
    prompt = "Create 5 short, powerful motivational tweets under 200 characters with emojis. Make them inspiring. Return ONLY the tweets, no numbers or bullet points."
    resp = model.generate_content(prompt).text
    texts = []
    for line in resp.split("\n"):
        text = line.strip()
        # Remove numbering like "1.", "1)", "1-", etc.
        if text and text[0].isdigit():
            text = text.lstrip("0123456789").lstrip(".-) ").strip()
        if 40 < len(text) < 200:
            texts.append(text + tags)
    texts = texts[:5]

    # 4 Image Quotes
    prompt2 = "Give me 4 beautiful one-line motivational quotes under 120 characters. Return ONLY the quotes, no numbers or bullet points."
    resp2 = model.generate_content(prompt2).text
    captions = []
    for line in resp2.split("\n"):
        text = line.strip()
        # Remove numbering
        if text and text[0].isdigit():
            text = text.lstrip("0123456789").lstrip(".-) ").strip()
        if text:
            captions.append(text + tags)
    captions = captions[:4]

    # 1 Thread (40% chance)
    if random.random() < 0.4:
        thr = model.generate_content("Write a 4-tweet motivational thread about discipline and consistency.").text
        thread_tweets = []
        for line in [x.strip() for x in thr.split("\n") if x.strip()]:
            tweet = line.split(":", 1)[1].strip() if ":" in line else line
            thread_tweets.append(tweet + tags)
        thread_str = "\n".join([f"{i+1}/4 {t}" for i, t in enumerate(thread_tweets)])
        queue.append({"type": "thread", "content": thread_str})

    # Add to queue
    for t in texts:
        queue.append({"type": "text", "text": t})
    for c in captions:
        img = make_image(c.split("#", 1)[0].strip())
        if img:
            queue.append({"type": "image", "text": c, "img": img})

    random.shuffle(queue)
    log(f"QUEUE READY → {len(queue)} posts with 3 trending hashtags")

# ==================== POST FUNCTION ====================
def post_now():
    global queue
    if len(queue) < 3:
        refill_queue()
    item = queue.pop(0)

    try:
        if item["type"] == "text":
            client.create_tweet(text=item["text"])
            log(f"POSTED TEXT → {item['text'][:90]}")

        elif item["type"] == "image":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
                f.write(item["img"].read())
                path = f.name
            media = api.media_upload(path)
            # Post only hashtags, no image caption text
            hashtags_only = " ".join([tag for tag in item["text"].split() if tag.startswith("#")])
            client.create_tweet(text=hashtags_only, media_ids=[media.media_id])
            os.remove(path)
            log("POSTED IMAGE with 3 trending hashtags")

        elif item["type"] == "thread":
            tweets = []
            for line in item["content"].split("\n"):
                if line.strip():
                    tweets.append(line.split(" ", 1)[1] if "/" in line else line.strip())
            last_id = None
            for t in tweets:
                resp = client.create_tweet(text=t, in_reply_to_tweet_id=last_id) if last_id else client.create_tweet(text=t)
                last_id = resp.data["id"]
                time.sleep(3)
            log("POSTED FULL THREAD (4 tweets)")

    except Exception as e:
        log(f"ERROR → {e} | Re-adding to queue")
        queue.insert(0, item)

# ==================== PERFECT 2025 SCHEDULE (10 POSTS/DAY) ====================
schedule.every().day.at("06:30").do(post_now)  # India morning
schedule.every().day.at("08:30").do(post_now)
schedule.every().day.at("10:30").do(post_now)
schedule.every().day.at("13:00").do(post_now)
schedule.every().day.at("16:30").do(post_now)
schedule.every().day.at("19:00").do(post_now)  # India prime time
schedule.every().day.at("21:00").do(post_now)
schedule.every().day.at("22:30").do(post_now)  # USA handover
schedule.every().day.at("01:00").do(post_now)  # USA peak
schedule.every().day.at("04:00").do(post_now)  # USA morning

refill_queue()
log("FINAL BOT IS NOW LIVE – 100% FREE 24/7")
log("Go to UptimeRobot.com → Add this Colab link → Ping every 5 minutes → Never dies")

# ==================== KEEP COLAB ALIVE FOREVER ====================
import threading
def heartbeat():
    while True:
        print(f"Bot running strong – {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST")
        time.sleep(60)
threading.Thread(target=heartbeat, daemon=True).start()

# ==================== MAIN LOOP ====================
try:
    while True:
        schedule.run_pending()
        time.sleep(30)
except KeyboardInterrupt:
    log("Bot stopped by user")
