# Quick Usage Guide

## Basic Command (English Transcripts Only)

```bash
python yt-transcript.py "YOUTUBE_URL"
```

This will:
1. Extract the **English transcript only**
2. Print it to your console
3. Save it to a `.txt` file named after the video title

## Examples

### Extract from a regular video
```bash
python yt-transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Extract from YouTube Shorts
```bash
python yt-transcript.py "https://www.youtube.com/shorts/VIDEO_ID"
```

### Save to a specific folder
```bash
mkdir my_transcripts
python yt-transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" -o my_transcripts/
```

### Print only (don't save file)
```bash
python yt-transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" --no-save
```

## Important Notes

### English Only
- **By default, the script ONLY fetches English transcripts**
- If a video doesn't have English captions, you'll get an error
- The script will NOT automatically try other languages
- If you want other languages, use `--lang` (e.g., `--lang es` for Spanish)

### Output Files
- Files are saved in the current directory (or use `-o` to specify)
- Filename is based on the video title
- Format: `Video_Title_Here.txt`

### Common Errors

**"No en transcript found"**
- The video doesn't have English captions
- Try watching the video on YouTube to see if captions are available

**"IP has been temporarily blocked"**
- You made too many requests to YouTube
- Wait 15-30 minutes and try again
- This is a YouTube rate limit, not a script issue

**"Transcripts are disabled"**
- The video creator disabled captions for this video
- Nothing can be done - find a different video

## All Options

```bash
python yt-transcript.py <URL> [OPTIONS]

Options:
  --lang, -l         Language code (default: en)
  --output-dir, -o   Where to save files (default: current directory)
  --no-save          Don't save file, only print to console
  --keep-stage       Keep [Music], [Applause] markers in text
  --debug, -d        Show detailed error information
```

## Need Help?

Run with `--debug` to see detailed information:
```bash
python yt-transcript.py "URL" --debug
```

This will show:
- Extracted video ID
- Full error messages
- Stack traces for debugging
