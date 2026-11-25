"""M3 Linear Algebra & Calculus — Eigenvalues & Eigenvectors Animation.

Run a single scene (fast preview):
    manim -pql Code/main.py Scene1_Hook

Render the complete 1080p 16:9 video:
    manim -qh --resolution 1920,1080 Code/main.py FullVideo
"""

from __future__ import annotations

import os
import sys

# Ensure `helpers.py` in the same directory is importable regardless of cwd.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from manim import (
    BOLD,
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UL,
    UP,
    UR,
    ApplyMatrix,
    Arc,
    Arrow,
    Circumscribe,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Flash,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    NumberPlane,
    Polygon,
    ReplacementTransform,
    RightAngle,
    RoundedRectangle,
    Scene,
    SurroundingRectangle,
    Text,
    Transform,
    TransformMatchingTex,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
    smooth,
)

from helpers import (
    A_MATRIX,
    ACCENT_GOLD,
    ACCENT_RED,
    BG_COLOR,
    EIG1_COLOR,
    EIG2_COLOR,
    OTHER_VEC_COLOR,
    PANEL_BG,
    PANEL_BORDER,
    SUBTLE_TEXT,
    TEXT_WHITE,
    UNIT_SHAPE_COLOR,
    V1,
    V2,
    angle_deg,
    interpolated_matrix,
    make_angle_arc,
    make_axis_labels,
    make_card,
    make_fast_vector,
    make_labelled_vector,
    make_matrix_mobject,
    make_plane_pair,
    make_section_header,
    make_span_line,
    make_transformed_circle,
    make_transformed_unit_square,
)


