from pathlib import Path
import json

import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch
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
        line_pts = np.array([-1.55 * direction, 1.55 * direction])
        ax.plot(line_pts[:, 0], line_pts[:, 1], color=INK, linewidth=3.0, zorder=2)
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

    actions = [
        ("Rotation", "R_-90°"),
        ("Skalierung", "Σ"),
        ("Rotation", "R_-45°"),
    ]
    arrow_y = 2.55
    for i, (action, formula) in enumerate(actions):
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
        ax.text(mid, 0.72, formula, ha="center", va="center", fontsize=18, color=MUTED)

    fig.savefig(OUT_DIR / "transformation_step_actions.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def save_svd_bridge():
    matrices = [
        np.eye(2),
        R90,
        S @ R90,
        R45 @ S @ R90,
    ]
    colors = [INK, SVDRED, YELLOW, SVDBLUE]
    labels = ["Start", "Rotation", "Skalierung", "Rotation"]

    fig, ax = plt.subplots(figsize=(7.0, 4.7))
    ax.set_xlim(0, 7.0)
    ax.set_ylim(0, 4.7)
    ax.axis("off")

    xs = [0.20, 1.85, 3.50, 5.15]
    for x, matrix, label, color in zip(xs, matrices, labels, colors):
        sub = ax.inset_axes([x / 7.0, 0.43, 0.19, 0.43])
        draw_shape(sub, matrix=matrix)
        ax.text(x + 0.66, 1.36, label, ha="center", va="center", fontsize=13, color=MUTED)

    for i, (color, label) in enumerate([(SVDRED, "Vᵀ"), (YELLOW, "Σ"), (SVDBLUE, "U")]):
        ax.add_patch(
            FancyArrowPatch(
                (xs[i] + 1.30, 2.62),
                (xs[i + 1] - 0.05, 2.62),
                arrowstyle="-|>",
                mutation_scale=16,
                linewidth=2.0,
                color=color,
            )
        )
        ax.text((xs[i] + xs[i + 1] + 1.25) / 2, 2.95, label, ha="center", va="center", fontsize=16, color=color)

    ax.text(
        3.5,
        0.48,
        "Vᵀ = R_-90°      Σ = diag(0.45, 1)      U = R_-45°",
        ha="center",
        va="center",
        fontsize=13,
        color=INK,
    )

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
    fig, ax = plt.subplots(figsize=(11.0, 3.8))
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 3.8)
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
    x0 = 0.85
    y0 = 2.55
    for row in range(4):
        for col in range(4):
            cell(x0 + col * cell_w, y0 - row * cell_h, cell_w, cell_h, matrix[row, col])
    ax.text(x0 + 2 * cell_w, 0.72, "16 Zahlen", ha="center", va="center", fontsize=18, color=MUTED)

    ax.text(3.65, 1.93, "=", ha="center", va="center", fontsize=24, color=MUTED)

    vx = 4.40
    blue = "#19a7ff"
    for row, value in enumerate(left_vec):
        cell(vx, y0 - row * cell_h, cell_w, cell_h, value, fill=blue)

    ax.text(5.28, 1.93, r"$\cdot$", ha="center", va="center", fontsize=24, color=MUTED)

    hx = 5.75
    hy = 1.72
    green = "#55c63a"
    for col, value in enumerate(right_vec):
        cell(hx + col * cell_w, hy, cell_w, cell_h, value, fill=green)
    ax.text(hx + 2 * cell_w, 0.72, "8 Zahlen", ha="center", va="center", fontsize=18, color=MUTED)

    ax.text(7.85, 2.48, r"$A = u v^T$", ha="left", va="center", fontsize=25, color=INK)
    ax.text(7.85, 1.82, "Alle Zeilen sind Vielfache\nvon (1, 2, 3, 4).", ha="left", va="top", fontsize=15, color=INK, linespacing=1.25)
    ax.text(7.85, 0.92, "Deshalb hat die Matrix Rang 1:\n4 Dimensionen, aber nur eine\nunabhängige Richtung.", ha="left", va="top", fontsize=14, color=MUTED, linespacing=1.25)

    fig.savefig(OUT_DIR / "rank1_matrix.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def save_rank_approximation():
    fig, ax = plt.subplots(figsize=(11.2, 3.8))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 3.8)
    ax.axis("off")

    matrix = np.array(
        [
            [3, 1, 4, 1],
            [5, 9, 2, 6],
            [5, 3, 5, 8],
            [9, 7, 9, 3],
        ]
    )

    def cell(x, y, w, h, text="", fill="#ffffff", fontsize=14):
        rect = plt.Rectangle((x, y), w, h, facecolor=fill, edgecolor=INK, linewidth=1.05)
        ax.add_patch(rect)
        if text != "":
            ax.text(x + w / 2, y + h / 2, str(text), ha="center", va="center", fontsize=fontsize, color=INK, fontweight="bold")

    cell_w = 0.42
    cell_h = 0.39
    x0 = 0.55
    y0 = 2.70
    for row in range(4):
        for col in range(4):
            cell(x0 + col * cell_w, y0 - row * cell_h, cell_w, cell_h, matrix[row, col])

    ax.text(x0 + 2 * cell_w, 0.78, "Rang 4", ha="center", va="center", fontsize=16, color=MUTED)
    ax.text(2.95, 1.95, "≈", ha="center", va="center", fontsize=24, color=MUTED)

    blue = "#19a7ff"
    green = "#55c63a"

    def rank_one_block(x, y, label, alpha):
        for row in range(4):
            cell(x, y0 - row * cell_h, cell_w, cell_h, "", fill=blue)
        ax.text(x + cell_w / 2, y0 - 4 * cell_h - 0.20, label, ha="center", va="center", fontsize=14, color=MUTED)
        hx = x + 0.74
        hy = y0 - 1.72 * cell_h
        for col in range(4):
            cell(hx + col * cell_w, hy, cell_w, cell_h, "", fill=green)
        ax.text(hx + 2 * cell_w, hy - 0.38, r"$u_i v_i^T$", ha="center", va="center", fontsize=15, color=MUTED)
        ax.text(x + 0.50, y0 + 0.18, alpha, ha="center", va="center", fontsize=16, color=YELLOW)

    rank_one_block(3.55, 1.80, "1. Baustein", r"$\sigma_1$")
    ax.text(6.05, 1.95, "+", ha="center", va="center", fontsize=22, color=MUTED)
    rank_one_block(6.65, 1.80, "2. Baustein", r"$\sigma_2$")
    ax.text(9.15, 1.95, "+", ha="center", va="center", fontsize=22, color=MUTED)
    ax.text(9.70, 1.95, "…", ha="left", va="center", fontsize=25, color=MUTED)

    ax.text(0.55, 3.42, "Voller Rang", ha="left", va="center", fontsize=16, color=INK)
    ax.text(3.55, 3.42, "Approximation durch Rang-1-Matrizen", ha="left", va="center", fontsize=16, color=INK)

    fig.savefig(OUT_DIR / "rank_approximation.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def save_duck_rank_terms():
    values = duck_matrix().astype(float)
    u, singular_values, vt = np.linalg.svd(values, full_matrices=True)
    accents = [RED, BLUE, GREEN]
    names = ["Rang 1", "Rang 2", "Rang 3"]

    fig, ax = plt.subplots(figsize=(12.0, 4.55))
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 4.55)
    ax.axis("off")

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

    def draw_vector(values_1d, x0, y0, cell_w, cell_h, vertical, color):
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

    duck_cell = 0.115
    draw_pixel_grid(values, 0.45, 3.98, duck_cell)
    ax.text(1.30, 2.22, "Ente als Matrix A", ha="center", va="center", fontsize=13, color=MUTED)

    ax.text(3.05, 3.55, r"$A = U\Sigma V^T$", ha="left", va="center", fontsize=30, color=INK)
    ax.text(3.05, 2.95, "Die SVD zerlegt die Bildmatrix in einzelne Rang-1-Beiträge.", ha="left", va="center", fontsize=15, color=INK)
    ax.text(3.05, 2.48, "Jeder Beitrag ist ein Spaltenvektor, ein Singulärwert und ein Zeilenvektor.", ha="left", va="center", fontsize=14, color=MUTED)

    card_y = 1.62
    card_xs = [0.35, 4.18, 8.01]
    for idx, x in enumerate(card_xs):
        color = accents[idx]
        component = singular_values[idx] * np.outer(u[:, idx], vt[idx, :])
        ax.add_patch(plt.Rectangle((x, 0.15), 3.25, 1.95, facecolor="none", edgecolor=color, linewidth=2.0))
        ax.text(x + 0.15, 1.90, f"{names[idx]} einzeln", ha="left", va="center", fontsize=13, color=color, fontweight="bold")

        draw_vector(u[:, idx], x + 0.20, card_y, 0.08, 0.10, True, color)
        ax.text(x + 0.36, 1.05, r"$u_" + str(idx + 1) + r"$", ha="center", va="center", fontsize=11, color=MUTED)

        ax.text(x + 0.72, 1.17, f"σ{idx + 1}", ha="center", va="center", fontsize=13, color=color)
        ax.text(x + 0.72, 0.82, f"{singular_values[idx]:.0f}", ha="center", va="center", fontsize=11, color=MUTED)

        draw_vector(vt[idx, :], x + 1.00, 1.20, 0.095, 0.08, False, color)
        ax.text(x + 1.62, 1.05, r"$v_" + str(idx + 1) + r"^T$", ha="center", va="center", fontsize=11, color=MUTED)

        ax.text(x + 2.08, 1.05, "=", ha="center", va="center", fontsize=16, color=MUTED)
        draw_pixel_grid(component, x + 2.32, 1.55, 0.052, stroke="#444", normalize=True)
        ax.text(x + 2.76, 0.72, r"$\sigma_" + str(idx + 1) + r"u_" + str(idx + 1) + r"v_" + str(idx + 1) + r"^T$", ha="center", va="center", fontsize=11, color=MUTED)

    fig.savefig(OUT_DIR / "duck_rank_terms.svg", format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)


def save_intro_symbols():
    fig, ax = plt.subplots(figsize=(4.3, 4.0))
    ax.set_xlim(0, 4.3)
    ax.set_ylim(0, 4.0)
    ax.axis("off")

    ax.add_patch(Arc((1.72, 2.42), 1.72, 1.72, theta1=28, theta2=318, linewidth=4.6, color=INK))
    ax.add_patch(
        FancyArrowPatch(
            (2.30, 1.93),
            (2.50, 1.76),
            arrowstyle="-|>",
            mutation_scale=27,
            linewidth=4.6,
            color=INK,
        )
    )
    ax.add_patch(FancyArrowPatch((0.55, 0.72), (3.55, 0.72), arrowstyle="<|-|>", mutation_scale=22, linewidth=4.8, color=INK))
    ax.add_patch(FancyArrowPatch((3.70, 0.95), (3.70, 3.35), arrowstyle="<|-|>", mutation_scale=22, linewidth=4.8, color=INK))
    ax.text(0.78, 0.18, "Rotieren", fontsize=15, color=MUTED)
    ax.text(2.35, 0.18, "Skalieren", fontsize=15, color=MUTED)

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
