from manimlib.imports import *

########## BEGIN UTILS BLOCK ##########

import typing
import itertools
import collections
import math

def set_colors(object: typing.Union[Mobject, Group, typing.Sequence], colors: typing.List[str]) -> object:
    [object[i].set_color(color) for i, color in enumerate(colors)]
    return object
def ReplacementMultiIndex(
    m1: Mobject, i1: typing.Iterable[typing.Union[int, typing.Sequence[int], range]],
    m2: Mobject, i2: typing.Iterable[typing.Union[int, typing.Sequence[int], range]],
    *, copy_first: bool = False, copy_second: bool = False, transformation: type = ReplacementTransform,
    fade_in: type = FadeIn, fade_out: type = FadeOut
):
    """
    Does a multi-index replacement.
    :param m1: The first object; is replaced.
    :param i1: The respective indexes.
    :param m2: The second object; is the replacer.
    :param i2: The respective replacer indexes.
    :param copy_first: If all replaced objects (in m1) should be copied. Defaults to False.
    :param copy_second: If all replacer objects (in m2) should be copied. Defaults to False.
    :param transformation: The transformation class to use (defaults to ReplacementTransform).
    :param fade_in: The transformation to use when ``None`` is specified on i1. Defaults to ``FadeIn``.
    :param fade_out: The transformation to use when ``None`` is specified on i2. Defaults to ``FadeOut``.
    :return:
    """
    i1 = list(i1)
    m_i2_enum = filter(lambda pair: isinstance(pair[1], collections.Iterable) and i1[0] is not None, enumerate(i2))
    multiple_i2 = list(map(lambda t: t[1], m_i2_enum))
    indexes_mult = map(lambda t: t[0], enumerate(multiple_i2))
    
    multiple_i1 = [i1[i] for i in indexes_mult]
    
    single_i1 = i1 if not multiple_i1 else filter(lambda el: el not in multiple_i1, i1)
    single_i2 = i2 if not multiple_i1 else filter(lambda el: el not in multiple_i2, i2)
    
    def copy_if_copy_first(obj):
        if copy_first and obj is not None:
            return obj.copy()
        return obj

    def copy_if_copy_second(obj):
        if copy_second and obj is not None:
            return obj.copy()
        return obj

    def converter(m, ii):
        if ii is None:
            return None

        if type(ii) == range or isinstance(ii, range):
            return m[ii.start:ii.stop:ii.step]

        if type(ii) in (list, tuple) or isinstance(ii, list) or isinstance(ii, tuple):
            return VGroup(*map(lambda i: m[i], ii))

        return m[ii]
    
    def resolve_transform(a1, a2):
        if a2 is None:
            return fade_out(a1)
        elif a1 is None:
            return fade_in(a2)
        else:
            return transformation(a1, a2)

    replacements = [
        resolve_transform(
            copy_if_copy_first(
                converter(m1, ii1)
            ),

            copy_if_copy_second(
                converter(m2, ii2)
            )
        ) for ii1, ii2 in zip(single_i1, single_i2)
    ] + sum([
        [
            resolve_transform(
                copy_if_copy_first(converter(m1, ii1)),
                copy_if_copy_second(converter(m2, ii2))
            ) for ii2 in itertools.islice(is2, 0, 1)  # just the first time this element appears; doesn't get copied
        ] + [
            resolve_transform(
                converter(m1, ii1).copy(),
                copy_if_copy_second(converter(m2, ii2))
            ) for ii2 in itertools.islice(is2, 1, None)  # others of this same element are necessarily copied
        ] for ii1, is2 in zip(multiple_i1, multiple_i2)
    ], [])
    return replacements

########## END UTILS BLOCK ##########

class Part1(Scene):
    def construct(self):
        svg = SVGMobject("logo", fill_opacity=0)
        introText = TextMobject("Safin Singh")
        introText2 = TextMobject("By ","Safin Singh")
        title = TextMobject("T","h","e"," ","P","h","y","s","i","c","s"," ","o","f"," ","W","a","v","e","s")
        introText.next_to(svg,DOWN)
        self.wait()
        self.play(Write(svg),Write(introText), run_time=4)
        self.wait()
        introText2.next_to(title,DOWN)
        self.play(ReplacementTransform(svg, title),*ReplacementMultiIndex(introText,[None,0],introText2,[0,1]))
        self.play(FadeOut(title))
        self.play(FadeOut(introText2))

        # end on wait
        self.wait()

