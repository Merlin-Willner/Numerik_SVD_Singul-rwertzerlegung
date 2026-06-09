from __future__ import annotations

import numpy as np
from manim import *


config.background_color = "#ffffff"
config.frame_width = 16
config.frame_height = 9
config.pixel_width = 1920
config.pixel_height = 1080


INK = "#111111"
MUTED = "#6e6e73"
RED = "#d93025"
BLUE = "#1a73e8"
GREEN = "#188038"
PANEL = "#f5f5f7"


R_MINUS_90 = np.array([[0.0, 1.0], [-1.0, 0.0]])
SIGMA = np.array([[0.45, 0.0], [0.0, 1.0]])
R_MINUS_45 = np.array(
    [
        [np.sqrt(2) / 2, np.sqrt(2) / 2],
        [-np.sqrt(2) / 2, np.sqrt(2) / 2],
    ]
)
BASE_POINTS = {
    RED: np.array([0.0, 1.0, 0.0]),
    BLUE: np.array([-0.67, -0.52, 0.0]),
    GREEN: np.array([0.73, -0.43, 0.0]),
}


def text(label: str, size: int = 28, color: str = INK, weight: str = "NORMAL") -> Text:
    return Text(label, font="Arial", font_size=size, color=color, weight=weight)


def matrix_2d_to_3d(matrix: np.ndarray) -> np.ndarray:
    out = np.eye(3)
    out[:2, :2] = matrix
    return out


def marked_shape(scale: float = 1.0) -> VGroup:
    shape = Circle(radius=1.0 * scale, color=INK, stroke_width=5, fill_color=INK, fill_opacity=0.88)
    points = VGroup(*(Dot(point * scale, radius=0.085 * scale, color=color) for color, point in BASE_POINTS.items()))
    for point in points:
        point.set_stroke(WHITE, width=3 * scale)
    return VGroup(shape, points)


def transformed_marked_shape(matrix: np.ndarray | None, scale: float = 1.0) -> VGroup:
    shape = Circle(radius=1.0 * scale, color=INK, stroke_width=5, fill_color=INK, fill_opacity=0.88)
    if matrix is not None:
        shape.apply_matrix(matrix_2d_to_3d(matrix))

    points = VGroup()
    for color, point in BASE_POINTS.items():
        target = point[:2] if matrix is None else matrix @ point[:2]
        dot = Dot(np.array([target[0], target[1], 0.0]) * scale, radius=0.085 * scale, color=color)
        dot.set_stroke(WHITE, width=3 * scale)
        points.add(dot)
    return VGroup(shape, points)


def shape_state(matrix: np.ndarray | None, label: str, scale: float = 0.82) -> VGroup:
    group = transformed_marked_shape(matrix, scale)
    caption = text(label, 22, MUTED, "BOLD").next_to(group, DOWN, buff=0.25)
    return VGroup(group, caption)


def math_label(tex: str, color: str = INK) -> MathTex:
    return MathTex(tex, color=color, font_size=30)


def operation_card(shape: VGroup, formula: MathTex | None = None) -> VGroup:
    box = RoundedRectangle(
        width=3.35,
        height=2.95,
        corner_radius=0.08,
        stroke_color="#d8d8de",
        stroke_width=1.6,
        fill_color=PANEL,
        fill_opacity=0.72,
    )
    shape.move_to(box.get_center() + UP * 0.22)
    content = VGroup(box, shape)
    if formula is not None:
        formula.next_to(box, DOWN, buff=0.16)
        content.add(formula)
    return content


