# YouTube Transcript Extractor

A Python command-line tool that extracts text transcripts from YouTube videos and saves them to text files.

## Features

- ✅ Extract transcripts from regular YouTube videos
- ✅ Support for YouTube Shorts
- ✅ Multiple URL format support (youtube.com, youtu.be, mobile, embed)
- ✅ English transcripts only (or specify other languages with --lang)
- ✅ Automatic file saving with video title as filename
- ✅ Clean text formatting (removes stage directions like [Music])
- ✅ Debug mode for troubleshooting

## Installation

1. Create a virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Extract transcript and save to file:
```bash
python yt-transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Command-Line Options

```bash
python yt-transcript.py <URL> [OPTIONS]
```

**Options:**
- `--lang`, `-l`: Preferred language code (default: `en`). Can be used multiple times.
- `--output-dir`, `-o`: Directory to save transcript files (default: current directory)
- `--keep-stage`: Keep bracketed stage directions like `[Music]`, `[Applause]`
- `--no-save`: Print transcript to console only, don't save to file
- `--debug`, `-d`: Enable debug output for troubleshooting

### Examples

**Extract English transcript:**
```bash
python yt-transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Extract Spanish transcript (if you want non-English):**
```bash
python yt-transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" --lang es
```

**Note:** By default, the script only fetches English transcripts. If you want transcripts in other languages, use the `--lang` flag. The script will NOT automatically fall back to other languages if English is not available.

**Save to specific directory:**
```bash
python yt-transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" --output-dir transcripts/
```

**Keep stage directions:**
```bash
python yt-transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" --keep-stage
```

**Print only (don't save):**
```bash
python yt-transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" --no-save
```

**YouTube Shorts:**
```bash
python yt-transcript.py "https://www.youtube.com/shorts/VIDEO_ID"
```

**Debug mode:**
```bash
python yt-transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" --debug
```

## Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`
- Just the video ID: `VIDEO_ID`

## Output Format

Transcripts are saved as `.txt` files with the following format:

```
Video ID: VIDEO_ID
Title: Video Title
URL: https://www.youtube.com/watch?v=VIDEO_ID

================================================================================

[Transcript text here...]
```

The filename is based on the video title (sanitized to remove invalid characters).

## Requirements

- Python 3.11+
- youtube-transcript-api >= 1.2.3
- requests >= 2.31.0

## Known Limitations

- Not all YouTube videos have transcripts (especially Shorts)
- Some videos may have transcripts disabled by the creator
- Rate limiting: Too many requests may temporarily block your IP

## Troubleshooting

**"No transcript found" error:**
- The video may not have captions/transcripts available
- Try a different language with `--lang`
- Use `--debug` to see detailed error information

**"IP Blocked" error:**
- You've made too many requests in a short time
- Wait a few minutes before trying again
- See the [youtube-transcript-api documentation](https://github.com/jdepoix/youtube-transcript-api) for workarounds

## License

MIT License - feel free to use and modify as needed.
