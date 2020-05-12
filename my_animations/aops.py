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
        axis1 = ThreeDAxes()
        self.play(ShowCreation(axis1))
        self.move_camera(phi=70 * DEGREES,theta=20*DEGREES,run_time=3)
        def Line1(t):
            return np.array((-1,0,1))+t*np.array((1,1,1))
        func = ParametricFunction(Line1, t_min=-10, max=10, fill_opacity=0,stroke_color=BLUE)
        A = Sphere(radius=0.1)
        V = Sphere(radius=0.1)
        A.move_to(np.array((-1,0,1)))
        V.move_to(np.array((0,3,2)))
        A_vector = ThreeDArrow(start=ORIGIN,end=A,stroke_color=RED,color=RED)
        V_vector = ThreeDArrow(start=ORIGIN,end=V,stroke_color=GREEN_E,color=GREEN_E)
        AV_vector = ThreeDArrow(start=V,end=A,stroke_color=YELLOW_E,stroke_width=2)
        self.play(ShowCreation(A_vector),run_time=3)
        self.play(ShowCreation(V_vector),run_time=3)
        self.play(ShowCreation(AV_vector),run_time=3)
        self.play(ShowCreation(func))

