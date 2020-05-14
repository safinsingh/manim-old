from manimlib.imports import *

class Part1(Scene):
    def construct(self):
        svg = SVGMobject("logo", fill_opacity=0)
        introText = TextMobject("Safin Singh")
        introText2 = TextMobject("By ","Safin Singh")
        title = TextMobject("Projections in 3D")
        introText.next_to(svg,DOWN)
        self.wait()
        self.play(Write(svg),Write(introText), run_time=4)
        self.wait()
        introText2.next_to(title,DOWN)
        self.play(ReplacementTransform(svg, title),ReplacementTransform(introText,introText2))
        self.wait(3)
        self.play(FadeOut(title))
        self.play(FadeOut(introText2))

        # end on wait
        self.wait()

class Part2(ThreeDScene):
    def construct(self):
        p1 = TextMobject("1. Let $V = (0,3,2)$ and $A = (-1,0,1).$ Let $P$ be the point on the line \\\\passing through $A$ with direction vector $(1,1,1)$ that is closest to $V$.")
        p1.scale(0.75)
        self.play(Write(p1),run_time=3)
        self.play(p1.move_to,UP*3)
        self.add_fixed_in_frame_mobjects(p1)
        axis1 = ThreeDAxes(x_min=-10,x_max=10,y_min=-10,y_max=10,z_min=-10,z_max=10)
        axis1.scale(0.8)
        axis1.move_to(np.array((0,0,-1)))
        axis1.x_axis
        axis1.y_axis
        axis1.z_axis
        x_label=TextMobject("x").move_to(axis1.x_axis.get_end()+np.array((0.5,0,0)))
        y_label=TextMobject("y").move_to(axis1.y_axis.get_end()+np.array((0,0.5,0)))
        z_label=TextMobject("z").move_to(axis1.z_axis.get_end()+np.array((0,0,0.5)))
        self.play(ShowCreation(axis1),Write(x_label),Write(y_label),Write(z_label))
        self.add_fixed_orientation_mobjects(x_label,y_label,z_label)
        self.move_camera(phi=70 * DEGREES,theta=20*DEGREES,run_time=3)
        def Line1(t):
            return np.array((-1,0,1))+t*np.array((1,1,1))
        func = ParametricFunction(Line1, t_min=-20, max=20, fill_opacity=0,stroke_color=BLUE)
        A_vector = ThreeDArrow(start=ORIGIN,end=np.array((-1,0,1)),stroke_color=RED,color=RED)
        V_vector = ThreeDArrow(start=ORIGIN,end=np.array((1,0,1)),stroke_color=GREEN,color=GREEN)
        self.play(ShowCreation(A_vector),run_time=3)
        self.play(ShowCreation(V_vector),run_time=3)
        self.play(ShowCreation(func))