class SVDPuzzleTransformation(Scene):
    def construct(self) -> None:
        title = text("Puzzle: Welche Transformation steckt dahinter?", 38, INK, "BOLD")
        title.to_edge(UP, buff=0.32)
        lead = text(
            "Wie kommt man von der Grafik links zur Grafik rechts?",
            25,
            MUTED,
        )
        lead.next_to(title, DOWN, buff=0.08)
        self.play(FadeIn(title), FadeIn(lead))

        start = marked_shape(1.15).move_to(LEFT * 4.65 + DOWN * 0.2)
        end = transformed_marked_shape(R_MINUS_45 @ SIGMA @ R_MINUS_90, 1.15)
        end.move_to(RIGHT * 4.65 + DOWN * 0.2)

        start_label = text("Ausgangsform", 24, MUTED, "BOLD").next_to(start, DOWN, buff=0.35)
        end_label = text("Zielbild", 24, MUTED, "BOLD").next_to(end, DOWN, buff=0.35)
        arrow = CurvedArrow(
            start_point=LEFT * 2.65 + UP * 0.2,
            end_point=RIGHT * 2.65 + UP * 0.2,
            angle=-TAU / 4,
            color=INK,
            stroke_width=5,
            tip_length=0.22,
        )
        arrow_label = text("lineare Transformation", 23, INK, "BOLD").next_to(arrow, UP, buff=0.15)

        self.play(FadeIn(start), FadeIn(start_label))
        self.play(Create(arrow), FadeIn(arrow_label))
        self.play(TransformFromCopy(start, end), FadeIn(end_label), run_time=1.8)
        self.wait(0.7)

        question = text("Die Form allein reicht nicht: Die Punkte muessen mitwandern.", 25, INK, "BOLD")
        question.to_edge(DOWN, buff=0.48)
        self.play(FadeIn(question, shift=UP * 0.15))
        self.wait(1.2)

        self.play(
            FadeOut(VGroup(start, end, start_label, end_label, arrow, arrow_label, question)),
            run_time=0.8,
        )
        self.show_decomposition(title, lead)

    def show_decomposition(self, title: Text, lead: Text) -> None:
        new_title = text("Schrittweise Zerlegung", 38, INK, "BOLD").to_edge(UP, buff=0.32)
        new_lead = text(
            "Sichtbare Reihenfolge: erst drehen, dann stauchen, dann erneut drehen.",
            24,
            MUTED,
        ).next_to(new_title, DOWN, buff=0.08)
        self.play(ReplacementTransform(title, new_title), ReplacementTransform(lead, new_lead))

        matrices = [
            None,
            R_MINUS_90,
            SIGMA @ R_MINUS_90,
            R_MINUS_45 @ SIGMA @ R_MINUS_90,
        ]
        labels = [
            "Ausgangskreis",
            "Rotation 90 Grad rechts",
            "Stauchung in x-Richtung",
            "Rotation 45 Grad rechts",
        ]
        formulas = [
            None,
            math_label(r"R_{-90^\circ}=\begin{pmatrix}0&1\\-1&0\end{pmatrix}", BLUE),
            math_label(r"\Sigma=\begin{pmatrix}0.45&0\\0&1\end{pmatrix}", RED),
            math_label(
                r"R_{-45^\circ}=\begin{pmatrix}\frac{\sqrt2}{2}&\frac{\sqrt2}{2}\\-\frac{\sqrt2}{2}&\frac{\sqrt2}{2}\end{pmatrix}",
                GREEN,
            ),
        ]

        cards = VGroup()
        for matrix, label, formula in zip(matrices, labels, formulas):
            state = shape_state(matrix, label)
            card = operation_card(state, formula)
            cards.add(card)
        cards.arrange(RIGHT, buff=0.28).move_to(DOWN * 0.2)

        arrows = VGroup()
        for left, right in zip(cards[:-1], cards[1:]):
            arrows.add(
                Arrow(
                    left.get_right() + RIGHT * 0.04,
                    right.get_left() + LEFT * 0.04,
                    color=INK,
                    buff=0.04,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.16,
                )
            )

        order = math_label(r"A=R_{-45^\circ}\,\Sigma\,R_{-90^\circ}=U\,\Sigma\,V^T")
        note = text("Die Reihenfolge folgt hier der sichtbaren Transformation.", 22, MUTED)
        summary = VGroup(order, note).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.28)

        self.play(FadeIn(cards[0], shift=UP * 0.15))
        for index in range(1, len(cards)):
            self.play(Create(arrows[index - 1]), FadeIn(cards[index], shift=RIGHT * 0.2), run_time=0.9)
            self.wait(0.25)
        self.play(FadeIn(summary, shift=UP * 0.15))
        self.wait(2.0)


class SVDPuzzleDecomposition(Scene):
    def construct(self) -> None:
        title = text("Schrittweise Zerlegung", 38, INK, "BOLD").to_edge(UP, buff=0.32)
        lead = text(
            "Vier Zustände als Reveal-Fragmente der Folie-3-Transformation.",
            24,
            MUTED,
        ).next_to(title, DOWN, buff=0.08)
        self.add(title, lead)
        self.show_decomposition(title, lead)

    def show_decomposition(self, title: Text, lead: Text) -> None:
        SVDPuzzleTransformation.show_decomposition(self, title, lead)
