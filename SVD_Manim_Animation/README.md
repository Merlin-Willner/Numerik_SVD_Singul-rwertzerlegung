# SVD Manim Animation

Diese Animation visualisiert die SVD einer 13x13-Gummienten-Matrix als Summe von Rang-1-Bausteinen:

```text
A ≈ σ1 u1 v1^T + σ2 u2 v2^T + σ3 u3 v3^T
```

Gezeigt wird pro Rang:

- welcher Teil von `U`, `Σ` und `V^T` verwendet wird
- wie `σ_i · u_i · v_i^T` einen Rang-1-Baustein bildet
- wie die kumulative Summe nach Rang 1, 2 und 3 gegen das Referenzbild aussieht

## Installation

Falls Manim noch nicht installiert ist:

```bash
python3 -m pip install -r requirements.txt
```

Je nach System braucht Manim zusätzlich LaTeX, FFmpeg und Pango/Cairo. Auf Windows ist die Installation über die offizielle Manim-Anleitung meist am robustesten.

## Rendern

Aus diesem Ordner:

```bash
manim -pql svd_rank_animation.py SVDRankBuildUp
```

Für die Puzzle-Transformation aus Folie 3 mit anschließender Zerlegung aus Folie 4:

```bash
manim -pql svd_puzzle_transformation.py SVDPuzzleTransformation
```

Nur die vier Zerlegungsschritte:

```bash
manim -pql svd_puzzle_transformation.py SVDPuzzleDecomposition
```

Für bessere Qualität:

```bash
manim -pqh svd_rank_animation.py SVDRankBuildUp
```

Das Video landet typischerweise unter:

```text
media/videos/svd_rank_animation/480p15/SVDRankBuildUp.mp4
```

bei hoher Qualität entsprechend unter `1080p60`.

## In Quarto einbinden

Nach dem Rendern kannst du das Video in Quarto mit dem Video-Shortcode einbinden:

```qmd
{{< video SVD_Manim_Animation/media/videos/svd_rank_animation/480p15/SVDRankBuildUp.mp4 >}}
```

Passe den Pfad an, falls du mit `-pqh` oder anderen Qualitätsstufen renderst.
