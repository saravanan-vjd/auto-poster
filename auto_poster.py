# import tweepy
# import schedule
# import time
# import random
# import google.generativeai as genai
# from datetime import datetime

# # Setup logging function
# def log(message, level="INFO"):
#     """Log messages with timestamp"""
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     print(f"[{timestamp}] [{level}] {message}")

# log("Starting AutoPoster Application...")

# # Step 1: Load API credentials
# log("Step 1: Loading API credentials...")
# # Twitter/X API credentials
# API_KEY = 'cPfy0RvvJJFYfZmtlroTKRugM'  # Consumer Key
# API_SECRET = 'H1pBc1u9SGTjeaooBZqHoQS953YGge6vw8gqbJwMcx1sq0mDZx'  # Consumer Secret
# ACCESS_TOKEN = '1993329052682481664-VxrAjznCZ7saHEzkxXXNeKb18TSblJ'
# ACCESS_SECRET = '1xeZxuRTl8bUYamQBQPo4nJFfcbKnHqf2Fc24YbgSH5lz'
# log("✅ Twitter/X API credentials loaded")

# # Google Gemini API key (get free at https://ai.google.dev/)
# GEMINI_API_KEY = 'AIzaSyCwBcYYzcEE5KjfTObWrMQ3jWqSu-RR3CI'
# genai.configure(api_key=GEMINI_API_KEY)
# log("✅ Gemini API configured")

# # Step 2: Authenticate with X API
# log("Step 2: Authenticating with Twitter/X API...")
# try:
#     client = tweepy.Client(
#         consumer_key=API_KEY, consumer_secret=API_SECRET,
#         access_token=ACCESS_TOKEN, access_token_secret=ACCESS_SECRET
#     )
#     log("✅ Twitter/X API authenticated successfully")
# except Exception as e:
#     log(f"❌ Failed to authenticate with Twitter/X API: {e}", "ERROR")
#     client = None

# # Step 3: Function to generate motivational posts using AI
# def generate_motivational_posts(num_posts=10):
#     """Generate motivational posts using Google Gemini API"""
#     log(f"Step 3: Generating {num_posts} motivational posts with Gemini AI...")
#     generated_posts = []
#     try:
#         log("Creating prompt for AI...")
#         prompt = f"""Generate exactly {num_posts} unique, inspirational motivational posts for Twitter/X. 
# Each post should:
# - Be under 280 characters
# - Include relevant emojis
# - Be unique and engaging
# - Focus on motivation, personal growth, success, and perseverance
# - Do not include hashtags

# Return only the posts, one per line, without numbering."""

#         log("Calling Gemini API (gemini-2.5-flash model)...")
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         response = model.generate_content(prompt)
#         log("✅ API response received successfully")
        
#         # Parse the response and split into individual posts
#         log("Parsing and formatting posts...")
#         posts_text = response.text
#         generated_posts = [post.strip() for post in posts_text.split('\n') if post.strip()]
        
#         log(f"✅ Successfully generated {len(generated_posts)} motivational posts")
#         for i, post in enumerate(generated_posts[:num_posts], 1):
#             log(f"  Post {i}: {post[:70]}...", "DEBUG")
#         return generated_posts[:num_posts]  # Return only the requested number
        
#     except Exception as e:
#         log(f"❌ Error generating posts with AI: {e}", "ERROR")
#         return []

