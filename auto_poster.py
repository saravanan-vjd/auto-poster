# ===================================================================
# FINAL EXPERT X/TWITTER BOT 2025 – PRODUCTION READY FOR GITHUB ACTIONS
# → Posts 1 item per run (text, image, or thread)
# → India/USA peak hours logic preserved
# → Gemini content generation, trends scraping, images, threads
# ===================================================================

import os
import time
import random
import io
import tempfile
import requests
import tweepy
import google.generativeai as genai
from bs4 import BeautifulSoup
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# ==================== ENV / SECRETS ====================
# API_KEY = os.getenv("API_KEY")
# API_SECRET = os.getenv("API_SECRET")
# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# ACCESS_SECRET = os.getenv("ACCESS_SECRET")
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

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
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {m}")

log("FINAL EXPERT BOT STARTED – PRODUCTION MODE")

# ==================== TREND SCRAPER ====================
def get_trends():
    hour = datetime.now().hour
    if 6 <= hour < 22:
        url = "https://trends24.in/india/"
        country = "INDIA"
    else:
        url = "https://trends24.in/united-states/"
        country = "USA"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        raw = []
        for a in soup.select(".trend-card__list li a"):
            text = a.get_text(strip=True)
            if text and len(text) > 1 and not text.startswith("http"):
                raw.append("#" + text.replace(" ", "").replace("#", ""))
        clean = list(dict.fromkeys(raw))[:3]
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
            font = ImageFont.truetype("arial.ttf", 80)
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

# ==================== CONTENT GENERATOR ====================
def refill_queue():
    trends = get_trends()
    tags = " " + " ".join(trends)
    model = genai.GenerativeModel("gemini-2.5-flash")
    queue = []

    # 5 Texts
    prompt_texts = "Create 5 short, powerful motivational tweets under 200 characters with emojis. Return ONLY the tweets."
    resp_texts = model.generate_content(prompt_texts).text
    texts = []
    for line in resp_texts.split("\n"):
        text = line.strip()
        if text and text[0].isdigit():
            text = text.lstrip("0123456789").lstrip(".-) ").strip()
        if 40 < len(text) < 200:
            texts.append(text + tags)
    texts = texts[:5]

    # 4 Image Quotes
    prompt_images = "Give 4 beautiful one-line motivational quotes under 120 characters. Return ONLY the quotes."
    resp_imgs = model.generate_content(prompt_images).text
    images = []
    for line in resp_imgs.split("\n"):
        text = line.strip()
        if text and text[0].isdigit():
            text = text.lstrip("0123456789").lstrip(".-) ").strip()
        if text:
            images.append(text + tags)
    images = images[:4]

    # 1 Thread (mandatory)
    thread = []
    # Temporarily disabled - will add back later
    # thr = model.generate_content("Write a 4-tweet motivational thread about discipline and consistency.").text
    # for line in [x.strip() for x in thr.split("\n") if x.strip()]:
    #     tweet = line.split(":",1)[1].strip() if ":" in line else line
    #     thread.append(tweet + tags)

    # Merge queue
    for t in texts:
        queue.append({"type":"text","text":t})
    for c in images:
        img = make_image(c.split("#",1)[0].strip())
        if img:
            queue.append({"type":"image","text":c,"img":img})
    # Thread disabled for now
    # if thread:
    #     thread_str = "\n".join([f"{i+1}/4 {t}" for i,t in enumerate(thread)])
    #     queue.append({"type":"thread","content":thread_str})

    random.shuffle(queue)
    return queue

# ==================== POST FUNCTION ====================
def post_now():
    queue = refill_queue()
    if not queue:
        log("Queue empty → Nothing to post")
        return

    item = queue.pop(0)
    try:
        if item["type"] == "text":
            client.create_tweet(text=item["text"])
            log(f"✅ POSTED TEXT → {item['text'][:90]}")
        elif item["type"] == "image":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
                f.write(item["img"].read())
                path = f.name
            media = api.media_upload(path)
            hashtags_only = " ".join([tag for tag in item["text"].split() if tag.startswith("#")])
            client.create_tweet(text=hashtags_only, media_ids=[media.media_id])
            os.remove(path)
            log("✅ POSTED IMAGE with hashtags")
        elif item["type"] == "thread":
            tweets = []
            for line in item["content"].split("\n"):
                if line.strip():
                    tweets.append(line.split(" ",1)[1] if "/" in line else line.strip())
            last_id = None
            for t in tweets:
                resp = client.create_tweet(text=t, in_reply_to_tweet_id=last_id) if last_id else client.create_tweet(text=t)
                last_id = resp.data["id"]
                time.sleep(3)
            log("✅ POSTED THREAD (4 tweets)")
    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg:
            log(f"❌ AUTH ERROR (403) → API credentials expired or invalid")
            log(f"   Fix: Go to https://developer.twitter.com/en/portal/dashboard")
            log(f"   Regenerate your API keys and update them in the code")
        elif "401" in error_msg:
            log(f"❌ UNAUTHORIZED (401) → Invalid credentials")
        else:
            log(f"❌ ERROR → {error_msg}")

# ==================== RUN BOT ====================
if __name__ == "__main__":
    post_now()
