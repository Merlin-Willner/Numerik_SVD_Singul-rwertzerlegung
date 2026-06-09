# AGENT.md

## Erfolgreiche Prozesse

- Die Präsentation in `SVD_Presentation2` bauen und `SVD_Presentation` nicht referenzieren. Der alte Ordner ist inhaltlich tabu.
- Quarto/RevealJS für Folienstruktur, Navigation, MathJax und Layout verwenden.
- Die mathematischen Transformationsgrafiken mit `generate_visuals.py` erzeugen:
  - Kreis-/Ovalpunkte werden über Matrizen berechnet.
  - SVGs liegen unter `assets/generated/`.
  - Matrixbilder und SVD-Daten werden ebenfalls aus dem Generator erzeugt.
  - Nach Änderungen am Generator immer neu ausführen und danach Quarto rendern.
- Für reproduzierbares Generieren:
  ```bash
  python3 -m venv /tmp/svd_quarto_venv
  . /tmp/svd_quarto_venv/bin/activate
  pip install -r SVD_Presentation2/requirements.txt
  python SVD_Presentation2/generate_visuals.py
  quarto render SVD_Presentation2/index.qmd
  ```
- Wenn die `/tmp`-Umgebung schon existiert, reichen:
  ```bash
  . /tmp/svd_quarto_venv/bin/activate
  python SVD_Presentation2/generate_visuals.py
  quarto render SVD_Presentation2/index.qmd
  ```
- Für visuelle Prüfung lokal aus `SVD_Presentation2` serven:
  ```bash
  python3 -m http.server 8765
  ```
  Danach Browser/Playwright gegen `http://127.0.0.1:8765/index.html` verwenden.

## Stolpersteine vermeiden

- Keine Raw-HTML-Blöcke in `index.qmd` für normale Folienstruktur verwenden. Quarto fenced divs (`:::`), Markdown-Bilder und normale Math-Blöcke sind stabiler und besser wartbar.
- Keine handgeschriebenen Inline-SVGs in der QMD für Transformationsgrafiken verwenden. Sie sind schwer zu pflegen und werden schnell falsch skaliert.
- Matplotlib nicht im OneDrive-Projektordner in eine `.venv` installieren. Das ist auf diesem Pfad sehr langsam. Für temporäre Arbeit `/tmp/svd_quarto_venv` nutzen.
- Markdown-Bilder nicht mit sichtbarem Alt-Text schreiben, wenn keine Caption gewünscht ist. Stattdessen:
  ```markdown
  ![](assets/generated/example.svg){fig-alt="Beschreibung"}
  ```
- Quarto-Klassen nicht als nachgestellte `{.class}` hinter normale Absätze setzen, wenn sie literal erscheinen. Stattdessen fenced divs verwenden:
  ```markdown
  ::: {.lead-text}
  Text
  :::
  ```
- Besser als Rasteroverlay: Matrixgrafiken als eine einzige SVG erzeugen. `duck_image_to_matrix.svg` zeichnet jede Zelle als eigenes Rechteck und vermeidet Subpixel-Verschiebungen zwischen Bild und CSS-Raster.
- Für interaktive Rang-k-Demos keine SVD im Browser neu faktorisieren. Python/NumPy soll `U`, `S`, `V^T` vorberechnen und als `duck_svd_data.js` ausgeben. Der Browser setzt dann pro Sliderwert nur die Rang-k-Summe zusammen.
- Lokale Daten lieber als JS-Konstante einbinden als per `fetch()` laden. Dadurch funktioniert die Folie stabiler mit Quarto/Reveal und vermeidet lokale Dateizugriffsprobleme.
- Für LaTeX-ähnliche Schrift nicht nur auf lokale Fonts hoffen. `header.html` bindet aktuell Computer Modern Webfont ein; offline müsste diese Schrift lokal ins Projekt kopiert werden.
- Nach jedem visuellen Eingriff nicht nur `quarto render` prüfen, sondern mindestens die betroffenen Folien im Browser ansehen.

## Aktueller Stack

- Quarto + RevealJS: Folien
- CSS: Layout, Typografie, Matrixraster
- MathJax: Formeln
- Python + NumPy + Matplotlib: generierte SVG-Visualisierungen
- JavaScript: interaktive Rang-k-Rekonstruktion aus vorberechneten SVD-Faktoren
- PNG: Pixel-Ente in `Folieninhalte/Gummiente.png`
