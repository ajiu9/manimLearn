from manim import *

config.background_color = WHITE
config.frame_height = 10
config.frame_width = 10

config.pixel_width = 500
config.pixel_height = 500

class Configuration(Scene):
    def construct(self):
        plan = NumberPlane()
        t = Triangle(color=RED, fill_opacity=0.5)
        self.add(plan, t)
