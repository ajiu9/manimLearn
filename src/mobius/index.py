import math
import random
import cmath
from manim import *


class UnitSphere(Sphere):
    def __init__(self, radius=1, **kwargs):
        super().__init__(radius=radius, 
                        #  stroke_color=YELLOW_B,
                         stroke_width=2,
                         fill_opacity=0.5,
                         **kwargs)
        self.axes = ThreeDAxes()
        self.set_fill_by_value(
            axes=self.axes, 
            colorscale=color_gradient([RED_E, RED, GREY, BLUE, BLUE_E], 5)
        )
        self.equator = self._construct_equator()
        # self.add(self.equator)
    
    def _construct_equator(self):
        equator = Circle(radius=self.radius, 
                         stroke_width=7,
                         num_components=40)
        equator.set_color_by_gradient(
            color_gradient([BLUE, GREEN], 10))\
            .set_z_index(self.z_index + 2)
        equator.move_to(self.get_center())
        return equator
        
class PointProjector(VGroup):
    def __init__ (self, sphere: Sphere, **kwargs):
        super().__init__()
        self.sphere = sphere
        self.plane = ComplexPlane(
            background_line_style={
                "stroke_color": GREY_A,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            **kwargs,
        )
        self.sphere.move_to(self.plane.coords_to_point(0, 0))
        self.base = self.sphere + self.plane
        # self.s_ext = self.sphere + self.sphere.north + self.sphere.equator
        self.s_ext = self.sphere + self.sphere.equator

        self.add(
            self.base,
            self.s_ext)

    def put_in_frame (self):
        # Every timem I run this it *insists* on creating the projected point
        # and the line from the north pole. Despite the fact that I have unadded
        # those mobjects from the sphere and the PointProjector and anything else
        # I can think of. Even the LABELS appear - and they're not even rendered
        # ANYWHERE ELSE. 
        # Time wasted trying to get this to work: 5 hours
        # Just Uncreate() me, manim
        smaller_plane = ComplexPlane(
            background_line_style={
                "stroke_color": GREY_A,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },

        )
        self.add(self.sphere)
        self.generate_target(use_deepcopy=True)
        self.target.shift(4 * LEFT + 2 * UP)
        # self.target.base += SurroundingRectangle(self.plane, color=WHITE)
        # new_base += self.s_ext
        # self.base += self.frame
        return MoveToTarget(self)
    
    def begin_projection (
            self,
            point: tuple[float, float],
            draw_lines=True):
        """
        Creates the projection line, the projected point, and its destination.
        Also initializes updaters so that they are updated every frame.

        Parameters
        ----------
        point : tuple[float, float]
            The point to be projected onto the sphere. Given in (u, v) coordinates.
            u should range [0, 2pi] and is the phi angle on the sphere.
            v should range [0, pi] and is the (negative) theta angle on the sphere.
        draw_lines : bool, optional
            Whether or not to draw lines from the horizontal axes to the projected point.
        """
        
        self.P = Dot3D(color=RED).set_z_index(self.z_index + 1)
        self.L = self.line_from_north(self.sphere.func(point[0], point[1]))
        self.P_proj = Dot3D(color=YELLOW).set_z_index(self.z_index + 2)


        self.create_point_labels()
        self._new_stereographic_projection(point, draw_lines=draw_lines)

        self.s_ext.add(self.P, self.L)
        self.add(self.P_proj, self.proj_lines)
        return self.P, self.L, self.P_proj
    
    def end_projection (self):
        return FadeOut(self.P, shift=OUT),\
            FadeOut(self.L, shift=OUT),\
            FadeOut(self.P_proj, shift=OUT),\
            FadeOut(self.proj_lines, shift=OUT)

    def create_point_labels (self) -> tuple[Matrix, Matrix]:
        P_label = Matrix([np.round(self.P.get_center(), 2)]).scale(0.3)
        P_proj_label = Matrix([np.round(self.P_proj.get_center(), 2)]).scale(0.3)
        P_label.add_updater(lambda m: m.next_to(self.P, UP))
        P_proj_label.add_updater(lambda m: m.next_to(self.P_proj, UP))
        self.labels = (P_label, P_proj_label)
        self.add(*self.labels)
        return self.labels

    def get_point_labels (self) -> tuple[Matrix, Matrix]:
        self.labels[0].become(Matrix([np.round(self.P.get_center(), 2)]).scale(0.3))
        self.labels[1].become(Matrix([np.round(self.P_proj.get_center(), 2)]).scale(0.3))
        return self.labels

    def new_projected_point (self, point: tuple[float, float], draw_lines=True):
        # self._update_stereographic_projection(point)
        # self.P.move_to(self.sphere.func(point[0], point[1]))
        coords = self.sphere.func(point[0], point[1])
        new_L = self.line_from_north(coords)
        # proj_lines = self.plane.get_lines_to_point(
        #     stereographic_projection(self.sphere.north.get_center(), coords))

        # new_P_proj = self.P_proj.copy().move_to(
        #     stereographic_projection(self.sphere.north.get_center(), new_P.get_center()))
        
        return self.P.animate.move_to(coords), Transform(self.L, new_L)

    def _new_stereographic_projection (self, point: tuple[float, float], draw_lines=True):
        s = self.sphere
        def move_with_P (P_proj):
            P_proj.move_to(stereographic_projection(
                s.north.get_center(), 
                self.P.get_center()))

        self.P.move_to(s.func(point[0], point[1]))
        self.P_proj = self.P_proj.add_updater(move_with_P)
    
        if draw_lines:
            def lines_to_proj ():
                return self.plane.get_lines_to_point(self.P_proj.get_center(), 
                                                     color=YELLOW_A,
                                                     stroke_width=2,
                                                     line_func=Line)
            self.proj_lines = always_redraw(lines_to_proj)
    
    def line_from_north (self, point: np.ndarray, length=8):
        north = self.sphere.north.get_center()
        line_dir = (point - north)
        line = Line3D(start=north, end=north + line_dir * length, color=BLUE)
        return line
    
    def strip_to_equator (self):
        stripped = self.sphere.copy().set_stroke(opacity=0).set_fill(BLUE_B)
        return Transform(self.sphere, stripped)

    def rotate_sphere (self, angle, axis=OUT, **kwargs):
        return self.s_ext.animate.rotate(angle, axis=axis, about_point=self.sphere.get_center(), **kwargs)

class EquatorProjector(PointProjector):
    def __init__ (self, sphere: Sphere, **kwargs):
        super().__init__(sphere, **kwargs)


        # TODO just make this update to the projection of the
        # sphere that is passed in


        self.equator = sphere.equator
    
    def begin_projection (self):
        def eq_proj ():
            return self.equator.copy().set_stroke(color=YELLOW).apply_function(
                # lambda p: stereographic_projection(self.sphere.north.get_center(), p))
                lambda p: stereographic_projection(self.sphere.get_zenith(), p))
            # return ApplyPointwiseFunction(
            #     lambda p: stereographic_projection(self.sphere.north, p),
            #     self.equator.copy())
            
        # self.eq_proj = eq_proj()
        self.eq_proj = always_redraw(eq_proj)
        self.add(self.eq_proj)
        return TransformFromCopy(self.eq_proj, self.equator)


class StereographicProjection(ThreeDScene):
    CONFIG = {
        "x_min": -4,
        "x_max": 4,
        "y_min": -4,
        "y_max": 4,
        "axis_config": {
            "stroke_color": GREY_A,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        },
        "x_range": [-4, 4, 1],
        "y_range": [-4, 4, 1],
    }

    def setup (self):
        self.sphere = UnitSphere().set_z_index(1)
        sans_eq = self.sphere.remove(self.sphere.equator)
        self.point_p = PointProjector(sans_eq,
                                      x_range=[-6, 6, 1],
                                      y_range=[-4, 4, 1],)
        # self.point_p\
        #     .rotate_about_origin(PI/4, axis=OUT)\
        #     .rotate_about_origin(PI/3, axis=LEFT)

        # self.point_p.add(Dot3D([1, 1, 0], color=PURPLE)\
        #     .rotate_about_origin(PI/4, axis=OUT)\
        #     .rotate_about_origin(PI/3, axis=LEFT))
            # .scale(1.5)\
        # self.equator_p.scale(0.7).to_corner(UR, buff=0.1)
        self.renderer.camera.light_source.move_to(2*OUT) # changes the source of the light
        # self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=2)

    def construct (self):
        # self.setup()
        # self.sphere_ext = VGroup(self.sphere, self.sphere.equator, self.sphere.north)
        # self.play(Create(self.point_p.plane), Create(self.point_p.sphere))

        # self.next_section("Point projection demo", skip_animations=True)
        # pp = self.point_p
        # self.add(pp)
        # self.start_point_stereographic_projection((-PI/4, PI/2))
        # self.demo_point_projection()

        # self.expose_topview()
        # self.next_section("Consider equator", skip_animations=False)
        # self.show_equator_p()
        ep = EquatorProjector(self.point_p.sphere)
        source = Dot3D(ep.sphere.get_zenith())
        self.add(ep, source)
        ep.s_ext.rotate_about_origin(PI/2, axis=LEFT)
        self.play(ep.begin_projection())
        self.play(Rotate(ep.s_ext, -PI/2, axis=LEFT))
        # self.play(Rotate(ep.s_ext, PI/2, axis=LEFT))
        # self.play(ep.rotate_sphere(PI/2, axis=LEFT),)
                #   Transform(ep.equator, ep.equator.copy().apply_function(
                #         lambda p: stereographic_projection(ep.sphere.north.get_center(), p)
                #   )))
        # self.add(ep.equator.apply_function(
        #     lambda p: stereographic_projection(ep.sphere.north.get_center(), p)))
        # self.wait()
        # self.play(self.point_p.rotate_sphere(PI/2, axis=LEFT))
        # self.play(self.point_p.rotate_sphere(PI/2, axis=LEFT))

        # self.next_section("Apply mappings", skip_animations=False)
        # self.move_camera(phi=65 * DEGREES, theta=-45 * DEGREES)

        # self.bring_point_projector()

        # self.wait()
        # self.move_mob_around(self.point_p.s_ext)
        # self.play(Create(self.point_p.sphere.equator))
        # self.play(DrawBorderThenFill(self.equator_p))

        # self.play(Uncreate(VGroup(self.sphere, self.plane), 0.5))
        # self.show_equator_projection()
        # self.wait()

    def expose_topview (self):
        # self.play(LaggedStart(
        #     Restore(self.point_p.s_ext),
        #     *self.point_p.new_projected_point((0, 0)),
        #     FadeOut(self.point_p.L, shift=IN),
        #     run_time=1.5
        # ))
        pp = self.point_p
        self.play(Restore(pp.s_ext), run_time=0.75)
        self.play(LaggedStart(*pp.end_projection()))
        # pp.add(pp.sphere.equator)
        self.move_camera(0, theta=-PI/2)
        self.play(pp.strip_to_equator(), Create(pp.sphere.equator))
        self.wait()
        pass

    def show_equator_p (self):
        new_pp = PointProjector(UnitSphere(radius=1),
                                      x_range=[-6, 6, 1],
                                      y_range=[-4, 4, 1],)
        new_pp.scale(1.5)
        pp = self.point_p

        self.equator_p = EquatorProjector(new_pp.sphere.equator)\
            .add_background_rectangle(color=BLACK, opacity=0.9)
        ep = self.equator_p

        frame = SurroundingRectangle(ep, buff=0.1, color=WHITE)
        ep.base += frame
        ep.scale(0.55).to_corner(UR, buff=0.25)

        # self.play(pp.put_in_frame()) # DO NOT USE. SEE FUNC DECL.
        # self.add_fixed_orientation_mobjects(pp)
        # self.play(Transform(self.point_p.sphere, pp.sphere))
        # self.play(Transform(self.point_p.base, pp.base))
        self.move_camera(zoom=1)
        self.play(Transform(pp.base, new_pp.base),
                    # IT WORKS OMG IT WORKS IT SIMULTANEOUSLY TRANSFORMS
                    # `pp` WHICH IS THE OLD ONE PROJECTOR INTO `new_pp` and `ep`
                    # SPLITTING UP THE BASE AND EQUATOR
                  ReplacementTransform(pp.sphere.equator, ep.equator), 
                  FadeIn(ep))
        self.add_fixed_in_frame_mobjects(ep)
        pp = new_pp
        
        #           pp.plane.set_)
        # self.add_fixed_orientation_mobjects(ep)

        # self.play(Create(pp.sphere.equator, run_time=2))

        # pp.base += frame
        # self.play(FadeIn(frame))
        # pp.base.generate_target(use_deepcopy=True)
        # pp.base.target.scale(0.4)
        # pp.base.target.to_corner(UL)
        # self.move_camera(zoom=1)
        # self.play(MoveToTarget(pp.base), ep.animate.shift(2*RIGHT))
        # self.wait()
        self.play(Indicate(ep.equator),
                  Indicate(pp.sphere.equator), 
                  run_time=1)
    
    def bring_point_projector (self):
        pp = self.point_p
        ep = self.equator_p
        pp.to_corner(UL, buff=0.1).scale(0.75)
        frame = SurroundingRectangle(pp.plane, buff=0.1)
        pp.base += frame
        
        self.play(FadeIn(pp.base, shift=LEFT))
                  
    def go_around_equator (self, mob):
        self.play(MoveAlongPath(self.point_p.P, self.point_p.equator), run_time=4, rate_func=linear)
    
    def demo_point_projection(self):
        points = [
            (30*DEGREES, 130 * DEGREES),
            (2*PI/3, 30 * DEGREES),
            (2.3*PI/2, 50 * DEGREES),
            (135 * DEGREES, 70 * DEGREES),
            (30*DEGREES, 130 * DEGREES),
        ]
        self.start_point_stereographic_projection(points[0])
        camera_angles = [-PI/4, PI/4, PI/3, PI/6, 3*PI/4]
        self.move_camera(theta=PI/4)

        for p in points[1:]:
            self.play(*self.point_p.new_projected_point(p), run_time=1)
            # self.move_camera(theta=random.choice(camera_angles))
            self.wait(0.5)


        self.point_p.s_ext.save_state()
        self.move_sphere_around(self.point_p.s_ext)

    def move_sphere_around (self, s):
        self.play(s.animate.shift(LEFT))
        self.play(
            self.point_p.rotate_sphere(15 * DEGREES, axis=OUT),
            rate_func=there_and_back_with_pause)
        self.play(s.animate.shift(OUT))

    def start_point_stereographic_projection(
            self, 
            point: tuple[float, float],
            draw_lines=True):
            # dot_config: dict = {}):
        P, L, P_proj = self.point_p.begin_projection(point, draw_lines=draw_lines)
        self.play(Create(P), run_time=0.5)
        self.play(Create(L), run_time=0.5)
        self.play(Create(P_proj), run_time=0.5)
        
        if draw_lines:
            self.play(Create(self.point_p.proj_lines), run_time=0.5)
        # self.play(Write(p_label), Write(proj_label), run_time=0.5)

    def move_mob_around (self, mob: Mobject):
        mob.save_state()
        self.play(Succession(
            mob.animate.shift(RIGHT * 1/2),
            Rotate(mob, -PI/2, axis=UP)))
        self.play(mob.animate.shift(UP * 1/2))
 
def complex_stereographic_projection (source: np.ndarray, point: np.ndarray) -> np.ndarray:
    Nx, Ny, Nz = source
    csource = complex(Nx, Ny)
    x, y, z = point
    cpoint = complex(x, y) - csource
    r, phi = cmath.polar(cpoint)
    r_p = Nz * r / (Nz - z)
    return cmath.rect(r_p, phi)
    
    
def stereographic_projection (source: np.ndarray, point: np.ndarray) -> np.ndarray:
    """
    Given a source point on the sphere and the point that is to be projected,
    returns the stereographic projection of the point onto the plane.

    Parameters
    ----------
    source : np.ndarray
        The source point on the sphere. Usually the north pole.
    point : np.ndarray
        The point to be projected onto the plane.
    
    Returns
    -------
    np.ndarray
        3D-coordinates of the projected point. z is always 0.
    """
    Nx, Ny, Nz = source
    shift = np.asarray([Nx, Ny, 0])
    x, y, z = point - shift
    if math.isclose(Nz, abs(z)):
        return np.asarray([0, 0, 0]) + shift
    #     if x == Nx:
    #         return np.asarray([0, 0, 0])
    #     elif x > Nx:
    #         return np.asarray([10, 0, 0])
    #     else:
    #         return np.asarray([-10, 0, 0])

    r = np.sqrt(x**2 + y**2)
    r_p = Nz * r / (Nz - z)
    theta_p = np.arctan2(y, x)
    proj_coords = polar_to_cartesian(r_p, theta_p) + shift
    if any(abs(proj_coords) > 100):
        return np.asarray([0, 0, 0]) + shift
    return proj_coords

def cartesian_to_polar(coords: np.ndarray):
    x, y = coords
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return np.asarray([r, theta])

def polar_to_cartesian(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return np.asarray([x, y, 0])

def cartesian_to_spherical(coords: np.ndarray):
    x, y, z = coords
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / r)
    phi = np.arctan2(y, x)
    return np.asarray([r, theta, phi])

def spherical_to_cartesian(coords: np.ndarray):
    r, theta, phi = coords
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return np.asarray([x, y, z])

def convert_to_uv(coords: np.ndarray):
    r, theta, phi = cartesian_to_spherical(coords)
    u = phi / (2 * np.pi)
    v = theta / np.pi
    return (theta, phi)