class Part2(GraphScene):
    CONFIG = {
        "y_max": 8,
        "y_axis_height": 5,
        "x_min":-0.5,
        "y_min":-0.5,
        "x_axis_label": "$sec$"
    }
    def get_sine_wave(self,dx=0):
        return FunctionGraph(
            lambda x: np.sin((x+dx)),
            x_min=-4,x_max=4
        )
    
    def get_sine_wave2(self,dx=0):
        return FunctionGraph(
            lambda x: np.sin((x+dx)),
            x_min=-8,x_max=8
        )
    

    def construct(self):
        svg2 = SVGMobject("wave", fill_opacity=0, stroke_width=1)
        text = TextMobject("What are"," waves?")
        text.scale(2)
        text.next_to(svg2,UP*3)
        self.play(Write(svg2),FadeIn(text), run_time=4)
        self.wait()
        self.play(FadeOut(svg2),text.scale,0.5,text.move_to,UL*3+LEFT*2)
        self.wait()
        self.setup_axes(animate=True)
        sine_function=self.get_sine_wave()
        self.play(Write(sine_function))
        d_theta=ValueTracker(0)
        def update_wave(func):
            func.become(self.get_sine_wave(dx=d_theta.get_value()))
            return func
        sine_function.add_updater(update_wave)
        self.add(sine_function)
        self.play(d_theta.increment_value,5*PI,rate_func=linear, run_time=6)
        sine_function.remove_updater(update_wave)
        axes2 = self.axes.copy()
        gVG = VGroup(axes2,sine_function)
        text2 = TextMobject("What are the")
        text2_2 = TextMobject("types of waves?")
        text2.move_to(text)
        text2_2.next_to(text2,DOWN)
        text2VG = VGroup(text2,text2_2)
        self.play(gVG.scale,0.3,gVG.move_to,DL*2.5+LEFT*2,FadeOut(self.axes),ReplacementTransform(text,text2VG))
        
        self.x_max=2.5
        self.y_max=2.5
        self.x_tick_frequency=0.5
        self.y_tick_frequency=0.5
        self.x_axis_label="$sec$"
        self.y_axis_label="$y$"
        newMobj = TexMobject("y")

        self.setup()
        self.setup_axes()
        self.remove(self.axes)
        self.play(self.axes.move_to,UR*0.6+RIGHT*1.2,self.axes.scale,0.9,run_time=0)
        self.play(Write(self.axes),self.axes.scale,1.1)
        self.play(newMobj.move_to,self.y_axis_label_mob, run_time=0)
        
        a = [0.125,0.25,0.375,0.5,0.625,0.75,0.875,1,1.125,1.25,1.375,1.5,1.625,1.75,1.875,2,2.125]
        time = ValueTracker(0)

        # BEGIN DOT DEFINITIONS

        dot0_0 = Dot(self.coords_to_point(a[0],0))
        dot1_0 = Dot(self.coords_to_point(a[1],0))
        dot2_0 = Dot(self.coords_to_point(a[2],0))
        dot3_0 = Dot(self.coords_to_point(a[3],0))
        dot4_0 = Dot(self.coords_to_point(a[4],0))
        dot5_0 = Dot(self.coords_to_point(a[5],0))
        dot6_0 = Dot(self.coords_to_point(a[6],0))
        dot7_0 = Dot(self.coords_to_point(a[7],0))
        dot8_0 = Dot(self.coords_to_point(a[8],0))
        dot9_0 = Dot(self.coords_to_point(a[9],0))
        dot10_0 = Dot(self.coords_to_point(a[10],0))
        dot11_0 = Dot(self.coords_to_point(a[11],0))
        dot12_0 = Dot(self.coords_to_point(a[12],0))
        dot13_0 = Dot(self.coords_to_point(a[13],0))
        dot14_0 = Dot(self.coords_to_point(a[14],0))
        dot15_0 = Dot(self.coords_to_point(a[15],0))
        dot16_0 = Dot(self.coords_to_point(a[16],0))

        dot0_1 = Dot(self.coords_to_point(a[0],0.5))
        dot1_1 = Dot(self.coords_to_point(a[1],0.5))
        dot2_1 = Dot(self.coords_to_point(a[2],0.5))
        dot3_1 = Dot(self.coords_to_point(a[3],0.5))
        dot4_1 = Dot(self.coords_to_point(a[4],0.5))
        dot5_1 = Dot(self.coords_to_point(a[5],0.5))
        dot6_1 = Dot(self.coords_to_point(a[6],0.5))
        dot7_1 = Dot(self.coords_to_point(a[7],0.5))
        dot8_1 = Dot(self.coords_to_point(a[8],0.5))
        dot9_1 = Dot(self.coords_to_point(a[9],0.5))
        dot10_1 = Dot(self.coords_to_point(a[10],0.5))
        dot11_1 = Dot(self.coords_to_point(a[11],0.5))
        dot12_1 = Dot(self.coords_to_point(a[12],0.5))
        dot13_1 = Dot(self.coords_to_point(a[13],0.5))
        dot14_1 = Dot(self.coords_to_point(a[14],0.5))
        dot15_1 = Dot(self.coords_to_point(a[15],0.5))
        dot16_1 = Dot(self.coords_to_point(a[16],0.5))

        dot0_2 = Dot(self.coords_to_point(a[0],1))
        dot1_2 = Dot(self.coords_to_point(a[1],1))
        dot2_2 = Dot(self.coords_to_point(a[2],1))
        dot3_2 = Dot(self.coords_to_point(a[3],1))
        dot4_2 = Dot(self.coords_to_point(a[4],1))
        dot5_2 = Dot(self.coords_to_point(a[5],1))
        dot6_2 = Dot(self.coords_to_point(a[6],1))
        dot7_2 = Dot(self.coords_to_point(a[7],1))
        dot8_2 = Dot(self.coords_to_point(a[8],1))
        dot9_2 = Dot(self.coords_to_point(a[9],1))
        dot10_2 = Dot(self.coords_to_point(a[10],1))
        dot11_2 = Dot(self.coords_to_point(a[11],1))
        dot12_2 = Dot(self.coords_to_point(a[12],1))
        dot13_2 = Dot(self.coords_to_point(a[13],1))
        dot14_2 = Dot(self.coords_to_point(a[14],1))
        dot15_2 = Dot(self.coords_to_point(a[15],1))
        dot16_2 = Dot(self.coords_to_point(a[16],1))

        dot0_3 = Dot(self.coords_to_point(a[0],1.5))
        dot1_3 = Dot(self.coords_to_point(a[1],1.5))
        dot2_3 = Dot(self.coords_to_point(a[2],1.5))
        dot3_3 = Dot(self.coords_to_point(a[3],1.5))
        dot4_3 = Dot(self.coords_to_point(a[4],1.5))
        dot5_3 = Dot(self.coords_to_point(a[5],1.5))
        dot6_3 = Dot(self.coords_to_point(a[6],1.5))
        dot7_3 = Dot(self.coords_to_point(a[7],1.5))
        dot8_3 = Dot(self.coords_to_point(a[8],1.5))
        dot9_3 = Dot(self.coords_to_point(a[9],1.5))
        dot10_3 = Dot(self.coords_to_point(a[10],1.5))
        dot11_3 = Dot(self.coords_to_point(a[11],1.5))
        dot12_3 = Dot(self.coords_to_point(a[12],1.5))
        dot13_3 = Dot(self.coords_to_point(a[13],1.5))
        dot14_3 = Dot(self.coords_to_point(a[14],1.5))
        dot15_3 = Dot(self.coords_to_point(a[15],1.5))
        dot16_3 = Dot(self.coords_to_point(a[16],1.5))

        dot0_4 = Dot(self.coords_to_point(a[0],2))
        dot1_4 = Dot(self.coords_to_point(a[1],2))
        dot2_4 = Dot(self.coords_to_point(a[2],2))
        dot3_4 = Dot(self.coords_to_point(a[3],2))
        dot4_4 = Dot(self.coords_to_point(a[4],2))
        dot5_4 = Dot(self.coords_to_point(a[5],2))
        dot6_4 = Dot(self.coords_to_point(a[6],2))
        dot7_4 = Dot(self.coords_to_point(a[7],2))
        dot8_4 = Dot(self.coords_to_point(a[8],2))
        dot9_4 = Dot(self.coords_to_point(a[9],2))
        dot10_4 = Dot(self.coords_to_point(a[10],2))
        dot11_4 = Dot(self.coords_to_point(a[11],2))
        dot12_4 = Dot(self.coords_to_point(a[12],2))
        dot13_4 = Dot(self.coords_to_point(a[13],2))
        dot14_4 = Dot(self.coords_to_point(a[14],2))
        dot15_4 = Dot(self.coords_to_point(a[15],2))
        dot16_4 = Dot(self.coords_to_point(a[16],2))

        dot0_5 = Dot(self.coords_to_point(a[0],2.5))
        dot1_5 = Dot(self.coords_to_point(a[1],2.5))
        dot2_5 = Dot(self.coords_to_point(a[2],2.5))
        dot3_5 = Dot(self.coords_to_point(a[3],2.5))
        dot4_5 = Dot(self.coords_to_point(a[4],2.5))
        dot5_5 = Dot(self.coords_to_point(a[5],2.5))
        dot6_5 = Dot(self.coords_to_point(a[6],2.5))
        dot7_5 = Dot(self.coords_to_point(a[7],2.5))
        dot8_5 = Dot(self.coords_to_point(a[8],2.5))
        dot9_5 = Dot(self.coords_to_point(a[9],2.5))
        dot10_5 = Dot(self.coords_to_point(a[10],2.5))
        dot11_5 = Dot(self.coords_to_point(a[11],2.5))
        dot12_5 = Dot(self.coords_to_point(a[12],2.5))
        dot13_5 = Dot(self.coords_to_point(a[13],2.5))
        dot14_5 = Dot(self.coords_to_point(a[14],2.5))
        dot15_5 = Dot(self.coords_to_point(a[15],2.5))
        dot16_5 = Dot(self.coords_to_point(a[16],2.5))

        # END DOT DEFINITIONS

        self.play(
            Write(dot0_0),
            Write(dot1_0),
            Write(dot2_0),
            Write(dot3_0),
            Write(dot4_0),
            Write(dot5_0),
            Write(dot6_0),
            Write(dot7_0),
            Write(dot8_0),
            Write(dot9_0),
            Write(dot10_0),
            Write(dot11_0),
            Write(dot12_0),
            Write(dot13_0),
            Write(dot14_0),
            Write(dot15_0),
            Write(dot16_0),
            Write(dot0_1),
            Write(dot1_1),
            Write(dot2_1),
            Write(dot3_1),
            Write(dot4_1),
            Write(dot5_1),
            Write(dot6_1),
            Write(dot7_1),
            Write(dot8_1),
            Write(dot9_1),
            Write(dot10_1),
            Write(dot11_1),
            Write(dot12_1),
            Write(dot13_1),
            Write(dot14_1),
            Write(dot15_1),
            Write(dot16_1),
            Write(dot0_2),
            Write(dot1_2),
            Write(dot2_2),
            Write(dot3_2),
            Write(dot4_2),
            Write(dot5_2),
            Write(dot6_2),
            Write(dot7_2),
            Write(dot8_2),
            Write(dot9_2),
            Write(dot10_2),
            Write(dot11_2),
            Write(dot12_2),
            Write(dot13_2),
            Write(dot14_2),
            Write(dot15_2),
            Write(dot16_2),
            Write(dot0_3),
            Write(dot1_3),
            Write(dot2_3),
            Write(dot3_3),
            Write(dot4_3),
            Write(dot5_3),
            Write(dot6_3),
            Write(dot7_3),
            Write(dot8_3),
            Write(dot9_3),
            Write(dot10_3),
            Write(dot11_3),
            Write(dot12_3),
            Write(dot13_3),
            Write(dot14_3),
            Write(dot15_3),
            Write(dot16_3),
            Write(dot0_4),
            Write(dot1_4),
            Write(dot2_4),
            Write(dot3_4),
            Write(dot4_4),
            Write(dot5_4),
            Write(dot6_4),
            Write(dot7_4),
            Write(dot8_4),
            Write(dot9_4),
            Write(dot10_4),
            Write(dot11_4),
            Write(dot12_4),
            Write(dot13_4),
            Write(dot14_4),
            Write(dot15_4),
            Write(dot16_4),
            Write(dot0_5),
            Write(dot1_5),
            Write(dot2_5),
            Write(dot3_5),
            Write(dot4_5),
            Write(dot5_5),
            Write(dot6_5),
            Write(dot7_5),
            Write(dot8_5),
            Write(dot9_5),
            Write(dot10_5),
            Write(dot11_5),
            Write(dot12_5),
            Write(dot13_5),
            Write(dot14_5),
            Write(dot15_5),
            Write(dot16_5)
        )

        def dot_updater_00(mobj):
            magic = a[0]+0.1*(np.sin(2*PI*(a[0]-time.get_value())))
            dot0_0.move_to(self.coords_to_point(magic,0))
            return dot0_0
        
        def dot_updater_10(mobj):
            magic = a[1]+0.1*(np.sin(2*PI*(a[1]-time.get_value())))
            dot1_0.move_to(self.coords_to_point(magic,0))
            return dot1_0
        
        def dot_updater_20(mobj):
            magic = a[2]+0.1*(np.sin(2*PI*(a[2]-time.get_value())))
            dot2_0.move_to(self.coords_to_point(magic,0))
            return dot2_0
        
        def dot_updater_30(mobj):
            magic = a[3]+0.1*(np.sin(2*PI*(a[3]-time.get_value())))
            dot3_0.move_to(self.coords_to_point(magic,0))
            return dot3_0
        
        def dot_updater_40(mobj):
            magic = a[4]+0.1*(np.sin(2*PI*(a[4]-time.get_value())))
            dot4_0.move_to(self.coords_to_point(magic,0))
            return dot4_0
        
        def dot_updater_50(mobj):
            magic = a[5]+0.1*(np.sin(2*PI*(a[5]-time.get_value())))
            dot5_0.move_to(self.coords_to_point(magic,0))
            return dot5_0
        
        def dot_updater_60(mobj):
            magic = a[6]+0.1*(np.sin(2*PI*(a[6]-time.get_value())))
            dot6_0.move_to(self.coords_to_point(magic,0))
            return dot6_0
        
        def dot_updater_70(mobj):
            magic = a[7]+0.1*(np.sin(2*PI*(a[7]-time.get_value())))
            dot7_0.move_to(self.coords_to_point(magic,0))
            return dot7_0
        
        def dot_updater_80(mobj):
            magic = a[8]+0.1*(np.sin(2*PI*(a[8]-time.get_value())))
            dot8_0.move_to(self.coords_to_point(magic,0))
            return dot8_0
        
        def dot_updater_90(mobj):
            magic = a[9]+0.1*(np.sin(2*PI*(a[9]-time.get_value())))
            dot9_0.move_to(self.coords_to_point(magic,0))
            return dot9_0
        
        def dot_updater_100(mobj):
            magic = a[10]+0.1*(np.sin(2*PI*(a[10]-time.get_value())))
            dot10_0.move_to(self.coords_to_point(magic,0))
            return dot10_0
        
        def dot_updater_110(mobj):
            magic = a[11]+0.1*(np.sin(2*PI*(a[11]-time.get_value())))
            dot11_0.move_to(self.coords_to_point(magic,0))
            return dot11_0
        
        def dot_updater_120(mobj):
            magic = a[12]+0.1*(np.sin(2*PI*(a[12]-time.get_value())))
            dot12_0.move_to(self.coords_to_point(magic,0))
            return dot12_0
        
        def dot_updater_130(mobj):
            magic = a[13]+0.1*(np.sin(2*PI*(a[13]-time.get_value())))
            dot13_0.move_to(self.coords_to_point(magic,0))
            return dot13_0
        
        def dot_updater_140(mobj):
            magic = a[14]+0.1*(np.sin(2*PI*(a[14]-time.get_value())))
            dot14_0.move_to(self.coords_to_point(magic,0))
            return dot14_0
        
        def dot_updater_150(mobj):
            magic = a[15]+0.1*(np.sin(2*PI*(a[15]-time.get_value())))
            dot15_0.move_to(self.coords_to_point(magic,0))
            return dot15_0
        
        def dot_updater_160(mobj):
            magic = a[16]+0.1*(np.sin(2*PI*(a[16]-time.get_value())))
            dot16_0.move_to(self.coords_to_point(magic,0))
            return dot16_0
        


        def dot_updater_01(mobj):
            magic = a[0]+0.1*(np.sin(2*PI*(a[0]-time.get_value())))
            dot0_1.move_to(self.coords_to_point(magic,0.5))
            return dot0_1
        
        def dot_updater_11(mobj):
            magic = a[1]+0.1*(np.sin(2*PI*(a[1]-time.get_value())))
            dot1_1.move_to(self.coords_to_point(magic,0.5))
            return dot1_1
        
        def dot_updater_21(mobj):
            magic = a[2]+0.1*(np.sin(2*PI*(a[2]-time.get_value())))
            dot2_1.move_to(self.coords_to_point(magic,0.5))
            return dot2_1
        
        def dot_updater_31(mobj):
            magic = a[3]+0.1*(np.sin(2*PI*(a[3]-time.get_value())))
            dot3_1.move_to(self.coords_to_point(magic,0.5))
            return dot3_1
        
        def dot_updater_41(mobj):
            magic = a[4]+0.1*(np.sin(2*PI*(a[4]-time.get_value())))
            dot4_1.move_to(self.coords_to_point(magic,0.5))
            return dot4_1
        
        def dot_updater_51(mobj):
            magic = a[5]+0.1*(np.sin(2*PI*(a[5]-time.get_value())))
            dot5_1.move_to(self.coords_to_point(magic,0.5))
            return dot5_1
        
        def dot_updater_61(mobj):
            magic = a[6]+0.1*(np.sin(2*PI*(a[6]-time.get_value())))
            dot6_1.move_to(self.coords_to_point(magic,0.5))
            return dot6_1
        
        def dot_updater_71(mobj):
            magic = a[7]+0.1*(np.sin(2*PI*(a[7]-time.get_value())))
            dot7_1.move_to(self.coords_to_point(magic,0.5))
            return dot7_1
        
        def dot_updater_81(mobj):
            magic = a[8]+0.1*(np.sin(2*PI*(a[8]-time.get_value())))
            dot8_1.move_to(self.coords_to_point(magic,0.5))
            return dot8_1
        
        def dot_updater_91(mobj):
            magic = a[9]+0.1*(np.sin(2*PI*(a[9]-time.get_value())))
            dot9_1.move_to(self.coords_to_point(magic,0.5))
            return dot9_1
        
        def dot_updater_101(mobj):
            magic = a[10]+0.1*(np.sin(2*PI*(a[10]-time.get_value())))
            dot10_1.move_to(self.coords_to_point(magic,0.5))
            return dot10_1
        
        def dot_updater_111(mobj):
            magic = a[11]+0.1*(np.sin(2*PI*(a[11]-time.get_value())))
            dot11_1.move_to(self.coords_to_point(magic,0.5))
            return dot11_1
        
        def dot_updater_121(mobj):
            magic = a[12]+0.1*(np.sin(2*PI*(a[12]-time.get_value())))
            dot12_1.move_to(self.coords_to_point(magic,0.5))
            return dot12_1
        
        def dot_updater_131(mobj):
            magic = a[13]+0.1*(np.sin(2*PI*(a[13]-time.get_value())))
            dot13_1.move_to(self.coords_to_point(magic,0.5))
            return dot13_1
        
        def dot_updater_141(mobj):
            magic = a[14]+0.1*(np.sin(2*PI*(a[14]-time.get_value())))
            dot14_1.move_to(self.coords_to_point(magic,0.5))
            return dot14_1
        
        def dot_updater_151(mobj):
            magic = a[15]+0.1*(np.sin(2*PI*(a[15]-time.get_value())))
            dot15_1.move_to(self.coords_to_point(magic,0.5))
            return dot15_1
        
        def dot_updater_161(mobj):
            magic = a[16]+0.1*(np.sin(2*PI*(a[16]-time.get_value())))
            dot16_1.move_to(self.coords_to_point(magic,0.5))
            return dot16_1



        def dot_updater_02(mobj):
            magic = a[0]+0.1*(np.sin(2*PI*(a[0]-time.get_value())))
            dot0_2.move_to(self.coords_to_point(magic,1))
            return dot0_2
        
        def dot_updater_12(mobj):
            magic = a[1]+0.1*(np.sin(2*PI*(a[1]-time.get_value())))
            dot1_2.move_to(self.coords_to_point(magic,1))
            return dot1_2
        
        def dot_updater_22(mobj):
            magic = a[2]+0.1*(np.sin(2*PI*(a[2]-time.get_value())))
            dot2_2.move_to(self.coords_to_point(magic,1))
            return dot2_2
        
        def dot_updater_32(mobj):
            magic = a[3]+0.1*(np.sin(2*PI*(a[3]-time.get_value())))
            dot3_2.move_to(self.coords_to_point(magic,1))
            return dot3_2
        
        def dot_updater_42(mobj):
            magic = a[4]+0.1*(np.sin(2*PI*(a[4]-time.get_value())))
            dot4_2.move_to(self.coords_to_point(magic,1))
            return dot4_2
        
        def dot_updater_52(mobj):
            magic = a[5]+0.1*(np.sin(2*PI*(a[5]-time.get_value())))
            dot5_2.move_to(self.coords_to_point(magic,1))
            return dot5_2
        
        def dot_updater_62(mobj):
            magic = a[6]+0.1*(np.sin(2*PI*(a[6]-time.get_value())))
            dot6_2.move_to(self.coords_to_point(magic,1))
            return dot6_2
        
        def dot_updater_72(mobj):
            magic = a[7]+0.1*(np.sin(2*PI*(a[7]-time.get_value())))
            dot7_2.move_to(self.coords_to_point(magic,1))
            return dot7_2
        
        def dot_updater_82(mobj):
            magic = a[8]+0.1*(np.sin(2*PI*(a[8]-time.get_value())))
            dot8_2.move_to(self.coords_to_point(magic,1))
            return dot8_2
        
        def dot_updater_92(mobj):
            magic = a[9]+0.1*(np.sin(2*PI*(a[9]-time.get_value())))
            dot9_2.move_to(self.coords_to_point(magic,1))
            return dot9_2
        
        def dot_updater_102(mobj):
            magic = a[10]+0.1*(np.sin(2*PI*(a[10]-time.get_value())))
            dot10_2.move_to(self.coords_to_point(magic,1))
            return dot10_2
        
        def dot_updater_112(mobj):
            magic = a[11]+0.1*(np.sin(2*PI*(a[11]-time.get_value())))
            dot11_2.move_to(self.coords_to_point(magic,1))
            return dot11_2
        
        def dot_updater_122(mobj):
            magic = a[12]+0.1*(np.sin(2*PI*(a[12]-time.get_value())))
            dot12_2.move_to(self.coords_to_point(magic,1))
            return dot12_2
        
        def dot_updater_132(mobj):
            magic = a[13]+0.1*(np.sin(2*PI*(a[13]-time.get_value())))
            dot13_2.move_to(self.coords_to_point(magic,1))
            return dot13_2
        
        def dot_updater_142(mobj):
            magic = a[14]+0.1*(np.sin(2*PI*(a[14]-time.get_value())))
            dot14_2.move_to(self.coords_to_point(magic,1))
            return dot14_2
        
        def dot_updater_152(mobj):
            magic = a[15]+0.1*(np.sin(2*PI*(a[15]-time.get_value())))
            dot15_2.move_to(self.coords_to_point(magic,1))
            return dot15_2
        
        def dot_updater_162(mobj):
            magic = a[16]+0.1*(np.sin(2*PI*(a[16]-time.get_value())))
            dot16_2.move_to(self.coords_to_point(magic,1))
            return dot16_2

        

        def dot_updater_03(mobj):
            magic = a[0]+0.1*(np.sin(2*PI*(a[0]-time.get_value())))
            dot0_3.move_to(self.coords_to_point(magic,1.5))
            return dot0_3
        
        def dot_updater_13(mobj):
            magic = a[1]+0.1*(np.sin(2*PI*(a[1]-time.get_value())))
            dot1_3.move_to(self.coords_to_point(magic,1.5))
            return dot1_3
        
        def dot_updater_23(mobj):
            magic = a[2]+0.1*(np.sin(2*PI*(a[2]-time.get_value())))
            dot2_3.move_to(self.coords_to_point(magic,1.5))
            return dot2_3
        
        def dot_updater_33(mobj):
            magic = a[3]+0.1*(np.sin(2*PI*(a[3]-time.get_value())))
            dot3_3.move_to(self.coords_to_point(magic,1.5))
            return dot3_3
        
        def dot_updater_43(mobj):
            magic = a[4]+0.1*(np.sin(2*PI*(a[4]-time.get_value())))
            dot4_3.move_to(self.coords_to_point(magic,1.5))
            return dot4_3
        
        def dot_updater_53(mobj):
            magic = a[5]+0.1*(np.sin(2*PI*(a[5]-time.get_value())))
            dot5_3.move_to(self.coords_to_point(magic,1.5))
            return dot5_3
        
        def dot_updater_63(mobj):
            magic = a[6]+0.1*(np.sin(2*PI*(a[6]-time.get_value())))
            dot6_3.move_to(self.coords_to_point(magic,1.5))
            return dot6_3
        
        def dot_updater_73(mobj):
            magic = a[7]+0.1*(np.sin(2*PI*(a[7]-time.get_value())))
            dot7_3.move_to(self.coords_to_point(magic,1.5))
            return dot7_3
        
        def dot_updater_83(mobj):
            magic = a[8]+0.1*(np.sin(2*PI*(a[8]-time.get_value())))
            dot8_3.move_to(self.coords_to_point(magic,1.5))
            return dot8_3
        
        def dot_updater_93(mobj):
            magic = a[9]+0.1*(np.sin(2*PI*(a[9]-time.get_value())))
            dot9_3.move_to(self.coords_to_point(magic,1.5))
            return dot9_3
        
        def dot_updater_103(mobj):
            magic = a[10]+0.1*(np.sin(2*PI*(a[10]-time.get_value())))
            dot10_3.move_to(self.coords_to_point(magic,1.5))
            return dot10_3
        
        def dot_updater_113(mobj):
            magic = a[11]+0.1*(np.sin(2*PI*(a[11]-time.get_value())))
            dot11_3.move_to(self.coords_to_point(magic,1.5))
            return dot11_3
        
        def dot_updater_123(mobj):
            magic = a[12]+0.1*(np.sin(2*PI*(a[12]-time.get_value())))
            dot12_3.move_to(self.coords_to_point(magic,1.5))
            return dot12_3
        
        def dot_updater_133(mobj):
            magic = a[13]+0.1*(np.sin(2*PI*(a[13]-time.get_value())))
            dot13_3.move_to(self.coords_to_point(magic,1.5))
            return dot13_3
        
        def dot_updater_143(mobj):
            magic = a[14]+0.1*(np.sin(2*PI*(a[14]-time.get_value())))
            dot14_3.move_to(self.coords_to_point(magic,1.5))
            return dot14_3
        
        def dot_updater_153(mobj):
            magic = a[15]+0.1*(np.sin(2*PI*(a[15]-time.get_value())))
            dot15_3.move_to(self.coords_to_point(magic,1.5))
            return dot15_3
        
        def dot_updater_163(mobj):
            magic = a[16]+0.1*(np.sin(2*PI*(a[16]-time.get_value())))
            dot16_3.move_to(self.coords_to_point(magic,1.5))
            return dot16_3

        

        def dot_updater_04(mobj):
            magic = a[0]+0.1*(np.sin(2*PI*(a[0]-time.get_value())))
            dot0_4.move_to(self.coords_to_point(magic,2))
            return dot0_4
        
        def dot_updater_14(mobj):
            magic = a[1]+0.1*(np.sin(2*PI*(a[1]-time.get_value())))
            dot1_4.move_to(self.coords_to_point(magic,2))
            return dot1_4
        
        def dot_updater_24(mobj):
            magic = a[2]+0.1*(np.sin(2*PI*(a[2]-time.get_value())))
            dot2_4.move_to(self.coords_to_point(magic,2))
            return dot2_4
        
        def dot_updater_34(mobj):
            magic = a[3]+0.1*(np.sin(2*PI*(a[3]-time.get_value())))
            dot3_4.move_to(self.coords_to_point(magic,2))
            return dot3_4
        
        def dot_updater_44(mobj):
            magic = a[4]+0.1*(np.sin(2*PI*(a[4]-time.get_value())))
            dot4_4.move_to(self.coords_to_point(magic,2))
            return dot4_4
        
        def dot_updater_54(mobj):
            magic = a[5]+0.1*(np.sin(2*PI*(a[5]-time.get_value())))
            dot5_4.move_to(self.coords_to_point(magic,2))
            return dot5_4
        
        def dot_updater_64(mobj):
            magic = a[6]+0.1*(np.sin(2*PI*(a[6]-time.get_value())))
            dot6_4.move_to(self.coords_to_point(magic,2))
            return dot6_4
        
        def dot_updater_74(mobj):
            magic = a[7]+0.1*(np.sin(2*PI*(a[7]-time.get_value())))
            dot7_4.move_to(self.coords_to_point(magic,2))
            return dot7_4
        
        def dot_updater_84(mobj):
            magic = a[8]+0.1*(np.sin(2*PI*(a[8]-time.get_value())))
            dot8_4.move_to(self.coords_to_point(magic,2))
            return dot8_4
        
        def dot_updater_94(mobj):
            magic = a[9]+0.1*(np.sin(2*PI*(a[9]-time.get_value())))
            dot9_4.move_to(self.coords_to_point(magic,2))
            return dot9_4
        
        def dot_updater_104(mobj):
            magic = a[10]+0.1*(np.sin(2*PI*(a[10]-time.get_value())))
            dot10_4.move_to(self.coords_to_point(magic,2))
            return dot10_4
        
        def dot_updater_114(mobj):
            magic = a[11]+0.1*(np.sin(2*PI*(a[11]-time.get_value())))
            dot11_4.move_to(self.coords_to_point(magic,2))
            return dot11_4
        
        def dot_updater_124(mobj):
            magic = a[12]+0.1*(np.sin(2*PI*(a[12]-time.get_value())))
            dot12_4.move_to(self.coords_to_point(magic,2))
            return dot12_4
        
        def dot_updater_134(mobj):
            magic = a[13]+0.1*(np.sin(2*PI*(a[13]-time.get_value())))
            dot13_4.move_to(self.coords_to_point(magic,2))
            return dot13_4
        
        def dot_updater_144(mobj):
            magic = a[14]+0.1*(np.sin(2*PI*(a[14]-time.get_value())))
            dot14_4.move_to(self.coords_to_point(magic,2))
            return dot14_4
        
        def dot_updater_154(mobj):
            magic = a[15]+0.1*(np.sin(2*PI*(a[15]-time.get_value())))
            dot15_4.move_to(self.coords_to_point(magic,2))
            return dot15_4
        
        def dot_updater_164(mobj):
            magic = a[16]+0.1*(np.sin(2*PI*(a[16]-time.get_value())))
            dot16_4.move_to(self.coords_to_point(magic,2))
            return dot16_4

        

        def dot_updater_05(mobj):
            magic = a[0]+0.1*(np.sin(2*PI*(a[0]-time.get_value())))
            dot0_5.move_to(self.coords_to_point(magic,2.5))
            return dot0_5
        
        def dot_updater_15(mobj):
            magic = a[1]+0.1*(np.sin(2*PI*(a[1]-time.get_value())))
            dot1_5.move_to(self.coords_to_point(magic,2.5))
            return dot1_5
        
        def dot_updater_25(mobj):
            magic = a[2]+0.1*(np.sin(2*PI*(a[2]-time.get_value())))
            dot2_5.move_to(self.coords_to_point(magic,2.5))
            return dot2_5
        
        def dot_updater_35(mobj):
            magic = a[3]+0.1*(np.sin(2*PI*(a[3]-time.get_value())))
            dot3_5.move_to(self.coords_to_point(magic,2.5))
            return dot3_5
        
        def dot_updater_45(mobj):
            magic = a[4]+0.1*(np.sin(2*PI*(a[4]-time.get_value())))
            dot4_5.move_to(self.coords_to_point(magic,2.5))
            return dot4_5
        
        def dot_updater_55(mobj):
            magic = a[5]+0.1*(np.sin(2*PI*(a[5]-time.get_value())))
            dot5_5.move_to(self.coords_to_point(magic,2.5))
            return dot5_5
        
        def dot_updater_65(mobj):
            magic = a[6]+0.1*(np.sin(2*PI*(a[6]-time.get_value())))
            dot6_5.move_to(self.coords_to_point(magic,2.5))
            return dot6_5
        
        def dot_updater_75(mobj):
            magic = a[7]+0.1*(np.sin(2*PI*(a[7]-time.get_value())))
            dot7_5.move_to(self.coords_to_point(magic,2.5))
            return dot7_5
        
        def dot_updater_85(mobj):
            magic = a[8]+0.1*(np.sin(2*PI*(a[8]-time.get_value())))
            dot8_5.move_to(self.coords_to_point(magic,2.5))
            return dot8_5
        
        def dot_updater_95(mobj):
            magic = a[9]+0.1*(np.sin(2*PI*(a[9]-time.get_value())))
            dot9_5.move_to(self.coords_to_point(magic,2.5))
            return dot9_5
        
        def dot_updater_105(mobj):
            magic = a[10]+0.1*(np.sin(2*PI*(a[10]-time.get_value())))
            dot10_5.move_to(self.coords_to_point(magic,2.5))
            return dot10_5
        
        def dot_updater_115(mobj):
            magic = a[11]+0.1*(np.sin(2*PI*(a[11]-time.get_value())))
            dot11_5.move_to(self.coords_to_point(magic,2.5))
            return dot11_5
        
        def dot_updater_125(mobj):
            magic = a[12]+0.1*(np.sin(2*PI*(a[12]-time.get_value())))
            dot12_5.move_to(self.coords_to_point(magic,2.5))
            return dot12_5
        
        def dot_updater_135(mobj):
            magic = a[13]+0.1*(np.sin(2*PI*(a[13]-time.get_value())))
            dot13_5.move_to(self.coords_to_point(magic,2.5))
            return dot13_5
        
        def dot_updater_145(mobj):
            magic = a[14]+0.1*(np.sin(2*PI*(a[14]-time.get_value())))
            dot14_5.move_to(self.coords_to_point(magic,2.5))
            return dot14_5
        
        def dot_updater_155(mobj):
            magic = a[15]+0.1*(np.sin(2*PI*(a[15]-time.get_value())))
            dot15_5.move_to(self.coords_to_point(magic,2.5))
            return dot15_5
        
        def dot_updater_165(mobj):
            magic = a[16]+0.1*(np.sin(2*PI*(a[16]-time.get_value())))
            dot16_5.move_to(self.coords_to_point(magic,2.5))
            return dot16_5

        

        dot0_0.add_updater(dot_updater_00)
        dot1_0.add_updater(dot_updater_10)
        dot2_0.add_updater(dot_updater_20)
        dot3_0.add_updater(dot_updater_30)
        dot4_0.add_updater(dot_updater_40)
        dot5_0.add_updater(dot_updater_50)
        dot6_0.add_updater(dot_updater_60)
        dot7_0.add_updater(dot_updater_70)
        dot8_0.add_updater(dot_updater_80)
        dot9_0.add_updater(dot_updater_90)
        dot10_0.add_updater(dot_updater_100)
        dot11_0.add_updater(dot_updater_110)
        dot12_0.add_updater(dot_updater_120)
        dot13_0.add_updater(dot_updater_130)
        dot14_0.add_updater(dot_updater_140)
        dot15_0.add_updater(dot_updater_150)
        dot16_0.add_updater(dot_updater_160)

        dot0_1.add_updater(dot_updater_01)
        dot1_1.add_updater(dot_updater_11)
        dot2_1.add_updater(dot_updater_21)
        dot3_1.add_updater(dot_updater_31)
        dot4_1.add_updater(dot_updater_41)
        dot5_1.add_updater(dot_updater_51)
        dot6_1.add_updater(dot_updater_61)
        dot7_1.add_updater(dot_updater_71)
        dot8_1.add_updater(dot_updater_81)
        dot9_1.add_updater(dot_updater_91)
        dot10_1.add_updater(dot_updater_101)
        dot11_1.add_updater(dot_updater_111)
        dot12_1.add_updater(dot_updater_121)
        dot13_1.add_updater(dot_updater_131)
        dot14_1.add_updater(dot_updater_141)
        dot15_1.add_updater(dot_updater_151)
        dot16_1.add_updater(dot_updater_161)

        dot0_2.add_updater(dot_updater_02)
        dot1_2.add_updater(dot_updater_12)
        dot2_2.add_updater(dot_updater_22)
        dot3_2.add_updater(dot_updater_32)
        dot4_2.add_updater(dot_updater_42)
        dot5_2.add_updater(dot_updater_52)
        dot6_2.add_updater(dot_updater_62)
        dot7_2.add_updater(dot_updater_72)
        dot8_2.add_updater(dot_updater_82)
        dot9_2.add_updater(dot_updater_92)
        dot10_2.add_updater(dot_updater_102)
        dot11_2.add_updater(dot_updater_112)
        dot12_2.add_updater(dot_updater_122)
        dot13_2.add_updater(dot_updater_132)
        dot14_2.add_updater(dot_updater_142)
        dot15_2.add_updater(dot_updater_152)
        dot16_2.add_updater(dot_updater_162)

        dot0_3.add_updater(dot_updater_03)
        dot1_3.add_updater(dot_updater_13)
        dot2_3.add_updater(dot_updater_23)
        dot3_3.add_updater(dot_updater_33)
        dot4_3.add_updater(dot_updater_43)
        dot5_3.add_updater(dot_updater_53)
        dot6_3.add_updater(dot_updater_63)
        dot7_3.add_updater(dot_updater_73)
        dot8_3.add_updater(dot_updater_83)
        dot9_3.add_updater(dot_updater_93)
        dot10_3.add_updater(dot_updater_103)
        dot11_3.add_updater(dot_updater_113)
        dot12_3.add_updater(dot_updater_123)
        dot13_3.add_updater(dot_updater_133)
        dot14_3.add_updater(dot_updater_143)
        dot15_3.add_updater(dot_updater_153)
        dot16_3.add_updater(dot_updater_163)

        dot0_4.add_updater(dot_updater_04)
        dot1_4.add_updater(dot_updater_14)
        dot2_4.add_updater(dot_updater_24)
        dot3_4.add_updater(dot_updater_34)
        dot4_4.add_updater(dot_updater_44)
        dot5_4.add_updater(dot_updater_54)
        dot6_4.add_updater(dot_updater_64)
        dot7_4.add_updater(dot_updater_74)
        dot8_4.add_updater(dot_updater_84)
        dot9_4.add_updater(dot_updater_94)
        dot10_4.add_updater(dot_updater_104)
        dot11_4.add_updater(dot_updater_114)
        dot12_4.add_updater(dot_updater_124)
        dot13_4.add_updater(dot_updater_134)
        dot14_4.add_updater(dot_updater_144)
        dot15_4.add_updater(dot_updater_154)
        dot16_4.add_updater(dot_updater_164)

        dot0_5.add_updater(dot_updater_05)
        dot1_5.add_updater(dot_updater_15)
        dot2_5.add_updater(dot_updater_25)
        dot3_5.add_updater(dot_updater_35)
        dot4_5.add_updater(dot_updater_45)
        dot5_5.add_updater(dot_updater_55)
        dot6_5.add_updater(dot_updater_65)
        dot7_5.add_updater(dot_updater_75)
        dot8_5.add_updater(dot_updater_85)
        dot9_5.add_updater(dot_updater_95)
        dot10_5.add_updater(dot_updater_105)
        dot11_5.add_updater(dot_updater_115)
        dot12_5.add_updater(dot_updater_125)
        dot13_5.add_updater(dot_updater_135)
        dot15_5.add_updater(dot_updater_145)
        dot15_5.add_updater(dot_updater_155)
        dot16_5.add_updater(dot_updater_165)
        

        self.add(dot0_0,dot1_0,dot2_0,dot3_0,dot4_0,dot5_0,dot6_0,dot7_0,dot8_0,dot9_0,dot10_0,dot11_0,dot12_0,dot13_0,dot14_0,dot15_0,dot16_0,dot0_1,dot1_1,dot2_1,dot3_1,dot4_1,dot5_1,dot6_1,dot7_1,dot8_1,dot9_1,dot10_1,dot11_1,dot12_1,dot13_1,dot14_1,dot15_1,dot16_1,dot0_2,dot1_2,dot2_2,dot3_2,dot4_2,dot5_2,dot6_2,dot7_2,dot8_2,dot9_2,dot10_2,dot11_2,dot12_2,dot13_2,dot14_2,dot15_2,dot16_2,dot0_3,dot1_3,dot2_3,dot3_3,dot4_3,dot5_3,dot6_3,dot7_3,dot8_3,dot9_3,dot10_3,dot11_3,dot12_3,dot13_3,dot14_3,dot15_3,dot16_3,dot0_4,dot1_4,dot2_4,dot3_4,dot4_4,dot5_4,dot6_4,dot7_4,dot8_4,dot9_4,dot10_4,dot11_4,dot12_4,dot13_4,dot14_4,dot15_4,dot16_4,dot0_5,dot1_5,dot2_5,dot3_5,dot4_5,dot5_5,dot6_5,dot7_5,dot8_5,dot9_5,dot10_5,dot11_5,dot12_5,dot13_5,dot14_5,dot15_5,dot16_5)

        self.play(time.increment_value,3,rate_func=linear,run_time=6)

        dot0_0.remove_updater(dot_updater_00)
        dot1_0.remove_updater(dot_updater_10)
        dot2_0.remove_updater(dot_updater_20)
        dot3_0.remove_updater(dot_updater_30)
        dot4_0.remove_updater(dot_updater_40)
        dot5_0.remove_updater(dot_updater_50)
        dot6_0.remove_updater(dot_updater_60)
        dot7_0.remove_updater(dot_updater_70)
        dot8_0.remove_updater(dot_updater_80)
        dot9_0.remove_updater(dot_updater_90)
        dot10_0.remove_updater(dot_updater_100)
        dot11_0.remove_updater(dot_updater_110)
        dot12_0.remove_updater(dot_updater_120)
        dot13_0.remove_updater(dot_updater_130)
        dot14_0.remove_updater(dot_updater_140)
        dot15_0.remove_updater(dot_updater_150)
        dot16_0.remove_updater(dot_updater_160)

        dot0_1.remove_updater(dot_updater_01)
        dot1_1.remove_updater(dot_updater_11)
        dot2_1.remove_updater(dot_updater_21)
        dot3_1.remove_updater(dot_updater_31)
        dot4_1.remove_updater(dot_updater_41)
        dot5_1.remove_updater(dot_updater_51)
        dot6_1.remove_updater(dot_updater_61)
        dot7_1.remove_updater(dot_updater_71)
        dot8_1.remove_updater(dot_updater_81)
        dot9_1.remove_updater(dot_updater_91)
        dot10_1.remove_updater(dot_updater_101)
        dot11_1.remove_updater(dot_updater_111)
        dot12_1.remove_updater(dot_updater_121)
        dot13_1.remove_updater(dot_updater_131)
        dot14_1.remove_updater(dot_updater_141)
        dot15_1.remove_updater(dot_updater_151)
        dot16_1.remove_updater(dot_updater_161)

        dot0_2.remove_updater(dot_updater_02)
        dot1_2.remove_updater(dot_updater_12)
        dot2_2.remove_updater(dot_updater_22)
        dot3_2.remove_updater(dot_updater_32)
        dot4_2.remove_updater(dot_updater_42)
        dot5_2.remove_updater(dot_updater_52)
        dot6_2.remove_updater(dot_updater_62)
        dot7_2.remove_updater(dot_updater_72)
        dot8_2.remove_updater(dot_updater_82)
        dot9_2.remove_updater(dot_updater_92)
        dot10_2.remove_updater(dot_updater_102)
        dot11_2.remove_updater(dot_updater_112)
        dot12_2.remove_updater(dot_updater_122)
        dot13_2.remove_updater(dot_updater_132)
        dot14_2.remove_updater(dot_updater_142)
        dot15_2.remove_updater(dot_updater_152)
        dot16_2.remove_updater(dot_updater_162)

        dot0_3.remove_updater(dot_updater_03)
        dot1_3.remove_updater(dot_updater_13)
        dot2_3.remove_updater(dot_updater_23)
        dot3_3.remove_updater(dot_updater_33)
        dot4_3.remove_updater(dot_updater_43)
        dot5_3.remove_updater(dot_updater_53)
        dot6_3.remove_updater(dot_updater_63)
        dot7_3.remove_updater(dot_updater_73)
        dot8_3.remove_updater(dot_updater_83)
        dot9_3.remove_updater(dot_updater_93)
        dot10_3.remove_updater(dot_updater_103)
        dot11_3.remove_updater(dot_updater_113)
        dot12_3.remove_updater(dot_updater_123)
        dot13_3.remove_updater(dot_updater_133)
        dot14_3.remove_updater(dot_updater_143)
        dot15_3.remove_updater(dot_updater_153)
        dot16_3.remove_updater(dot_updater_163)

        dot0_4.remove_updater(dot_updater_04)
        dot1_4.remove_updater(dot_updater_14)
        dot2_4.remove_updater(dot_updater_24)
        dot3_4.remove_updater(dot_updater_34)
        dot4_4.remove_updater(dot_updater_44)
        dot5_4.remove_updater(dot_updater_54)
        dot6_4.remove_updater(dot_updater_64)
        dot7_4.remove_updater(dot_updater_74)
        dot8_4.remove_updater(dot_updater_84)
        dot9_4.remove_updater(dot_updater_94)
        dot10_4.remove_updater(dot_updater_104)
        dot11_4.remove_updater(dot_updater_114)
        dot12_4.remove_updater(dot_updater_124)
        dot13_4.remove_updater(dot_updater_134)
        dot14_4.remove_updater(dot_updater_144)
        dot15_4.remove_updater(dot_updater_154)
        dot16_4.remove_updater(dot_updater_164)

        dot0_5.remove_updater(dot_updater_05)
        dot1_5.remove_updater(dot_updater_15)
        dot2_5.remove_updater(dot_updater_25)
        dot3_5.remove_updater(dot_updater_35)
        dot4_5.remove_updater(dot_updater_45)
        dot5_5.remove_updater(dot_updater_55)
        dot6_5.remove_updater(dot_updater_65)
        dot7_5.remove_updater(dot_updater_75)
        dot8_5.remove_updater(dot_updater_85)
        dot9_5.remove_updater(dot_updater_95)
        dot10_5.remove_updater(dot_updater_105)
        dot11_5.remove_updater(dot_updater_115)
        dot12_5.remove_updater(dot_updater_125)
        dot13_5.remove_updater(dot_updater_135)
        dot15_5.remove_updater(dot_updater_145)
        dot15_5.remove_updater(dot_updater_155)
        dot16_5.remove_updater(dot_updater_165)


        dotsVG = VGroup(dot0_0,dot1_0,dot2_0,dot3_0,dot4_0,dot5_0,dot6_0,dot7_0,dot8_0,dot9_0,dot10_0,dot11_0,dot12_0,dot13_0,dot14_0,dot15_0,dot16_0,dot0_1,dot1_1,dot2_1,dot3_1,dot4_1,dot5_1,dot6_1,dot7_1,dot8_1,dot9_1,dot10_1,dot11_1,dot12_1,dot13_1,dot14_1,dot15_1,dot16_1,dot0_2,dot1_2,dot2_2,dot3_2,dot4_2,dot5_2,dot6_2,dot7_2,dot8_2,dot9_2,dot10_2,dot11_2,dot12_2,dot13_2,dot14_2,dot15_2,dot16_2,dot0_3,dot1_3,dot2_3,dot3_3,dot4_3,dot5_3,dot6_3,dot7_3,dot8_3,dot9_3,dot10_3,dot11_3,dot12_3,dot13_3,dot14_3,dot15_3,dot16_3,dot0_4,dot1_4,dot2_4,dot3_4,dot4_4,dot5_4,dot6_4,dot7_4,dot8_4,dot9_4,dot10_4,dot11_4,dot12_4,dot13_4,dot14_4,dot15_4,dot16_4,dot0_5,dot1_5,dot2_5,dot3_5,dot4_5,dot5_5,dot6_5,dot7_5,dot8_5,dot9_5,dot10_5,dot11_5,dot12_5,dot13_5,dot14_5,dot15_5,dot16_5,self.axes,newMobj)

        self.play(FadeOut(dotsVG))

        self.play(sine_function.scale,4,sine_function.move_to,ORIGIN,FadeOut(axes2))
        midline = Line(start=LEFT*8,end=RIGHT*8)
        fullGraph = FunctionGraph(
            lambda x: np.sin(x),
            x_min=-8,x_max=8
        )
        fullGraphExt = FunctionGraph(
            lambda x: np.sin(x/1.2),
            x_min=-8,x_max=8
        )
        fullGraphExt2 = FunctionGraph(
            lambda x: 1.5*np.sin(x),
            x_min=-8,x_max=8
        )

        text3=TextMobject("What are some")
        text3_2 = TextMobject("properties of waves?")
        text3.move_to(UL*3+LEFT)
        text3_2.next_to(text3,DOWN)
        text3VG = VGroup(text3,text3_2)

        self.play(ShowCreation(midline),ReplacementTransform(sine_function,fullGraph),ReplacementTransform(text2VG,text3VG))

        wlDot0 = Dot(point=np.array((-9*np.pi/5,1,0)))
        wlDot1 = Dot(point=np.array((-3*np.pi/2,1,0)))
        wlDot2 = Dot(point=np.array((np.pi/2,1,0)))
        wlDot3 = Dot(point=np.array((3*np.pi/5,1,0)))
        ampDot1 = Dot(point=np.array((-3*np.pi/2,0,0)))
        ampDot2 = Dot(point=np.array((-3*np.pi/2,1.5,0)))
        line11 = Line(start=wlDot1,end=wlDot2)
        line111 = Line(start=wlDot0,end=wlDot3)
        line21 = Line(start=wlDot1,end=ampDot1)
        line211 = Line(start=ampDot2,end=ampDot1)
        wlBrace = Brace(line11,direction=UP)
        wlBrace2 = Brace(line111,direction=UP)
        ampBrace = Brace(line21,direction=RIGHT)
        ampBrace2 = Brace(line211,direction=RIGHT)
        wlB_lbl = TextMobject("Wavelength, $\\lambda$ ($4m$)")
        ampB_lbl = TextMobject("Amplitude, $A$ ($2m$)")
        per_lbl = TextMobject("Period, $T$:")
        freqB_lbl = TextMobject("Frequency, $f$ ($1 \\over s$, $Hz$)")
        wlB_lbl.next_to(wlBrace,UP)
        ampB_lbl.next_to(ampBrace,RIGHT)
        self.play(FadeOut(text3VG),run_time=0.5)
        self.play(Write(wlDot1),Write(wlDot2),ShowCreation(wlBrace),Write(wlB_lbl))
        def wLBLup(self):
            wlB_lbl.next_to(wlBrace,UP)
        wlB_lbl.add_updater(wLBLup)
        self.add(wlB_lbl)
        self.play(Transform(fullGraph,fullGraphExt),Transform(wlBrace,wlBrace2),Transform(wlDot2,wlDot3),Transform(wlDot1,wlDot0),rate_func=there_and_back,run_time=3)
        wlB_lbl.remove_updater(wLBLup)
        self.play(Transform(wlDot2,ampDot1),ReplacementTransform(wlBrace,ampBrace),ReplacementTransform(wlB_lbl,ampB_lbl))
        def ampLBLup(self):
            ampB_lbl.next_to(ampBrace,RIGHT)
        ampB_lbl.add_updater(ampLBLup)
        self.add(ampB_lbl)
        self.play(Transform(fullGraph,fullGraphExt2),Transform(ampBrace,ampBrace2),Transform(wlDot1,ampDot2),rate_func=there_and_back,run_time=3)
        ampB_lbl.remove_updater(ampB_lbl)
        self.play(FadeOut(ampBrace),FadeOut(ampB_lbl),FadeOut(wlDot2),FadeOut(wlDot1))
        self.wait()
        pDot1 = Dot(point=np.array((-3*np.pi/2,5,0)))
        pDot2 = Dot(point=np.array((-3*np.pi/2,-5,0)))
        pDot3 = Dot(point=np.array((np.pi/2,5,0)))
        pDot4 = Dot(point=np.array((np.pi/2,-5,0)))
        pDot5 = Dot(point=np.array((-3*np.pi/2,1,0)))
        pDot6 = Dot(point=np.array((np.pi/2,1,0)))
        pLine1 = Line(start=pDot1,end=pDot2,color=RED)
        pLine2 = Line(start=pDot3,end=pDot4,color=RED)
        pLine3 = Line(start=pDot5,end=pDot6)
        pBrace = Brace(pLine3,direction=UP)
        pLabel = DecimalNumber(number = 0, num_decimal_places = 2, unit = "sec")
        def pLabelUpdater(self):
            pLabel.move_to(pLine1.get_center()+RIGHT+UP*3)
            pLabel.set_value((pLine1.get_center()[0]+6)/((2/1.2)*np.pi)-0.25)
        pLabel.add_updater(pLabelUpdater)
        self.add(pLabel)
        self.play(ShowCreation(pLine1))
        self.play(Transform(pLine1,pLine2),run_time=5)
        pLabel.remove_updater(pLabelUpdater)
        self.play(CounterclockwiseTransform(pLine1,pBrace),pLabel.move_to,pBrace.get_center()+UP*0.5)
        per_lbl.move_to(pLabel.get_center()+UP*0.5)
        self.play(Write(per_lbl))
        freqEq = TexMobject("f = {1\\over","T}")
        freqEq2 = TexMobject("f = {1\\over","1.20sec}")
        pLabel2 = TexMobject("T=1.20sec")
        freqEq.move_to(pBrace)
        pLabel2.move_to(pBrace.get_center()+UP*0.4)
        myVG22 = VGroup(pLabel,per_lbl)
        self.play(ReplacementTransform(myVG22,pLabel2))
        self.play(Write(freqEq),freqEq.move_to,freqEq.get_center()+RIGHT*1+UP*0.75,pLabel2.move_to,freqEq.get_center()+LEFT*1.5+UP*0.7)
        freqEq2.move_to(pBrace.get_center()+UP*1)
        self.play(FadeOut(pLabel2))
        self.play(Transform(freqEq,freqEq2))
        freqEq3 = TexMobject("f \\approx 0.83 Hz")
        freqEq3.move_to(pBrace.get_center()+UP*0.7)
        self.play(Transform(freqEq,freqEq3))
        freqVG = VGroup(freqEq,pLine1)
        self.play(FadeOut(freqVG))
        self.remove(fullGraph)
        d_theta2=ValueTracker(0)
        sine_function2=self.get_sine_wave2()
        self.play(ShowCreation(sine_function2),run_time=0)
        def update_wave(func):
            func.become(
                self.get_sine_wave2(dx=d_theta2.get_value())
            )
            return func
        sine_function2.add_updater(update_wave)
        self.add(sine_function2)
        self.play(d_theta2.increment_value,6*PI,rate_func=linear,run_time=4)
        speedEq1 = TexMobject("v = \\lambda\\times f")
        speedEq2 = TexMobject("v = 4m\\times","0.83Hz")
        speedEq3 = TexMobject("v = 4m\\times","0.83\\frac{1}{s}")
        speedEq4 = TexMobject("v = 3.32\\frac{m}{s}")
        speedEq1.move_to(ORIGIN+UP*2)
        speedEq2.move_to(ORIGIN+UP*2)
        speedEq3.move_to(ORIGIN+UP*2)
        speedEq4.move_to(ORIGIN+UP*2)
        wavelEq1 = TexMobject("\\lambda = 4m",color=DARK_GRAY)
        wavelEq1.next_to(speedEq1,UP)
        freqEq4 = TexMobject("f = 0.83 Hz",color=DARK_GRAY)
        freqEq4.next_to(wavelEq1,UP)
        self.play(Write(speedEq1))
        self.play(Write(wavelEq1))
        self.play(Write(freqEq4))
        speedPoint = speedEq1.get_center()
        print(speedPoint)
        self.play(FadeOutAndShift(wavelEq1),FadeOutAndShift(freqEq4),Transform(speedEq1,speedEq2))
        self.play(Transform(speedEq1,speedEq3))
        self.play(Transform(speedEq1,speedEq4))
        #wEq1 = TexMobject("\\lambda = 4m")
        self.play(FadeOut(speedEq1))
        propEq1 = TexMobject("E \\propto A^2")
        propEq1.move_to(ORIGIN+UP*2)
        self.play(Write(propEq1))
        fullGraphExt3 = FunctionGraph(
            lambda x: 2*np.sin(x),
            x_min=-8,x_max=8
        )
        fullGraphExt4 = FunctionGraph(
            lambda x: 3*np.sin(x),
            x_min=-8,x_max=8
        )
        final_sine = FunctionGraph(
            lambda x: np.sin(x),
            x_min=-8,x_max=8
        )
        # self.play(ReplacementTransform(sine_function2,fullGraphExt3))
        # self.play(ReplacementTransform(fullGraphExt3,fullGraphExt4))
        # self.play(ReplacementTransform(fullGraphExt4,final_sine))

        eDot1 = Dot(point=np.array((-3*np.pi/2,0,0)))
        eDot1_2 = Dot(point=np.array((-3*np.pi/2,1,0)))
        eDot2 = Dot(point=np.array((-3*np.pi/2,2,0)))
        eDot3 = Dot(point=np.array((-3*np.pi/2,3,0)))

        eLine1 = Line(start=eDot1,end=eDot1_2)
        eLine2 = Line(start=eDot1,end=eDot2)
        eLine3 = Line(start=eDot1,end=eDot3)

        eBrace1 = Brace(eLine1,direction=RIGHT)
        eBrace2 = Brace(eLine2,direction=RIGHT)
        eBrace3 = Brace(eLine3,direction=RIGHT)

        eLbl1 = TexMobject("A=1")
        eLbl2 = TexMobject("A=2")
        eLbl3 = TexMobject("A=3")

        eLbl1.next_to(eBrace1,RIGHT)
        eLbl2.next_to(eBrace2,RIGHT)
        eLbl3.next_to(eBrace3,RIGHT)

        propEq1_2 = TextMobject("$E = 2$ units")
        propEq2 = TextMobject("$E = 8$ units")
        propEq3 = TextMobject("$E = 18$ units")

        propEq1_2.move_to(ORIGIN+UP*2)
        propEq2.move_to(ORIGIN+UP*2)
        propEq3.move_to(ORIGIN+UP*2)


        self.play(Write(eDot1))
        self.play(Write(eDot1_2))
        self.play(Write(eBrace1))
        self.play(Write(eLbl1))
        self.play(propEq1.move_to,ORIGIN+UP*3)
        self.play(Write(propEq1_2))

        self.play(ReplacementTransform(sine_function2,fullGraphExt3),ReplacementTransform(eBrace1,eBrace2),ReplacementTransform(eLbl1,eLbl2),ReplacementTransform(eDot1_2,eDot2),ReplacementTransform(propEq1_2,propEq2))
        self.play(ReplacementTransform(fullGraphExt3,fullGraphExt4),ReplacementTransform(eBrace2,eBrace3),ReplacementTransform(eLbl2,eLbl3),ReplacementTransform(eDot2,eDot3),ReplacementTransform(propEq2,propEq3))
        eDot1_2 = Dot(point=np.array((-3*np.pi/2,1,0)))
        propEq1_2.move_to(ORIGIN+UP*2)
        eBrace1 = Brace(eLine1,direction=RIGHT)
        eLbl1 = TexMobject("A=1")
        eLbl1.next_to(eBrace1,RIGHT)
        propEq1_2 = TextMobject("$E = 2$ units")
        propEq1_2.move_to(ORIGIN+UP*2)
        self.play(ReplacementTransform(fullGraphExt4,final_sine),ReplacementTransform(eBrace3,eBrace1),ReplacementTransform(eLbl3,eLbl1),ReplacementTransform(eDot3,eDot1_2),ReplacementTransform(propEq3,propEq1_2))
        self.play(FadeOut(eDot1_2),FadeOut(eDot1),FadeOut(eBrace1),FadeOut(eLbl1))
        