class EigenBaseScene(Scene):
    """Base scene providing shared setup, teardown, and all 6 storyboard methods.

    Each storyboard scene class inherits from this base and runs its own method,
    while `FullVideo` chains all 6 methods sequentially in one continuous render.
    """

    def setup_dark_canvas(self) -> None:
        """Apply the consistent dark slate background to the scene camera."""
        self.camera.background_color = BG_COLOR

    def clear_scene(self, fade_time: float = 0.6) -> None:
        """Detach updaters and fade out all active mobjects cleanly between scenes."""
        if not self.mobjects:
            return
        for mob in list(self.mobjects):
            # Clear updaters first so always_redraw objects do not fight FadeOut.
            mob.clear_updaters()
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=fade_time)
        self.clear()

    # =========================================================================
    # SCENE 1: HOOK & OPENING FRAME (0:00 - 0:31, ~31.0s)
    # =========================================================================
    def play_scene_1(self) -> None:
        """Animated opening title card followed by the geometric hook transformation."""
        self.setup_dark_canvas()

        # --- 0:00 to 0:06 (6.0s): Opening Frame with Subtle Ambient Lattice ---
        bg_lattice = NumberPlane(
            x_range=(-8, 8, 1),
            y_range=(-5, 5, 1),
            background_line_style={
                "stroke_color": "#1C2A3A",
                "stroke_width": 1.2,
                "stroke_opacity": 0.45,
            },
            axis_config={"stroke_opacity": 0.2},
        )
        bg_eig1 = make_span_line(V1, ORIGIN, 1.0, 7.0, EIG1_COLOR, 0.25)
        bg_eig2 = make_span_line(V2, ORIGIN, 1.0, 7.0, EIG2_COLOR, 0.25)

        title = Text(
            "Eigenvalues & Eigenvectors",
            font_size=54,
            weight=BOLD,
            color=TEXT_WHITE,
        )
        underline = Line(LEFT * 4.2, RIGHT * 4.2, color=ACCENT_GOLD, stroke_width=3.0)
        concept_line = Text(
            "Linear Algebra & Calculus (M3)  •  Invariant Directions Under Transformations",
            font_size=23,
            color=EIG2_COLOR,
        )
        student_info = Text(
            "Student Name: Shlok Sharma    |    Student ID: E25B070773",
            font_size=22,
            color=SUBTLE_TEXT,
        )
        opening_group = VGroup(title, underline, concept_line, student_info).arrange(
            DOWN, buff=0.28
        )
        opening_card = make_card(
            opening_group, padding_x=0.95, padding_y=0.72, fill_opacity=0.94
        )

        self.play(
            FadeIn(bg_lattice),
            Create(bg_eig1),
            Create(bg_eig2),
            FadeIn(opening_card[0]),
            Write(title),
            run_time=1.3,
        )
        self.play(
            Create(underline),
            FadeIn(concept_line, shift=UP * 0.1),
            FadeIn(student_info, shift=UP * 0.1),
            run_time=1.0,
        )
        self.wait(2.8)
        self.play(
            FadeOut(opening_card),
            FadeOut(bg_lattice),
            FadeOut(bg_eig1),
            FadeOut(bg_eig2),
            run_time=0.9,
        )

        # --- 0:06 to 0:11 (5.0s): Setup Grid, Unit Square, Unit Circle & Vectors ---
        unit_size = 0.85
        plane_center = ORIGIN
        ghost_plane, active_plane = make_plane_pair(
            x_range=(-6, 6, 1),
            y_range=(-4, 4, 1),
            unit_size=unit_size,
            center=plane_center,
        )
        axis_labels = make_axis_labels(ghost_plane)

        # Unit square & unit circle morph visibly to reveal shear + principal axes.
        unit_sq = make_transformed_unit_square(np.eye(2), plane_center, unit_size)
        unit_circ = make_transformed_circle(np.eye(2), plane_center, unit_size)

        mat_label = MathTex("A =", font_size=34, color=TEXT_WHITE)
        mat_mob = make_matrix_mobject([[2, 1], [1, 2]], color=ACCENT_GOLD, scale=0.78)
        hud_row = VGroup(mat_label, mat_mob).arrange(RIGHT, buff=0.18)
        hud_card = make_card(hud_row, padding_x=0.35, padding_y=0.22).to_corner(
            UL, buff=0.35
        )

        sample_vecs = [
            (np.array([1.0, 0.0]), "(1,0)", DOWN + RIGHT),
            (np.array([0.0, 1.0]), "(0,1)", UP + LEFT),
            (np.array([2.0, -1.0]), "(2,-1)", DOWN + RIGHT),
        ]
        grey_arrows = VGroup(
            *[
                make_labelled_vector(
                    v, plane_center, unit_size, OTHER_VEC_COLOR, lbl, ldir, font_size=22
                )
                for v, lbl, ldir in sample_vecs
            ]
        )
        eig1_init = make_labelled_vector(
            V1, plane_center, unit_size, OTHER_VEC_COLOR, "(1,1)", UP + LEFT, font_size=22
        )
        eig2_init = make_labelled_vector(
            V2, plane_center, unit_size, OTHER_VEC_COLOR, "(1,-1)", DOWN + RIGHT, font_size=22
        )

        self.play(
            FadeIn(ghost_plane),
            Create(active_plane),
            FadeIn(axis_labels),
            FadeIn(hud_card),
            Create(unit_sq),
            Create(unit_circ),
            run_time=1.8,
        )
        self.play(
            LaggedStart(
                *[GrowArrow(grp[0]) for grp in grey_arrows],
                GrowArrow(eig1_init[0]),
                GrowArrow(eig2_init[0]),
                lag_ratio=0.12,
            ),
            *[FadeIn(grp[1:]) for grp in grey_arrows],
            FadeIn(eig1_init[1:]),
            FadeIn(eig2_init[1:]),
            run_time=1.7,
        )
        self.wait(1.5)

        # --- 0:11 to 0:17 (6.0s): ApplyMatrix Shear & Stretch ---
        target_sq = make_transformed_unit_square(A_MATRIX, plane_center, unit_size)
        target_circ = make_transformed_circle(A_MATRIX, plane_center, unit_size)

        transformed_grey = VGroup(
            *[
                make_labelled_vector(
                    A_MATRIX @ v,
                    plane_center,
                    unit_size,
                    OTHER_VEC_COLOR,
                    f"({int((A_MATRIX @ v)[0])},{int((A_MATRIX @ v)[1])})",
                    ldir,
                    font_size=22,
                )
                for v, _, ldir in sample_vecs
            ]
        )
        eig1_after = make_labelled_vector(
            A_MATRIX @ V1,
            plane_center,
            unit_size,
            EIG1_COLOR,
            "(3,3)",
            UP + LEFT,
            stroke_width=5.5,
            font_size=24,
        )
        eig2_after = make_labelled_vector(
            A_MATRIX @ V2,
            plane_center,
            unit_size,
            EIG2_COLOR,
            "(1,-1)",
            DOWN + RIGHT,
            stroke_width=5.5,
            font_size=24,
        )

        self.play(
            ApplyMatrix(A_MATRIX, active_plane, about_point=plane_center),
            Transform(unit_sq, target_sq),
            Transform(unit_circ, target_circ),
            *[
                Transform(grey_arrows[i], transformed_grey[i])
                for i in range(len(sample_vecs))
            ],
            Transform(eig1_init, eig1_after),
            Transform(eig2_init, eig2_after),
            run_time=4.8,
            rate_func=smooth,
        )
        self.wait(1.2)

        # --- 0:17 to 0:23 (6.0s): Reveal Surviving Span Lines & Flash Tips ---
        span1 = make_span_line(V1, plane_center, unit_size, 5.2, EIG1_COLOR, 0.78)
        span2 = make_span_line(V2, plane_center, unit_size, 5.2, EIG2_COLOR, 0.78)

        self.play(Create(span1), Create(span2), run_time=1.4)
        self.play(
            Flash(
                plane_center + unit_size * np.array([3.0, 3.0, 0.0]),
                color=EIG1_COLOR,
                flash_radius=0.35,
            ),
            Flash(
                plane_center + unit_size * np.array([1.0, -1.0, 0.0]),
                color=EIG2_COLOR,
                flash_radius=0.35,
            ),
            Indicate(eig1_init, color=EIG1_COLOR, scale_factor=1.06),
            Indicate(eig2_init, color=EIG2_COLOR, scale_factor=1.06),
            run_time=1.6,
        )
        self.wait(3.0)

        # --- 0:23 to 0:31 (8.0s): Guiding Question ---
        question_txt = Text(
            "Which directions survive a transformation?",
            font_size=34,
            weight=BOLD,
            color=ACCENT_GOLD,
        )
        question_card = make_card(
            question_txt, padding_x=0.55, padding_y=0.28, stroke_color=ACCENT_GOLD
        ).to_edge(DOWN, buff=0.28)

        self.play(FadeIn(question_card, shift=UP * 0.15), run_time=1.0)
        self.play(Circumscribe(question_card, color=ACCENT_GOLD, time_width=0.6), run_time=1.5)
        self.wait(4.5)
        self.clear_scene(fade_time=1.0)

    # =========================================================================
    # SCENE 2: CONCEPT INTRODUCTION (0:31 - 1:16, 45.0s)
    # =========================================================================
    def play_scene_2(self) -> None:
        """Define Av = lambda*v with braces and animate geometric comparison."""
        self.setup_dark_canvas()

        # --- 0:00 to 0:08 (8.0s): Header & Learning Goal ---
        header = make_section_header(
            "What Is an Eigenvector?",
            "Defining the Core Idea & Notation",
        )
        goal_txt = Text(
            "Learning Goal: Explain eigenvectors geometrically and\n"
            "find eigenvalues & eigenvectors of any 2×2 matrix.",
            font_size=28,
            color=TEXT_WHITE,
            line_spacing=1.25,
        )
        goal_card = make_card(
            goal_txt, padding_x=0.6, padding_y=0.4, stroke_color=EIG2_COLOR
        ).move_to(ORIGIN)

        self.play(FadeIn(header), run_time=0.8)
        self.play(FadeIn(goal_card, shift=UP * 0.15), run_time=1.2)
        self.play(Circumscribe(goal_card, color=EIG2_COLOR, fade_out=True), run_time=1.5)
        self.wait(3.5)
        self.play(FadeOut(goal_card), run_time=1.0)

        # --- 0:08 to 0:24 (16.0s): Equation Av = lambda*v with Animated Symbol Cards ---
        eq = MathTex(
            "A", "\\mathbf{v}", "=", "\\lambda", "\\mathbf{v}", font_size=72
        ).move_to(UP * 1.5)
        eq[0].set_color(ACCENT_GOLD)
        eq[1].set_color(EIG1_COLOR)
        eq[3].set_color(EIG2_COLOR)
        eq[4].set_color(EIG1_COLOR)

        self.play(Write(eq), run_time=1.4)
        self.wait(0.8)

        def_a = make_card(
            VGroup(
                MathTex("A", font_size=34, color=ACCENT_GOLD),
                Text("2×2 transformation matrix", font_size=24, color=TEXT_WHITE),
            ).arrange(RIGHT, buff=0.25),
            stroke_color=ACCENT_GOLD,
        )
        def_v = make_card(
            VGroup(
                MathTex("\\mathbf{v} \\neq \\mathbf{0}", font_size=34, color=EIG1_COLOR),
                Text(
                    "Eigenvector (keeps its direction / span line)",
                    font_size=24,
                    color=TEXT_WHITE,
                ),
            ).arrange(RIGHT, buff=0.25),
            stroke_color=EIG1_COLOR,
        )
        def_lam = make_card(
            VGroup(
                MathTex("\\lambda", font_size=36, color=EIG2_COLOR),
                Text(
                    "Eigenvalue (scalar scaling factor along v)",
                    font_size=24,
                    color=TEXT_WHITE,
                ),
            ).arrange(RIGHT, buff=0.25),
            stroke_color=EIG2_COLOR,
        )
        defs_col = (
            VGroup(def_a, def_v, def_lam)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            .next_to(eq, DOWN, buff=0.45)
        )

        # Highlight each equation symbol as its definition card slides in.
        for sym, card, w_sec in [
            (eq[0], def_a, 2.2),
            (eq[1], def_v, 2.5),
            (eq[3], def_lam, 2.2),
        ]:
            self.play(
                Indicate(sym, scale_factor=1.25),
                FadeIn(card, shift=RIGHT * 0.25),
                run_time=1.0,
            )
            self.wait(w_sec)

        nonzero_note = Text(
            "Why v ≠ 0? Because A·0 = λ·0 holds trivially for every λ — giving no direction!",
            font_size=22,
            color=ACCENT_GOLD,
        ).next_to(defs_col, DOWN, buff=0.32)
        self.play(FadeIn(nonzero_note, shift=UP * 0.1), run_time=1.0)
        self.wait(2.9)

        # --- 0:24 to 0:45 (21.0s): Live Animated Geometric Contrast ---
        self.play(
            FadeOut(defs_col),
            FadeOut(nonzero_note),
            eq.animate.shift(UP * 0.35),
            run_time=1.0,
        )

        # ValueTracker s in [0, 1] animates eigenvector stretch & general vector rotation simultaneously.
        s_tracker = ValueTracker(0.0)

        left_origin = np.array([-3.7, -1.35, 0.0])
        left_dir = np.array([1.0, 0.5, 0.0])
        left_span = make_span_line(left_dir, left_origin, 1.0, 2.5, EIG1_COLOR, 0.65)
        left_ghost = Arrow(
            left_origin,
            left_origin + left_dir * 1.1,
            buff=0,
            color=EIG1_COLOR,
            stroke_width=4,
            stroke_opacity=0.3,
        )
        left_dyn = always_redraw(
            lambda: Arrow(
                left_origin,
                left_origin + left_dir * (1.1 * (1.0 + 1.2 * s_tracker.get_value())),
                buff=0,
                color=EIG1_COLOR,
                stroke_width=5.5,
            )
        )
        left_badge = always_redraw(
            lambda: Text(
                f"λ = {1.0 + 1.2 * s_tracker.get_value():.2f}×   (Δθ = 0°)",
                font_size=21,
                color=EIG1_COLOR,
            ).move_to(np.array([-3.2, -2.55, 0.0]))
        )

        right_origin = np.array([2.1, -1.35, 0.0])
        right_u0 = np.array([1.5, 0.0, 0.0])
        right_span = make_span_line(right_u0, right_origin, 1.0, 2.3, OTHER_VEC_COLOR, 0.5)
        right_ghost = Arrow(
            right_origin,
            right_origin + right_u0,
            buff=0,
            color=OTHER_VEC_COLOR,
            stroke_width=4,
            stroke_opacity=0.35,
        )

        def _rot_u():
            s = s_tracker.get_value()
            ang = s * (42.0 * np.pi / 180.0)
            scale = 1.0 + 0.35 * s
            return np.array([1.5 * scale * np.cos(ang), 1.5 * scale * np.sin(ang), 0.0])

        right_dyn = always_redraw(
            lambda: Arrow(
                right_origin,
                right_origin + _rot_u(),
                buff=0,
                color=ACCENT_RED if s_tracker.get_value() > 0.1 else OTHER_VEC_COLOR,
                stroke_width=5.5,
            )
        )
        right_arc = always_redraw(
            lambda: Arc(
                radius=0.58,
                start_angle=0.0,
                angle=max(0.001, s_tracker.get_value() * 42.0 * np.pi / 180.0),
                arc_center=right_origin,
                color=ACCENT_RED,
                stroke_width=3.0,
            )
        )
        right_badge = always_redraw(
            lambda: Text(
                f"Knocked off line!  Δθ = {s_tracker.get_value() * 42.0:.1f}°",
                font_size=21,
                color=ACCENT_RED if s_tracker.get_value() > 0.1 else SUBTLE_TEXT,
            ).move_to(np.array([3.2, -2.55, 0.0]))
        )

        self.play(
            Create(left_span),
            FadeIn(left_ghost),
            FadeIn(left_dyn),
            FadeIn(left_badge),
            Create(right_span),
            FadeIn(right_ghost),
            FadeIn(right_dyn),
            FadeIn(right_arc),
            FadeIn(right_badge),
            run_time=1.8,
        )
        self.wait(1.5)
        self.play(s_tracker.animate.set_value(1.0), run_time=4.0, rate_func=smooth)
        self.wait(2.5)
        self.play(s_tracker.animate.set_value(0.0), run_time=2.2, rate_func=smooth)
        self.play(s_tracker.animate.set_value(1.0), run_time=2.5, rate_func=smooth)

        summary_pill = make_card(
            Text(
                "Eigenvectors keep their span; eigenvalues measure the scaling factor.",
                font_size=24,
                weight=BOLD,
                color=ACCENT_GOLD,
            ),
            stroke_color=ACCENT_GOLD,
        ).to_edge(DOWN, buff=0.25)

        self.play(FadeIn(summary_pill, shift=UP * 0.12), run_time=1.0)
        self.wait(3.5)
        self.clear_scene(fade_time=1.0)

    # =========================================================================
    # SCENE 3: VISUAL INTUITION (1:16 - 2:31, 75.0s)
    # =========================================================================
    def play_scene_3(self) -> None:
        """Continuous ValueTracker transformation with ellipse, unit square & angle arcs."""
        self.setup_dark_canvas()

        # --- 0:00 to 0:10 (10.0s): Grid, Deforming Shapes, Ghost Vectors & HUD ---
        unit_size = 0.85
        plane_center = ORIGIN
        ghost_plane, active_plane = make_plane_pair(
            x_range=(-6, 6, 1),
            y_range=(-4, 4, 1),
            unit_size=unit_size,
            center=plane_center,
        )
        axis_labels = make_axis_labels(ghost_plane)
        base_grid = active_plane.copy()

        t_tracker = ValueTracker(0.0)
        highlight_tracker = ValueTracker(0.0)

        active_plane.add_updater(
            lambda m: m.become(base_grid.copy()).apply_matrix(
                interpolated_matrix(t_tracker.get_value()),
                about_point=plane_center,
            )
        )

        # Deforming unit square and unit circle -> ellipse (fast, no LaTeX!).
        dyn_square = always_redraw(
            lambda: make_transformed_unit_square(
                interpolated_matrix(t_tracker.get_value()),
                plane_center,
                unit_size,
                fill_opacity=0.14,
            )
        )
        dyn_circle = always_redraw(
            lambda: make_transformed_circle(
                interpolated_matrix(t_tracker.get_value()),
                plane_center,
                unit_size,
                color=ACCENT_GOLD,
                stroke_opacity=0.45,
            )
        )

        # Top-left HUD panel.
        hud_mat = VGroup(
            MathTex("A =", font_size=30, color=TEXT_WHITE),
            make_matrix_mobject([[2, 1], [1, 2]], color=ACCENT_GOLD, scale=0.72),
        ).arrange(RIGHT, buff=0.14)
        hud_box = RoundedRectangle(
            corner_radius=0.14,
            width=3.2,
            height=1.75,
            fill_color=PANEL_BG,
            fill_opacity=0.92,
            stroke_color=PANEL_BORDER,
            stroke_width=1.8,
        ).to_corner(UL, buff=0.28)
        hud_mat.move_to(hud_box.get_center() + UP * 0.25)
        t_readout = always_redraw(
            lambda: Text(
                f"t = {t_tracker.get_value():.2f}  (I → A)",
                font_size=20,
                color=SUBTLE_TEXT,
            ).move_to(hud_box.get_center() + DOWN * 0.55)
        )

        non_eig_specs = [
            (np.array([1.0, 0.0]), "u₁", DOWN + RIGHT, 0.55),
            (np.array([0.0, 1.0]), "u₂", UP + LEFT, 0.45),
            (np.array([2.0, -1.0]), "u₃", DOWN + RIGHT, 0.65),
        ]
        non_eig_spans = VGroup(
            *[
                make_span_line(v, plane_center, unit_size, 5.2, OTHER_VEC_COLOR, 0.3)
                for v, _, _, _ in non_eig_specs
            ]
        )
        # Ghost copies of initial vectors remain faint so turning is immediately visible.
        ghost_vecs = VGroup(
            *[
                Arrow(
                    plane_center,
                    plane_center + unit_size * np.array([v[0], v[1], 0.0]),
                    buff=0,
                    color=OTHER_VEC_COLOR,
                    stroke_width=3.0,
                    stroke_opacity=0.25,
                )
                for v, _, _, _ in non_eig_specs
            ]
        )

        eig1_span = always_redraw(
            lambda: make_span_line(
                V1,
                plane_center,
                unit_size,
                5.3,
                EIG1_COLOR,
                0.28 + 0.58 * highlight_tracker.get_value(),
            )
        )
        eig2_span = always_redraw(
            lambda: make_span_line(
                V2,
                plane_center,
                unit_size,
                5.3,
                EIG2_COLOR,
                0.28 + 0.58 * highlight_tracker.get_value(),
            )
        )

        # Live red angle arcs for general vectors u1, u2, u3.
        angle_arcs = VGroup(
            *[
                always_redraw(
                    lambda v=v, r=rad: make_angle_arc(
                        v,
                        interpolated_matrix(t_tracker.get_value()) @ v,
                        plane_center,
                        radius=r,
                        color=ACCENT_RED,
                    )
                )
                for v, _, _, rad in non_eig_specs
            ]
        )

        def fast_labelled_dyn_vec(
            vec_2d: np.ndarray,
            base_color: str,
            name_txt: str,
            ldir: np.ndarray,
            is_eig: int = 0,
        ):
            """Fast 60fps vector + Text readout (avoids expensive per-frame LaTeX calls)."""

            def _builder():
                t = t_tracker.get_value()
                cur = interpolated_matrix(t) @ vec_2d
                hl = highlight_tracker.get_value()
                if is_eig == 1 and hl > 0.5:
                    col = EIG1_COLOR
                elif is_eig == 2 and hl > 0.5:
                    col = EIG2_COLOR
                else:
                    col = base_color
                arr = make_fast_vector(
                    cur,
                    plane_center,
                    unit_size,
                    col,
                    stroke_width=5.6 if (is_eig and hl > 0.5) else 4.5,
                )
                tip = plane_center + unit_size * np.array([cur[0], cur[1], 0.0])
                coord_str = (
                    f"({cur[0]:.1f}, {cur[1]:.1f})"
                    if 0.01 < t < 0.99
                    else f"({int(round(cur[0]))}, {int(round(cur[1]))})"
                )
                lbl = Text(
                    f"{name_txt} = {coord_str}",
                    font_size=18,
                    weight=BOLD if (is_eig and hl > 0.5) else "NORMAL",
                    color=col,
                ).next_to(tip, ldir, buff=0.14)
                return VGroup(arr, lbl)

            return always_redraw(_builder)

        u1_mob = fast_labelled_dyn_vec(non_eig_specs[0][0], OTHER_VEC_COLOR, "u₁", DOWN + RIGHT)
        u2_mob = fast_labelled_dyn_vec(non_eig_specs[1][0], OTHER_VEC_COLOR, "u₂", UP + LEFT)
        u3_mob = fast_labelled_dyn_vec(non_eig_specs[2][0], OTHER_VEC_COLOR, "u₃", DOWN + RIGHT)
        v1_mob = fast_labelled_dyn_vec(V1, OTHER_VEC_COLOR, "v₁", UP + LEFT, is_eig=1)
        v2_mob = fast_labelled_dyn_vec(V2, OTHER_VEC_COLOR, "v₂", DOWN + LEFT, is_eig=2)

        angle_box = RoundedRectangle(
            corner_radius=0.14,
            width=4.25,
            height=2.25,
            fill_color=PANEL_BG,
            fill_opacity=0.92,
            stroke_color=PANEL_BORDER,
            stroke_width=1.8,
        ).to_corner(UR, buff=0.28)

        def make_angle_table():
            t = t_tracker.get_value()
            M = interpolated_matrix(t)
            hl = highlight_tracker.get_value()
            rows = []
            specs = [
                ("u₁ (1,0)", non_eig_specs[0][0], OTHER_VEC_COLOR),
                ("u₂ (0,1)", non_eig_specs[1][0], OTHER_VEC_COLOR),
                ("u₃ (2,-1)", non_eig_specs[2][0], OTHER_VEC_COLOR),
                ("v₁ (1,1)", V1, EIG1_COLOR if hl > 0.5 else OTHER_VEC_COLOR),
                ("v₂ (1,-1)", V2, EIG2_COLOR if hl > 0.5 else OTHER_VEC_COLOR),
            ]
            for name, v, col in specs:
                dtheta = abs(angle_deg(M @ v) - angle_deg(v))
                if dtheta > 180:
                    dtheta = 360 - dtheta
                rows.append(
                    Text(f"{name}:  Δθ = {dtheta:4.1f}°", font_size=18, color=col)
                )
            grp = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            grp.move_to(angle_box.get_center())
            return grp

        angle_table = always_redraw(make_angle_table)

        self.play(
            FadeIn(ghost_plane),
            FadeIn(active_plane),
            FadeIn(axis_labels),
            FadeIn(dyn_square),
            FadeIn(dyn_circle),
            FadeIn(hud_box),
            FadeIn(hud_mat),
            FadeIn(t_readout),
            FadeIn(angle_box),
            FadeIn(angle_table),
            run_time=2.0,
        )
        self.play(
            Create(non_eig_spans),
            FadeIn(ghost_vecs),
            Create(eig1_span),
            Create(eig2_span),
            FadeIn(angle_arcs),
            FadeIn(u1_mob),
            FadeIn(u2_mob),
            FadeIn(u3_mob),
            FadeIn(v1_mob),
            FadeIn(v2_mob),
            run_time=2.0,
        )
        self.wait(6.0)

        # --- 0:10 to 0:30 (20.0s): Smooth ValueTracker Sweep 0 -> 1 -> 0 -> 1 ---
        self.play(t_tracker.animate.set_value(1.0), run_time=6.0, rate_func=smooth)
        self.wait(4.0)
        self.play(t_tracker.animate.set_value(0.0), run_time=3.5, rate_func=smooth)
        self.wait(1.5)
        self.play(t_tracker.animate.set_value(1.0), run_time=3.5, rate_func=smooth)
        self.wait(1.5)

        # --- 0:30 to 0:55 (25.0s): Highlight Eigenlines & Countable 1x/2x/3x Dots ---
        self.play(t_tracker.animate.set_value(0.0), run_time=2.0, rate_func=smooth)

        eig_dots = VGroup(
            Dot(plane_center + unit_size * np.array([1.0, 1.0, 0.0]), color=EIG1_COLOR, radius=0.07),
            Dot(plane_center + unit_size * np.array([2.0, 2.0, 0.0]), color=EIG1_COLOR, radius=0.07),
            Dot(plane_center + unit_size * np.array([3.0, 3.0, 0.0]), color=EIG1_COLOR, radius=0.09),
            Dot(plane_center + unit_size * np.array([1.0, -1.0, 0.0]), color=EIG2_COLOR, radius=0.09),
        )
        self.play(
            highlight_tracker.animate.set_value(1.0),
            non_eig_spans.animate.set_opacity(0.08),
            FadeIn(eig_dots, scale=1.3),
            run_time=1.5,
        )
        self.wait(2.5)
        self.play(t_tracker.animate.set_value(1.0), run_time=5.5, rate_func=smooth)

        eig_banner = make_card(
            VGroup(
                Text("v₁ = (1, 1) → (3, 3) = 3 v₁   (Δθ = 0°)", font_size=22, color=EIG1_COLOR),
                Text("v₂ = (1, -1) → (1, -1) = 1 v₂   (Δθ = 0°)", font_size=22, color=EIG2_COLOR),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            stroke_color=ACCENT_GOLD,
        ).to_edge(DOWN, buff=0.25)

        self.play(
            FadeIn(eig_banner, shift=UP * 0.15),
            Flash(plane_center + unit_size * np.array([3.0, 3.0, 0.0]), color=EIG1_COLOR),
            Flash(plane_center + unit_size * np.array([1.0, -1.0, 0.0]), color=EIG2_COLOR),
            run_time=1.5,
        )
        self.wait(12.0)

        # --- 0:55 to 1:15 (20.0s): Bridge to Algebraic Method ---
        bridge_card = make_card(
            VGroup(
                Text(
                    "Visual guessing works on simple grids...",
                    font_size=26,
                    color=TEXT_WHITE,
                ),
                Text(
                    "How do we find λ and v algebraically for ANY 2×2 matrix?",
                    font_size=26,
                    weight=BOLD,
                    color=ACCENT_GOLD,
                ),
                MathTex(
                    "\\text{Next: Solve } \\det(A - \\lambda I) = 0",
                    font_size=34,
                    color=EIG2_COLOR,
                ),
            ).arrange(DOWN, buff=0.25),
            padding_x=0.6,
            padding_y=0.45,
            stroke_color=ACCENT_GOLD,
            fill_opacity=0.96,
        ).move_to(ORIGIN)

        self.play(FadeIn(bridge_card, scale=0.95), run_time=1.5)
        self.wait(17.5)
        self.clear_scene(fade_time=1.0)

    # =========================================================================
    # SCENE 4: WORKED EXAMPLE (2:31 - 4:01, 90.0s)
    # =========================================================================
    def play_scene_4(self) -> None:
        """Animated step-by-step algebraic derivation with mini-plane verification."""
        self.setup_dark_canvas()

        header = make_section_header(
            "Worked Example: Computing Eigenvalues & Eigenvectors",
            "Matrix A = [[2, 1], [1, 2]]  —  Every Step Shown",
        )
        self.play(FadeIn(header), run_time=0.8)

        # --- Part A (0:00 to 0:12): TransformMatchingTex Av=λv -> (A-λI)v=0 ---
        left_x = -3.4
        right_x = 3.2

        given_row = VGroup(
            MathTex("A =", font_size=34, color=TEXT_WHITE),
            make_matrix_mobject([[2, 1], [1, 2]], color=ACCENT_GOLD, scale=0.8),
        ).arrange(RIGHT, buff=0.18)

        # Use double braces {{...}} so TransformMatchingTex animates symbol motion cleanly.
        eq_m1 = MathTex("A", "\\mathbf{v}", "=", "\\lambda", "\\mathbf{v}", font_size=36)
        eq_m2 = MathTex(
            "A", "\\mathbf{v}", "-", "\\lambda", "I", "\\mathbf{v}", "=", "\\mathbf{0}",
            font_size=36,
        )
        eq_m3 = MathTex(
            "(", "A", "-", "\\lambda", "I", ")", "\\mathbf{v}", "=", "\\mathbf{0}",
            font_size=38,
            color=EIG2_COLOR,
        )

        det_insight = make_card(
            MathTex(
                "\\mathbf{v} \\neq \\mathbf{0} \\iff \\det(A - \\lambda I) = 0",
                font_size=28,
                color=ACCENT_GOLD,
            ),
            padding_x=0.35,
            padding_y=0.22,
            stroke_color=ACCENT_GOLD,
        )

        given_row.move_to(np.array([left_x, 1.35, 0.0]))
        eq_pos = np.array([left_x, -0.05, 0.0])
        eq_m1.move_to(eq_pos)
        eq_m2.move_to(eq_pos)
        eq_m3.move_to(eq_pos)
        det_insight.move_to(np.array([left_x, -1.35, 0.0]))

        self.play(FadeIn(given_row), Write(eq_m1), run_time=1.6)
        self.wait(1.8)
        self.play(TransformMatchingTex(eq_m1, eq_m2), run_time=1.8)
        self.wait(1.6)
        self.play(TransformMatchingTex(eq_m2, eq_m3), run_time=1.8)
        self.wait(1.0)
        self.play(
            FadeIn(det_insight, shift=UP * 0.12),
            Circumscribe(det_insight, color=ACCENT_GOLD),
            run_time=1.6,
        )
        self.wait(1.0)

        # --- Part A continued (0:12 to 0:42): Characteristic Equation ---
        a_minus_lam = MathTex(
            "A - \\lambda I = \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix} - \\begin{bmatrix} \\lambda & 0 \\\\ 0 & \\lambda \\end{bmatrix} = \\begin{bmatrix} 2-\\lambda & 1 \\\\ 1 & 2-\\lambda \\end{bmatrix}",
            font_size=27,
            color=TEXT_WHITE,
        )
        det_1 = MathTex(
            "\\det(A - \\lambda I) = (2-\\lambda)(2-\\lambda) - (1)(1) = 0",
            font_size=27,
            color=TEXT_WHITE,
        )
        det_2 = MathTex("(2 - \\lambda)^2 - 1 = 0", font_size=30, color=TEXT_WHITE)
        det_3 = MathTex("(4 - 4\\lambda + \\lambda^2) - 1 = 0", font_size=30, color=TEXT_WHITE)
        det_4 = MathTex("\\lambda^2 - 4\\lambda + 3 = 0", font_size=32, color=ACCENT_GOLD)
        det_5 = MathTex("(\\lambda - 3)(\\lambda - 1) = 0", font_size=32, color=ACCENT_GOLD)

        lam1_pill = make_card(
            MathTex("\\lambda_1 = 3", font_size=32, color=EIG1_COLOR),
            padding_x=0.35,
            padding_y=0.2,
            stroke_color=EIG1_COLOR,
        )
        lam2_pill = make_card(
            MathTex("\\lambda_2 = 1", font_size=32, color=EIG2_COLOR),
            padding_x=0.35,
            padding_y=0.2,
            stroke_color=EIG2_COLOR,
        )
        lam_row = VGroup(lam1_pill, lam2_pill).arrange(RIGHT, buff=0.45)

        right_col = (
            VGroup(a_minus_lam, det_1, det_2, det_3, det_4, det_5, lam_row)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            .move_to(np.array([right_x, -0.45, 0.0]))
        )

        for mob, w_time in [
            (a_minus_lam, 2.8),
            (det_1, 2.8),
            (det_2, 2.4),
            (det_3, 2.8),
            (det_4, 2.8),
            (det_5, 2.8),
        ]:
            self.play(Write(mob), run_time=1.3)
            self.wait(w_time)

        self.play(
            FadeIn(lam1_pill, shift=DOWN * 0.15),
            FadeIn(lam2_pill, shift=DOWN * 0.15),
            run_time=1.3,
        )
        self.play(Indicate(lam1_pill, color=EIG1_COLOR), Indicate(lam2_pill, color=EIG2_COLOR), run_time=1.0)
        self.wait(2.5)

        part_a_objs = VGroup(given_row, eq_m3, det_insight, right_col)
        self.play(FadeOut(part_a_objs), run_time=1.0)

        # --- Part B (0:42 to 1:30): Nullspace Equations + Mini-Grid Verification ---
        divider = Line(UP * 2.1, DOWN * 3.55, color=PANEL_BORDER, stroke_width=2)
        self.play(Create(divider), run_time=0.5)

        def build_mini_plot(center_pt: np.ndarray, vec_2d: np.ndarray, scale_f: float, col: str, label_end: str):
            """Small visual check showing v -> lambda*v on its eigenline."""
            axes = NumberPlane(
                x_range=(-1, 3.5, 1),
                y_range=(-2, 3.5, 1),
                x_length=2.2,
                y_length=1.45,
                background_line_style={"stroke_color": "#243040", "stroke_width": 0.9, "stroke_opacity": 0.6},
                axis_config={"stroke_color": SUBTLE_TEXT, "stroke_width": 1.3, "include_numbers": False},
            ).move_to(center_pt)
            origin_c = axes.c2p(0, 0)
            v_start = Arrow(origin_c, axes.c2p(vec_2d[0], vec_2d[1]), buff=0, color=col, stroke_width=4)
            v_end = Arrow(origin_c, axes.c2p(scale_f * vec_2d[0], scale_f * vec_2d[1]), buff=0, color=col, stroke_width=4.5)
            lbl = Text(label_end, font_size=16, color=col).next_to(v_end.get_end(), RIGHT, buff=0.1)
            return axes, v_start, v_end, lbl

        # Case 1: lambda1 = 3
        c1_title = Text("Case 1: λ₁ = 3", font_size=26, weight=BOLD, color=EIG1_COLOR)
        c1_s1 = MathTex("(A - 3I)\\mathbf{v}_1 = \\mathbf{0}", font_size=26, color=TEXT_WHITE)
        c1_s2 = MathTex(
            "\\begin{bmatrix} -1 & 1 \\\\ 1 & -1 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\end{bmatrix} = \\begin{bmatrix} 0 \\\\ 0 \\end{bmatrix}",
            font_size=24,
            color=TEXT_WHITE,
        )
        c1_s3 = MathTex("-x + y = 0 \\implies y = x", font_size=26, color=ACCENT_GOLD)
        c1_s4 = MathTex(
            "\\text{Set } x = 1 \\implies \\mathbf{v}_1 = \\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}",
            font_size=26,
            color=EIG1_COLOR,
        )
        c1_ver = MathTex(
            "A\\mathbf{v}_1 = \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix}\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix} = \\begin{bmatrix} 3 \\\\ 3 \\end{bmatrix} = 3\\mathbf{v}_1 \\;\\checkmark",
            font_size=23,
            color=EIG1_COLOR,
        )
        case1_col = (
            VGroup(c1_title, c1_s1, c1_s2, c1_s3, c1_s4, c1_ver)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            .move_to(np.array([-3.45, 0.25, 0.0]))
        )
        c1_box = SurroundingRectangle(c1_s4, color=EIG1_COLOR, buff=0.1, corner_radius=0.08)
        m1_axes, m1_vs, m1_ve, m1_lbl = build_mini_plot(
            np.array([-3.45, -2.75, 0.0]), V1, 3.0, EIG1_COLOR, "(3,3) = 3v₁"
        )

        self.play(FadeIn(c1_title), Write(c1_s1), run_time=1.3)
        self.wait(1.2)
        self.play(Write(c1_s2), run_time=1.6)
        self.wait(2.8)
        self.play(Write(c1_s3), run_time=1.4)
        self.wait(2.0)
        self.play(Write(c1_s4), Create(c1_box), run_time=1.5)
        self.wait(2.0)
        self.play(
            Write(c1_ver),
            FadeIn(m1_axes),
            GrowArrow(m1_vs),
            run_time=1.6,
        )
        self.play(Transform(m1_vs.copy(), m1_ve), FadeIn(m1_lbl), run_time=1.5)
        self.wait(3.8)

        # Case 2: lambda2 = 1
        c2_title = Text("Case 2: λ₂ = 1", font_size=26, weight=BOLD, color=EIG2_COLOR)
        c2_s1 = MathTex("(A - 1I)\\mathbf{v}_2 = \\mathbf{0}", font_size=26, color=TEXT_WHITE)
        c2_s2 = MathTex(
            "\\begin{bmatrix} 1 & 1 \\\\ 1 & 1 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\end{bmatrix} = \\begin{bmatrix} 0 \\\\ 0 \\end{bmatrix}",
            font_size=24,
            color=TEXT_WHITE,
        )
        c2_s3 = MathTex("x + y = 0 \\implies y = -x", font_size=26, color=ACCENT_GOLD)
        c2_s4 = MathTex(
            "\\text{Set } x = 1 \\implies \\mathbf{v}_2 = \\begin{bmatrix} 1 \\\\ -1 \\end{bmatrix}",
            font_size=26,
            color=EIG2_COLOR,
        )
        c2_ver = MathTex(
            "A\\mathbf{v}_2 = \\begin{bmatrix} 2 & 1 \\\\ 1 & 2 \\end{bmatrix}\\begin{bmatrix} 1 \\\\ -1 \\end{bmatrix} = \\begin{bmatrix} 1 \\\\ -1 \\end{bmatrix} = 1\\mathbf{v}_2 \\;\\checkmark",
            font_size=23,
            color=EIG2_COLOR,
        )
        case2_col = (
            VGroup(c2_title, c2_s1, c2_s2, c2_s3, c2_s4, c2_ver)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            .move_to(np.array([3.45, 0.25, 0.0]))
        )
        c2_box = SurroundingRectangle(c2_s4, color=EIG2_COLOR, buff=0.1, corner_radius=0.08)
        m2_axes, m2_vs, m2_ve, m2_lbl = build_mini_plot(
            np.array([3.45, -2.75, 0.0]), V2, 1.0, EIG2_COLOR, "(1,-1) = 1v₂"
        )

        self.play(FadeIn(c2_title), Write(c2_s1), run_time=1.3)
        self.wait(1.2)
        self.play(Write(c2_s2), run_time=1.6)
        self.wait(2.8)
        self.play(Write(c2_s3), run_time=1.4)
        self.wait(2.0)
        self.play(Write(c2_s4), Create(c2_box), run_time=1.5)
        self.wait(2.0)
        self.play(
            Write(c2_ver),
            FadeIn(m2_axes),
            GrowArrow(m2_vs),
            run_time=1.6,
        )
        self.play(Indicate(m2_vs, color=EIG2_COLOR), FadeIn(m2_lbl), run_time=1.5)
        self.wait(3.8)

        self.clear_scene(fade_time=1.0)

    # =========================================================================
    # SCENE 5: INTERPRETATION (4:01 - 4:49, 48.0s)
    # =========================================================================
    def play_scene_5(self) -> None:
        """Eigen-box scaling, live animated lambda slider, and engineering applications."""
        self.setup_dark_canvas()

        # --- 0:00 to 0:20 (20.0s): Eigen-Box Area Scaling + Vector Stretching ---
        unit_size = 0.72
        plane_center = np.array([-2.65, 0.05, 0.0])
        ghost_plane, active_plane = make_plane_pair(
            x_range=(-4, 4, 1),
            y_range=(-4, 4, 1),
            unit_size=unit_size,
            center=plane_center,
        )
        axis_labels = make_axis_labels(ghost_plane)
        base_grid = active_plane.copy()
        t_tracker = ValueTracker(0.0)

        active_plane.add_updater(
            lambda m: m.become(base_grid.copy()).apply_matrix(
                interpolated_matrix(t_tracker.get_value()),
                about_point=plane_center,
            )
        )

        span1 = make_span_line(V1, plane_center, unit_size, 4.3, EIG1_COLOR, 0.65)
        span2 = make_span_line(V2, plane_center, unit_size, 4.3, EIG2_COLOR, 0.65)

        # Parallelogram spanned by v1 and v2 visibly scales area by det(A) = lambda1*lambda2 = 3.
        eigen_box = always_redraw(
            lambda: Polygon(
                plane_center,
                plane_center + unit_size * np.array([*(interpolated_matrix(t_tracker.get_value()) @ V1), 0.0]),
                plane_center
                + unit_size * np.array([*(interpolated_matrix(t_tracker.get_value()) @ (V1 + V2)), 0.0]),
                plane_center + unit_size * np.array([*(interpolated_matrix(t_tracker.get_value()) @ V2), 0.0]),
                color=UNIT_SHAPE_COLOR,
                stroke_width=2.0,
                fill_color=UNIT_SHAPE_COLOR,
                fill_opacity=0.16,
            )
        )

        v1_dyn = always_redraw(
            lambda: VGroup(
                make_fast_vector(
                    interpolated_matrix(t_tracker.get_value()) @ V1,
                    plane_center,
                    unit_size,
                    EIG1_COLOR,
                    stroke_width=5.6,
                ),
                Text(
                    f"{1.0 + 2.0 * t_tracker.get_value():.1f} v₁",
                    font_size=20,
                    weight=BOLD,
                    color=EIG1_COLOR,
                ).next_to(
                    plane_center
                    + unit_size * np.array([*(interpolated_matrix(t_tracker.get_value()) @ V1), 0.0]),
                    UP + LEFT,
                    buff=0.12,
                ),
            )
        )
        v2_dyn = always_redraw(
            lambda: VGroup(
                make_fast_vector(
                    interpolated_matrix(t_tracker.get_value()) @ V2,
                    plane_center,
                    unit_size,
                    EIG2_COLOR,
                    stroke_width=5.6,
                ),
                Text(
                    "1.0 v₂",
                    font_size=20,
                    weight=BOLD,
                    color=EIG2_COLOR,
                ).next_to(
                    plane_center
                    + unit_size * np.array([*(interpolated_matrix(t_tracker.get_value()) @ V2), 0.0]),
                    DOWN + RIGHT,
                    buff=0.12,
                ),
            )
        )

        perp_mark = RightAngle(
            Line(plane_center, plane_center + unit_size * np.array([1.0, 1.0, 0.0])),
            Line(plane_center, plane_center + unit_size * np.array([1.0, -1.0, 0.0])),
            length=0.25,
            color=ACCENT_GOLD,
        )

        interp_panel = make_card(
            VGroup(
                Text("What λ Means Geometrically", font_size=25, weight=BOLD, color=TEXT_WHITE),
                Text("λ₁ = 3  →  3× stretch along (1, 1)", font_size=21, color=EIG1_COLOR),
                Text("λ₂ = 1  →  1× unchanged along (1, -1)", font_size=21, color=EIG2_COLOR),
                Text("v₁ ⊥ v₂  &  Area scales by λ₁·λ₂ = 3", font_size=20, color=ACCENT_GOLD),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16),
            padding_x=0.38,
            padding_y=0.26,
        ).move_to(np.array([3.65, 2.25, 0.0]))

        self.play(
            FadeIn(ghost_plane),
            FadeIn(active_plane),
            FadeIn(axis_labels),
            Create(span1),
            Create(span2),
            FadeIn(eigen_box),
            FadeIn(v1_dyn),
            FadeIn(v2_dyn),
            Create(perp_mark),
            FadeIn(interp_panel),
            run_time=2.5,
        )
        self.wait(2.0)
        self.play(t_tracker.animate.set_value(1.0), run_time=5.5, rate_func=smooth)
        self.wait(8.0)

        # --- 0:20 to 0:38 (18.0s): Live Animated Lambda-Slider Showcase ---
        lam_tracker = ValueTracker(2.0)
        slider_center = np.array([3.65, -0.7, 0.0])

        slider_frame = RoundedRectangle(
            corner_radius=0.14,
            width=5.4,
            height=2.85,
            fill_color=PANEL_BG,
            fill_opacity=0.92,
            stroke_color=ACCENT_GOLD,
            stroke_width=1.8,
        ).move_to(slider_center)

        slider_title = Text(
            "How Other λ Values Act on v",
            font_size=23,
            weight=BOLD,
            color=TEXT_WHITE,
        ).move_to(slider_center + UP * 1.05)

        axis_1d = DashedLine(
            slider_center + LEFT * 2.2 + DOWN * 0.1,
            slider_center + RIGHT * 2.2 + DOWN * 0.1,
            color=SUBTLE_TEXT,
            stroke_width=2.0,
        )
        zero_dot = Dot(slider_center + DOWN * 0.1, color=TEXT_WHITE, radius=0.06)

        def _build_lam_arrow():
            lam = lam_tracker.get_value()
            origin_1d = slider_center + DOWN * 0.1
            end_x = lam * 0.85
            if abs(lam) < 0.08:
                col = ACCENT_GOLD
                vec_mob = Dot(origin_1d, radius=0.11, color=ACCENT_GOLD)
                status = "λ = 0  →  Collapses line to 0  (det A = 0!)"
            elif lam < 0:
                col = ACCENT_RED
                vec_mob = Arrow(origin_1d, origin_1d + RIGHT * end_x, buff=0, color=col, stroke_width=5.5)
                status = f"λ = {lam:+.1f}  →  Flips 180° & scales by |λ|"
            elif lam < 1.0:
                col = EIG2_COLOR
                vec_mob = Arrow(origin_1d, origin_1d + RIGHT * end_x, buff=0, color=col, stroke_width=5.5)
                status = f"λ = {lam:+.1f}  →  Shrinks toward origin"
            else:
                col = EIG1_COLOR
                vec_mob = Arrow(origin_1d, origin_1d + RIGHT * end_x, buff=0, color=col, stroke_width=5.5)
                status = f"λ = {lam:+.1f}  →  Stretches along eigenline"
            txt = Text(status, font_size=19, weight=BOLD, color=col).move_to(
                slider_center + DOWN * 0.92
            )
            return VGroup(vec_mob, txt)

        dyn_lam_view = always_redraw(_build_lam_arrow)

        self.play(
            FadeIn(slider_frame),
            FadeIn(slider_title),
            Create(axis_1d),
            FadeIn(zero_dot),
            FadeIn(dyn_lam_view),
            run_time=1.5,
        )
        # Sweep through: stretch (+2.0) -> shrink (+0.5) -> singular collapse (0.0) -> 180° flip (-2.0).
        self.play(lam_tracker.animate.set_value(0.5), run_time=2.5, rate_func=smooth)
        self.wait(1.8)
        self.play(lam_tracker.animate.set_value(0.0), run_time=2.2, rate_func=smooth)
        self.play(Flash(slider_center + DOWN * 0.1, color=ACCENT_GOLD, flash_radius=0.32), run_time=0.8)
        self.wait(2.2)
        self.play(lam_tracker.animate.set_value(-2.0), run_time=2.8, rate_func=smooth)
        self.wait(4.2)

        # --- 0:38 to 0:48 (10.0s): Engineering Applications Cards ---
        app1 = make_card(
            Text("Vibrations: natural mode shapes", font_size=20, color=EIG1_COLOR),
            padding_x=0.35,
            padding_y=0.22,
            stroke_color=EIG1_COLOR,
        )
        app2 = make_card(
            Text("PCA: principal data axes", font_size=20, color=EIG2_COLOR),
            padding_x=0.35,
            padding_y=0.22,
            stroke_color=EIG2_COLOR,
        )
        app3 = make_card(
            Text("Google PageRank: web authority", font_size=20, color=ACCENT_GOLD),
            padding_x=0.35,
            padding_y=0.22,
            stroke_color=ACCENT_GOLD,
        )
        apps_row = VGroup(app1, app2, app3).arrange(RIGHT, buff=0.32).to_edge(DOWN, buff=0.25)

        self.play(
            LaggedStart(
                FadeIn(app1, shift=UP * 0.15),
                FadeIn(app2, shift=UP * 0.15),
                FadeIn(app3, shift=UP * 0.15),
                lag_ratio=0.22,
            ),
            run_time=2.2,
        )
        self.wait(6.8)
        self.clear_scene(fade_time=1.0)

    # =========================================================================
    # SCENE 6: SUMMARY & CLOSING CREDITS (4:49 - 5:14, 25.0s)
    # =========================================================================
    def play_scene_6(self) -> None:
        """Kinetic 3-takeaway recap followed by references and closing credits."""
        self.setup_dark_canvas()

        # --- 0:00 to 0:13 (13.0s): 3 Core Takeaways ---
        header = make_section_header("Summary: 3 Key Takeaways")
        self.play(FadeIn(header), run_time=0.8)

        t1 = make_card(
            VGroup(
                Text("1. Geometric Meaning", font_size=26, weight=BOLD, color=EIG1_COLOR),
                Text(
                    "Eigenvectors stay on their own span line under A  (Av = λv).",
                    font_size=22,
                    color=TEXT_WHITE,
                ),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            stroke_color=EIG1_COLOR,
        )
        t2 = make_card(
            VGroup(
                Text("2. Algebraic Method", font_size=26, weight=BOLD, color=EIG2_COLOR),
                Text(
                    "Solve det(A - λI) = 0 for λ, then solve (A - λI)v = 0 for v.",
                    font_size=22,
                    color=TEXT_WHITE,
                ),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            stroke_color=EIG2_COLOR,
        )
        t3 = make_card(
            VGroup(
                Text("3. Scaling Factor λ", font_size=26, weight=BOLD, color=ACCENT_GOLD),
                Text(
                    "λ tells whether v stretches, shrinks, flips (λ < 0), or collapses (λ = 0).",
                    font_size=22,
                    color=TEXT_WHITE,
                ),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            stroke_color=ACCENT_GOLD,
        )
        takeaways = VGroup(t1, t2, t3).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.25)

        for card, col in [(t1, EIG1_COLOR), (t2, EIG2_COLOR), (t3, ACCENT_GOLD)]:
            self.play(FadeIn(card, shift=RIGHT * 0.25), run_time=1.0)
            self.play(Circumscribe(card, color=col, fade_out=True), run_time=1.0)
            self.wait(1.2)

        self.wait(2.6)
        self.play(FadeOut(takeaways), FadeOut(header), run_time=0.8)

        # --- 0:13 to 0:25 (12.0s): Closing Frame ---
        closing_title = Text(
            "References & Credits",
            font_size=36,
            weight=BOLD,
            color=TEXT_WHITE,
        )
        refs = Text(
            "References:\n"
            "• Gilbert Strang, Introduction to Linear Algebra (5th ed.)\n"
            "• 3Blue1Brown, Essence of Linear Algebra — Ch. 14: Eigenvectors & Eigenvalues\n"
            "• M3 Course Lecture Notes — Linear Algebra & Calculus",
            font_size=22,
            color=SUBTLE_TEXT,
            line_spacing=1.35,
        )
        footer = Text(
            "Student Name: Shlok Sharma    |    Student ID: E25B070773",
            font_size=24,
            weight=BOLD,
            color=EIG2_COLOR,
        )

        closing_group = VGroup(closing_title, refs, footer).arrange(
            DOWN, aligned_edge=LEFT, buff=0.38
        )
        closing_card = make_card(closing_group, padding_x=0.7, padding_y=0.55)

        self.play(FadeIn(closing_card, scale=0.96), run_time=1.2)
        self.wait(9.2)
        self.play(FadeOut(closing_card), run_time=0.8)


class Scene1_Hook(EigenBaseScene):
    """Standalone Scene 1: Opening Frame & Hook."""

    def construct(self) -> None:
        self.play_scene_1()


class Scene2_ConceptIntro(EigenBaseScene):
    """Standalone Scene 2: Concept Introduction."""

    def construct(self) -> None:
        self.play_scene_2()


class Scene3_VisualIntuition(EigenBaseScene):
    """Standalone Scene 3: Visual Intuition."""

    def construct(self) -> None:
        self.play_scene_3()


class Scene4_WorkedExample(EigenBaseScene):
    """Standalone Scene 4: Worked Example."""

    def construct(self) -> None:
        self.play_scene_4()


class Scene5_Interpretation(EigenBaseScene):
    """Standalone Scene 5: Interpretation & Applications."""

    def construct(self) -> None:
        self.play_scene_5()


class Scene6_Summary(EigenBaseScene):
    """Standalone Scene 6: Summary & Credits."""

    def construct(self) -> None:
        self.play_scene_6()


class FullVideo(EigenBaseScene):
    """Complete ~5:14 video chaining all 6 storyboard scenes seamlessly."""

    def construct(self) -> None:
        self.play_scene_1()
        self.play_scene_2()
        self.play_scene_3()
        self.play_scene_4()
        self.play_scene_5()
        self.play_scene_6()
