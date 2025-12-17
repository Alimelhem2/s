import os, json, requests
from gtts import gTTS

# 1. LOAD DATA FROM PIPEDREAM
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

# 3. DOWNLOAD BACKGROUND IMAGE (With verification)
# I've updated the URL to a more reliable 'tech' source
img_url = "https://source.unsplash.com/featured/1080x1920/?technology,galaxy"
img_response = requests.get(img_url, allow_redirects=True)

if img_response.status_code == 200 and 'image' in img_response.headers.get('Content-Type', ''):
    with open('bg.jpg', 'wb') as f:
        f.write(img_response.content)
    print("Image downloaded successfully.")
else:
    # FALLBACK: If download fails, create a solid black background
    print("Image download failed. Creating fallback background...")
    os.system("ffmpeg -f lavfi -i color=c=black:s=1080x1920:d=1 -vframes 1 bg.jpg")

# 4. RENDER FINAL VIDEO
# Added '-y' to overwrite and '-pix_fmt yuv420p' for mobile compatibility
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