class Part3(Scene):
    def construct(self):
        circle = Circle(radius=1.5)
        line1 = Line(start=circle.get_top(),end=circle.get_top()+UP)
        line3 = Line(start=circle.get_bottom(),end=circle.get_bottom()+DOWN)
        line2 = Line(start=circle.get_right(),end=circle.get_right()+RIGHT)
        line4 = Line(start=circle.get_left(),end=circle.get_left()+LEFT)
        line4 = Line(start=np.array((1.5*math.sqrt(2)/2,1.5*math.sqrt(2)/2,0)),end=np.array(()))
        self.play(ShowCreation(circle))
        self.play(ShowCreation(line1))
        self.play(ShowCreation(line2))
        self.play(ShowCreation(line3))
        self.play(ShowCreation(line4))

class Outro(Scene):
    def construct(self):
        svg = SVGMobject("logo", fill_opacity=0)
        outro = TextMobject("All animations created by Safin Singh")
        outro2 = TextMobject("With the Manim Python library")
        outro3 = TextMobject("See source code in description")
        outro2.next_to(outro,DOWN)
        outro3.next_to(outro,DOWN)
        svg.scale_in_place(2)
        self.add(svg)
        self.play(Unwrite(svg), run_time=4)
        self.play(Write(outro))
        self.play(Write(outro2))
        self.wait()
        self.play(Transform(outro2,outro3))
        
        # end on wait
        self.wait()
