from __future__ import annotations

import numpy as np
from manim import *


config.background_color = "#ffffff"
config.frame_width = 16
config.frame_height = 9
config.pixel_width = 1920
config.pixel_height = 1080


U_COLOR = "#007aff"
SIGMA_COLOR = "#ffb000"
VT_COLOR = "#ff3b30"
SUM_COLOR = "#34c759"
INK = "#111111"
MUTED = "#6e6e73"
GRID = "#d8d8de"


REFERENCE = np.array(
    [
        [0, 0, 0, 105, 105, 105, 105, 0, 0, 0, 0, 0, 0],
        [0, 0, 105, 105, 105, 105, 105, 105, 0, 0, 0, 0, 0],
        [0, 105, 105, 105, 105, 105, 105, 105, 105, 0, 0, 0, 0],
        [0, 105, 105, 105, 255, 105, 105, 105, 105, 0, 0, 0, 0],
        [175, 175, 175, 105, 105, 105, 105, 105, 105, 0, 0, 0, 0],
        [0, 175, 175, 105, 105, 105, 105, 105, 0, 0, 0, 0, 0],
        [0, 0, 0, 105, 105, 105, 105, 0, 0, 0, 0, 105, 105],
        [0, 0, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105],
        [0, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 0],
        [0, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 0],
        [0, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 0, 0],
        [0, 0, 105, 105, 105, 105, 105, 105, 105, 105, 0, 0, 0],
        [0, 0, 0, 105, 105, 105, 105, 105, 105, 0, 0, 0, 0],
    ],
    dtype=float,
)


def t(text: str, size: int = 28, color: str = INK, weight: str = "NORMAL") -> Text:
    return Text(text, font="Arial", font_size=size, color=color, weight=weight)


def gray_from_darkness(value: float) -> str:
    gray = int(np.clip(255 - value, 0, 255))
    return rgb_to_hex((gray / 255, gray / 255, gray / 255))


def diverging_color(value: float, limit: float) -> str:
    if limit <= 0:
        return "#f5f5f7"
    x = float(np.clip(value / limit, -1, 1))
    if x >= 0:
        base = np.array(hex_to_rgb(U_COLOR))
    else:
        base = np.array(hex_to_rgb(VT_COLOR))
    white = np.ones(3)
    rgb = white * (1 - abs(x)) + base * abs(x)
    return rgb_to_hex(rgb)


def image_grid(values: np.ndarray, cell: float = 0.13, outline: bool = True) -> VGroup:
    group = VGroup()
    rows, cols = values.shape
    for r in range(rows):
        for c in range(cols):
            square = Square(
                side_length=cell,
                stroke_width=0.7 if outline else 0,
                stroke_color=GRID,
                fill_opacity=1,
                fill_color=gray_from_darkness(values[r, c]),
            )
            square.move_to(((c - (cols - 1) / 2) * cell, ((rows - 1) / 2 - r) * cell, 0))
            group.add(square)
    border = Rectangle(
        width=cols * cell,
        height=rows * cell,
        stroke_color=INK,
        stroke_width=1.8,
        fill_opacity=0,
    )
    border.move_to(group.get_center())
    return VGroup(group, border)


def heat_grid(values: np.ndarray, cell: float = 0.105, limit: float | None = None) -> VGroup:
    limit = float(np.max(np.abs(values))) if limit is None else limit
    group = VGroup()
    rows, cols = values.shape
    for r in range(rows):
        for c in range(cols):
            square = Square(
                side_length=cell,
                stroke_width=0.35,
                stroke_color="#eeeeee",
                fill_opacity=1,
                fill_color=diverging_color(values[r, c], limit),
            )
            square.move_to(((c - (cols - 1) / 2) * cell, ((rows - 1) / 2 - r) * cell, 0))
            group.add(square)
    border = Rectangle(
        width=cols * cell,
        height=rows * cell,
        stroke_color=INK,
        stroke_width=1.3,
        fill_opacity=0,
    )
    border.move_to(group.get_center())
    return VGroup(group, border)


