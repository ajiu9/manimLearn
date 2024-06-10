from manim import *

from colour import Color
class BasicAnimation(Scene):
    def construct(self):
        polys = VGroup(
            *[RegularPolygon(5, radius=1, fill_opacity=0.5, color=Color(hue=j/5, saturation=0.5, luminance=0.5)) for j in range(5)]
            ).arrange(RIGHT)
        self.play(DrawBorderThenFill(polys), run_time=2)
        self.play(
            Rotate(polys[0], PI, rate_func=lambda t: t), # linear
            Rotate(polys[1], PI, rate_func=smooth), # default behavior
            Rotate(polys[2], PI, rate_func=lambda t: np.sin(t*PI)),
            Rotate(polys[3], PI, rate_func=there_and_back),
            Rotate(polys[4], PI, rate_func=lambda t: 1 - abs(1- 2*t)),
           run_time=2
        )
        self.wait()

class ConflictingAnimation(Scene):
    def construct(self):
        s = Square(color=RED, fill_opacity=0.5)
        self.play(Rotate(s,PI), Rotate(s,-PI), run_time=3)
        self.wait()

class LaggingAnimation(Scene):
    def construct(self):
        squares = VGroup(
            *[Square(color=Color(hue=j/20, saturation=0.5, luminance=0.5), fill_opacity=0.5) for j in range(20)]
        ).arrange_in_grid(4,5).scale(0.75)
        self.play(AnimationGroup(*[FadeIn(s) for s in squares], lag_ratio=0.25, run_time=2))

