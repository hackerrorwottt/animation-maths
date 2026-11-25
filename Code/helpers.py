"""Shared styling, geometry builders, and math helpers for the Eigenvectors animation.

All constants and factory functions live here so every scene shares consistent
1080p typography, color coding, coordinate-plane scaling, and matrix formatting.
"""

from __future__ import annotations

import numpy as np
from manim import (
    BOLD,
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Arc,
    Arrow,
    BackgroundRectangle,
    Circle,
    DashedLine,
    Dot,
    MathTex,
    Matrix,
    NumberPlane,
    Polygon,
    RoundedRectangle,
    Text,
    VGroup,
)

# ---------------------------------------------------------------------------
# Color Palette (high-contrast dark theme optimized for 1080p readability)
# ---------------------------------------------------------------------------
BG_COLOR = "#0D1117"           # Deep slate-navy background
PANEL_BG = "#161B22"           # Card / HUD panel fill
PANEL_BORDER = "#30363D"       # Subtle border for cards

# Consistent vector color coding required across all scenes:
EIG1_COLOR = "#FF8C42"         # Orange -> Eigenvector 1: v1 = (1, 1), lambda1 = 3
EIG2_COLOR = "#2EC4B6"         # Teal   -> Eigenvector 2: v2 = (1, -1), lambda2 = 1
OTHER_VEC_COLOR = "#9AA5B1"    # Grey   -> Non-eigenvector sample vectors

# Supporting UI & grid colors
GRID_GHOST_COLOR = "#243040"   # Faint reference grid that never moves
GRID_ACTIVE_COLOR = "#2E6F95"  # Deforming grid lines
AXIS_COLOR = "#CBD5E1"         # Static x/y axes
UNIT_SHAPE_COLOR = "#58A6FF"   # Unit square / unit circle morphing accent
ACCENT_GOLD = "#FFD166"        # Key insights, eigenvalues, checkmarks
ACCENT_RED = "#EF476F"         # Singular / negative scaling emphasis
TEXT_WHITE = "#F8FAFC"         # Primary body and equation text
SUBTLE_TEXT = "#94A3B8"        # Secondary captions and credits

# ---------------------------------------------------------------------------
# Worked Example Matrix & Exact Eigenpairs (verified by hand)
# ---------------------------------------------------------------------------
A_MATRIX = np.array([[2.0, 1.0], [1.0, 2.0]])
LAMBDA_1 = 3.0
V1 = np.array([1.0, 1.0])
LAMBDA_2 = 1.0
V2 = np.array([1.0, -1.0])


def make_plane_pair(
    x_range: tuple[float, float, float] = (-6, 6, 1),
    y_range: tuple[float, float, float] = (-4, 4, 1),
    unit_size: float = 0.85,
    center: np.ndarray = ORIGIN,
) -> tuple[NumberPlane, NumberPlane]:
    """Create a static reference grid (with tick labels) and an active grid.

    Separating the static labelled axes from the deforming grid keeps coordinate
    numbers crisp and upright while the grid lines shear/stretch smoothly.
    """
    x_len = (x_range[1] - x_range[0]) * unit_size
    y_len = (y_range[1] - y_range[0]) * unit_size

    ghost_plane = NumberPlane(
        x_range=x_range,
        y_range=y_range,
        x_length=x_len,
        y_length=y_len,
        background_line_style={
            "stroke_color": GRID_GHOST_COLOR,
            "stroke_width": 1.3,
            "stroke_opacity": 0.6,
        },
        axis_config={
            "stroke_color": AXIS_COLOR,
            "stroke_width": 2.0,
            "stroke_opacity": 0.75,
            "include_numbers": True,
            "font_size": 20,
            "decimal_number_config": {"num_decimal_places": 0, "color": SUBTLE_TEXT},
        },
    ).move_to(center)

    active_plane = NumberPlane(
        x_range=x_range,
        y_range=y_range,
        x_length=x_len,
        y_length=y_len,
        background_line_style={
            "stroke_color": GRID_ACTIVE_COLOR,
            "stroke_width": 2.0,
            "stroke_opacity": 0.72,
        },
        axis_config={
            "stroke_color": AXIS_COLOR,
            "stroke_width": 2.2,
            "stroke_opacity": 0.85,
            "include_numbers": False,
        },
    ).move_to(center)

    return ghost_plane, active_plane