def factor_matrix(rows: int, cols: int, cell: float, selected: tuple[int, int] | None, color: str) -> VGroup:
    group = VGroup()
    for r in range(rows):
        for c in range(cols):
            active = selected is not None and selected == (r, c)
            square = Square(
                side_length=cell,
                stroke_width=0.45,
                stroke_color="#ececf0",
                fill_opacity=1,
                fill_color=color if active else "#f5f5f7",
            )
            square.move_to(((c - (cols - 1) / 2) * cell, ((rows - 1) / 2 - r) * cell, 0))
            group.add(square)
    border = Rectangle(width=cols * cell, height=rows * cell, stroke_color=INK, stroke_width=1.2)
    border.move_to(group.get_center())
    return VGroup(group, border)


def highlighted_factor_panel(rank_index: int) -> VGroup:
    u = factor_matrix(13, 13, 0.06, None, U_COLOR)
    sigma = factor_matrix(13, 13, 0.06, None, SIGMA_COLOR)
    vt = factor_matrix(13, 13, 0.06, None, VT_COLOR)

    for row in range(13):
        u[0][row * 13 + rank_index].set_fill(U_COLOR, opacity=1)
    sigma[0][rank_index * 13 + rank_index].set_fill(SIGMA_COLOR, opacity=1)
    for col in range(13):
        vt[0][rank_index * 13 + col].set_fill(VT_COLOR, opacity=1)

    labels = VGroup(t("U", 20, U_COLOR, "BOLD"), t("Σ", 20, SIGMA_COLOR, "BOLD"), t("Vᵀ", 20, VT_COLOR, "BOLD"))
    matrices = VGroup(u, sigma, vt).arrange(RIGHT, buff=0.26)
    for label, matrix in zip(labels, matrices):
        label.next_to(matrix, UP, buff=0.08)
    return VGroup(matrices, labels)


def vector_column(values: np.ndarray, cell: float = 0.105) -> VGroup:
    return heat_grid(values.reshape(-1, 1), cell=cell, limit=float(np.max(np.abs(values))))


def vector_row(values: np.ndarray, cell: float = 0.105) -> VGroup:
    return heat_grid(values.reshape(1, -1), cell=cell, limit=float(np.max(np.abs(values))))


def sigma_box(value: float, index: int) -> VGroup:
    box = RoundedRectangle(
        width=1.15,
        height=0.56,
        corner_radius=0.08,
        stroke_color=INK,
        fill_color=SIGMA_COLOR,
        fill_opacity=1,
        stroke_width=2,
    )
    label = t(f"σ{index + 1} = {value:.1f}", 22, INK, "BOLD")
    label.move_to(box)
    return VGroup(box, label)


def equation_panel(rank_index: int, u_col: np.ndarray, sigma: float, vt_row: np.ndarray, component: np.ndarray) -> VGroup:
    u_vec = vector_column(u_col)
    s_box = sigma_box(sigma, rank_index)
    v_vec = vector_row(vt_row)
    out = heat_grid(component, cell=0.105)
    labels = [
        t(f"u{rank_index + 1}", 19, U_COLOR, "BOLD"),
        t(f"σ{rank_index + 1}", 19, SIGMA_COLOR, "BOLD"),
        t(f"v{rank_index + 1}ᵀ", 19, VT_COLOR, "BOLD"),
        t(f"Rang-{rank_index + 1}-Baustein", 19, SUM_COLOR, "BOLD"),
    ]
    pieces = VGroup(
        VGroup(u_vec, labels[0]).arrange(DOWN, buff=0.08),
        t("·", 32, INK, BOLD),
        VGroup(s_box, labels[1]).arrange(DOWN, buff=0.08),
        t("·", 32, INK, BOLD),
        VGroup(v_vec, labels[2]).arrange(DOWN, buff=0.08),
        t("=", 32, INK, BOLD),
        VGroup(out, labels[3]).arrange(DOWN, buff=0.08),
    ).arrange(RIGHT, buff=0.23)
    return pieces


