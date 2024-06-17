from fourier_series import FourierOfTrebleClef
from manim import *
from pathlib import Path
script_dir = Path(__file__).parent


class ComplexFourierSeriesExample(FourierOfTrebleClef):
    CONFIG = {
        "file_name": "LOVE.svg",
        "run_time": 10,
        "n_vectors": 200,
        "n_cycles": 2,
        "max_circle_stroke_width": 0.75,
        "drawing_height": 5,
        "center_point": DOWN,
        "top_row_center": 3 * UP,
        "top_row_label_y": 2,
        "top_row_x_spacing": 1.75,
        "top_row_copy_scale_factor": 0.9,
        "start_drawn": False,
        "plane_config": {
            "axis_config": {"unit_size": 2},
            "y_min": -1.25,
            "y_max": 1.25,
            "x_min": -2.5,
            "x_max": 2.5,
            "background_line_style": {
                "stroke_width": 1,
                "stroke_color": GREY_B,
            },
        },
        "top_rect_height": 2.5,
    }

    def setup(self):
        super().setup()
        self.file_name = 'LOVE.svg'
        self.run_time = 10
        self.n_vectors = 200
        self.n_cycles = 2
        self.max_circle_stroke_width = 0.75
        self.top_row_copy_scale_factor = 0.9
        self.start_drawn = False
        self.plane_config = {
            "axis_config": {"unit_size": 2},
            "y_min": -1.25,
            "y_max": 1.25,
            "x_min": -2.5,
            "x_max": 2.5,
            "background_line_style": {
                "stroke_width": 1,
                "stroke_color": GREY_B,
            },
        }
        self.top_rect_height = False

        self.add_vectors_circles_path()
        self.add_top_row(self.vectors, self.circles)
        self.write_title()
        self.highlight_vectors_one_by_one()
        self.change_shape()


    def write_title(self):
        title = OldTexText("Complex\\\\Fourier series")
        title.scale(1.5)
        title.to_edge(LEFT)
        title.match_y(self.path)

        self.wait(11)
        self.play(FadeInFromDown(title))
        self.wait(2)
        self.title = title

    def highlight_vectors_one_by_one(self):
        # Don't know why these vectors can't get copied.
        # That seems like a problem that will come up again.
        labels = self.top_row[-1]
        next_anims = []
        for vector, circle, label in zip(self.vectors, self.circles, labels):
            # v_color = vector.get_color()
            c_color = circle.get_color()
            c_stroke_width = circle.get_stroke_width()

            rect = SurroundingRectangle(label, color=PINK)
            self.play(
                # vector.set_color, PINK,
                circle.set_stroke, RED, 3,
                FadeIn(rect),
                *next_anims
            )
            self.wait()
            next_anims = [
                # vector.set_color, v_color,
                circle.set_stroke, c_color, c_stroke_width,
                FadeOut(rect),
            ]
        self.play(*next_anims)

    def change_shape(self):
        # path_mob = OldTex("\\pi")
        path_mob = SVGMobject("Nail_And_Gear")
        new_path = path_mob.family_members_with_points()[0]
        new_path.set_height(4)
        new_path.move_to(self.path, DOWN)
        new_path.shift(0.5 * UP)

        self.transition_to_alt_path(new_path)
        for n in range(self.n_cycles):
            self.run_one_cycle()

    def transition_to_alt_path(self, new_path, morph_path=False):
        new_coefs = self.get_coefficients_of_path(new_path)
        new_vectors = self.get_rotating_vectors(
            coefficients=new_coefs
        )
        new_drawn_path = self.get_drawn_path(new_vectors)

        self.vector_clock.suspend_updating()

        vectors = self.vectors
        anims = []

        for vect, new_vect in zip(vectors, new_vectors):
            new_vect.update()
            new_vect.clear_updaters()

            line = Line(stroke_width=0)
            line.put_start_and_end_on(*vect.get_start_and_end())
            anims.append(ApplyMethod(
                line.put_start_and_end_on,
                *new_vect.get_start_and_end()
            ))
            vect.freq = new_vect.freq
            vect.coefficient = new_vect.coefficient

            vect.line = line
            vect.add_updater(
                lambda v: v.put_start_and_end_on(
                    *v.line.get_start_and_end()
                )
            )
        if morph_path:
            anims.append(
                ReplacementTransform(
                    self.drawn_path,
                    new_drawn_path
                )
            )
        else:
            anims.append(
                FadeOut(self.drawn_path)
            )

        self.play(*anims, run_time=3)
        for vect in self.vectors:
            vect.remove_updater(vect.updaters[-1])

        if not morph_path:
            self.add(new_drawn_path)
            self.vector_clock.set_value(0)

        self.vector_clock.resume_updating()
        self.drawn_path = new_drawn_path

    #
    def get_path(self):
        path = super().get_path()
        path.set_height(self.drawing_height)
        path.to_edge(DOWN)
        return path

    def add_top_row(self, vectors, circles, max_freq=3):
        self.top_row = self.get_top_row(
            vectors, circles, max_freq
        )
        self.add(self.top_row)

    def get_top_row(self, vectors, circles, max_freq=3):
        vector_copies = VGroup()
        circle_copies = VGroup()
        for vector, circle in zip(vectors, circles):
            if vector.freq > max_freq:
                break
            vcopy = vector.copy()
            vcopy.clear_updaters()
            ccopy = circle.copy()
            ccopy.clear_updaters()
            ccopy.original = circle
            vcopy.original = vector

            vcopy.center_point = op.add(
                self.top_row_center,
                vector.freq * self.top_row_x_spacing * RIGHT,
            )
            ccopy.center_point = vcopy.center_point
            vcopy.add_updater(self.update_top_row_vector_copy)
            ccopy.add_updater(self.update_top_row_circle_copy)
            vector_copies.add(vcopy)
            circle_copies.add(ccopy)

        dots = VGroup(*[
            OldTex("\\dots").next_to(
                circle_copies, direction,
                MED_LARGE_BUFF,
            )
            for direction in [LEFT, RIGHT]
        ])
        labels = self.get_top_row_labels(vector_copies)
        return VGroup(
            vector_copies,
            circle_copies,
            dots,
            labels,
        )

    def update_top_row_vector_copy(self, vcopy):
        vcopy.become(vcopy.original)
        vcopy.scale(self.top_row_copy_scale_factor)
        vcopy.shift(vcopy.center_point - vcopy.get_start())
        return vcopy

    def update_top_row_circle_copy(self, ccopy):
        ccopy.become(ccopy.original)
        ccopy.scale(self.top_row_copy_scale_factor)
        ccopy.move_to(ccopy.center_point)
        return ccopy

    def get_top_row_labels(self, vector_copies):
        labels = VGroup()
        for vector_copy in vector_copies:
            freq = vector_copy.freq
            label = Integer(freq)
            label.move_to(np.array([
                freq * self.top_row_x_spacing,
                self.top_row_label_y,
                0
            ]))
            labels.add(label)
        return labels

    def setup_plane(self):
        plane = ComplexPlane(**self.plane_config)
        plane.shift(self.center_point)
        plane.add_coordinates()

        top_rect = Rectangle(
            width=FRAME_WIDTH,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0,
            height=self.top_rect_height,
        )
        top_rect.to_edge(UP, buff=0)

        self.plane = plane
        self.add(plane)
        self.add(top_rect)

    def get_path_end(self, vectors, stroke_width=None, **kwargs):
        if stroke_width is None:
            stroke_width = self.drawn_path_st
        full_path = self.get_vector_sum_path(vectors, **kwargs)
        path = VMobject()
        path.set_stroke(
            self.drawn_path_color,
            stroke_width
        )

        def update_path(p):
            alpha = self.get_vector_time() % 1
            p.pointwise_become_partial(
                full_path,
                np.clip(alpha - 0.01, 0, 1),
                np.clip(alpha, 0, 1),
            )
            p.get_points()[-1] = vectors[-1].get_end()

        path.add_updater(update_path)
        return path

    def get_drawn_path_alpha(self):
        return super().get_drawn_path_alpha() - 0.002

    def get_drawn_path(self, vectors, stroke_width=2, **kwargs):
        odp = super().get_drawn_path(vectors, stroke_width, **kwargs)
        return VGroup(
            odp,
            self.get_path_end(vectors, stroke_width, **kwargs),
        )

    def get_vertically_falling_tracing(self, vector, color, stroke_width=3, rate=0.25):
        path = VMobject()
        path.set_stroke(color, stroke_width)
        path.start_new_path(vector.get_end())
        path.vector = vector

        def update_path(p, dt):
            p.shift(rate * dt * DOWN)
            p.add_smooth_curve_to(p.vector.get_end())
        path.add_updater(update_path)
        return path