# Broken Code that I tried

# class DotsOld(GraphScene):
#     CONFIG = {
#         "y_max": 8,
#         "x_tick_frequency": 0.25,
#         "x_max":3,
#         "y_axis_height": 5,
#         "x_axis_label": "$\\theta$"
#     }

#     def construct(self):
#         self.setup_axes(animate=True)
        
#         def sin_param(xpos_1,t):
#             global time
#             time = t
#             return np.array([xpos_1,np.sin(2*PI*(xpos_1-int(t))),0])

#         def get_sin(xpos_2):
#             return sin_param(xpos_2,time)[1]
        
#         t=0

#         #dot stuff

#         a = [0,0.125,0.25,0.375,0.5,0.625,0.75,0.875,1,1.125,1.25,1.375,1.5,1.625,1.75,1.875,2]

#         dot0_0 = Dot(self.coords_to_point(a[0],0))
#         dot1_0 = Dot(self.coords_to_point(a[1],0))
#         dot2_0 = Dot(self.coords_to_point(a[2],0))
#         dot3_0 = Dot(self.coords_to_point(a[3],0))
#         dot4_0 = Dot(self.coords_to_point(a[4],0))
#         dot5_0 = Dot(self.coords_to_point(a[5],0))
#         dot6_0 = Dot(self.coords_to_point(a[6],0))
#         dot7_0 = Dot(self.coords_to_point(a[7],0))
#         dot8_0 = Dot(self.coords_to_point(a[8],0))
#         dot9_0 = Dot(self.coords_to_point(a[9],0))
#         dot10_0 = Dot(self.coords_to_point(a[10],0))
#         dot11_0 = Dot(self.coords_to_point(a[11],0))
#         dot12_0 = Dot(self.coords_to_point(a[12],0))
#         dot13_0 = Dot(self.coords_to_point(a[13],0))
#         dot14_0 = Dot(self.coords_to_point(a[14],0))
#         dot15_0 = Dot(self.coords_to_point(a[15],0))
#         dot16_0 = Dot(self.coords_to_point(a[16],0))

