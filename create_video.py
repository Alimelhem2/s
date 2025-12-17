import os, json, re, googleapiclient.discovery, googleapiclient.http
from google.oauth2.credentials import Credentials
from gtts import gTTS
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip

# 1. AUTHENTICATION
creds = Credentials(
    None, 
    refresh_token=os.getenv("YT_REFRESH_TOKEN"),
    token_uri="https://oauth2.googleapis.com/token",
    client_id=os.getenv("YT_CLIENT_ID"),
    client_secret=os.getenv("YT_CLIENT_SECRET")
)
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

# 2. RENDER (Using AI Data from Pipedream)
raw_payload = os.getenv("AI_DATA")
ai_data = json.loads(re.search(r'\{.*\}', raw_payload, re.DOTALL).group())

print(f"Rendering: {ai_data['title']}")
gTTS(text=ai_data['script'], lang='en').save('v.mp3')
aud = AudioFileClip('v.mp3')
bg = ColorClip(size=(1080, 1920), color=(25, 25, 25)).set_duration(aud.duration)
txt = TextClip(ai_data['script'], fontsize=70, color='white', method='caption', size=(900, None)).set_duration(aud.duration).set_position('center')

CompositeVideoClip([bg, txt]).set_audio(aud).write_videofile('final.mp4', fps=24, codec='libx264')

# 3. UPLOAD AS PUBLIC SHORT
print("Uploading...")
youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {"title": ai_data['title'], "description": "#shorts", "categoryId": "22"},
        "status": {"privacyStatus": "public"}
    },
    media_body=googleapiclient.http.MediaFileUpload("final.mp4", chunksize=-1, resumable=True)
).execute()
print("Success!")
