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

class AnimationSyntax(Scene):
    def construct(self):
        s = Square(color=RED, fill_opacity=0.5)
        c = Circle(color=BLUE, fill_opacity=0.5)
        self.play(s.animate.shift(UP), c.animate.shift(DOWN))
        self.play(VGroup(s,c).animate.arrange(RIGHT, buff=1))
        self.play(c.animate(rate_func=linear).shift(RIGHT).scale(2))


class AnimationProblems(Scene):
        def construct(self):
            left_square = Square(color=RED, fill_opacity=0.5)
            right_square = Square(color=GREEN, fill_opacity=0.5)
            VGroup(left_square, right_square).arrange(RIGHT, buff=1)
            self.add(left_square, right_square)
            self.play(left_square.animate.rotate(PI), Rotate(right_square, PI), run_time=2)
            self.wait()

class AnimationMechanics(Scene):
    def construct(self):
        c = Circle()
        c.generate_target()
        c.target.set_fill(color=GREEN, opacity=1)
        c.target.shift(2*RIGHT + UP).scale(0.5)
        self.add(c)
        self.wait()
        self.play(MoveToTarget(c))

        s = Square()
        s.save_state()
        self.play(FadeIn(s))
        self.play(s.animate.set_color(PURPLE).set_opacity(0.5).shift(2*LEFT).scale(3))
        self.play(s.animate.shift(5*DOWN).rotate(PI/2))
        self.wait()
        self.play(Restore(s), run_time=2)
        self.wait()