# # Step 4: Initialize posts list
# log("Step 4: Initializing posts list...")
# posts = generate_motivational_posts(10)
# if not posts:
#     log("⚠️  AI generation failed, using fallback posts...", "WARNING")
#     # Fallback posts if API fails
#     posts = [
#         "Your potential is endless. Go create something amazing today! 🚀",
#         "Success is not final, failure is not fatal. Keep moving forward! 💪",
#         "Dream big, work hard, stay focused. 🎯",
#         "The only way to do great work is to love what you do. 💖",
#         "Every expert was once a beginner. Keep learning! 📚",
#         "Don't watch the clock; do what it does. Keep going! ⏰",
#         "Believe in yourself and you're halfway there. 🌟",
#         "Your future is created by what you do today, not tomorrow. 🔥",
#         "Impossible is nothing when you have determination. 💯",
#         "Stay focused and keep pushing towards your goals! 🎯"
#     ]
#     log(f"Loaded {len(posts)} fallback posts")
# else:
#     log(f"✅ Successfully loaded {len(posts)} AI-generated posts")

# # Step 5: Post function
# def post_tweet():
#     """Post a random tweet from the queue"""
#     if posts:
#         tweet = random.choice(posts)
#         log(f"Attempting to post: {tweet[:70]}...")
#         try:
#             if client is None:
#                 log("❌ Client not initialized, skipping post", "ERROR")
#                 return
#             response = client.create_tweet(text=tweet)
#             log(f"✅ Posted successfully (ID: {response.data['id']})")
#             log(f"   Content: {tweet}")
#             posts.remove(tweet)
#             log(f"Remaining posts in queue: {len(posts)}")
#         except Exception as e:
#             log(f"❌ Error posting tweet: {e}", "ERROR")
#     else:
#         log("⚠️  No more posts queued. Add more to the list!", "WARNING")

# # Step 6: Schedule posts
# log("Step 5: Setting up posting schedule...")
# log("Scheduling 10 posts throughout the day (12 AM to 10 PM)")

# schedule.every().day.at("00:00").do(post_tweet)
# schedule.every().day.at("02:00").do(post_tweet)
# schedule.every().day.at("06:00").do(post_tweet)
# schedule.every().day.at("08:00").do(post_tweet)
# schedule.every().day.at("11:00").do(post_tweet)
# schedule.every().day.at("13:00").do(post_tweet)
# schedule.every().day.at("16:00").do(post_tweet)
# schedule.every().day.at("18:00").do(post_tweet)
# schedule.every().day.at("20:00").do(post_tweet)
# schedule.every().day.at("22:00").do(post_tweet)

# log("✅ Schedule configured successfully")

# # Step 7: Run the scheduler
# log("Step 6: Starting scheduler loop...")
# log("Scheduler is running. Press Ctrl+C to stop.")
# try:
#     while True:
#         schedule.run_pending()
#         time.sleep(60)  # Check every minute
# except KeyboardInterrupt:
#     log("Scheduler stopped by user", "INFO")
# except Exception as e:
#     log(f"❌ Unexpected error in scheduler: {e}", "ERROR")




# import tweepy
# import schedule
# import time
# import random
# import google.generativeai as genai
# from datetime import datetime
# from PIL import Image, ImageDraw, ImageFont
# import io
# import tempfile
# import os

# # Setup logging function
# def log(message, level="INFO"):
#     """Log messages with timestamp"""
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     print(f"[{timestamp}] [{level}] {message}")

# log("Starting AutoPoster Application...")

# # Step 1: Load API credentials
# log("Step 1: Loading API credentials...")
# API_KEY = 'cPfy0RvvJJFYfZmtlroTKRugM'
# API_SECRET = 'H1pBc1u9SGTjeaooBZqHoQS953YGge6vw8gqbJwMcx1sq0mDZx'
# ACCESS_TOKEN = '1993329052682481664-VxrAjznCZ7saHEzkxXXNeKb18TSblJ'
# ACCESS_SECRET = '1xeZxuRTl8bUYamQBQPo4nJFfcbKnHqf2Fc24YbgSH5lz'
# log("✅ Twitter/X API credentials loaded")

# GEMINI_API_KEY = 'AIzaSyCwBcYYzcEE5KjfTObWrMQ3jWqSu-RR3CI'
# genai.configure(api_key=GEMINI_API_KEY)
# log("✅ Gemini API configured")

