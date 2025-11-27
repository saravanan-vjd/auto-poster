# # ===================================================================
# # FINAL EXPERT X/TWITTER BOT 2025 – PRODUCTION READY FOR GITHUB ACTIONS
# # → Posts 1 item per run (text, image, or thread)
# # → India/USA peak hours logic preserved (IST/UTC safe)
# # → Gemini content generation, trends scraping, images, threads
# # ===================================================================

# import os
# import io
# import tempfile
# import random
# import requests
# import tweepy
# import google.generativeai as genai
# from bs4 import BeautifulSoup
# from datetime import datetime
# from zoneinfo import ZoneInfo
# from PIL import Image, ImageDraw, ImageFont

# # ==================== ENV / SECRETS ====================
# API_KEY = os.getenv("API_KEY")
# API_SECRET = os.getenv("API_SECRET")
# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# ACCESS_SECRET = os.getenv("ACCESS_SECRET")
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# genai.configure(api_key=GOOGLE_API_KEY)

# client = tweepy.Client(
#     consumer_key=API_KEY,
#     consumer_secret=API_SECRET,
#     access_token=ACCESS_TOKEN,
#     access_token_secret=ACCESS_SECRET,
#     wait_on_rate_limit=True
# )
# auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
# api = tweepy.API(auth)

# # ==================== LOGGING ====================
# def log(m):
#     now = datetime.now(ZoneInfo("Asia/Kolkata"))
#     print(f"[{now.strftime('%Y-%m-%d %H:%M:%S IST')}] {m}")

# log("FINAL EXPERT BOT STARTED – PRODUCTION MODE")

# # ==================== TREND SCRAPER ====================
# def get_trends():
#     now_ist = datetime.now(ZoneInfo("Asia/Kolkata"))
#     hour = now_ist.hour
#     if 6 <= hour < 22:
#         url = "https://trends24.in/india/"
#         country = "INDIA"
#     else:
#         url = "https://trends24.in/united-states/"
#         country = "USA"
#     try:
#         r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
#         soup = BeautifulSoup(r.text, "html.parser")
#         raw = []
#         for a in soup.select(".trend-card__list li a"):
#             text = a.get_text(strip=True)
#             if text and len(text) > 1 and not text.startswith("http"):
#                 raw.append("#" + text.replace(" ", "").replace("#", ""))
#         clean = list(dict.fromkeys(raw))[:3]
#         log(f"{country} TRENDS → {' | '.join(clean)}")
#         return clean
#     except:
#         log("Trend fetch failed → using safe hashtags")
#         return ["#Motivation", "#Success", "#Growth"]

# # ==================== IMAGE GENERATOR ====================
# def make_image(text):
#     try:
#         img = Image.new("RGB", (1200, 630), "#0d0d26")
#         d = ImageDraw.Draw(img)
#         try:
#             font = ImageFont.truetype("arial.ttf", 120)  # BIGGER FONT
#         except:
#             font = ImageFont.load_default()
#         # Force single-line text
#         w = d.textlength(text, font=font)
#         d.text(((1200 - w)/2, 280), text, fill="#ffffff", font=font)
#         buf = io.BytesIO()
#         img.save(buf, "PNG")
#         buf.seek(0)
#         return buf
#     except:
#         return None

# # ==================== CONTENT GENERATOR ====================
# def refill_queue():
#     trends = get_trends()
#     tags = " " + " ".join(trends)
#     model = genai.GenerativeModel("gemini-2.5-flash")
#     queue = []

#     # 5 Texts
#     prompt_texts = "Create 5 short, powerful motivational tweets under 200 characters with emojis. Return ONLY the tweets."
#     resp_texts = model.generate_content(prompt_texts).text
#     texts = []
#     for line in resp_texts.split("\n"):
#         text = line.strip()
#         if text and text[0].isdigit():
#             text = text.lstrip("0123456789").lstrip(".-) ").strip()
#         if 40 < len(text) < 200:
#             texts.append(text + tags)
#     texts = texts[:5]

#     # 4 Image Quotes (temporarily disabled)
#     # prompt_images = "Give 4 beautiful one-line motivational quotes under 80 characters. Return ONLY the quotes."
#     # resp_imgs = model.generate_content(prompt_images).text
#     images = []
#     # for line in resp_imgs.split("\n"):
#     #     text = line.strip()
#     #     if text and text[0].isdigit():
#     #         text = text.lstrip("0123456789").lstrip(".-) ").strip()
#     #     if text:
#     #         images.append(text + tags)
#     # images = images[:4]

#     # 1 Thread (temporarily disabled)
#     # thread = []
#     # if random.random() < 0.4:
#     #     thr = model.generate_content("Write a 4-tweet motivational thread about discipline and consistency.").text
#     #     for line in [x.strip() for x in thr.split("\n") if x.strip()]:
#     #         tweet = line.split(":",1)[1].strip() if ":" in line else line
#     #         thread.append(tweet + tags)

