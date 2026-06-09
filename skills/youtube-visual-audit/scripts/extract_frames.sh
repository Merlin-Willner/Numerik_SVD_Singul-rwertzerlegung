#!/bin/bash

# YouTube Visual Audit: Frame Extraction Script
# Usage: ./extract_frames.sh <youtube_url> <interval_seconds> <output_dir>

URL=$1
INTERVAL=$2
OUTPUT_DIR=$3

if [ -z "$URL" ] || [ -z "$INTERVAL" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: $0 <youtube_url> <interval_seconds> <output_dir>"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Establish YT-DLP path (assumed to be in ~/.local/bin/yt-dlp based on project setup)
YTDLP="$HOME/.local/bin/yt-dlp"

if [ ! -f "$YTDLP" ]; then
    echo "Error: yt-dlp not found at $YTDLP. Please install it first."
    exit 1
fi

echo "Retrieving stream URL..."
# We use a temp file to avoid session expiry issues if the stream is long
TEMP_VIDEO="temp_video_for_audit.mp4"

# Better approach for reliable extraction: download a lightweight version
$YTDLP -f "bestvideo[height<=720][ext=mp4]" -o "$TEMP_VIDEO" "$URL"

if [ $? -ne 0 ]; then
    echo "Error: Failed to download video stream."
    exit 1
fi

echo "Extracting frames every $INTERVAL seconds..."
ffmpeg -i "$TEMP_VIDEO" -vf "fps=1/$INTERVAL" -y "$OUTPUT_DIR/frame_%04d.jpg"

if [ $? -ne 0 ]; then
    echo "Error: ffmpeg extraction failed."
    rm "$TEMP_VIDEO"
    exit 1
fi

rm "$TEMP_VIDEO"
echo "Success: Frames extracted to $OUTPUT_DIR"