def bottom_comparison(k: int, reconstruction: np.ndarray) -> VGroup:
    approx = image_grid(reconstruction, cell=0.115)
    ref = image_grid(REFERENCE, cell=0.115)
    plus = t("+", 32, INK, BOLD)
    left = VGroup(approx, t(f"Summe Rang 1 bis {k}", 20, SUM_COLOR, "BOLD")).arrange(DOWN, buff=0.1)
    right = VGroup(ref, t("Referenzbild", 20, INK, "BOLD")).arrange(DOWN, buff=0.1)
    caption = t("Je mehr Rang-1-Bausteine addiert werden, desto naeher kommt die Rekonstruktion an das Original.", 20, MUTED)
    row = VGroup(left, plus, right).arrange(RIGHT, buff=0.55)
    return VGroup(row, caption).arrange(DOWN, buff=0.16)


class SVDRankBuildUp(Scene):
    def construct(self) -> None:
        u, singular_values, vt = np.linalg.svd(REFERENCE, full_matrices=False)
        components = [singular_values[i] * np.outer(u[:, i], vt[i, :]) for i in range(3)]
        reconstructions = [np.sum(components[: i + 1], axis=0) for i in range(3)]

        title = t("SVD als Summe von Rang-1-Matrizen", 38, INK, "BOLD").to_edge(UP, buff=0.28)
        subtitle = t("A = σ1 u1 v1ᵀ + σ2 u2 v2ᵀ + σ3 u3 v3ᵀ + ...", 24, MUTED)
        subtitle.next_to(title, DOWN, buff=0.08)
        self.play(FadeIn(title), FadeIn(subtitle))

        rank_label = t("Rang 1", 34, SUM_COLOR, "BOLD").to_edge(LEFT, buff=0.52).shift(UP * 3.1)
        factors = highlighted_factor_panel(0).scale(1.2).move_to(UP * 2.15)
        equation = equation_panel(0, u[:, 0], singular_values[0], vt[0, :], components[0]).move_to(UP * 0.35)
        bottom = bottom_comparison(1, reconstructions[0]).move_to(DOWN * 2.55)

        self.play(FadeIn(rank_label), FadeIn(factors, shift=DOWN * 0.15))
        self.play(FadeIn(equation, shift=UP * 0.15))
        self.play(FadeIn(bottom, shift=UP * 0.15))
        self.wait(1.2)

        current_label = rank_label
        current_factors = factors
        current_equation = equation
        current_bottom = bottom

        for i in range(1, 3):
            new_label = t(f"Rang {i + 1}", 34, SUM_COLOR, "BOLD").to_edge(LEFT, buff=0.52).shift(UP * 3.1)
            new_factors = highlighted_factor_panel(i).scale(1.2).move_to(UP * 2.15)
            new_equation = equation_panel(i, u[:, i], singular_values[i], vt[i, :], components[i]).move_to(UP * 0.35)
            new_bottom = bottom_comparison(i + 1, reconstructions[i]).move_to(DOWN * 2.55)

            self.play(
                ReplacementTransform(current_label, new_label),
                ReplacementTransform(current_factors, new_factors),
                ReplacementTransform(current_equation, new_equation),
                ReplacementTransform(current_bottom, new_bottom),
                run_time=1.25,
            )
            self.wait(1.2)
            current_label = new_label
            current_factors = new_factors
            current_equation = new_equation
            current_bottom = new_bottom

        final_note = t("Nach drei Bausteinen ist die grobe Entenform sichtbar, Details fehlen noch.", 24, INK, "BOLD")
        final_note.next_to(current_bottom, UP, buff=0.15)
        self.play(FadeIn(final_note))
        self.wait(2)
