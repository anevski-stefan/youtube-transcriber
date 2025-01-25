from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from pydantic import BaseModel
import whisper
import yt_dlp
import os
import re
from yt_dlp import YoutubeDL

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Whisper model (will download on first run)
model = whisper.load_model("base")

class YouTubeURL(BaseModel):
    url: str

def extract_video_id(url: str) -> str:
    # Handle different YouTube URL formats
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise HTTPException(status_code=400, detail="Invalid YouTube URL")

def download_audio(video_id: str) -> str:
    output_file = f"temp_{video_id}.mp3"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'temp_{video_id}.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
    
    return output_file

@app.post("/transcribe")
async def transcribe_video(youtube_url: YouTubeURL):
    try:
        video_id = extract_video_id(youtube_url.url)
        
        # Get video title
        with YoutubeDL() as ydl:
            info = ydl.extract_info(video_id, download=False)
            video_title = info['title']
        
        # First try to get YouTube's own transcription
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            full_transcript = " ".join([entry['text'] for entry in transcript_list])
            return {"transcript": full_transcript, "method": "youtube_captions", "title": video_title}
        except:
            # If YouTube transcription fails, use Whisper
            try:
                # Download audio
                audio_file = download_audio(video_id)
                
                # Transcribe using Whisper
                result = model.transcribe(audio_file)
                
                # Clean up the audio file
                if os.path.exists(audio_file):
                    os.remove(audio_file)
                
                return {"transcript": result["text"], "method": "whisper", "title": video_title}
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Whisper transcription failed: {str(e)}")
                
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Add cleanup endpoint to remove temporary files
@app.on_event("shutdown")
async def cleanup():
    # Remove any remaining temporary files
    for file in os.listdir():
        if file.startswith("temp_") and file.endswith(".mp3"):
            os.remove(file)
