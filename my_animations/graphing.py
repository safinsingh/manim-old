from manimlib.imports import *

class P3(ThreeDScene):
    def construct(self):
        plane = ThreeDAxes()
        self.play(Write(plane))
        self.move_camera(phi=80 * DEGREES,theta=45*DEGREES,run_time=3)
        self.wait()