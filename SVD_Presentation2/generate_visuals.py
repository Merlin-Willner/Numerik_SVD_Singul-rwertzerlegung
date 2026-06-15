from pathlib import Path
import json

import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch, FancyBboxPatch, Polygon
import numpy as np
from PIL import Image

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman", "CMU Serif", "DejaVu Serif"],
        "mathtext.fontset": "cm",
    }
)

OUT_DIR = Path(__file__).parent / "assets" / "generated"
OUT_DIR.mkdir(parents=True, exist_ok=True)
DUCK_PATH = Path(__file__).parent / "Folieninhalte" / "Gummiente.png"
EINSTEIN_PATH = Path(__file__).parent / "assets" / "Albert_Einstein_Gute_Qualität.jpg"
EINSTEIN_PRESENTATION_WIDTH = 600

RED = "#c62828"
BLUE = "#1e5aa8"
GREEN = "#2e7d32"
INK = "#111111"
MUTED = "#666666"
YELLOW = "#f2aa00"
SVDBLUE = "#1e88ff"
SVDRED = "#ff3b35"


def rotation_clockwise(degrees: float) -> np.ndarray:
    theta = np.deg2rad(degrees)
    return np.array(
        [
            [np.cos(theta), np.sin(theta)],
            [-np.sin(theta), np.cos(theta)],
        ]
    )


R90 = rotation_clockwise(90)
S = np.array([[0.45, 0.0], [0.0, 1.0]])
R45 = rotation_clockwise(45)

POINTS = np.array(
    [
        [0.0, 1.0],
        [-0.78, -0.58],
        [0.78, -0.58],
    ]
)
POINT_COLORS = [RED, BLUE, GREEN]


def duck_matrix() -> np.ndarray:
    image = Image.open(DUCK_PATH).convert("L")
    width, height = image.size
    if width != height or width % 13 != 0:
        raise ValueError(f"Expected square 13x13 pixel-art duck, got {image.size}")
    cell = width // 13
    values = np.zeros((13, 13), dtype=int)
    for row in range(13):
        for col in range(13):
            values[row, col] = int(image.getpixel((col * cell + cell // 2, row * cell + cell // 2)))
    return values


def luminance_to_hex(value: float) -> str:
    value = int(np.clip(round(value), 0, 255))
    return f"#{value:02x}{value:02x}{value:02x}"


def save_duck_matrix_svg():
    values = duck_matrix()
    cell = 34
    image_size = cell * 13
    matrix_x = 690
    top = 30
    arrow_y = top + image_size / 2
    width = matrix_x + image_size + 35
    height = top + image_size + 112

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>',
        '.label{font-family:"Computer Modern Serif","Latin Modern Roman",serif;fill:#666;font-size:34px;text-anchor:middle}',
        '.celltext{font-family:"Computer Modern Serif","Latin Modern Roman",serif;font-size:13px;text-anchor:middle;dominant-baseline:middle;fill:#111}',
        '.celltext.dark{fill:#fff}',
        '</style>',
        f'<rect x="30" y="{top}" width="{image_size}" height="{image_size}" fill="none" stroke="#111" stroke-width="3"/>',
    ]

    for row in range(13):
        for col in range(13):
            value = values[row, col]
            x = 30 + col * cell
            y = top + row * cell
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{luminance_to_hex(value)}"/>')

    parts.append(f'<text class="label" x="{30 + image_size / 2}" y="{top + image_size + 62}">Bild</text>')
    parts.append(
        f'<path d="M {30 + image_size + 95} {arrow_y} H {matrix_x - 95}" '
        'stroke="#111" stroke-width="8" fill="none" marker-end="url(#arrow)"/>'
    )
    parts.insert(
        1,
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#111"/></marker></defs>',
    )

    parts.append(f'<rect x="{matrix_x}" y="{top}" width="{image_size}" height="{image_size}" fill="none" stroke="#111" stroke-width="3"/>')
    for row in range(13):
        for col in range(13):
            value = values[row, col]
            x = matrix_x + col * cell
            y = top + row * cell
            text_class = "celltext dark" if value < 60 else "celltext"
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{luminance_to_hex(value)}" stroke="#111" stroke-width="1.5"/>')
            parts.append(f'<text class="{text_class}" x="{x + cell / 2}" y="{y + cell / 2}">{value}</text>')

    parts.append(f'<text class="label" x="{matrix_x + image_size / 2}" y="{top + image_size + 62}">Matrixwerte 0 bis 255</text>')
    parts.append("</svg>")
    (OUT_DIR / "duck_image_to_matrix.svg").write_text("\n".join(parts), encoding="utf-8")


def save_duck_original_grid_svg():
    values = duck_matrix()
    cell = 22
    size = cell * 13
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">',
    ]
    for row in range(13):
        for col in range(13):
            value = values[row, col]
            x = col * cell
            y = row * cell
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                f'fill="{luminance_to_hex(value)}" stroke="#111" stroke-width="0.8"/>'
            )
    parts.append(f'<rect x="0" y="0" width="{size}" height="{size}" fill="none" stroke="#111" stroke-width="2"/>')
    parts.append("</svg>")
    (OUT_DIR / "duck_original_grid.svg").write_text("\n".join(parts), encoding="utf-8")


def save_duck_svd_data():
    values = duck_matrix().astype(float)
    u, singular_values, vt = np.linalg.svd(values, full_matrices=True)
    payload = {
        "rows": int(values.shape[0]),
        "cols": int(values.shape[1]),
        "rank": int(len(singular_values)),
        "original": values.astype(int).tolist(),
        "u": np.round(u, 10).tolist(),
        "s": np.round(singular_values, 10).tolist(),
        "vt": np.round(vt, 10).tolist(),
    }
    js = "window.DUCK_SVD_DATA = " + json.dumps(payload, separators=(",", ":")) + ";\n"
    (OUT_DIR / "duck_svd_data.js").write_text(js, encoding="utf-8")


def save_einstein_svd_data():
    image = Image.open(EINSTEIN_PATH).convert("L")
    source_width, source_height = image.size
    target_height = round(source_height * EINSTEIN_PRESENTATION_WIDTH / source_width)
    image = image.resize((EINSTEIN_PRESENTATION_WIDTH, target_height), Image.Resampling.LANCZOS)
    values = np.array(image, dtype=float)
    u, singular_values, vt = np.linalg.svd(values, full_matrices=False)
    payload = {
        "rows": int(values.shape[0]),
        "cols": int(values.shape[1]),
        "sourceRows": int(source_height),
        "sourceCols": int(source_width),
        "rank": int(len(singular_values)),
        "original": values.astype(int).tolist(),
        "u": np.round(u, 8).tolist(),
        "s": np.round(singular_values, 8).tolist(),
        "vt": np.round(vt, 8).tolist(),
    }
    js = "window.EINSTEIN_SVD_DATA = " + json.dumps(payload, separators=(",", ":")) + ";\n"
    (OUT_DIR / "einstein_svd_data.js").write_text(js, encoding="utf-8")


