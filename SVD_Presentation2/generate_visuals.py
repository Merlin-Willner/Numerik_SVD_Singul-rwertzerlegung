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


def save_intro_symbols():
    fig, ax = plt.subplots(figsize=(4.3, 4.0))
    ax.set_xlim(0, 4.3)
    ax.set_ylim(0, 4.0)
    ax.axis("off")

    ax.add_patch(
        FancyArrowPatch(
            (0.95, 2.45),
            (2.68, 2.45),
            connectionstyle="arc3,rad=-1.05",
            arrowstyle="-|>",
            mutation_scale=26,
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
