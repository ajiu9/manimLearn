from manim import *
from manim.opengl import *


class OpenGLIntro(ThreeDScene):
    def construct(self):
        hello_world = Text("Hello World!").to_edge(UL)
        self.play(Write(hello_world))
        self.wait(1)
        self.play(FadeOut(hello_world))

        # 定义三维表面
        surface = Surface(
            lambda u, v: np.array([u, v, u*np.sin(v) + v*np.cos(u)]),  # 曲面方程
            u_range=(-3, 3),  # u轴范围
            v_range=(-3, 3),  # v轴范围
        )

        # 设置相机视角
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
         # 动画创建表面
        self.play(Create(surface))
        self.wait()  # 显示表面一段时间


class OpenGLIntro1(Scene):
    def construct(self):
        hello_world = Text("Hello World!")
        self.play(Write(hello_world))
        self.wait(1)

        self.play(
            self.camera.animate.set_euler_angles(
                phi=50 * DEGREES,
                theta=-10 * DEGREES,
            )
        )
        self.play(FadeOut(hello_world))

        surface = OpenGLSurface(
            lambda u, v: np.array([u, v, u*np.sin(v) + v*np.cos(u)]),  # 曲面方程
            u_range=(-3, 3),  # u轴范围
            v_range=(-3, 3),  # v轴范围
        )
        surface_mesh = OpenGLSurfaceMesh(surface)
        self.play(Create(surface_mesh))
        self.play(FadeTransform(surface_mesh, surface))
        self.wait()

        light = self.camera.light_source
        self.play(light.animate.shift([0,0,-20]))
        self.play(light.animate.shift([0,0,10]))
        self.play(self.camera.animate.set_euler_angles(theta=60*DEGREES))
        self.wait()

        # # 设置相机视角
        # self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        #  # 动画创建表面
        # self.play(Create(surface))
        # self.wait()  # 显示表面一段时间
