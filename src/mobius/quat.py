from manim import *

class Nudging(Scene):
    def construct(self):
        # func = lambda pos: np.sin(pos[1] / 2) * RIGHT + np.cos(pos[0] / 2) * UP
        def func (pos):
            x, y, z = pos
            return RIGHT * (8 * x + 6 * y) + UP * (-9 * x - 7 * y)
            # return RIGHT * (x + y) + UP * (4*x + y)
            return RIGHT * 2*x + UP* -3 * y
            return RIGHT * (-3*x + y) + UP*(-2*x - y)
            return x * (-3*RIGHT - 2*UP) + y * (1*RIGHT - 1*UP)

        vector_field = ArrowVectorField(
            func, x_range=[-7, 7, 1], y_range=[-7, 7, 1], 
            # length_func=lambda x: np.log(x),
            max_color_scheme_value=30
        )
        self.add(vector_field)
        # dot = Dot().move_to([2, 0, 0])
        dots = 10
        dots_m = VGroup()
        for i in range(dots):
            # get evenly spaced points on the circle certened at the origin
            # with radius 1
            dot_ref = Dot().move_to([4, 0, 0])
            d = dot_ref.copy().rotate(i * 2*PI/dots, about_point=ORIGIN)
            # vector_field.nudge(d, -0.3, 30)
            d.add_updater(vector_field.get_nudge_updater(speed=0.75))
            t = TracedPath(d.get_center, 
                           stroke_color=color_gradient([RED_E, RED_A], 3),)
                        #    dissipating_time=1,
                        #    stroke_opacity=[0, 1])
            dots_m.add(d, t)

        # vector_field.nudge(dots_m, -1, 60)
        # vector_field.nudge(dot, -0.5, 60)

        # circle.add_updater(vector_field.get_nudge_updater(pointwise=True))
        # dot.add_updater(vector_field.get_nudge_updater())
        # dots_m.add_updater(vector_field.get_nudge_updater())

        # self.add(circle, dot)
        dots_m.suspend_updating()
        self.add(dots_m)
        self.wait()
        dots_m.resume_updating()
        self.wait(4)

class SphereWithLines(ThreeDScene):
    CONFIG = {
        'frame_height': 7,
    }

    def construct(self):
        # Set up the 2-sphere
        self.next_section(skip_animations=True)
        axes = ThreeDAxes(
            # tips=False,
            axis_config={
                'unit_size': 1,
            },
            z_range = [-10, 10, 1],
            z_axis_config={
                'unit_size': 3,
                # 'length': config.frame_height + 2,
            },
         )
        # labels = axes.get_axis_labels(
        #     Tex("x-axis"), Text("y-axis"), Text("z-axis")
        # )
        # self.add(labels)

        sphere = Sphere(radius=1, resolution=(20, 20),
                        stroke_color=YELLOW_B, stroke_width=2).set_z_index(1)
        # sphere.set_opacity(1)
        sphere.set_fill(opacity=0.25)
        # sphere.set_color_by_gradient(BLUE, GREEN, PINK)
        self.set_camera_orientation(phi=0, theta=0, zoom=1.5)
        # TODO: replace with 3DAxes - need to find out how to have complex plane and R on z-axis
        self.play(DrawBorderThenFill(axes)) 
        self.add(ComplexPlane(
            background_line_style={
                "stroke_color": GREY_A,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            }
        ))
        self.play(Create(sphere))

        self.next_section(skip_animations=True)

        # Set up the north pole
        north_pole = Sphere(radius=0.1).set_fill(YELLOW)
        north_pole.move_to(sphere.get_zenith())

        # Set up the south pole
        south_pole = Sphere(radius=0.1).set_fill(RED)
        south_pole.move_to(sphere.get_nadir())

        self.play(Create(north_pole), Create(south_pole))
        north_label = Text("North")
        north_label.next_to(north_pole, 2*OUT)
        self.add_fixed_orientation_mobjects(north_label)
        self.play(Write(north_label))


        self.move_camera(phi=55*DEGREES, theta=PI/4)

        self.next_section()

        top = sphere.get_top()
        north = sphere.get_zenith()
        line_ref = (top - north) * 10

        line = Line3D(start=north, end=north + line_ref, color=BLUE)
        self.play(Create(line))

        line.add_updater(
            # lambda m: m.put_start_and_end_on(sphere.get_zenith(), [0, 2, 0])
            
            lambda m: m.become(Line3D(start=sphere.get_zenith(), end=sphere.get_zenith() + line_ref, color=BLUE))
        )
        self.move_camera(theta=2*PI/4)

        self.move_camera(theta=PI/4)
        self.play(sphere.animate.shift(OUT))
        
        # self.play(Write(north_label))
        # Generate lines from north pole to south pole
        num_lines = 10
        # for i in range(num_lines):
        #     line = Line(start=north_pole.get_center(), end=south_pole.get_center())
        #     line.rotate(i*2*PI/num_lines, about_point=north_pole.get_center())
        #     self.play(Create(line))

