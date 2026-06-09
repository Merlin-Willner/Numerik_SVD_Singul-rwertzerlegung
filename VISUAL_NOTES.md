# Visuelles Audit Protokoll: Luis Serrano SVD

## Allgemeine Ästhetik
- **Hintergrund**: Reines Weiß (`#ffffff`).
- **Typografie**: Moderner Sans-Serif Look (Inter / Helvetica).
- **Linienstärke**: Dünn und präzise (2px - 3px für Achsen).
- **Akzentfarben**: 
  - Blau (Input/U): `#007aff`
  - Gelb (Singulärwerte): `#ffcc00`
  - Rot (Output/V^T): `#ff3b30`

## Frame-Analyse & Umsetzung

| Zeit (s) | Frame | Visueller Inhalt | Geplante Umsetzung |
| :--- | :--- | :--- | :--- |
| 00:20 | 0001 | Titel "Singular Value Decomposition" | Schlichte, zentrierte Apple-Style Slide. |
| 00:45 | 0003 | 2D Koordinatensystem mit Gitter | SVG Gitter mit grauen Linien (`#e5e5ea`). |
| 01:05 | 0004 | Einheitskreis (Blau) | SVG Kreis mit Radius 80, zentriert. |
| 01:15 | 0005 | Verformung zur Ellipse (Rot) | SVG Ellipse, transformiert durch Matrix-Faktoren. |
| 03:00 | 0010 | Grüne Vektoren v1, v2 im Kreis | Elegante Pfeile mit `marker-end`. |
| 04:30 | 0015 | Formel A = UΣV^T erscheint | Große LaTeX-Formel mit farbigen Overlays. |
| 07:00 | 0021 | Skalierung (Sigma) isoliert | Gelbe Ellipse mit gestrichelten Hauptachsen. |
| 12:00 | 0036 | Film-User Matrix Tabelle | Cleane Apple-Tabelle mit runden Ecken. |
| 24:00 | 0072 | Bildkompression Gummiente | 10x10 schwarzes N auf weißem Grund. |

## Spezielle Assets
- **Buchstabe N**: 10x10 Matrix, Schwarz auf Weiß.
- **Gummiente**: Pixel-Art Stil für den Vergleich (Folie 11/12).
