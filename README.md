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
```bash
git clone https://github.com/anevski-stefan/youtube-transcriber
cd youtube-transcriber
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the required Python packages:
```bash
cd backend
pip install -r requirements.txt
```

4. Install FFmpeg:
- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
- **MacOS**: `brew install ffmpeg`
- **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)

## Usage

1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

2. Open `frontend/index.html` in your web browser

3. Enter a YouTube URL and click "Get Transcript"

## Project Structure

```
youtube-transcriber/
├── backend/
│   ├── main.py           # FastAPI backend server
│   └── requirements.txt  # Python dependencies
├── frontend/
│   └── index.html       # Web interface
├── LICENSE              # MIT License
└── README.md           # Project documentation
```

## API Endpoints

### POST /transcribe
Accepts a YouTube URL and returns the video transcript and title.

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
    "method": "youtube_captions" or "whisper",
    "title": "Video Title"
}
```

## How It Works

1. The application extracts the video ID from various YouTube URL formats
2. It retrieves the video title using yt-dlp
3. The system first attempts to retrieve YouTube's own captions using the `youtube_transcript_api`
4. If captions are unavailable, it downloads the audio and uses OpenAI's Whisper model for transcription
5. Temporary audio files are automatically cleaned up after processing

## Error Handling

- Invalid YouTube URLs
- Failed transcription attempts
- Network connectivity issues
- Automatic cleanup of temporary audio files
- Graceful fallback between transcription methods

## Development

The project uses:
- FastAPI for the backend
- Whisper AI for speech-to-text
- youtube-transcript-api for captions
- yt-dlp for video information and audio extraction
- Modern CSS with flexbox for responsive design

## File Management

The project automatically handles temporary files:
- Temporary audio files are created with format: `temp_[VIDEO_ID].mp3`
- All temporary files are automatically cleaned up after processing
- Whisper model files are cached for better performance

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.