#         def dot_updater0(mobj):
#             xc0 = (a[0] + 0.1)*get_sin(a[0])
#             mobj.move_to(self.coords_to_point(xc0,0))
#             print(get_sin(0))
        
#         def dot_updater1(mobj):
#             xc1 = (a[1] + 0.1)*get_sin(a[1])
#             mobj.move_to(self.coords_to_point(xc1,0))
        
#         def dot_updater2(mobj):
#             xc2 = (a[2] + 0.1)*get_sin(a[2])
#             mobj.move_to(self.coords_to_point(xc2,0))
        
#         def dot_updater3(mobj):
#             xc3 = (a[3] + 0.1)*get_sin(a[3])
#             mobj.move_to(self.coords_to_point(xc3,0))
        
#         def dot_updater4(mobj):
#             xc4 = (a[4] + 0.1)*get_sin(a[4])
#             mobj.move_to(self.coords_to_point(xc4,0))
        
#         def dot_updater5(mobj):
#             xc5 = (a[5] + 0.1)*get_sin(a[5])
#             mobj.move_to(self.coords_to_point(xc5,0))
        
#         def dot_updater6(mobj):
#             xc6 = (a[6] + 0.1)*get_sin(a[6])
#             mobj.move_to(self.coords_to_point(xc6,0))
        
