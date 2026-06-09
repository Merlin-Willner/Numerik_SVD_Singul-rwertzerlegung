(function () {
  function clampByte(value) {
    return Math.max(0, Math.min(255, Math.round(value)));
  }

  function reconstruct(data, rank) {
    const out = Array.from({ length: data.rows }, () => Array(data.cols).fill(0));
    for (let k = 0; k < rank; k += 1) {
      const sigma = data.s[k];
      for (let row = 0; row < data.rows; row += 1) {
        const left = data.u[row][k] * sigma;
        for (let col = 0; col < data.cols; col += 1) {
          out[row][col] += left * data.vt[k][col];
        }
      }
    }
    return out;
  }

  function svgGrid(values, showNumbers) {
    const rows = values.length;
    const cols = values[0].length;
    const cell = 22;
    const width = cols * cell;
    const height = rows * cell;
    const parts = [
      `<svg class="svd-grid-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="Rangrekonstruktion der Entenmatrix">`,
    ];

    for (let row = 0; row < rows; row += 1) {
      for (let col = 0; col < cols; col += 1) {
        const value = clampByte(values[row][col]);
        const hex = value.toString(16).padStart(2, "0");
        const fill = `#${hex}${hex}${hex}`;
        const x = col * cell;
        const y = row * cell;
        parts.push(`<rect x="${x}" y="${y}" width="${cell}" height="${cell}" fill="${fill}" stroke="#111" stroke-width="0.8"/>`);
        if (showNumbers) {
          const cls = value < 60 ? "light" : "dark";
          parts.push(`<text class="${cls}" x="${x + cell / 2}" y="${y + cell / 2}">${value}</text>`);
        }
      }
    }
    parts.push("</svg>");
    return parts.join("");
  }

  function storageCount(data, rank) {
    return rank * (data.rows + data.cols + 1);
  }

  function initDemo(root) {
    const data = window.DUCK_SVD_DATA;
    if (!data || root.dataset.ready === "true") return;
    root.dataset.ready = "true";

    const slider = root.querySelector('[data-role="rank-slider"]');
    const rankLabel = root.querySelector('[data-role="rank-label"]');
    const storageLabel = root.querySelector('[data-role="storage-label"]');
    const original = root.querySelector('[data-role="original-grid"]');
    const reconstructed = root.querySelector('[data-role="reconstructed-grid"]');

    slider.max = String(data.rank);
    slider.value = "1";
    original.innerHTML = svgGrid(data.original, false);

    function render() {
      const rank = Number(slider.value);
      const approx = reconstruct(data, rank);
      reconstructed.innerHTML = svgGrid(approx, false);
      rankLabel.textContent = String(rank);
      storageLabel.textContent = `${storageCount(data, rank)} statt ${data.rows * data.cols} Zahlen`;
    }

    slider.addEventListener("input", render);
    render();
  }

  function initAll() {
    document.querySelectorAll(".svd-rank-demo").forEach(initDemo);
  }

  document.addEventListener("DOMContentLoaded", initAll);
  document.addEventListener("slidechanged", initAll);
})();
