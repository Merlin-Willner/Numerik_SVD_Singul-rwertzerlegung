---
name: youtube-visual-audit
description: Automated extraction of frames from YouTube videos for high-fidelity visual reconstruction and audit tasks. Use this when the agent needs to "see" specific moments in a video to replicate drawings, UI layouts, or pedagogical steps.
---

# YouTube Visual Audit

This skill enables the extraction of static frames from YouTube videos at specified intervals. It is designed to bridge the gap between video content and visual reconstruction tasks.

## Prerequisites

- `yt-dlp` must be installed in `~/.local/bin/yt-dlp`.
- `ffmpeg` must be available in the system PATH.

## Usage

Use the provided script to extract frames:

```bash
bash skills/youtube-visual-audit/scripts/extract_frames.sh <youtube_url> <interval_in_seconds> <output_directory>
```

### Visual Analysis Workflow

1. **Extraction**: Run the script to generate a series of JPEGs (e.g., one frame every 20 seconds).
2. **Cataloging**: List the files in the output directory to confirm density.
3. **Analysis**: Use image analysis tools or multi-modal capabilities to describe the visual state of key frames.
4. **Reconstruction**: Translate visual findings (colors, arrow styles, layout proportions) into code (e.g., SVG, CSS, Quarto).

## Best Practices

- **Interval**: 20-30 seconds is usually sufficient for whiteboard-style lectures. For UI/UX audits, use 1-5 seconds.
- **Cleanup**: The script automatically handles temporary video downloads to ensure session persistence during extraction.
- **Visibility**: Always store frames in a project-visible subfolder (e.g., `visual_audit/`) so they can be referenced by the user and other models.
