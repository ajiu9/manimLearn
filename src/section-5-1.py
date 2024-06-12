from manim import *

class AllUpdaterTypes(Scene):
    def construct(self):
        red_dot = Dot(color=RED).shift(LEFT)
        pointer = Arrow(ORIGIN, RIGHT).next_to(red_dot, LEFT)
        pointer.add_updater(lambda m: m.next_to(red_dot, LEFT))

        def shifter(m, dt): # make dot move 2 munits RIGHT/sec
            m.shift(2* RIGHT * dt)
        red_dot.add_updater(shifter)
       
        def scene_scaler(dt): # scale mobjects depending on instance to ORIGIN
            for mob in self.mobjects:
                mob.set(width=2/(1+np.linalg.norm(mob.get_center())))
        self.add_updater(scene_scaler)

        self.add(red_dot, pointer)
        self.update_self(0)
        self.wait(5)

class UpdateAndAnimation(Scene):
    def construct(self):
        red_dot = Dot(color=RED).shift(LEFT)
        rotating_square = Square()
        rotating_square.add_updater(lambda m, dt: m.rotate(PI*dt))

        def shifter(m, dt): 
            m.shift(2* RIGHT * dt)
        red_dot.add_updater(shifter)

        self.add(red_dot, rotating_square)
        self.wait(1)
        red_dot.suspend_updating()
        self.wait(1)

        self.play(
            red_dot.animate.shift(UP),
            rotating_square.animate.move_to([-2,-2,0])
        )

        self.wait(1)


class ValueTracker(Scene):
    def construct(self):
        line = NumberLine(x_range=[-5,5])
        position = ValueTracker(0)
        pointer = Vector(DOWN)
        
        pointer.add_updater(
            lambda m: m.move_to(line.number_to_point(position.get_value()), UP)
        )
        pointer.update()
        self.add(line, pointer)

        self.wait()
        self.play(position.animate.set_value(4))
        self.play(position.animate.set_value(-2))

        








