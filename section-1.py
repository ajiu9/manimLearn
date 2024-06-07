from manim import *

class Try(Scene):
    def construct(self):
        c = Circle(fill_opacity=1)
        s = Square(color=YELLOW, fill_opacity=1)
        self.play(FadeIn(c))
        self.wait()
        self.play(ReplacementTransform(c, s))
        self.wait()
        self.play(FadeOut(s))
        self.wait()


class SecondExample(Scene): 
    def construct(self):
        ax = Axes(x_range=[-3, 3], y_range=[-3, 3])
        curve = ax.plot(lambda x: (x+2)*x*(x-2)/2, color=RED)
        area = ax.get_area(curve, x_range=[-2, 2])
        self.play(Create(ax, run_time=2), Create(curve, run_time=5))
        self.play(FadeIn(area))
        # self.add(ax, curve, area)

class SquareToCircle(Scene):
    def construct(self):
        square = Square(color=RED, fill_opacity=0.5)
        circle = Circle(color=BLUE, fill_opacity=0.5)
        self.play(DrawBorderThenFill(square))
        self.play(ReplacementTransform(square, circle))
        self.play(FadeOut(circle))