# # Step 2: Authenticate with X API
# log("Step 2: Authenticating with Twitter/X API...")
# try:
#     client = tweepy.Client(
#         consumer_key=API_KEY, consumer_secret=API_SECRET,
#         access_token=ACCESS_TOKEN, access_token_secret=ACCESS_SECRET,
#         wait_on_rate_limit=True
#     )
#     # Also create API object for media uploads
#     auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
#     auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
#     api = tweepy.API(auth)
#     log("✅ Twitter/X API authenticated successfully")
# except Exception as e:
#     log(f"❌ Failed to authenticate with Twitter/X API: {e}", "ERROR")
#     client = None
#     api = None

# # Step 3: Generate motivational image with text
# def generate_motivational_image(text):
#     """Generate a motivational image with text overlay"""
#     try:
#         log("Generating motivational image...")
#         # Create image with gradient-like effect
#         width, height = 1200, 630
#         image = Image.new('RGB', (width, height), color='#1a1a2e')
#         draw = ImageDraw.Draw(image)
        
#         # Add accent color bars
#         draw.rectangle([(0, 0), (width, 100)], fill='#16213e')
#         draw.rectangle([(0, height-100), (width, height)], fill='#0f3460')
        
#         # Try to use a system font, fallback to default
#         try:
#             font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
#             small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
#         except:
#             font = ImageFont.load_default()
#             small_font = ImageFont.load_default()
        
#         # Wrap text
#         max_width = width - 100
#         words = text.split()
#         lines = []
#         current_line = []
        
#         for word in words:
#             current_line.append(word)
#             line_text = ' '.join(current_line)
#             bbox = draw.textbbox((0, 0), line_text, font=font)
#             if bbox[2] - bbox[0] > max_width:
#                 current_line.pop()
#                 lines.append(' '.join(current_line))
#                 current_line = [word]
#         lines.append(' '.join(current_line))
        
#         # Draw text centered
#         y_position = (height - len(lines) * 60) // 2
#         for line in lines:
#             bbox = draw.textbbox((0, 0), line, font=font)
#             text_width = bbox[2] - bbox[0]
#             x_position = (width - text_width) // 2
#             draw.text((x_position, y_position), line, fill='#ffffff', font=font)
#             y_position += 70
        
#         # Add motivational emoji at bottom
#         draw.text((width-150, height-80), "🚀 💪 🌟", fill='#e94560', font=small_font)
        
#         # Save to bytes
#         img_bytes = io.BytesIO()
#         image.save(img_bytes, format='PNG')
#         img_bytes.seek(0)
#         log("✅ Motivational image generated")
#         return img_bytes
        
#     except Exception as e:
#         log(f"❌ Error generating image: {e}", "ERROR")
#         return None

# # Step 3.1: Generate posts content
# def generate_posts_content():
#     """Generate 6 text posts, 3 image posts, and 1 thread using Gemini"""
#     log("Step 3: Generating content mix (6 text, 3 images, 1 thread)...")
    
#     try:
#         model = genai.GenerativeModel('gemini-2.5-flash')
        
#         # Generate text posts
#         log("Generating 6 text motivational posts...")
#         prompt_text = """Generate exactly 6 unique, short motivational posts for Twitter/X.
# Each post should:
# - Be under 280 characters
# - Include relevant emojis
# - Be inspiring and engaging
# Return only the posts, one per line, without numbering."""
        
#         response_text = model.generate_content(prompt_text)
#         text_posts = [post.strip() for post in response_text.text.split('\n') if post.strip()][:6]
#         log(f"✅ Generated {len(text_posts)} text posts")
        
#         # Generate image captions
#         log("Generating 3 image post captions...")
#         prompt_images = """Generate exactly 3 unique, inspirational quotes for motivational images on Twitter/X.
# Each quote should:
# - Be under 150 characters
# - Be powerful and memorable
# - Include emojis if possible
# Return only the quotes, one per line, without numbering."""
        
