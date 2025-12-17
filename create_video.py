import os, json, requests
from gtts import gTTS

# 1. LOAD DATA
try:
    raw_payload = os.getenv("AI_DATA")
    data = json.loads(raw_payload)
    print(f"Data received: {data['title']}")
except Exception as e:
    print(f"Error parsing AI_DATA: {e}")
    data = {"title": "Error", "script": "Could not read script data."}

# 2. GENERATE VOICEOVER
tts = gTTS(text=data['script'], lang='en')
tts.save("voice.mp3")

# 3. DOWNLOAD IMAGE
# Using a static high-quality image URL for testing to avoid 404s
img_url = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1080&h=1920&auto=format&fit=crop"
img_response = requests.get(img_url)
with open('bg.jpg', 'wb') as f:
    f.write(img_response.content)

# 4. RENDER FINAL VIDEO (The "Black Screen" Fix)
# -loop 1: Repeat the image
# -pix_fmt yuv420p: Standard format for all players
# -shortest: Stop the video as soon as the audio ends
cmd = (
    "ffmpeg -y -loop 1 -i bg.jpg -i voice.mp3 "
    "-c:v libx264 -tune stillimage -c:a aac -b:a 192k "
    "-pix_fmt yuv420p -shortest final.mp4"
)
os.system(cmd)

if os.path.exists("final.mp4"):
    print("SUCCESS: final.mp4 is ready!")
else:
    print("ERROR: Video rendering failed.")
