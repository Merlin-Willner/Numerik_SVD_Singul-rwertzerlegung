# Visual slide checks

Use `capture_slides.ps1` from the repository root in PowerShell. It renders the
Reveal deck in a real browser and writes screenshots after a wait period so
MathJax and layout have time to settle.

Capture one slide by number:

```powershell
powershell -ExecutionPolicy Bypass -File .\SVD_Presentation2\tools\capture_slides.ps1 -Slide 4
```

Render Quarto first, then capture slide 4:

```powershell
powershell -ExecutionPolicy Bypass -File .\SVD_Presentation2\tools\capture_slides.ps1 -Render -Slide 4
```

Capture by Reveal section id:

```powershell
powershell -ExecutionPolicy Bypass -File .\SVD_Presentation2\tools\capture_slides.ps1 -Id rotation-skalierung-rotation
```

Capture all slides:

```powershell
powershell -ExecutionPolicy Bypass -File .\SVD_Presentation2\tools\capture_slides.ps1 -Render -All
```

Screenshots are written to `output/browser-slides/` by default.