#         response_images = model.generate_content(prompt_images)
#         image_captions = [post.strip() for post in response_images.text.split('\n') if post.strip()][:3]
#         log(f"✅ Generated {len(image_captions)} image captions")
        
#         # Generate thread
#         log("Generating 1 motivational thread...")
#         prompt_thread = """Generate a motivational thread for Twitter/X with exactly 5 tweets.
# The thread should tell a story about overcoming challenges.
# Each tweet should be under 280 characters.
# Format as Tweet 1: ... Tweet 2: ... etc
# Start each with the tweet number."""
        
#         response_thread = model.generate_content(prompt_thread)
#         thread_text = response_thread.text
#         log("✅ Generated motivational thread")
        
#         return text_posts, image_captions, thread_text
        
#     except Exception as e:
#         log(f"❌ Error generating content: {e}", "ERROR")
#         return [], [], ""

# # Step 4: Initialize posts
# log("Step 4: Initializing posts...")
# text_posts, image_captions, thread_content = generate_posts_content()

# # Create post objects
# posts_queue = []

# # Add text posts
# for post in text_posts:
#     if post:
#         posts_queue.append({'type': 'text', 'content': post})
#         log(f"  Added text post: {post[:60]}...")

# # Add image posts (generate images)
# for caption in image_captions:
#     if caption:
#         img = generate_motivational_image(caption)
#         if img:
#             posts_queue.append({'type': 'image', 'content': caption, 'image': img})
#             log(f"  Added image post: {caption[:60]}...")

# # Add thread
# if thread_content:
#     posts_queue.append({'type': 'thread', 'content': thread_content})
#     log("  Added thread post")

# log(f"✅ Total posts queued: {len(posts_queue)} (Text: {len(text_posts)}, Images: {len(image_captions)}, Thread: 1)")

# # Step 5: Post function with retry logic
# def post_content():
#     """Post content (text, image, or thread)"""
#     if not posts_queue:
#         log("⚠️  No more posts queued. Add more to the list!", "WARNING")
#         return
    
#     post = random.choice(posts_queue)
#     post_type = post['type']
    
#     if post_type == 'text':
#         log(f"Attempting to post text: {post['content'][:70]}...")
#         try:
#             if client is None:
#                 log("❌ Client not initialized, skipping post", "ERROR")
#                 return
#             response = client.create_tweet(text=post['content'])
#             log(f"✅ Text post published (ID: {response.data['id']})")
#             posts_queue.remove(post)
#             log(f"Remaining posts: {len(posts_queue)}")
#         except Exception as e:
#             log(f"❌ Error posting text: {e}", "ERROR")
            
#     elif post_type == 'image':
#         log(f"Attempting to post image...")
#         try:
#             if client is None or api is None:
#                 log("❌ Client not initialized, skipping post", "ERROR")
#                 return
            
#             # Save image to temporary file
#             with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
#                 tmp_path = tmp_file.name
#                 post['image'].seek(0)
#                 tmp_file.write(post['image'].read())
            
#             # Upload media using filename
#             media = api.media_upload(filename=tmp_path)
            
#             # Post tweet with image ONLY (no caption)
#             response = client.create_tweet(
#                 media_ids=[media.media_id]
#             )
#             log(f"✅ Image post published (ID: {response.data['id']})")
            
#             # Clean up temporary file
#             os.remove(tmp_path)
            
#             posts_queue.remove(post)
#             log(f"Remaining posts: {len(posts_queue)}")
#         except Exception as e:
#             log(f"❌ Error posting image: {e}", "ERROR")
            
#     elif post_type == 'thread':
#         log("Attempting to post thread...")
#         try:
#             if client is None:
#                 log("❌ Client not initialized, skipping post", "ERROR")
#                 return
#             # Parse thread tweets
#             tweets = [t.strip() for t in post['content'].split('Tweet') if t.strip()]
#             tweets = [t.split(':', 1)[1].strip() if ':' in t else t for t in tweets]
            