def make_axis_labels(plane: NumberPlane) -> VGroup:
    """Return crisp x and y axis labels positioned just outside the plane ends."""
    x_lbl = MathTex("x", font_size=28, color=AXIS_COLOR).next_to(
        plane.x_axis.get_end(), RIGHT, buff=0.14
    )
    y_lbl = MathTex("y", font_size=28, color=AXIS_COLOR).next_to(
        plane.y_axis.get_end(), UP, buff=0.14
    )
    return VGroup(x_lbl, y_lbl)


def make_span_line(
    vec_2d: np.ndarray,
    origin_pt: np.ndarray,
    unit_size: float = 0.85,
    length_units: float = 5.5,
    color: str = SUBTLE_TEXT,
    stroke_opacity: float = 0.45,
) -> DashedLine:
    """Build a dashed line representing span{vec_2d} centered at origin_pt."""
    norm = float(np.linalg.norm(vec_2d))
    direction = np.array([vec_2d[0], vec_2d[1], 0.0]) / (norm if norm > 0 else 1.0)
    half_span = direction * (length_units * unit_size)
    return DashedLine(
        start=origin_pt - half_span,
        end=origin_pt + half_span,
        dash_length=0.14,
        dashed_ratio=0.55,
        color=color,
        stroke_width=2.2,
        stroke_opacity=stroke_opacity,
    )


def make_labelled_vector(
    vec_2d: np.ndarray,
    origin_pt: np.ndarray,
    unit_size: float = 0.85,
    color: str = OTHER_VEC_COLOR,
    label_tex: str | None = None,
    label_dir: np.ndarray = UP + RIGHT,
    stroke_width: float = 5.0,
    font_size: int = 24,
) -> VGroup:
    """Create a 2D vector arrow anchored at origin_pt with an optional MathTex label."""
    tip = origin_pt + unit_size * np.array([vec_2d[0], vec_2d[1], 0.0])
    if np.linalg.norm(tip - origin_pt) < 1e-4:
        arrow = Dot(point=origin_pt, radius=0.08, color=color)
    else:
        arrow = Arrow(
            start=origin_pt,
            end=tip,
            buff=0,
            color=color,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.22,
            tip_length=0.22,
        )

    if label_tex:
        lbl = MathTex(label_tex, font_size=font_size, color=color)
        lbl.next_to(tip, label_dir, buff=0.14)
        bg = BackgroundRectangle(lbl, color=BG_COLOR, fill_opacity=0.82, buff=0.05)
        return VGroup(arrow, bg, lbl)
    return VGroup(arrow)


def make_fast_vector(
    vec_2d: np.ndarray,
    origin_pt: np.ndarray,
    unit_size: float = 0.85,
    color: str = OTHER_VEC_COLOR,
    stroke_width: float = 5.0,
) -> Arrow | Dot:
    """Create a lightweight vector arrow (no LaTeX compile) for fast 60fps updaters."""
    tip = origin_pt + unit_size * np.array([vec_2d[0], vec_2d[1], 0.0])
    if np.linalg.norm(tip - origin_pt) < 1e-4:
        return Dot(point=origin_pt, radius=0.08, color=color)
    return Arrow(
        start=origin_pt,
        end=tip,
        buff=0,
        color=color,
        stroke_width=stroke_width,
        max_tip_length_to_length_ratio=0.22,
        tip_length=0.22,
    )


