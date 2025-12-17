import os, json, requests

# 1. LOAD DATA
raw_payload = os.getenv("AI_DATA", '{"title":"Wait", "script":"No data found"}')
data = json.loads(raw_payload)

# 2. GENERATE ASSETS
# Voiceover (Google TTS)
from gtts import gTTS
gTTS(text=data['script'], lang='en').save("voice.mp3")

# Background Image (Random high-quality image)
img_url = f"https://images.unsplash.com/photo-1461747541664-bf5f518061ee?q=80&w=1080&h=1920&fit=crop"
with open('bg.jpg', 'wb') as f:
    f.write(requests.get(img_url).content)

# 3. RENDER WITH FFMPEG (Bulletproof method)
os.system("ffmpeg -loop 1 -i bg.jpg -i voice.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest final.mp4")
print("Video created: final.mp4")
