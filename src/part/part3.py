from manim import *

class Cardioid_by_TwoCircles(Scene):

    CONFIG = {
        'bg_color': WHITE,
        'circle_color': ManimColor("#F1F3F8"),
        # 'circle_num': 36,
        'circle_width': 6,
        'curve_color': RED_B,
        'curve_width': 4,
        'circle_r': 1.25,
        'circle_loc': ORIGIN,
        'arrow_color': RED,

        "parametric_function_step_size": 0.005,
        "slow_factor": 0.25,
        "draw_time": 4,
    }
    def setup(self):
        config = {**Cardioid_by_TwoCircles.CONFIG, **type(self).CONFIG}
        for key, value in config.items():
            setattr(self, key, value)

        for key, value in self.CONFIG.items():
          if hasattr(self, key):
              setattr(self, key, value)



    def construct(self):

        self.setup_scene()
        self.wait(0.4)

        self.play(FadeIn(self.origin), run_time=0.5)
        self.play(Create(self.circle_0), run_time=0.8)
        self.wait(0.2)
        self.play(Create(self.circle_1[0]), run_time=0.8)
        self.wait(0.2)
        self.play(Create(self.circle_1[1]), run_time=0.8)
        self.wait(0.8)
        self.always_continually_update = True

        dt = 1/29.9
        step_n = 160
        d_theta = -TAU/step_n
        self.line_group = VGroup()
        p_old = self.circle_1[2].get_center()

        # path = self.get_path()
        # broken_path = CurvesAsSubmobjects(path)
        # broken_path.curr_time = 0
        # broken_path.set_color(self.curve_color)

        # self.draw_path()

        for i in range(1, step_n + 1):
            self.circle_1.rotate_about_origin(d_theta)
            self.circle_1.rotate(d_theta)
            p_new = self.circle_1[2].get_center()
            line_i = Line(p_old, p_new, color=self.curve_color, stroke_width=self.curve_width)
            self.line_group.add(line_i)
            self.add(line_i)
            self.wait(dt)
            p_old = p_new

            # alpha = path.curr_time * self.get_slow_factor()
            # n_curves = len(path)
            # for a, sp in zip(np.linspace(0, 1, n_curves), path):
            #     b = alpha - a
            #     if b < 0:
            #         width = 0
            #     else:
            #         width = self.curve_width
            #     sp.set_stroke(width=width)
            # path.curr_time += dt
            self.wait(dt)

        self.wait(3)

    def setup_scene(self):
        bg_rect = Rectangle(fill_color=self.bg_color, fill_opacity=1).scale(20)
        self.add(bg_rect)
        self.wait(0.25)

        self.origin = Circle(radius=0.05, color=RED_B, fill_color=RED_B, fill_opacity=1)

        self.circle_0 = Circle(radius=self.circle_r, color=self.circle_color).move_to(self.circle_loc)
        self.circle_1 = VGroup(Circle(radius=self.circle_r, color=self.circle_color),
                               Vector(DOWN * self.circle_r, color=self.arrow_color),
                               Dot(DOWN * self.circle_r, color=self.arrow_color),
                               Vector(UP * self.circle_r, color=self.arrow_color),
                               Dot(UP * self.circle_r, color=self.arrow_color)).shift(self.circle_loc + 2 * UP * self.circle_r)
        self.two_cirlce = VGroup(self.circle_0, self.circle_1)

    def define_func(self):
        self.func = lambda t: self.circle_loc + np.array([(1 - np.sin(t)) * np.cos(t), (1 - np.sin(t)) * np.sin(t), 0]) * self.circle_r * 2

    def setup_slow_factor(self):
        self.slow_factor_tracker = ValueTracker(
            self.slow_factor
        )

    def get_slow_factor(self):
        return self.slow_factor_tracker.get_value()

    def get_path(self):
        self.define_func()
        path = ParametricFunction(
            self.func,
            t_min=0,
            t_max=2 * PI,
            color=self.curve_color,
            step_size=self.parametric_function_step_size
        )
        return path

    def draw_path(self):
        self.setup_slow_factor()
        path = self.get_path()
        broken_path = CurvesAsSubmobjects(path)
        broken_path.curr_time = 0

        def update_path(path, dt):
            alpha = path.curr_time * self.get_slow_factor()
            n_curves = len(path)
            for a, sp in zip(np.linspace(0, 1, n_curves), path):
                b = alpha - a
                if b < 0:
                    width = 0
                else:
                    width = self.curve_width
                sp.set_stroke(width=width)
            path.curr_time += dt
            return path

        broken_path.set_color(self.curve_color)
        broken_path.add_updater(update_path)
        return broken_path