def make_transformed_unit_square(
    mat: np.ndarray,
    origin_pt: np.ndarray,
    unit_size: float = 0.85,
    color: str = UNIT_SHAPE_COLOR,
    fill_opacity: float = 0.16,
) -> Polygon:
    """Build the image of the unit square [0,1]^2 under linear matrix `mat`."""
    corners_2d = [
        np.array([0.0, 0.0]),
        mat @ np.array([1.0, 0.0]),
        mat @ np.array([1.0, 1.0]),
        mat @ np.array([0.0, 1.0]),
    ]
    pts = [origin_pt + unit_size * np.array([c[0], c[1], 0.0]) for c in corners_2d]
    return Polygon(
        *pts,
        color=color,
        stroke_width=2.2,
        stroke_opacity=0.8,
        fill_color=color,
        fill_opacity=fill_opacity,
    )


def make_transformed_circle(
    mat: np.ndarray,
    origin_pt: np.ndarray,
    unit_size: float = 0.85,
    color: str = ACCENT_GOLD,
    stroke_opacity: float = 0.55,
) -> Circle:
    """Build the image of the unit circle (an ellipse) under linear matrix `mat`."""
    circ = Circle(
        radius=unit_size,
        color=color,
        stroke_width=2.0,
        stroke_opacity=stroke_opacity,
    ).move_to(origin_pt)
    circ.apply_matrix(mat, about_point=origin_pt)
    return circ


def make_angle_arc(
    start_vec: np.ndarray,
    cur_vec: np.ndarray,
    origin_pt: np.ndarray,
    radius: float = 0.45,
    color: str = ACCENT_RED,
) -> Arc:
    """Draw a clean arc from start_vec's angle to cur_vec's angle around origin_pt."""
    a0 = float(np.arctan2(start_vec[1], start_vec[0]))
    a1 = float(np.arctan2(cur_vec[1], cur_vec[0]))
    # Shortest signed angular difference in (-pi, pi]
    delta = (a1 - a0 + np.pi) % (2 * np.pi) - np.pi
    return Arc(
        radius=radius,
        start_angle=a0,
        angle=delta,
        arc_center=origin_pt,
        color=color,
        stroke_width=3.0,
    )


def make_matrix_mobject(
    entries: list[list[str | int | float]],
    color: str = TEXT_WHITE,
    scale: float = 0.85,
    h_buff: float = 0.85,
    v_buff: float = 0.65,
) -> Matrix:
    """Build a cleanly spaced square-bracket Matrix mobject."""
    mat = Matrix(
        entries,
        left_bracket="[",
        right_bracket="]",
        h_buff=h_buff,
        v_buff=v_buff,
    )
    mat.set_color(color)
    mat.scale(scale)
    return mat


def make_card(
    content,
    padding_x: float = 0.4,
    padding_y: float = 0.28,
    fill_color: str = PANEL_BG,
    stroke_color: str = PANEL_BORDER,
    fill_opacity: float = 0.92,
) -> VGroup:
    """Wrap any mobject or VGroup inside a rounded dark UI card."""
    box = RoundedRectangle(
        corner_radius=0.14,
        width=content.width + padding_x,
        height=content.height + padding_y,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
        stroke_color=stroke_color,
        stroke_width=1.8,
    )
    box.move_to(content.get_center())
    return VGroup(box, content)


def make_section_header(title_text: str, subtitle_text: str | None = None) -> VGroup:
    """Build a consistent top-of-frame header banner for non-grid scenes."""
    title = Text(title_text, font_size=36, weight=BOLD, color=TEXT_WHITE)
    title.to_edge(UP, buff=0.35)
    if subtitle_text:
        sub = Text(subtitle_text, font_size=22, color=SUBTLE_TEXT)
        sub.next_to(title, DOWN, buff=0.12)
        return VGroup(title, sub)
    return VGroup(title)


def interpolated_matrix(t: float) -> np.ndarray:
    """Return M(t) = (1 - t) * I + t * A_MATRIX for smooth ValueTracker animations."""
    return (1.0 - t) * np.eye(2) + t * A_MATRIX


def angle_deg(vec_2d: np.ndarray) -> float:
    """Return vector angle in degrees wrapped to (-180, 180]."""
    return float(np.degrees(np.arctan2(vec_2d[1], vec_2d[0])))