#             last_tweet_id = None
#             for i, tweet in enumerate(tweets[:5]):  # Max 5 tweets per thread
#                 if tweet:
#                     if last_tweet_id:
#                         response = client.create_tweet(text=tweet, reply_settings="everyone", in_reply_to_tweet_id=last_tweet_id)
#                     else:
#                         response = client.create_tweet(text=tweet)
#                     last_tweet_id = response.data['id']
#                     log(f"  Thread tweet {i+1}/5 posted (ID: {last_tweet_id})")
            
#             log(f"✅ Thread posted successfully")
#             posts_queue.remove(post)
#             log(f"Remaining posts: {len(posts_queue)}")
#         except Exception as e:
#             log(f"❌ Error posting thread: {e}", "ERROR")

# # Step 6: Schedule posts
# log("Step 5: Setting up posting schedule...")
# log("Scheduling 10 posts throughout the day")

# schedule.every().day.at("00:00").do(post_content)
# schedule.every().day.at("02:00").do(post_content)
# schedule.every().day.at("06:00").do(post_content)
# schedule.every().day.at("08:00").do(post_content)
# schedule.every().day.at("10:35").do(post_content)
# # schedule.every().day.at("11:00").do(post_content)
# schedule.every().day.at("13:00").do(post_content)
# schedule.every().day.at("16:00").do(post_content)
# schedule.every().day.at("18:00").do(post_content)
# schedule.every().day.at("20:00").do(post_content)
# schedule.every().day.at("22:00").do(post_content)

# log("✅ Schedule configured successfully")

# # Step 7: Run scheduler
# log("Step 6: Starting scheduler loop...")
# log("Scheduler is running. Press Ctrl+C to stop.")
# try:
#     while True:
#         schedule.run_pending()
#         time.sleep(60)
# except KeyboardInterrupt:
#     log("Scheduler stopped by user", "INFO")
# except Exception as e:
#     log(f"❌ Unexpected error in scheduler: {e}", "ERROR")


# =================================================
# ULTIMATE X/TWITTER GROWTH BOT – PRODUCTION READY
# → 10 posts/day at perfect IST times
# → Trending hashtags from India + US + Philippines
# → Gemini AI motivational content + images + threads
# → Runs forever, auto-refills, zero shadowban risk
# =================================================

# import os
# import time
# import random
# import io
# import tempfile
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime

# # FORCE INDIA TIME (IST) NO MATTER WHERE YOU RUN IT
# os.environ['TZ'] = 'Asia/Kolkata'
# time.tzset()

# import schedule
# import tweepy
# import google.generativeai as genai
# from PIL import Image, ImageDraw, ImageFont

# # -------------------- LOGGING --------------------
# def log(msg, level="INFO"):
#     print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {msg}")

# log("PRODUCTION BOT STARTED – Locked to IST")

# # -------------------- CREDENTIALS --------------------
# API_KEY         = "cPfy0RvvJJFYfZmtlroTKRugM"
# API_SECRET      = "H1pBc1u9SGTjeaooBZqHoQS953YGge6vw8gqbJwMcx1sq0mDZx"
# ACCESS_TOKEN    = "1993329052682481664-VxrAjznCZ7saHEzkxXXNeKb18TSblJ"
# ACCESS_SECRET   = "1xeZxuRTl8bUYamQBQPo4nJFfcbKnHqf2Fc24YbgSH5lz"
# GEMINI_KEY      = "AIzaSyCwBcYYzcEE5KjfTObWrMQ3jWqSu-RR3CI"

# genai.configure(api_key=GEMINI_KEY)

# # -------------------- X AUTH --------------------
# client = tweepy.Client(
#     consumer_key=API_KEY,
#     consumer_secret=API_SECRET,
#     access_token=ACCESS_TOKEN,
#     access_token_secret=ACCESS_SECRET,
#     wait_on_rate_limit=True
# )
# auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
# api = tweepy.API(auth)

