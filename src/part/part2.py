from manim import *

class Cardioid_by_Circle(Scene):

    CONFIG = {
        'bg_color': WHITE,
        # 'bg_color': BLACK,
        'circle_color': RED,
        'circle_num': 36,
        'circle_width': 2,
        # 'curve_color': RED_B,
        # 'curve_width': 4,
        'circle_r': 1,
        'circle_loc': ORIGIN,
    }

    def setup(self):
        config = {**Cardioid_by_Circle.CONFIG, **type(self).CONFIG}
        for key, value in config.items():
            setattr(self, key, value)

        for key, value in self.CONFIG.items():
          if hasattr(self, key):
              setattr(self, key, value)



    def construct(self):

        bg_rect = Rectangle(fill_color=self.bg_color, fill_opacity=1).scale(20)
        self.add(bg_rect)
        self.wait(0.25)

        self.create_all()

        self.play(FadeIn(self.circle))
        self.wait()

        # self.always_continually_update = True

        for i in range(self.circle_num):

            self.play(ReplacementTransform(self.r_group[i], self.r_group[i+1]), run_time=0.1)
            self.play(Create(self.circles[i]), run_time=0.2)
        self.play(FadeOut(self.r_group[-1]), FadeOut(self.circle))

        self.wait(2)

    def create_all(self):

        n = self.circle_num
        self.circle = Circle(radius=self.circle_r, color=BLUE, stroke_width=self.circle_width).move_to(self.circle_loc)

        self.circles = VGroup()

        delta_a = TAU / (n + 1)
        vector_0 = UP * self.circle_r

        r1 = Line(self.circle.get_center() + UP * self.circle_r, self.circle.get_center() + UP * self.circle_r, color=self.circle_color)
        r2 = Line(self.circle.get_center(), self.circle.get_center() + UP * self.circle_r, color=BLUE)

        self.r_group = VGroup(VGroup(r1, r2))

        for i in range(n):
            vector_i = np.array([np.sin(delta_a * (i + 1)), np.cos(delta_a * (i + 1)), 0]) * self.circle_r
            circle_i = Circle(radius=np.sqrt(sum((vector_i-vector_0) ** 2)), color=self.circle_color, stroke_width=self.circle_width).move_to(self.circle.get_center() + vector_i)
            self.circles.add(circle_i)

            r1_i = Line(self.circle.get_center() + UP * self.circle_r, self.circles[i].get_center(), color=self.circle_color)
            r2_i = Line(self.circle.get_center(), self.circles[i].get_center(), color=BLUE)
            self.r_group.add(VGroup(r1_i, r2_i))