#         def dot_updater7(mobj):
#             xc7 = (a[7] + 0.1)*get_sin(a[7])
#             mobj.move_to(self.coords_to_point(xc7,0))
        
#         def dot_updater8(mobj):
#             xc8 = (a[8] + 0.1)*get_sin(a[8])
#             mobj.move_to(self.coords_to_point(xc8,0))
        
#         def dot_updater9(mobj):
#             xc9 = (a[9] + 0.1)*get_sin(a[9])
#             mobj.move_to(self.coords_to_point(xc9,0))
        
#         def dot_updater10(mobj):
#             xc10 = (a[10] + 0.1)*get_sin(a[10])
#             mobj.move_to(self.coords_to_point(xc10,0))
        
#         def dot_updater11(mobj):
#             xc11 = (a[11] + 0.1)*get_sin(a[11])
#             mobj.move_to(self.coords_to_point(xc11,0))
        
#         def dot_updater12(mobj):
#             xc12 = (a[12] + 0.1)*get_sin(a[12])
#             mobj.move_to(self.coords_to_point(xc12,0))
        
#         def dot_updater13(mobj):
#             xc13 = (a[13] + 0.1)*get_sin(a[13])
#             mobj.move_to(self.coords_to_point(xc13,0))
        
#         def dot_updater14(mobj):
#             xc14 = (a[14] + 0.1)*get_sin(a[14])
#             mobj.move_to(self.coords_to_point(xc14,0))
        
