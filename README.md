# YouTube Video Transcriber

A web application that transcribes YouTube videos using either YouTube's built-in captions or Whisper AI for speech-to-text conversion when captions are unavailable.

## Features

- Transcribe any YouTube video by URL
- Automatic fallback to Whisper AI if YouTube captions are unavailable
- Simple and intuitive web interface
- Support for various YouTube URL formats

## Prerequisites

- Python 3.8 or higher
- FFmpeg installed on your system
- Node.js (for development)

## Installation

1. Clone the repository:
bash
git clone https://github.com/anevski-stefan/youtube-transcriber
cd youtube-transcriber

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate 
```

3. Install the required Python packages:
```bash
pip install -r requirements.txt
```

4. Install FFmpeg:
- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
- **MacOS**: `brew install ffmpeg`
- **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)

## Usage

1. Start the backend server:
```bash
uvicorn backend.main:app --reload
```

2. Open `frontend/index.html` in your web browser

3. Enter a YouTube URL and click "Get Transcript"

## How It Works

1. The application first attempts to retrieve YouTube's own captions using the `youtube_transcript_api`
2. If captions are unavailable, it downloads the audio and uses OpenAI's Whisper model for transcription
3. The transcript is then displayed in the web interface

## Project Structure

- `frontend/index.html`: Web interface for the application
- `backend/main.py`: FastAPI backend server
- `backend/requirements.txt`: Python dependencies

## API Endpoints

### POST /transcribe
Accepts a YouTube URL and returns the video transcript.

Request body:
```json
{
    "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

Response:
```json
{
    "transcript": "The transcribed text...",
    "method": "youtube_captions" or "whisper"
}
```

## Error Handling

- Invalid YouTube URLs
- Failed transcription attempts
- Network connectivity issues
- Automatic cleanup of temporary audio files