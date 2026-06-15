# Codex Skill: Quarto RevealJS PDF Export

This folder is a complete Codex skill.

Install it by copying the whole folder to:

```text
~/.codex/skills/quarto-revealjs-pdf-export
```

After copying, Codex can use the skill for exporting Quarto RevealJS presentations to PDF with decktape.

The folder must contain:

```text
quarto-revealjs-pdf-export/
  SKILL.md
  README.md
  scripts/
    export_decktape_pdf.sh
```

Requirements on the machine that exports the PDF:

- Quarto installed and available as `quarto`
- Node.js/npm installed so `npx` works
- Python 3 installed so `python3 -m http.server` works

Example:

```bash
bash ~/.codex/skills/quarto-revealjs-pdf-export/scripts/export_decktape_pdf.sh \
  path/to/deck-dir index.qmd output.pdf 1280x720
```
