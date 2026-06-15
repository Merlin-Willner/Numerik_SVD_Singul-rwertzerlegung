---
name: quarto-revealjs-pdf-export
description: Use when exporting a Quarto RevealJS presentation to PDF without breaking browser layout, especially when Chrome print preview, ?print-pdf, or screenshot-based PDFs cause layout shifts, clipping, or pixelation. Provides the tested decktape workflow for sharp RevealJS PDFs.
metadata:
  short-description: Export Quarto RevealJS decks to sharp PDFs
---

# Quarto RevealJS PDF Export

Use this skill when a Quarto/RevealJS deck must become a PDF that looks like the browser presentation.

## Preferred Workflow

Use `decktape`, not the normal Chrome print dialog.

1. Render the deck normally:

```bash
quarto render path/to/index.qmd
```

2. Start a local server from the rendered deck directory:

```bash
python3 -m http.server 8765
```

3. Export with decktape:

```bash
npx --yes decktape reveal --size 1280x720 --pause 1200 --load-pause 2500 \
  http://127.0.0.1:8765/index.html output.pdf
```

Match `--size` to the RevealJS `width` and `height` in the Quarto YAML.

## Why This Works

- Chrome print preview can reflow RevealJS slides and break CSS grids, SVG sizing, MathJax, and page boundaries.
- Screenshot-to-PDF preserves layout but makes the entire deck rasterized and visibly pixelated.
- `decktape reveal` drives RevealJS slide-by-slide and exports PDF pages without using the fragile browser print dialog.
- Text, formulas, and SVGs usually remain sharp/vector-like. True bitmap images and canvas-rendered content remain raster, which is expected.

## Validation Checklist

After export:

- Confirm the PDF has the expected number of pages.
- Open at least one visually dense slide and one image/canvas slide.
- Check for clipped content, broken grid layout, oversized SVGs, missing MathJax, or pixelated text.
- Stop the local server after validation.

## Known Pitfalls

- Do not use ordinary browser `Print -> Save as PDF` for RevealJS decks with custom CSS.
- Do not rely on `index.html?print-pdf` if it changes slide dimensions or drops content.
- Avoid screenshot PDFs unless layout preservation matters more than text sharpness.
- Give MathJax and interactive/canvas slides enough load time with `--load-pause` and `--pause`.

## Reusable Script

For a standard Quarto RevealJS deck, use:

```bash
bash ~/.codex/skills/quarto-revealjs-pdf-export/scripts/export_decktape_pdf.sh \
  path/to/deck-dir index.qmd output.pdf 1280x720
```