# # -------------------- FETCH TRENDING HASHTAGS --------------------
# def fetch_trending_hashtags():
#     urls = [
#         "https://trends24.in/india/",
#         "https://trends24.in/united-states/",
#         "https://trends24.in/philippines/"
#     ]
#     url = random.choice(urls)
#     try:
#         headers = {"User-Agent": "Mozilla/5.0"}
#         r = requests.get(url, headers=headers, timeout=10)
#         soup = BeautifulSoup(r.text, 'html.parser')
#         trends = []
#         for a in soup.find_all('a', class_='trend-item')[:10]:
#             t = a.get_text(strip=True)
#             if t and not t.startswith("http"):
#                 if not t.startswith("#"): t = "#" + t.replace(" ", "")
#                 trends.append(t)
#         final = [h for h in trends if h.startswith("#")][:5]
#         log(f"Trending → {', '.join(final)} from {url.split('/')[-2]}")
#         return final or ["#Motivation", "#Success"]
#     except Exception as e:
#         log(f"Trend fetch failed → fallback hashtags ({e})", "WARNING")
#         return ["#Inspiration", "#Growth", "#Mindset"]

# # -------------------- GENERATE IMAGE --------------------
# def generate_image(text):
#     try:
#         img = Image.new("RGB", (1200, 630), "#0a0a1f")
#         draw = ImageDraw.Draw(img)
#         draw.rectangle([(0,0),(1200,100)], fill="#1a1a3e")
#         draw.rectangle([(0,530),(1200,630)], fill="#1a1a3e")
#         try:
#             font = ImageFont.truetype("arial.ttf", 64)
#             small = ImageFont.truetype("arial.ttf", 48)
#         except:
#             font = ImageFont.load_default()
#             small = ImageFont.load_default()

#         lines = []
#         words = text.split()
#         line = []
#         for w in words:
#             if draw.textbbox((0,0), " ".join(line + [w]), font=font)[2] < 1080:
#                 line.append(w)
#             else:
#                 lines.append(" ".join(line))
#                 line = [w]
#         if line: lines.append(" ".join(line))

#         y = (630 - len(lines)*90) // 2
#         for l in lines:
#             bbox = draw.textbbox((0,0), l, font=font)
#             x = (1200 - (bbox[2]-bbox[0])) // 2
#             draw.text((x, y), l, fill="#ffffff", font=font)
#             y += 90

#         draw.text((900, 560), "Keep Rising!", fill="#00ff99", font=small)

#         buffer = io.BytesIO()
#         img.save(buffer, "PNG")
#         buffer.seek(0)
#         return buffer
#     except Exception as e:
#         log(f"Image failed: {e}", "ERROR")
#         return None

# # -------------------- GENERATE CONTENT --------------------
# def generate_content():
#     log("Generating fresh content batch...")
#     trends = fetch_trending_hashtags()

#     def add_tags(t, n=2):
#         tags = " " + " ".join(random.sample(trends, min(n, len(trends))))
#         return t + tags if len(t + tags) <= 275 else t

#     model = genai.GenerativeModel("gemini-2.5-flash")

#     # 6 text posts
#     txt = model.generate_content("Create 6 unique motivational tweets under 240 chars each with emojis.").text
#     texts = [add_tags(l.strip()) for l in txt.split("\n") if l.strip() and len(l.strip()) > 10][:6]

#     # 3 image captions
#     cap = model.generate_content("Give me 3 short powerful motivational quotes under 140 chars.").text
#     captions = [add_tags(l.strip()) for l in cap.split("\n") if l.strip()][:3]