def transform_points(points: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    return points @ matrix.T


def circle_points(matrix: np.ndarray | None = None, count: int = 480) -> np.ndarray:
    t = np.linspace(0, 2 * np.pi, count)
    pts = np.column_stack([np.cos(t), np.sin(t)])
    if matrix is not None:
        pts = transform_points(pts, matrix)
    return pts


def draw_shape(ax, matrix=None, points=None, label=None):
    boundary = circle_points(matrix)
    ax.plot(boundary[:, 0], boundary[:, 1], color=INK, linewidth=3.0, zorder=2)

    pts = POINTS if points is None else points
    if matrix is not None and points is None:
        pts = transform_points(POINTS, matrix)

    for (x, y), color in zip(pts, POINT_COLORS):
        ax.scatter([x], [y], s=260, color=color, edgecolor="white", linewidth=2.8, zorder=3)

    ax.set_aspect("equal")
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)
    ax.axis("off")
    if label:
        ax.text(0, -1.35, label, ha="center", va="top", fontsize=15, color=MUTED)


def draw_grid(ax, extent=1.5, step=0.25):
    ax.set_aspect("equal")
    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)
    ticks = np.arange(-extent, extent + 1e-9, step)
    for tick in ticks:
        ax.plot([-extent, extent], [tick, tick], color="#d0d0d0", linewidth=0.6, zorder=0)
        ax.plot([tick, tick], [-extent, extent], color="#d0d0d0", linewidth=0.6, zorder=0)
    ax.axhline(0, color="#666666", linewidth=1.1, zorder=1)
    ax.axvline(0, color="#666666", linewidth=1.1, zorder=1)


def draw_shape_on_grid(ax, matrix=None, line=False, label=None):
    draw_grid(ax)
    if line:
        direction = matrix @ np.array([0.0, 1.0]) if matrix is not None else np.array([0.0, 1.0])
        norm = np.linalg.norm(direction)
        if norm == 0:
            direction = np.array([1.0, 0.0])
        else:
            direction = direction / norm
        line_pts = np.array([-1.5 * direction, 1.5 * direction])
        ax.plot(line_pts[:, 0], line_pts[:, 1], color=INK, linewidth=3.1, zorder=2)
    else:
        boundary = circle_points(matrix)
        ax.plot(boundary[:, 0], boundary[:, 1], color=INK, linewidth=2.8, zorder=2)

    pts = transform_points(POINTS, matrix) if matrix is not None else POINTS
    for (x, y), color in zip(pts, POINT_COLORS):
        ax.scatter([x], [y], s=110, color=color, edgecolor="white", linewidth=1.8, zorder=3)

    ax.axis("off")
    if label:
        ax.text(0, -1.78, label, ha="center", va="top", fontsize=13, color=MUTED)


def add_arc_arrow(ax, xy_a, xy_b, rad=0.32, text=None):
    arrow = FancyArrowPatch(
        xy_a,
        xy_b,
        connectionstyle=f"arc3,rad={rad}",
        arrowstyle="-|>",
        mutation_scale=28,
        linewidth=3.4,
        color=INK,
        shrinkA=2,
        shrinkB=2,
    )
    ax.add_patch(arrow)
    if text:
        ax.text(
            (xy_a[0] + xy_b[0]) / 2,
            max(xy_a[1], xy_b[1]) + 0.75,
            text,
            ha="center",
            va="bottom",
            fontsize=15,
            color=MUTED,
        )