#         def dot_updater15(mobj):
#             xc15 = (a[15] + 0.1)*get_sin(a[15])
#             mobj.move_to(self.coords_to_point(xc15,0))
        
#         def dot_updater16(mobj):
#             xc16 = (a[16] + 0.1)*get_sin(a[16])
#             mobj.move_to(self.coords_to_point(xc16,0))

#         dot0_0.add_updater(dot_updater0)
#         dot1_0.add_updater(dot_updater1)
#         dot2_0.add_updater(dot_updater2)
#         dot3_0.add_updater(dot_updater3)
#         dot4_0.add_updater(dot_updater4)
#         dot5_0.add_updater(dot_updater5)
#         dot6_0.add_updater(dot_updater6)
#         dot7_0.add_updater(dot_updater7)
#         dot8_0.add_updater(dot_updater8)
#         dot9_0.add_updater(dot_updater9)
#         dot10_0.add_updater(dot_updater10)
#         dot11_0.add_updater(dot_updater11)
#         dot12_0.add_updater(dot_updater12)
#         dot13_0.add_updater(dot_updater13)
#         dot14_0.add_updater(dot_updater14)
#         dot15_0.add_updater(dot_updater15)
#         dot16_0.add_updater(dot_updater16)

#         #end dot stuff

#         func = ParametricFunction(sin_param, t_max=2, fill_opacity=0)
#         self.play(
#             Write(dot0_0),
#             Write(dot1_0),
#             Write(dot2_0),
#             Write(dot3_0),
#             Write(dot4_0),
#             Write(dot5_0),
#             Write(dot6_0),
#             Write(dot7_0),
#             Write(dot8_0),
#             Write(dot9_0),
#             Write(dot10_0),
#             Write(dot11_0),
#             Write(dot12_0),
#             Write(dot13_0),
#             Write(dot14_0),
#             Write(dot15_0),
#             Write(dot16_0)
#         )
#         self.play(ShowCreation(func), run_time=10)