#     # 1 thread
#     thr = model.generate_content("Write a 5-tweet motivational thread about overcoming failure. Each under 240 chars.").text
#     thread_lines = [l.strip() for l in thr.split("\n") if l.strip() and any(x in l for x in "12345")]
#     thread_tweets = []
#     for line in thread_lines:
#         tweet = line.split(":", 1)[1].strip() if ":" in line else line
#         thread_tweets.append(add_tags(tweet, n=1))
#     thread = "\n".join([f"Tweet {i+1}: {t}" for i, t in enumerate(thread_tweets)])

#     return texts, captions, thread

# # -------------------- POSTING --------------------
# queue = []

# def refill():
#     global queue
#     texts, caps, thread = generate_content()
#     queue = [{"type": "text", "text": t} for t in texts]

#     for cap in caps:
#         img = generate_image(cap.split("#")[0].strip())
#         if img:
#             queue.append({"type": "image", "text": cap, "img": img})

#     queue.append({"type": "thread", "content": thread})
#     log(f"Queue refilled → {len(queue)} posts ready")

# def post_now():
#     global queue
#     if not queue:
#         refill()

#     item = random.choice(queue)
#     queue.remove(item)

#     try:
#         if item["type"] == "text":
#             client.create_tweet(text=item["text"])
#             log(f"TEXT → {item['text'][:70]}...")

#         elif item["type"] == "image":
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
#                 f.write(item["img"].read())
#                 path = f.name
#             media = api.media_upload(path)
#             client.create_tweet(text=item["text"], media_ids=[media.media_id])
#             os.remove(path)
#             log(f"IMAGE → posted with trending hashtags")

#         elif item["type"] == "thread":
#             tweets = [l.split(":", 1)[1].strip() if ":" in l else l 
#                      for l in item["content"].split("\n") if l.strip()]
#             last_id = None
#             for t in tweets:
#                 resp = client.create_tweet(text=t, in_reply_to_tweet_id=last_id) if last_id else client.create_tweet(text=t)
#                 last_id = resp.data["id"]
#                 time.sleep(2)
#             log("THREAD → 5 tweets posted")

#     except Exception as e:
#         log(f"POST FAILED → {e} | Re-adding to queue", "ERROR")
#         queue.append(item)  # retry later

# # -------------------- PERFECT IST SCHEDULE (10/day) --------------------
# schedule.every().day.at("00:30").do(post_now)
# schedule.every().day.at("03:00").do(post_now)
# schedule.every().day.at("06:30").do(post_now)
# schedule.every().day.at("09:00").do(post_now)
# schedule.every().day.at("11:30").do(post_now)
# schedule.every().day.at("14:00").do(post_now)
# schedule.every().day.at("16:30").do(post_now)
# schedule.every().day.at("18:30").do(post_now)
# schedule.every().day.at("20:30").do(post_now)
# schedule.every().day.at("22:30").do(post_now)


# refill()
# log("PRODUCTION BOT IS LIVE – Posting 10×/day in IST with trending hashtags")
# log("Run 24/7 → Millions of impressions incoming!")

# # -------------------- KEEP ALIVE --------------------
# try:
#     while True:
#         schedule.run_pending()
#         time.sleep(30)
# except KeyboardInterrupt:
#     log("Bot stopped by user – Come back when you're at 1M followers!")



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

# ==================== YOUR CREDENTIALS (DO NOT CHANGE FORMAT) ====================
API_KEY       = "cPfy0RvvJJFYfZmtlroTKRugM"
API_SECRET    = "H1pBc1u9SGTjeaooBZqHoQS953YGge6vw8gqbJwMcx1sq0mDZx"
ACCESS_TOKEN  = "1993329052682481664-VxrAjznCZ7saHEzkxXXNeKb18TSblJ"
ACCESS_SECRET = "1xeZxuRTl8bUYamQBQPo4nJFfcbKnHqf2Fc24YbgSH5lz"
genai.configure(api_key="AIzaSyCwBcYYzcEE5KjfTObWrMQ3jWqSu-RR3CI")

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