class SomePlot(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-10,10], 
            y_range=[-6,6], 
            x_length=10, 
            y_length=5,
            # axis_config={
            #     "numbers_to_include": np.arange(-10, 10, 2),
            # },
            tips=False
        ).add_coordinates(np.arange(-10, 10, 2), np.arange(-6, 6, 2))
        func = lambda x: np.sin(x)   
        graph = axes.plot(func, color=RED)

        self.play(Create(axes))
        # self.play(Create(graph))
        self.play(Create(graph, run_time=2.5))
        self.wait(2)

class TwoSphere(ThreeDScene):
    def construct(self):
        template_sphere = Sphere(radius=1)
        template_sphere.set_stroke(width=0)
        template_sphere.set_color_by_gradient(BLUE_B, GREEN_B)
        template_sphere.set_opacity(0.8)
        
        self.set_camera_orientation(phi=PI/4, theta=PI/4)
        self.play(DrawBorderThenFill(ComplexPlane()))
        self.play(Create(template_sphere), run_time=2)
        self.move_camera(phi=60 * DEGREES, theta=55 *
                         DEGREES, run_time=3, zoom=1.25)
        self.play(Uncreate(template_sphere))
        self.wait()


class LorenzAttractor(VMobject):

    # CONFIG = {    
    #     "stroke_opacity": 1.0,
    #     "stroke_color": "FF8C00",
    #     "stroke_width":2,
    #     "sheen":   0, #0.04
    #     "sheen_direction": UR,
    # }


    def __init__(self, iterations=5000, x=0.01, y=0.0, z=0.0,**kwargs):
        self.iterations = iterations
        self.x , self.y , self.z = x,y,z

        VMobject.__init__(self, **kwargs)


    def generate_points(self):

        a = 10.0
        b = 28.0
        c = 8.0/3.0

        x,y,z = self.x, self.y, self.z

        self.pts = []

        for _ in range(self.iterations):
            dt = 0.01
            dx = (a * (y - x))*dt
            dy = (x * (b - z) - y)*dt
            dz = (x * y - c * z)*dt;

            x = x + dx;
            y = y + dy;
            z = z + dz;

            self.pts.append(np.array([x,y,z]))


        self.set_points_smoothly(self.pts)
        self.scale(0.1)
        self.move_to(ORIGIN)


class Lorenz(ThreeDScene):

    CONFIG = {
        "should_apply_shading": False,
    }


    def construct(self):

        #rainbow = ["#9400D3","#4B0082","#0000FF","#00FF00","#FFFF00","#FF7F00","#FF0000"]
        #loren = LorenzAttractor().set_color_by_gradient(rainbow)

        loren = LorenzAttractor()
        self.add(loren)
        # anim =  ShowCreation(loren, run_time=10)
        self.set_camera_orientation(phi=-TAU/4, theta=None, distance=20.0, gamma=0)
        # self.begin_ambient_camera_rotation(rate=0.05)
        # self.play(anim)
        # self.wait(1)