#     # Merge queue
#     for t in texts:
#         queue.append({"type":"text","text":t})
#     # Images disabled for now
#     # for c in images:
#     #     img = make_image(c.split("#",1)[0].strip())
#     #     if img:
#     #         queue.append({"type":"image","text":c,"img":img})
#     # Threads disabled for now
#     # if thread:
#     #     thread_str = "\n".join([f"{i+1}/4 {t}" for i,t in enumerate(thread)])
#     #     queue.append({"type":"thread","content":thread_str})

#     random.shuffle(queue)
#     return queue

# # ==================== POST FUNCTION ====================
# def post_now():
#     queue = refill_queue()
#     if not queue:
#         log("Queue empty → Nothing to post")
#         return

#     item = queue.pop(0)
#     try:
#         if item["type"] == "text":
#             client.create_tweet(text=item["text"])
#             log(f"✅ POSTED TEXT → {item['text'][:90]}")
#         # elif item["type"] == "image":
#         #     with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
#         #         f.write(item["img"].read())
#         #         path = f.name
#         #     media = api.media_upload(path)
#         #     hashtags_only = " ".join([tag for tag in item["text"].split() if tag.startswith("#")])
#         #     client.create_tweet(text=hashtags_only, media_ids=[media.media_id])
#         #     os.remove(path)
#         #     log("✅ POSTED IMAGE with hashtags")
#         # elif item["type"] == "thread":
#         #     tweets = []
#         #     for line in item["content"].split("\n"):
#         #         if line.strip():
#         #             tweets.append(line.split(" ",1)[1] if "/" in line else line.strip())
#         #     last_id = None
#         #     for t in tweets:
#         #         resp = client.create_tweet(text=t, in_reply_to_tweet_id=last_id) if last_id else client.create_tweet(text=t)
#         #         last_id = resp.data["id"]
#         #     log("✅ POSTED THREAD (4 tweets)")
#     except Exception as e:
#         log(f"❌ ERROR → {str(e)}")

# # ==================== RUN BOT ====================
# if __name__ == "__main__":
#     post_now()


# ===================================================================
# FINAL EXPERT X/TWITTER BOT 2025 – PRODUCTION READY (5 HASHTAGS)
# → Posts 1 item per run (text only for now)
# → Trends-based 5-hashtag mix (including any trending topic — T3)
# → UTC-safe logic (ready for GitHub Actions cron)
# ===================================================================

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

log("BOT STARTED – UTC SAFE, 5 HASHTAG MODE T3")

# ==================== TREND FETCHER (returns top 5 hashtags) ====================
def get_trends(n=5):
    now_utc = datetime.now(ZoneInfo("UTC"))
    hour = now_utc.hour

    # Determine region: choose India if roughly daytime in India, else use US trends
    # India peak roughly UTC 1:00 to 17:00 (IST 6:30–22:00)
    if 1 <= hour < 17:
        url = "https://trends24.in/india/"
        region = "INDIA"
    else:
        url = "https://trends24.in/united-states/"
        region = "USA"

    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        raw = []
        for a in soup.select(".trend-card__list li a"):
            text = a.get_text(strip=True)
            if text and len(text) > 0 and not text.startswith("http"):
                tag = "#" + text.replace(" ", "").replace("#", "")
                raw.append(tag)
        # dedupe and return top n
        clean = []
        for t in raw:
            if t not in clean:
                clean.append(t)
            if len(clean) >= n:
                break
        log(f"TRENDS → {region}: {' | '.join(clean)}")
        return clean
    except Exception as e:
        log(f"Trend fetch failed ({e}) → fallback tags")
        return ["#Motivation", "#Success", "#Growth", "#Inspiration", "#Mindset"]

# ==================== CONTENT GENERATOR & POST ====================
def post_now():
    # Fetch trending hashtags
    tags = get_trends(5)
    tag_str = " " + " ".join(tags)

    # Generate a tweet via Gemini
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = "Create 1 short, powerful motivational tweet under 200 characters with emojis. Return ONLY the tweet text (no numbering)."
    resp = model.generate_content(prompt).text.strip()

    # Clean numbering or bullets if any
    if resp and resp[0].isdigit():
        resp = resp.lstrip("0123456789").lstrip(".-) ").strip()

    # Validate length
    if len(resp) < 20 or len(resp) > 200:
        log("Generated tweet length invalid — skipping")
        return

    tweet = resp + tag_str

    try:
        client.create_tweet(text=tweet)
        log("✅ POSTED TEXT → " + tweet[:100] + " ...")
    except Exception as e:
        log("❌ ERROR on tweet → " + str(e))

if __name__ == "__main__":
    post_now()
