#!/usr/bin/env python3

from manimlib.imports import *
import typing
import itertools
import collections

class Introduction(Scene):
    def construct(self):
        text1=TextMobject("Simplifying Expressions with Exponents")
        text2=TextMobject("Problem 21")
        text3=TextMobject("by Safin Singh")
        text2.next_to(text1,DOWN)
        text3.next_to(text1,DOWN)
        self.play(Write(text1))
        self.wait()
        self.play(Write(text2))
        self.wait()
        self.play(Transform(text2,text3))
        self.play(FadeOut(text2))
        self.play(FadeOut(text1))
        
class Solving(Scene):
    def construct(self):
        eq1=TexMobject("(2pm^{-1}", "q^0", ")^{-4}\\cdot{2m^{-1}p^3} \\over 2pq^{2}")
        eq2=TexMobject("(2pm^{-1}", "(1)", ")^{-4}\\cdot{2m^{-1}p^3} \\over 2pq^{2}")
        eq3=TexMobject("(2pm^{-1}", ")^{-4}\\cdot{2m^{-1}p^3} \\over 2pq^{2}")
        eq3_v2=TexMobject("(2pm^{-1})^{-4}", "\\cdot{2m^{-1}p^3} \\over 2pq^{2}")
        eq4=TexMobject("(\\frac{1}{16}p^{-4}m^{4})", "\\cdot{2m^{-1}p^3} \\over 2pq^{2}")
        eq4_v2=TexMobject("(\\frac{1}{16}p^{-4}m^{4})\\cdot{2m^{-1}p^3}", "\\over 2pq^{2}")
        eq5=TexMobject("\\frac{1}{4}p^{-1}m^{3}", "\\over 2pq^{2}")
        eq5_v2=TexMobject("\\frac{1}{4}", "p^{-1}m^{3} \\over", "2", "pq^{2}")
        eq6=TexMobject("p^{-1}m^{3} \\over", "8", "pq^{2}")
        eq6_v2=TexMobject("p^{-1}", "m^{3} \\over 8", "p", "q^{2}")
        eq7=TexMobject("m^{3} \\over 8", "p^{2}", "q^{2}")
        rect = Rectangle(height=2,width=8/3)
        
        self.play(Write(eq1))
        self.wait(3)
        self.play(Transform(eq1,eq2))
        self.wait(3)
        self.play(Transform(eq1,eq3))
        self.wait(3)
        eq1.become(eq3_v2)
        self.play(Transform(eq1[0],eq4[0]))
        self.wait(3)
        eq1.become(eq4_v2)
        self.play(Transform(eq1,eq5))
        self.wait(3)
        eq1.become(eq5_v2)
        self.play(*ReplacementMultiIndex(eq1, [0, 1, 2, 3], eq6, [None, 0, 1, 2], transformation=Transform))
        self.wait(3)
        eq1.become(eq6_v2)
        self.play(*ReplacementMultiIndex(eq1, [0, 1, 2, 3], eq7, [None, 0, 1, 2], transformation=Transform))

        self.play(ShowCreation(rect))
        self.wait(3)