class Lorenz_Attractor(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            # x_min=-3.5,
            # x_max=3.5,
            # y_min=-3.5,
            # y_max=3.5,
            # z_min=0,
            # z_max=6,
            axis_config={
                "include_tip": True,
                "include_ticks": True,
                "stroke_width": 1})
        dot = Sphere(radius=0.05,fill_color=BLUE).move_to(0*RIGHT + 0.1*UP + 0.105*OUT)
        
        self.set_camera_orientation(phi=65 * DEGREES,theta=30*DEGREES,gamma = 90*DEGREES)  
        self.begin_ambient_camera_rotation(rate=0.05)            #Start move camera

        dtime = 0.1
        numsteps = 30

        self.add(axes,dot)

        def lorenz(x, y, z, s=10, r=28, b=2.667):
            x_dot = s*(y - x)
            y_dot = r*x - y - x*z
            z_dot = x*y - b*z
            return x_dot, y_dot, z_dot

        def update_trajectory(self, dt):
            new_point = dot.get_center()
            if np.linalg.norm(new_point - self.points[-1]) > 0.01:
                self.add_smooth_curve_to(new_point)

        traj = VMobject()
        traj.start_new_path(dot.get_center())
        traj.set_stroke(BLUE, 1.5, opacity=0.8)
        traj.add_updater(update_trajectory)
        self.add(traj)

        def update_position(self,dt):
            x_dot, y_dot, z_dot = lorenz(dot.get_center()[0]*10, dot.get_center()[1]*10, dot.get_center()[2]*10)
            x = x_dot * dt/10
            y = y_dot * dt/10
            z = z_dot * dt/10
            self.shift(x/10*RIGHT + y/10*UP + z/10*OUT)

        dot.add_updater(update_position)
        self.wait(4)
class ContinuousMotion(Scene):
    def construct(self):
        def func (pos):
            x, y, z = pos
            return RIGHT*(x + y) + UP*(4*x + y)
            return RIGHT * (-3*x + 1) + UP*(-x + y)
        
        # def func (pos):
        #     x, y, z = pos
        #     return 10 * (y - x) * LEFT + x * (28 - z) - y * UP + x*y - 8/3 * z * OUT

        stream_lines = StreamLines(func, 
                                   stroke_width=2, 
                                   max_anchors_per_line=30,
                                   max_color_scheme_value=30)
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=False, flow_speed=1.5)
        dots = 0
        dots_m = VGroup()
        for i in range(dots):
            # get evenly spaced points on the circle certened at the origin
            # with radius 1
            dot_ref = Dot().move_to([1, 0, 0])
            d = dot_ref.copy().rotate(i * 2*PI/dots, about_point=ORIGIN)
            # vector_field.nudge(d, -0.3, 30)
            d.add_updater(stream_lines.get_nudge_updater(speed=0.75))
            t = TracedPath(d.get_center, 
                           stroke_color=color_gradient([RED_E, RED_A], 3),)
                        #    dissipating_time=1,
                        #    stroke_opacity=[0, 1])
            dots_m.add(d, t)
        # vector_field.nudge(circle, -2, 60, True)

        d1 = Dot(color=YELLOW).move_to([1, -2, 0])
        d2 = Dot(color=YELLOW).move_to(np.asarray([1, 2, 0]) / 5)
        l1 = Line([-10, 20, 0], [10, -20, 0])
        l2 = Line([-10, -20, 0], [10, 20, 0])

        d1.add_updater(stream_lines.get_nudge_updater(speed=0.75))
        d2.add_updater(stream_lines.get_nudge_updater(speed=0.75))
        # dots_m.add_updater(stream_lines.get_nudge_updater())
        self.add(dots_m, d1, d2, l1, l2)
        # self.wait(stream_lines.virtual_time / stream_lines.flow_speed)
        self.wait(5)


class SqtoCirc(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(square.animate.FadeOut().Transform())

class displayText(Scene):
    def construct(self):
        l1 = Text('Create animations')
        l2 = Text('using manim')
        l3 = Text('you can try it too', color=RED)
        t1 = Tex(r'you can use $LaTeX$')
        
        l2.next_to(l1, DOWN)

        self.wait(1)
        self.play(Write(l1), Write(l2))
        self.wait(1)
        self.play(ReplacementTransform(l1, l3), FadeOut(l2))
        self.wait(2)
        self.play(Write(t1))
        
class CreateGraph(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-5, 5],
            axis_config={"color": BLUE},
        )

        # Create Graph
        graph = axes.plot(lambda x: x**2, color=WHITE)
        graph_label = axes.get_graph_label(graph, label='x^{2}')

        graph2 = axes.plot(lambda x: x**3, color=WHITE)
        graph_label2 = axes.get_graph_label(graph2, label='x^{3}')

        # Display graph
        self.play(Create(axes), Create(graph), Write(graph_label))
        self.wait(1)
        self.play(Transform(graph, graph2), Transform(graph_label, graph_label2))
        self.wait(1)