def save_puzzle():
    final_matrix = R45 @ S @ R90
    fig, ax = plt.subplots(figsize=(11.6, 4.0))
    ax.set_xlim(0, 11.6)
    ax.set_ylim(0, 4.0)
    ax.axis("off")

    start_ax = ax.inset_axes([0.06, 0.12, 0.28, 0.76])
    draw_shape(start_ax, label="Ausgangsform")

    end_ax = ax.inset_axes([0.68, 0.12, 0.28, 0.76])
    draw_shape(end_ax, matrix=final_matrix, label="Zielbild")

    add_arc_arrow(ax, (4.30, 2.30), (7.40, 2.30), rad=-0.32, text="lineare Transformation")
    fig.savefig(OUT_DIR / "transformation_puzzle.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def save_steps():
    matrices = [
        np.eye(2),
        R90,
        S @ R90,
        R45 @ S @ R90,
    ]
    labels = ["Start", "Rotation", "Streckung", "Rotation"]

    fig, axes = plt.subplots(1, 4, figsize=(11.6, 2.8))
    for ax, matrix, label in zip(axes, matrices, labels):
        draw_shape(ax, matrix=matrix)
        ax.text(0, -1.35, label, ha="center", va="top", fontsize=15, color=INK)

    fig.savefig(OUT_DIR / "transformation_steps.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def save_step_actions():
    matrices = [
        np.eye(2),
        R90,
        S @ R90,
        R45 @ S @ R90,
    ]
    fig, ax = plt.subplots(figsize=(12.0, 4.25))
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 4.25)
    ax.axis("off")

    xs = [0.45, 3.35, 6.25, 9.15]
    for x, matrix in zip(xs, matrices):
        sub = ax.inset_axes([x / 12.0, 0.43, 0.18, 0.55])
        draw_shape(sub, matrix=matrix)

    actions = ["Rotation", "Skalierung", "Rotation"]
    arrow_y = 2.55
    for i, action in enumerate(actions):
        start = xs[i] + 2.05
        end = xs[i + 1] - 0.12
        ax.add_patch(
            FancyArrowPatch(
                (start, arrow_y),
                (end, arrow_y),
                arrowstyle="-|>",
                mutation_scale=21,
                linewidth=2.4,
                color=INK,
            )
        )
        mid = (start + end) / 2
        ax.text(mid, 1.25, action, ha="center", va="center", fontsize=15, color=INK)

    fig.savefig(OUT_DIR / "transformation_step_actions.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def draw_small_matrix(ax, cx, cy, entries, color=INK, fontsize=11):
    """Zeichnet eine 2x2-Matrix mit eckigen Klammern (mathtext kann keine pmatrix)."""
    (a, b), (c, d) = entries
    colx, rowy = 0.30, 0.20
    for (ex, ey, txt) in (
        (cx - colx, cy + rowy, a),
        (cx + colx, cy + rowy, b),
        (cx - colx, cy - rowy, c),
        (cx + colx, cy - rowy, d),
    ):
        ax.text(ex, ey, txt, ha="center", va="center", fontsize=fontsize, color=color)
    bx, by, tick, lw = colx + 0.26, rowy + 0.16, 0.07, 1.4
    for sx, tdir in ((cx - bx, 1), (cx + bx, -1)):
        ax.plot([sx, sx], [cy - by, cy + by], color=color, lw=lw, solid_capstyle="round")
        ax.plot([sx, sx + tdir * tick], [cy + by, cy + by], color=color, lw=lw, solid_capstyle="round")
        ax.plot([sx, sx + tdir * tick], [cy - by, cy - by], color=color, lw=lw, solid_capstyle="round")


def save_svd_bridge():
    matrices = [
        np.eye(2),
        R90,
        S @ R90,
        R45 @ S @ R90,
    ]

    fig, ax = plt.subplots(figsize=(7.2, 4.7))
    ax.set_xlim(0, 7.2)
    ax.set_ylim(0, 4.7)
    ax.axis("off")

    xs = [0.18, 1.92, 3.66, 5.40]
    for x, matrix in zip(xs, matrices):
        sub = ax.inset_axes([x / 7.2, 0.51, 0.19, 0.37])
        draw_shape(sub, matrix=matrix)

    # (Farbe, Pfeil-Label = SVD-Faktor, Box-Notation, Matrix-Eintraege, Schriftgroesse der Matrix)
    actions = [
        (SVDRED, r"$V^T$", r"$R_{-90^\circ}$", ((r"$0$", r"$1$"), (r"$-1$", r"$0$")), 11),
        (YELLOW, r"$\Sigma$", r"$\Sigma$", ((r"$0.45$", r"$0$"), (r"$0$", r"$1$")), 11),
        (SVDBLUE, r"$U$", r"$R_{-45^\circ}$", ((r"$0.71$", r"$0.71$"), (r"$-0.71$", r"$0.71$")), 9.5),
    ]

    for i, (color, arrow_label, box_label, entries, mfs) in enumerate(actions):
        ax.add_patch(
            FancyArrowPatch(
                (xs[i] + 1.32, 3.05),
                (xs[i + 1] - 0.08, 3.05),
                arrowstyle="-|>",
                mutation_scale=18,
                linewidth=2.2,
                color=color,
            )
        )
        mid = (xs[i] + xs[i + 1] + 1.24) / 2
        ax.text(mid, 3.42, arrow_label, ha="center", va="center", fontsize=17, color=color)

        box = FancyBboxPatch(
            (mid - 0.74, 0.05),
            1.48,
            1.30,
            boxstyle="round,pad=0.035,rounding_size=0.045",
            linewidth=1.6,
            edgecolor=color,
            facecolor="none",
        )
        ax.add_patch(box)
        ax.text(mid, 1.06, box_label, ha="center", va="center", fontsize=15, color=color)
        draw_small_matrix(ax, mid, 0.46, entries, color=INK, fontsize=mfs)

    fig.savefig(OUT_DIR / "svd_bridge.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def save_dimension_reduction():
    sigma_rank1 = np.array([[0.0, 0.0], [0.0, 1.0]])
    matrices = [
        np.eye(2),
        R90,
        sigma_rank1 @ R90,
        R45 @ sigma_rank1 @ R90,
    ]
    labels = ["Start", "Vᵀ: drehen", "Σ₁: eine Richtung", "U: zurück drehen"]
    action_labels = [("Vᵀ", SVDRED), ("Σ₁", YELLOW), ("U", SVDBLUE)]

    fig, ax = plt.subplots(figsize=(12.0, 3.9))
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 3.9)
    ax.axis("off")

    xs = [0.35, 3.08, 5.81, 8.54]
    for x, label, matrix, is_line in zip(xs, labels, matrices, [False, False, True, True]):
        sub = ax.inset_axes([x / 12.0, 0.30, 0.19, 0.56])
        draw_shape_on_grid(sub, matrix=matrix, line=is_line, label=label)

    for i, (label, color) in enumerate(action_labels):
        start_x = xs[i] + 2.18
        end_x = xs[i + 1] - 0.18
        arrow_y = 2.02
        ax.add_patch(
            FancyArrowPatch(
                (start_x, arrow_y),
                (end_x, arrow_y),
                arrowstyle="-|>",
                mutation_scale=20,
                linewidth=2.2,
                color=color,
            )
        )
        ax.text((start_x + end_x) / 2, 2.34, label, ha="center", va="center", fontsize=18, color=color)

    fig.savefig(OUT_DIR / "dimension_reduction.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def save_rank1_matrix():
    # Compact layout: elements closer together so SVG ratio is ~2.1:1 (fills slide height better)
    fig, ax = plt.subplots(figsize=(5.9, 2.75))
    ax.set_xlim(0.30, 6.20)
    ax.set_ylim(0.40, 3.15)
    ax.axis("off")

    matrix = np.array(
        [
            [1, 2, 3, 4],
            [-1, -2, -3, -4],
            [2, 4, 6, 8],
            [10, 20, 30, 40],
        ]
    )
    left_vec = [1, -1, 2, 10]
    right_vec = [1, 2, 3, 4]

    def cell(x, y, w, h, text, fill="#ffffff", fontsize=15):
        rect = plt.Rectangle((x, y), w, h, facecolor=fill, edgecolor=INK, linewidth=1.15)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, str(text), ha="center", va="center", fontsize=fontsize, color=INK, fontweight="bold")

    cell_w = 0.48
    cell_h = 0.42
    x0 = 0.50
    y0 = 2.55
    for row in range(4):
        for col in range(4):
            cell(x0 + col * cell_w, y0 - row * cell_h, cell_w, cell_h, matrix[row, col])
    ax.text(x0 + 2 * cell_w, 0.72, "16 Zahlen", ha="center", va="center", fontsize=18, color=MUTED)

    # "=" and "·" at matrix center y=2.13 so formula aligns visually with the matrix
    ax.text(2.90, 2.13, "=", ha="center", va="center", fontsize=24, color=MUTED)

    vx = 3.22
    blue = "#19a7ff"
    for row, value in enumerate(left_vec):
        cell(vx, y0 - row * cell_h, cell_w, cell_h, value, fill=blue)

    ax.text(3.84, 2.13, r"$\cdot$", ha="center", va="center", fontsize=24, color=MUTED)

    hx = 4.05
    hy = 1.92  # center of row vector = 2.13 = matrix center
    green = "#55c63a"
    for col, value in enumerate(right_vec):
        cell(hx + col * cell_w, hy, cell_w, cell_h, value, fill=green)
    ax.text(hx + 2 * cell_w, 0.72, "8 Zahlen", ha="center", va="center", fontsize=18, color=MUTED)

    fig.savefig(OUT_DIR / "rank1_matrix.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def save_rank_approximation():
    SLIDE7_BLUE = "#19a7ff"
    SLIDE7_GREEN = "#55c63a"

    fig, ax = plt.subplots(figsize=(11.4, 2.6))
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0.85, 3.35)
    ax.axis("off")

    matrix = np.array(
        [
            [3, 1, 4, 1],
            [5, 9, 2, 6],
            [5, 3, 5, 8],
            [9, 7, 9, 3],
        ]
    )

    def cell(x, y, w, h, text="", fill="#ffffff", edge=INK, fontsize=14, color=INK):
        rect = plt.Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge, linewidth=1.05)
        ax.add_patch(rect)
        if text != "":
            ax.text(x + w / 2, y + h / 2, str(text), ha="center", va="center", fontsize=fontsize, color=color, fontweight="bold")

    cell_w = 0.38
    cell_h = 0.36
    x0 = 0.22
    y0 = 2.88
    for row in range(4):
        for col in range(4):
            cell(x0 + col * cell_w, y0 - row * cell_h, cell_w, cell_h, matrix[row, col])

    matrix_center_y = y0 - cell_h
    matrix_bottom = y0 - 4 * cell_h
    ax.text(x0 + 2 * cell_w, matrix_bottom - 0.16, "Rang 4", ha="center", va="top", fontsize=15, color=MUTED)
    ax.text(2.10, matrix_center_y, "=", ha="center", va="center", fontsize=26, color=MUTED)

    sigma_w = 0.44
    sigma_h = 0.44
    u_w = 0.38
    u_h = 1.52
    v_w = 1.30
    v_h = 0.38
    gap = 0.06
    center_y = matrix_center_y

    def rank1_solid_block(x_start, idx):
        sx = x_start
        sy = center_y - sigma_h / 2
        ax.add_patch(plt.Rectangle((sx, sy), sigma_w, sigma_h,
                                    facecolor=YELLOW, edgecolor=INK, linewidth=1.2))
        ax.text(sx + sigma_w / 2, center_y, rf"$\sigma_{idx}$",
                ha="center", va="center", fontsize=11, color=INK)

        ux = sx + sigma_w + gap
        uy = center_y - u_h / 2
        ax.add_patch(plt.Rectangle((ux, uy), u_w, u_h,
                                    facecolor=SLIDE7_BLUE, edgecolor=INK, linewidth=1.2))
        ax.text(ux + u_w / 2, center_y, rf"$\mathbf{{U}}_{idx}$",
                ha="center", va="center", fontsize=11, color=INK)

        vx = ux + u_w + gap
        vy = center_y - v_h / 2
        ax.add_patch(plt.Rectangle((vx, vy), v_w, v_h,
                                    facecolor=SLIDE7_GREEN, edgecolor=INK, linewidth=1.2))
        ax.text(vx + v_w / 2, center_y, rf"$\mathbf{{v}}_{idx}^T$",
                ha="center", va="center", fontsize=11, color=INK)

        block_w = sigma_w + gap + u_w + gap + v_w
        ax.text(x_start + block_w / 2, center_y - u_h / 2 - 0.18, "Rang 1",
                ha="center", va="top", fontsize=13, color=MUTED)

        return x_start + block_w

    x = 2.38
    x = rank1_solid_block(x, "1") + 0.22
    ax.text(x, center_y, "+", ha="center", va="center", fontsize=22, color=MUTED)
    x = rank1_solid_block(x + 0.22, "2") + 0.22
    ax.text(x, center_y, "+", ha="center", va="center", fontsize=22, color=MUTED)
    rank1_solid_block(x + 0.22, "3")

    fig.savefig(OUT_DIR / "rank_approximation.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def save_duck_rank_terms():
    values = duck_matrix().astype(float)
    u, singular_values, vt = np.linalg.svd(values, full_matrices=True)
    accents = [SVDBLUE, YELLOW, SVDRED]

    def draw_pixel_grid(matrix, x0, y0, cell, stroke="#111", show_values=False, normalize=False):
        display = matrix.copy().astype(float)
        if normalize:
            lo = display.min()
            hi = display.max()
            if hi > lo:
                display = (display - lo) / (hi - lo) * 255
            else:
                display = np.zeros_like(display) + 128
        for row in range(display.shape[0]):
            for col in range(display.shape[1]):
                value = display[row, col]
                rect = plt.Rectangle(
                    (x0 + col * cell, y0 - (row + 1) * cell),
                    cell,
                    cell,
                    facecolor=luminance_to_hex(value),
                    edgecolor=stroke,
                    linewidth=0.35,
                )
                ax.add_patch(rect)
                if show_values:
                    ax.text(x0 + (col + 0.5) * cell, y0 - (row + 0.5) * cell, str(int(round(value))), ha="center", va="center", fontsize=5)

    def draw_vector(ax, values_1d, x0, y0, cell_w, cell_h, vertical, color):
        scaled = values_1d / (np.max(np.abs(values_1d)) or 1)
        for idx, value in enumerate(scaled):
            alpha = 0.18 + 0.75 * abs(value)
            face = color
            if vertical:
                x = x0
                y = y0 - (idx + 1) * cell_h
            else:
                x = x0 + idx * cell_w
                y = y0 - cell_h
            rect = plt.Rectangle((x, y), cell_w, cell_h, facecolor=face, alpha=alpha, edgecolor=INK, linewidth=0.25)
            ax.add_patch(rect)

    def draw_component(ax, idx, x, y, cell=0.048, label=True):
        component = singular_values[idx] * np.outer(u[:, idx], vt[idx, :])
        draw_pixel_grid(component, x, y, cell, stroke="#444", normalize=True)
        if label:
            ax.text(
                x + component.shape[1] * cell / 2,
                y - component.shape[0] * cell - 0.15,
                rf"$\sigma_{idx + 1}u_{idx + 1}v_{idx + 1}^T$",
                ha="center",
                va="top",
                fontsize=12,
                color=INK,
            )

    # Variante A: links Grafik, rechts erklärendes Textfeld.
    fig, ax = plt.subplots(figsize=(12.0, 4.55))
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 4.55)
    ax.axis("off")

    ax.text(0.45, 4.05, "Einzelne Beiträge der SVD", ha="left", va="center", fontsize=17, color=INK)
    card_xs = [0.45, 2.75, 5.05]
    for idx, x in enumerate(card_xs):
        color = accents[idx]
        ax.add_patch(plt.Rectangle((x, 0.55), 1.92, 3.30, facecolor="none", edgecolor=color, linewidth=1.8))
        ax.text(x + 0.16, 3.55, f"Beitrag {idx + 1}", ha="left", va="center", fontsize=13, color=color, fontweight="bold")
        ax.text(x + 0.96, 3.18, "Rang 1", ha="center", va="center", fontsize=13, color=INK)
        ax.text(x + 0.96, 2.86, rf"$\sigma_{idx + 1}={singular_values[idx]:.0f}$", ha="center", va="center", fontsize=12, color=MUTED)
        draw_component(ax, idx, x + 0.32, 2.55, cell=0.066, label=False)
        ax.text(x + 0.96, 0.82, rf"$\sigma_{idx + 1}u_{idx + 1}v_{idx + 1}^T$", ha="center", va="center", fontsize=12, color=INK)

    ax.plot([7.35, 7.35], [0.42, 4.05], color=INK, linewidth=1.6)
    ax.text(7.70, 3.78, "Wichtig:", ha="left", va="center", fontsize=17, color=INK)
    ax.text(7.70, 3.24, "Jeder einzelne Beitrag ist eine Matrix vom Rang 1.", ha="left", va="top", fontsize=14, color=INK, wrap=True)
    ax.text(7.70, 2.38, "Die Beiträge unterscheiden sich nicht im Rang, sondern in ihrem Singulärwert und in den beiden Richtungsvektoren.", ha="left", va="top", fontsize=14, color=INK, wrap=True)
    ax.text(7.70, 1.30, "Die kleinen Enten links sind einzeln normalisiert, damit man die Muster sehen kann. Sie sind noch nicht aufsummiert.", ha="left", va="top", fontsize=13, color=MUTED, wrap=True)
    fig.savefig(OUT_DIR / "duck_rank_terms_v1.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)

    # Variante B: Formelkarte mit explizitem Aufbau aus Vektor, Wert, Vektor.
    fig, ax = plt.subplots(figsize=(12.0, 4.55))
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 4.55)
    ax.axis("off")

    ax.text(0.45, 4.10, "Ein Rang-1-Beitrag besteht immer aus drei Teilen", ha="left", va="center", fontsize=18, color=INK)
    for idx, x in enumerate([0.55, 4.20, 7.85]):
        color = accents[idx]
        ax.add_patch(FancyBboxPatch((x, 0.62), 3.05, 3.25, boxstyle="round,pad=0.035,rounding_size=0.045", linewidth=1.7, edgecolor=color, facecolor="none"))
        ax.text(x + 1.52, 3.52, rf"$\sigma_{idx + 1}u_{idx + 1}v_{idx + 1}^T$", ha="center", va="center", fontsize=18, color=INK)
        draw_vector(ax, u[:, idx], x + 0.40, 2.95, 0.11, 0.135, True, SVDBLUE)
        ax.text(x + 0.45, 1.12, rf"$u_{idx + 1}$", ha="center", va="center", fontsize=14, color=SVDBLUE)
        ax.text(x + 1.25, 2.15, rf"$\sigma_{idx + 1}$", ha="center", va="center", fontsize=16, color=YELLOW)
        ax.text(x + 1.25, 1.74, f"{singular_values[idx]:.0f}", ha="center", va="center", fontsize=12, color=MUTED)
        draw_vector(ax, vt[idx, :], x + 1.70, 2.22, 0.075, 0.10, False, SVDRED)
        ax.text(x + 2.18, 1.72, rf"$v_{idx + 1}^T$", ha="center", va="center", fontsize=14, color=SVDRED)
        ax.text(x + 1.52, 0.92, "ergibt eine Rang-1-Matrix", ha="center", va="center", fontsize=12, color=MUTED)
    fig.savefig(OUT_DIR / "duck_rank_terms_v2.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)

    # Variante C: je Beitrag das Bild und direkt darunter die Zerlegung sigma * u(Spalte) * v^T(Zeile).
    fig, ax = plt.subplots(figsize=(12.0, 5.0))
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 5.0)
    ax.axis("off")

    contrib_x = [0.50, 2.65, 4.80]

    ax.text(0.45, 4.80, r"Jeder Rang-1-Beitrag: das Bild und direkt darunter die Zerlegung $\sigma_i\, u_i\, v_i^{T}$", ha="left", va="center", fontsize=15, color=INK)

    for idx, x in enumerate(contrib_x):
        color = accents[idx]
        ax.add_patch(FancyBboxPatch((x - 0.05, 1.45), 1.95, 3.02, boxstyle="round,pad=0.03,rounding_size=0.05", linewidth=1.6, edgecolor=color, facecolor="none"))
        # Name des Beitrags (oben)
        ax.text(x + 0.90, 4.28, rf"$\sigma_{idx + 1}u_{idx + 1}v_{idx + 1}^T$", ha="center", va="center", fontsize=13, color=INK)
        # Bild (Rang-1-Matrix)
        draw_component(ax, idx, x + 0.60, 4.05, cell=0.046, label=False)
        # Zerlegung darunter: Reihenfolge u(Spalte) * sigma * v^T(Zeile) -- wie A = U Sigma V^T
        ymid = 2.45
        # Spalte u_i (senkrecht, um ymid zentriert)
        draw_vector(ax, u[:, idx], x + 0.14, ymid + 0.60, 0.10, 0.092, True, SVDBLUE)
        ax.text(x + 0.19, ymid - 0.78, rf"$u_{idx + 1}$", ha="center", va="center", fontsize=11, color=SVDBLUE)
        ax.text(x + 0.43, ymid, r"$\cdot$", ha="center", va="center", fontsize=15, color=MUTED)
        # Singulaerwert sigma_i (Mitte)
        ax.text(x + 0.66, ymid + 0.13, rf"$\sigma_{idx + 1}$", ha="center", va="center", fontsize=14, color=YELLOW)
        ax.text(x + 0.66, ymid - 0.23, f"{singular_values[idx]:.0f}", ha="center", va="center", fontsize=10, color=MUTED)
        ax.text(x + 0.92, ymid, r"$\cdot$", ha="center", va="center", fontsize=15, color=MUTED)
        # Zeile v_i^T (waagerecht, um ymid zentriert)
        draw_vector(ax, vt[idx, :], x + 1.02, ymid + 0.045, 0.055, 0.088, False, SVDRED)
        ax.text(x + 1.38, ymid - 0.30, rf"$v_{idx + 1}^{{T}}$", ha="center", va="center", fontsize=11, color=SVDRED)

    # Summation rechts (auf Hoehe der Bilder)
    ax.text(2.47, 4.02, "+", ha="center", va="center", fontsize=18, color=MUTED)
    ax.text(4.62, 4.02, "+", ha="center", va="center", fontsize=18, color=MUTED)
    ax.text(6.95, 4.02, r"$\longrightarrow$", ha="center", va="center", fontsize=24, color=INK)
    cumulative = np.zeros_like(values)
    for idx in range(3):
        cumulative += singular_values[idx] * np.outer(u[:, idx], vt[idx, :])
    draw_pixel_grid(cumulative, 7.40, 4.35, 0.052, stroke="#444", normalize=False)
    ax.text(7.74, 3.50, r"$A_3=\sum_{i=1}^{3}\sigma_i u_i v_i^T$", ha="center", va="center", fontsize=11, color=INK)
    draw_pixel_grid(values, 9.55, 4.35, 0.052, stroke="#444", normalize=False)
    ax.text(9.89, 3.50, "Original", ha="center", va="center", fontsize=12, color=INK)

    # Erklaerung rechts unten
    ax.text(7.05, 2.95, r"Der Singulärwert $\sigma_i$ gewichtet den", ha="left", va="top", fontsize=11.5, color=INK)
    ax.text(7.05, 2.62, r"Beitrag; $u_i$ und $v_i^{T}$ geben das Muster.", ha="left", va="top", fontsize=11.5, color=INK)
    ax.text(7.05, 2.12, r"Je größer $\sigma_i$, desto stärker prägt", ha="left", va="top", fontsize=11, color=MUTED)
    ax.text(7.05, 1.84, r"der Beitrag das Bild.", ha="left", va="top", fontsize=11, color=MUTED)
    fig.savefig(OUT_DIR / "duck_rank_terms_v3.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def save_duck_rank_terms_v4():
    """Oben: 3 Rang-1-Pixel-Bilder + A3. Unten: sigma·U·V Zerlegung (Rang-1-Diagramm)."""
    values = duck_matrix().astype(float)
    u, singular_values, vt = np.linalg.svd(values, full_matrices=True)
    VGREEN = "#55c63a"

    fig, ax = plt.subplots(figsize=(12.0, 5.0))
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 5.0)
    ax.axis("off")

    def draw_grid(mat, x0, y0, cell, stroke="#555"):
        d = np.clip(np.round(mat), 0, 255).astype(int)
        for row in range(d.shape[0]):
            for col in range(d.shape[1]):
                ax.add_patch(plt.Rectangle(
                    (x0 + col * cell, y0 - (row + 1) * cell), cell, cell,
                    facecolor=luminance_to_hex(d[row, col]), edgecolor=stroke, linewidth=0.22))

    def draw_vec(vals, x0, y0, cw, ch, vertical, color):
        sc = vals / (np.max(np.abs(vals)) or 1)
        for i, v in enumerate(sc):
            a = 0.15 + 0.80 * abs(v)
            xy = (x0, y0 - (i + 1) * ch) if vertical else (x0 + i * cw, y0 - ch)
            ax.add_patch(plt.Rectangle(xy, cw, ch,
                                        facecolor=color, alpha=a,
                                        edgecolor="#333", linewidth=0.22))

    def norm255(mat):
        lo, hi = mat.min(), mat.max()
        return (mat - lo) / (hi - lo) * 255 if hi > lo else mat * 0 + 128

    # ── Geometrie ──────────────────────────────────────────────────
    sigma_w = 0.40
    u_cw, u_ch = 0.30, 0.10   # U-Spalte: 0.30 breit, 13*0.10=1.30 hoch
    v_cw, v_ch = 0.10, 0.28   # V-Zeile:  13*0.10=1.30 breit, 0.28 hoch
    u_h = 13 * u_ch            # 1.30
    v_w = 13 * v_cw            # 1.30
    GAP = 0.10
    u_off = sigma_w + GAP      # 0.50
    v_off = u_off + u_cw + GAP # 0.90
    TERM_W = v_off + v_w       # 2.20

    term_cx = [2.40, 5.30, 8.20]               # horizontale Mittelpunkte der Terme
    term_xs = [cx - TERM_W / 2 for cx in term_cx]  # linke Kanten

    vec_cy = 1.60    # vertikaler Mittelpunkt der unteren Zerlegung
    duck_y0 = 4.70   # obere Kante der Pixel-Bilder
    img_t = 1.30     # 13 * 0.10
    cell_t = 0.10

    components = [singular_values[i] * np.outer(u[:, i], vt[i, :]) for i in range(3)]
    cumul3 = components[0] + components[1] + components[2]

    # ── Unten: σ·U·V Rang-1-Diagramm ─────────────────────────────
    for i, tx in enumerate(term_xs):
        # σ-Box (gelb)
        ax.add_patch(FancyBboxPatch(
            (tx, vec_cy - 0.20), sigma_w, 0.40,
            boxstyle="round,pad=0.025", facecolor=YELLOW, edgecolor="#555", linewidth=1.3))
        ax.text(tx + sigma_w / 2, vec_cy, rf"$\sigma_{i+1}$",
                ha="center", va="center", fontsize=10, color=INK, fontweight="bold")

        # U-Spalte (blau)
        ux = tx + u_off
        draw_vec(u[:, i], ux, vec_cy + u_h / 2, u_cw, u_ch, True, SVDBLUE)
        ax.add_patch(plt.Rectangle((ux, vec_cy - u_h / 2), u_cw, u_h,
                                    facecolor="none", edgecolor=SVDBLUE, linewidth=1.6))
        ax.text(ux + u_cw / 2, vec_cy, rf"$u_{i+1}$",
                ha="center", va="center", fontsize=8, color="white", fontweight="bold")

        # V-Zeile (grün)
        vx = tx + v_off
        draw_vec(vt[i, :], vx, vec_cy + v_ch / 2, v_cw, v_ch, False, VGREEN)
        ax.add_patch(plt.Rectangle((vx, vec_cy - v_ch / 2), v_w, v_ch,
                                    facecolor="none", edgecolor=VGREEN, linewidth=1.6))
        ax.text(vx + v_w / 2, vec_cy, rf"$v_{i+1}^T$",
                ha="center", va="center", fontsize=8, color="white", fontweight="bold")

        ax.text(term_cx[i], 0.40, "Rang 1",
                ha="center", va="center", fontsize=11.5, color=MUTED)

    # "+" zwischen unteren Termen (gleiche x wie oben)
    for px in [(term_cx[0] + term_cx[1]) / 2, (term_cx[1] + term_cx[2]) / 2]:
        ax.text(px, vec_cy, "+", ha="center", va="center", fontsize=22, color=MUTED)

    # ── Trennlinie ─────────────────────────────────────────────────
    ax.plot([0.20, 11.80], [3.00, 3.00], color="#d8d8d8", linewidth=1.2)

    # ── Oben: Rang-1-Pixel-Bilder + A3 ───────────────────────────
    mid_y = duck_y0 - img_t / 2  # 4.45

    for i, cx in enumerate(term_cx):
        dx = cx - img_t / 2
        draw_grid(norm255(components[i]), dx, duck_y0, cell_t)
        # Neutraler Rahmen (kein Farbcode pro Term)
        ax.add_patch(plt.Rectangle((dx, duck_y0 - img_t), img_t, img_t,
                                    facecolor="none", edgecolor="#555", linewidth=1.5))
        # Farbige Formel-Labels oben: σᵢ gelb, uᵢ blau, vᵢᵀ grün
        ly = duck_y0 + 0.20
        ax.text(dx + 0.18, ly, rf"$\sigma_{i+1}$",
                ha="center", va="bottom", fontsize=11, color=YELLOW)
        ax.text(dx + 0.58, ly, rf"$u_{i+1}$",
                ha="center", va="bottom", fontsize=11, color=SVDBLUE)
        ax.text(dx + 1.00, ly, rf"$v_{i+1}^T$",
                ha="center", va="bottom", fontsize=11, color=VGREEN)
        # σ-Wert unter dem Bild
        ax.text(cx, duck_y0 - img_t - 0.08,
                rf"$\sigma_{i+1} = {singular_values[i]:.0f}$",
                ha="center", va="top", fontsize=9, color=MUTED)

    # "+" zwischen Pixel-Bildern (gleiche x wie untere "+")
    for px in [(term_cx[0] + term_cx[1]) / 2, (term_cx[1] + term_cx[2]) / 2]:
        ax.text(px, mid_y, "+", ha="center", va="center", fontsize=22, color=MUTED)

    # "=" und A3
    ax.text(9.65, mid_y, "=", ha="center", va="center", fontsize=22, color=INK)
    a3x = 10.05
    draw_grid(norm255(cumul3), a3x, duck_y0, cell_t)
    ax.add_patch(plt.Rectangle((a3x, duck_y0 - img_t), img_t, img_t,
                                facecolor="none", edgecolor="#555", linewidth=1.8))
    ax.text(a3x + img_t / 2, duck_y0 + 0.20, r"$A_3$",
            ha="center", va="bottom", fontsize=12, color=INK, fontweight="bold")

    fig.savefig(OUT_DIR / "duck_rank_terms_v4.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def save_duck_svd_first_component_layout():
    values = duck_matrix().astype(float)
    u, singular_values, vt = np.linalg.svd(values, full_matrices=True)
    rank = np.linalg.matrix_rank(values)

    fig, ax = plt.subplots(figsize=(13.8, 7.3))
    ax.set_xlim(0, 13.8)
    ax.set_ylim(0, 7.3)
    ax.axis("off")

    def draw_pixel_grid(matrix, x0, y0, cell, stroke="#111", show_values=False, normalize=False):
        display = matrix.copy().astype(float)
        if normalize:
            lo = display.min()
            hi = display.max()
            display = (display - lo) / (hi - lo) * 255 if hi > lo else np.zeros_like(display) + 128
        for row in range(display.shape[0]):
            for col in range(display.shape[1]):
                value = display[row, col]
                ax.add_patch(
                    plt.Rectangle(
                        (x0 + col * cell, y0 - (row + 1) * cell),
                        cell,
                        cell,
                        facecolor=luminance_to_hex(value),
                        edgecolor=stroke,
                        linewidth=0.5,
                    )
                )
                if show_values:
                    text_color = "white" if value < 70 else INK
                    ax.text(
                        x0 + (col + 0.5) * cell,
                        y0 - (row + 0.5) * cell,
                        str(int(round(value))),
                        ha="center",
                        va="center",
                        fontsize=5.0,
                        color=text_color,
                    )

    def draw_numeric_matrix(matrix, x, y, w, h, highlight=None, color="#1e88ff", max_rows=7, max_cols=7):
        rows, cols = matrix.shape
        shown = matrix[:max_rows, :max_cols]
        lines = []
        for r in range(max_rows):
            vals = [f"{shown[r, c]: .2f}" for c in range(max_cols)]
            lines.append("[" + " ".join(vals) + (" ..." if cols > max_cols else "") + "]")
        if rows > max_rows:
            lines.append("   ...")
        ax.text(
            x,
            y,
            "[\n" + "\n".join(lines) + "\n]",
            ha="left",
            va="top",
            fontsize=7.3,
            color=INK,
            family="DejaVu Sans Mono",
            linespacing=1.22,
        )
        row_h = h / (max_rows + 1.7)
        col_w = w / (max_cols + 1.7)
        if highlight == "col":
            ax.add_patch(
                FancyBboxPatch(
                    (x + 0.18, y - row_h * max_rows - 0.10),
                    col_w * 1.22,
                    row_h * max_rows + 0.18,
                    boxstyle="round,pad=0.03,rounding_size=0.04",
                    edgecolor=color,
                    facecolor="none",
                    linewidth=2.0,
                )
            )
        elif highlight == "row":
            ax.add_patch(
                FancyBboxPatch(
                    (x + 0.18, y - row_h - 0.01),
                    col_w * max_cols + 0.92,
                    row_h * 1.05,
                    boxstyle="round,pad=0.03,rounding_size=0.04",
                    edgecolor=color,
                    facecolor="none",
                    linewidth=2.0,
                )
            )

    def draw_sigma_matrix(x, y, cell=0.27, n=7):
        for row in range(n):
            for col in range(n):
                fill = "#ff341b" if row == col and row == 0 else "white"
                edge = INK if row == col and row == 0 else "#777777"
                lw = 2.0 if row == col and row == 0 else 0.75
                ax.add_patch(plt.Rectangle((x + col * cell, y - (row + 1) * cell), cell, cell, facecolor=fill, edgecolor=edge, linewidth=lw))
                if row == col:
                    val = singular_values[row] if row < len(singular_values) else 0
                    label = f"{val:.0f}" if row == 0 else f"{val:.1f}"
                    ax.text(x + (col + 0.5) * cell, y - (row + 0.5) * cell, label, ha="center", va="center", fontsize=5.7, color=INK)
        ax.text(x + 0.12, y + 0.18, r"$\Sigma$", ha="left", va="center", fontsize=13, color=YELLOW)

    ax.text(0.55, 6.82, "SVD der Entenmatrix: erster Rang-1-Beitrag", ha="left", va="center", fontsize=19, color=INK)
    draw_pixel_grid(values, 0.85, 6.40, 0.155, stroke="#333")
    ax.text(1.86, 4.20, rf"$A$ als Pixelmatrix, Rang ${rank}$", ha="center", va="center", fontsize=14, color=MUTED)
    ax.text(3.25, 5.36, r"$=$", ha="center", va="center", fontsize=25, color=MUTED)

    ax.text(0.55, 4.04, r"$U$", ha="left", va="center", fontsize=16, color=SVDBLUE)
    draw_numeric_matrix(u, 0.55, 3.85, 3.40, 1.90, highlight="col", color=SVDBLUE)
    ax.text(4.70, 3.32, r"$\times$", ha="center", va="center", fontsize=18, color=MUTED)
    draw_sigma_matrix(5.05, 3.85)
    ax.text(7.36, 3.32, r"$\times$", ha="center", va="center", fontsize=18, color=MUTED)
    ax.text(7.75, 4.04, r"$V^T$", ha="left", va="center", fontsize=16, color=SVDRED)
    draw_numeric_matrix(vt, 7.75, 3.85, 4.55, 1.90, highlight="row", color=SVDRED)

    component = singular_values[0] * np.outer(u[:, 0], vt[0, :])
    ax.text(3.05, 1.18, r"Der erste markierte Spalten-/Zeilenvektor liefert den ersten Bildbaustein:", ha="left", va="center", fontsize=14, color=INK)
    ax.text(3.05, 0.62, r"$\sigma_1$", ha="left", va="center", fontsize=24, color=YELLOW)
    ax.text(3.82, 0.62, r"$u_1$", ha="left", va="center", fontsize=24, color=SVDBLUE)
    ax.text(4.35, 0.62, r"$v_1^T$", ha="left", va="center", fontsize=24, color=SVDRED)
    ax.text(5.35, 0.62, rf"mit $\sigma_1={singular_values[0]:.0f}$", ha="left", va="center", fontsize=16, color=MUTED)
    ax.text(9.10, 2.58, r"$\sigma_1 u_1 v_1^T$", ha="center", va="center", fontsize=22, color=INK)
    draw_pixel_grid(component, 8.12, 2.30, 0.15, stroke="#777", normalize=True)
    ax.text(9.10, 0.10, "Rang 1, zur Sichtbarkeit skaliert", ha="center", va="bottom", fontsize=11, color=MUTED)

    fig.savefig(OUT_DIR / "duck_svd_first_component_layout.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def save_svd_rank_sum_reconstruction():
    fig, ax = plt.subplots(figsize=(13.8, 7.3))
    ax.set_xlim(0, 13.8)
    ax.set_ylim(0, 7.3)
    ax.axis("off")

    blue = SVDBLUE      # U   – Deck-Farbschema
    sigma_red = YELLOW  # Σ   – Deck-Farbschema
    green = "#55c63a"   # V^T – Deck-Farbschema
    grid = "#666666"

    def rect(x, y, w, h, fill="none", edge=INK, lw=1.6):
        patch = plt.Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge, linewidth=lw)
        ax.add_patch(patch)
        return patch

    def label(x, y, text, size=16, color=INK, weight="bold", ha="center", va="center"):
        ax.text(x, y, text, fontsize=size, color=color, fontweight=weight, ha=ha, va=va)

    def draw_matrix_grid(x, y, size, n=4, text="A"):
        cell = size / n
        for r in range(n):
            for c in range(n):
                rect(x + c * cell, y + (n - 1 - r) * cell, cell, cell, fill="white", edge=grid, lw=1.0)
        rect(x, y, size, size, fill="none", edge=grid, lw=1.0)
        label(x + size / 2, y + size / 2, text, size=28, color=INK, weight="bold")

    def draw_u_matrix(x, y, w, h, n=4):
        col = w / n
        for i in range(n):
            rect(x + i * col, y, col, h, fill=blue, edge=INK, lw=1.9)
            label(x + (i + 0.5) * col, y + h / 2, rf"$\mathbf{{U}}_{i + 1}$", size=18)
        rect(x, y, w, h, fill="none", edge=INK, lw=2.2)

    def draw_sigma_matrix(x, y, size, n=4):
        cell = size / n
        for r in range(n):
            for c in range(n):
                fill = sigma_red if r == c else "white"
                lw = 2.2 if r == c else 1.0
                edge = INK if r == c else grid
                rect(x + c * cell, y + (n - 1 - r) * cell, cell, cell, fill=fill, edge=edge, lw=lw)
                if r == c:
                    label(x + (c + 0.5) * cell, y + (n - r - 0.5) * cell, rf"$\sigma_{r + 1}$", size=17)
        rect(x, y, size, size, fill="none", edge=grid, lw=1.0)

    def draw_v_matrix(x, y, w, h, n=4):
        row = h / n
        for i in range(n):
            rect(x, y + (n - 1 - i) * row, w, row, fill=green, edge=INK, lw=1.9)
            label(x + w / 2, y + (n - i - 0.5) * row, rf"$\mathbf{{v}}_{i + 1}$", size=18)
        rect(x, y, w, h, fill="none", edge=INK, lw=2.2)

    def draw_rank_one_term(x, y, idx):
        rect(x, y + 0.84, 0.46, 0.46, fill=sigma_red, edge=INK, lw=2.0)
        label(x + 0.23, y + 1.07, rf"$\sigma_{idx}$", size=16)
        rect(x + 0.62, y, 0.45, 2.25, fill=blue, edge=INK, lw=2.0)
        label(x + 0.845, y + 1.12, rf"$\mathbf{{U}}_{idx}$", size=16)
        rect(x + 1.22, y + 0.83, 1.58, 0.52, fill=green, edge=INK, lw=2.0)
        label(x + 2.01, y + 1.09, rf"$\mathbf{{v}}_{idx}$", size=16)
        label(x + 1.68, y - 0.75, "Rang 1", size=20, color=MUTED, weight="normal")

    # Top product form
    draw_matrix_grid(1.55, 4.80, 1.80)
    label(4.30, 5.70, "=", size=22, color=MUTED, weight="normal")
    draw_u_matrix(5.25, 4.80, 1.80, 1.80)
    draw_sigma_matrix(7.90, 4.80, 1.80)
    draw_v_matrix(10.55, 4.80, 1.80, 1.80)

    # Bottom rank-one sum
    y = 1.33
    xs = [0.55, 3.88, 7.21, 10.54]
    for i, x in enumerate(xs, start=1):
        draw_rank_one_term(x, y, i)
        if i < 4:
            label(x + 3.03, y + 1.10, "+", size=23, color=MUTED, weight="normal")

    fig.savefig(OUT_DIR / "svd_rank_sum_reconstruction.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def save_intro_symbols():
    fig, ax = plt.subplots(figsize=(4.3, 4.0))
    ax.set_xlim(-1.15, 4.3)
    ax.set_ylim(0, 4.0)
    ax.set_aspect("equal")
    ax.axis("off")

    # Rotation glyph: a true circular arc so the arrowhead can be aligned
    # exactly along the tangent (a Bezier arc3 leaves the head visibly skewed).
    cx, cy, R = 1.78, 2.15, 1.02
    head_ang = np.deg2rad(316.0)          # arrowhead sits at lower-right
    tail_ang = np.deg2rad(46.0)           # open end at upper-right (gap on the right)
    head_len = 0.42                       # tip length along the tangent
    head_half_w = 0.29                    # half-width of the arrowhead base

    tang = np.array([-np.sin(head_ang), np.cos(head_ang)])  # CCW travel direction
    perp = np.array([-tang[1], tang[0]])
    end_pt = np.array([cx + R * np.cos(head_ang), cy + R * np.sin(head_ang)])

    # Draw the stroke counter-clockwise all the way to the head; the filled
    # arrowhead (same colour) is overlaid on top so there is no visible seam.
    ts = np.linspace(tail_ang, head_ang, 240)
    ax.plot(cx + R * np.cos(ts), cy + R * np.sin(ts), color=INK, lw=4.6, solid_capstyle="round")

    tip = end_pt + tang * (head_len * 0.62)
    base = end_pt - tang * (head_len * 0.38)
    ax.add_patch(Polygon([tip, base + perp * head_half_w, base - perp * head_half_w], closed=True, color=INK))
    ax.add_patch(FancyArrowPatch((0.55, 0.72), (3.55, 0.72), arrowstyle="<|-|>", mutation_scale=22, linewidth=4.8, color=INK))
    ax.add_patch(FancyArrowPatch((3.70, 0.95), (3.70, 3.35), arrowstyle="<|-|>", mutation_scale=22, linewidth=4.8, color=INK))
    ax.text(-1.05, 2.42, "Rotieren", fontsize=15, color=MUTED, ha="left", va="center")
    ax.text(2.05, 0.18, "Skalieren", fontsize=15, color=MUTED, ha="center")

    fig.savefig(OUT_DIR / "intro_transform_symbols.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    save_duck_matrix_svg()
    save_duck_original_grid_svg()
    save_duck_svd_data()
    save_einstein_svd_data()
    save_intro_symbols()
    save_puzzle()
    save_steps()
    save_step_actions()
    save_svd_bridge()
    save_dimension_reduction()
    save_rank1_matrix()
    save_rank_approximation()
    save_duck_rank_terms()
    save_duck_rank_terms_v4()
    save_duck_svd_first_component_layout()
    save_svd_rank_sum_reconstruction()
