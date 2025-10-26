#!/usr/bin/env python3
"""
YouTube Transcript Extractor
Extracts text transcripts from YouTube videos.

pip install youtube-transcript-api
"""

from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import argparse
import re
import sys
import os
from pathlib import Path


def extract_video_id(url_or_id: str) -> str:
    """
    Extract the video ID from common YouTube URL formats or return the input if it already looks like an ID.
    Supports watch, youtu.be, embed, shorts, and mobile subdomains.
    """
    s = url_or_id.strip()

    # If it already looks like a bare ID (11 chars, alnum, - and _), return as-is
    if re.fullmatch(r'[\w-]{11}', s):
        return s

    try:
        p = urlparse(s)
        host = (p.netloc or '').lower()

        # youtube.com/watch?v=...
        if 'youtube.com' in host or 'm.youtube.com' in host:
            qs = parse_qs(p.query)
            if 'v' in qs and qs['v']:
                return qs['v'][0]
            # /embed/<id> or /shorts/<id>
            parts = [x for x in p.path.split('/') if x]
            if len(parts) >= 2 and parts[0] in ('embed', 'shorts'):
                return parts[1]

        # youtu.be/<id>
        if 'youtu.be' in host:
            parts = [x for x in p.path.split('/') if x]
            if parts:
                return parts[0]
    except Exception:
        pass

    # Fallback: return original; upstream will throw if invalid
    return s


def pick_best_transcript(video_id: str, preferred_langs: list[str]) -> list[dict]:
    """
    Try to get a transcript in preferred languages only.
    Does NOT fall back to other languages.
    Uses the new API (v1.2.3+) which returns FetchedTranscript with snippets.
    """
    api = YouTubeTranscriptApi()

    # Try to fetch transcript with preferred languages only
    try:
        fetched = api.fetch(video_id, languages=preferred_langs)
        # Convert snippets to dict format for backward compatibility
        return [{'text': snippet.text, 'start': snippet.start, 'duration': snippet.duration}
                for snippet in fetched.snippets]
    except NoTranscriptFound:
        # Re-raise with more specific message
        raise
    except Exception:
        raise

    # If we got here, nothing worked
    raise NoTranscriptFound(
        video_id=video_id,
        requested_language_codes=preferred_langs,
        transcript_data=[]
    )


def clean_text(text: str, strip_stage_dirs: bool) -> str:
    if strip_stage_dirs:
        text = re.sub(r'\[(?:[^\]]+)\]', '', text)  # remove [Music], [Applause], etc.
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_video_title(video_id: str) -> str:
    """
    Try to get the video title. If it fails, return the video ID.
    """
    try:
        import requests
        response = requests.get(f'https://www.youtube.com/watch?v={video_id}')
        # Extract title from HTML
        match = re.search(r'<title>(.+?)</title>', response.text)
        if match:
            title = match.group(1)
            # Remove " - YouTube" suffix
            title = re.sub(r'\s*-\s*YouTube\s*$', '', title)
            return title
    except Exception:
        pass
    return video_id


def sanitize_filename(filename: str) -> str:
    """
    Remove or replace characters that are invalid in filenames.
    """
    # Replace invalid characters with underscores
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    # Limit length to 200 characters
    if len(filename) > 200:
        filename = filename[:200]
    return filename


def save_transcript_to_file(video_id: str, transcript_text: str, output_dir: str = '.') -> str:
    """
    Save transcript to a text file with a filename based on the video title.
    Returns the path to the saved file.
    """
    # Get video title and sanitize it
    title = get_video_title(video_id)
    safe_title = sanitize_filename(title)

    # Create filename
    filename = f"{safe_title}.txt"
    filepath = os.path.join(output_dir, filename)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Video ID: {video_id}\n")
        f.write(f"Title: {title}\n")
        f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
        f.write("\n" + "="*80 + "\n\n")
        f.write(transcript_text)

    return filepath


def get_transcript(video_url: str, languages: list[str], strip_stage_dirs: bool, debug: bool = False) -> str:
    video_id = extract_video_id(video_url)
    if debug:
        print(f"Debug: Extracted video ID: {video_id}")
    try:
        segments = pick_best_transcript(video_id, languages)
        transcript_text = ' '.join(seg['text'] for seg in segments)
        return clean_text(transcript_text, strip_stage_dirs)
    except TranscriptsDisabled:
        return "Error: Transcripts are disabled for this video."
    except NoTranscriptFound as e:
        if debug:
            print(f"Debug: NoTranscriptFound - {e}")

        # Check if the error mentions available languages
        error_msg = str(e)
        lang_str = ', '.join(languages)

        if "transcripts are available in the following languages" in error_msg.lower():
            # Extract available languages from error message if present
            return f"Error: No {lang_str} transcript found for this video. The video may have transcripts in other languages only."
        elif "ipblocked" in error_msg.lower() or "ip" in error_msg.lower() and "block" in error_msg.lower():
            return f"Error: {error_msg.lower()} :-Your IP has been temporarily blocked by YouTube due to too many requests. Please wait 15-30 minutes and try again."
        else:
            return f"Error: No {lang_str} transcript found for this video. Many Shorts and recent uploads do not have captions."
    except Exception as e:
        if debug:
            print(f"Debug: Exception type: {type(e).__name__}")
            print(f"Debug: Exception details: {e}")
            import traceback
            traceback.print_exc()
        msg = str(e)
        if "ipblocked" in msg.lower() or ("ip" in msg.lower() and "block" in msg.lower()):
            return f"--Error---: {msg.lower()} :- Your IP has been temporarily blocked by YouTube due to too many requests --. Please wait 15-30 minutes and try again."
        elif "no element found" in msg.lower():
            return "Error: Unable to fetch transcript. This video may not have captions available."
        return f"Error: {msg}"


def main():
    parser = argparse.ArgumentParser(description="Extract text transcript from a YouTube video.")
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument("--lang", "-l", action="append", default=None,
                        help="Preferred language code, can be given multiple times. Default: en")
    parser.add_argument("--keep-stage", action="store_true",
                        help="Keep bracketed stage directions like [Music].")
    parser.add_argument("--debug", "-d", action="store_true",
                        help="Enable debug output to troubleshoot issues.")
    parser.add_argument("--output-dir", "-o", default=".",
                        help="Directory to save transcript files. Default: current directory")
    parser.add_argument("--no-save", action="store_true",
                        help="Don't save to file, only print to console")
    args = parser.parse_args()

    # Handle language default properly
    if args.lang is None:
        args.lang = ["en"]

    print(f"Fetching transcript for: {args.url}")
    print(f"Preferred languages: {args.lang}\n")

    # Extract video ID
    video_id = extract_video_id(args.url)

    # Get transcript
    text = get_transcript(args.url, args.lang, strip_stage_dirs=not args.keep_stage, debug=args.debug)

    # Check if it's an error message
    if text.startswith("Error:"):
        print(text)
        return 1

    # Print to console
    print(text)
    print()

    # Save to file unless --no-save flag is set
    if not args.no_save:
        try:
            filepath = save_transcript_to_file(video_id, text, args.output_dir)
            print(f"\n✓ Transcript saved to: {filepath}")
        except Exception as e:
            print(f"\n✗ Failed to save transcript: {e}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
