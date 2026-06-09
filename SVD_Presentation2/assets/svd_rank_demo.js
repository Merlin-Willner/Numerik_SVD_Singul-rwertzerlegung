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

  function svgGrid(values, showNumbers, label) {
    const rows = values.length;
    const cols = values[0].length;
    const cell = 22;
    const width = cols * cell;
    const height = rows * cell;
    const parts = [
      `<svg class="svd-grid-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="${label}">`,
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

  function drawCanvas(container, values, label) {
    const rows = values.length;
    const cols = values[0].length;
    let canvas = container.querySelector("canvas");
    if (!canvas) {
      canvas = document.createElement("canvas");
      canvas.className = "svd-image-canvas";
      canvas.setAttribute("role", "img");
      container.innerHTML = "";
      container.appendChild(canvas);
    }

    canvas.width = cols;
    canvas.height = rows;
    canvas.setAttribute("aria-label", label);

    const context = canvas.getContext("2d");
    const imageData = context.createImageData(cols, rows);
    let offset = 0;
    for (let row = 0; row < rows; row += 1) {
      for (let col = 0; col < cols; col += 1) {
        const value = clampByte(values[row][col]);
        imageData.data[offset] = value;
        imageData.data[offset + 1] = value;
        imageData.data[offset + 2] = value;
        imageData.data[offset + 3] = 255;
        offset += 4;
      }
    }
    context.putImageData(imageData, 0, 0);
  }

  function renderImage(container, values, showNumbers, label, renderMode) {
    if (renderMode === "canvas") {
      drawCanvas(container, values, label);
      return;
    }
    container.innerHTML = svgGrid(values, showNumbers, label);
  }

  function dataFor(root) {
    const source = root.dataset.svdSource || "duck";
    if (source === "einstein") return window.EINSTEIN_SVD_DATA;
    return window.DUCK_SVD_DATA;
  }

  function storageCount(data, rank) {
    return rank * (data.rows + data.cols + 1);
  }

  function initDemo(root) {
    const data = dataFor(root);
    if (!data || root.dataset.ready === "true") return;
    root.dataset.ready = "true";

    const renderMode = root.dataset.render || "svg";
    const slider = root.querySelector('[data-role="rank-slider"]');
    const rankLabel = root.querySelector('[data-role="rank-label"]');
    const storageLabel = root.querySelector('[data-role="storage-label"]');
    const original = root.querySelector('[data-role="original-grid"]');
    const reconstructed = root.querySelector('[data-role="reconstructed-grid"]');

    slider.max = String(data.rank);
    slider.value = "1";
    renderImage(original, data.original, false, "Originalbild als Matrix", renderMode);

    function render() {
      const rank = Number(slider.value);
      const approx = reconstruct(data, rank);
      renderImage(reconstructed, approx, false, `Rang-${rank}-Rekonstruktion`, renderMode);
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
