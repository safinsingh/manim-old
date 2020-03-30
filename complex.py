#!/usr/bin/env python3

from manimlib.imports import *

class WhatComp(Scene):
    def construct(self):
        eq1 = TexMobject("1", "+",  "i")
        eq2 = TexMobject("a", "+", "b", "i")
        ex1 = TextMobject("Real Part")
        ex2 = TextMobject("Imaginary Part")
        im = TexMobject("i")
        imE = TexMobject("i", "=", "\\sqrt{-1}")
        im.scale(3)
        imE.scale(3)
        
        ex1.set_color(BLUE)
        ex2.set_color(RED)
        
        self.play(Write(eq1))
        self.wait()
        self.play(ReplacementTransform(eq1,eq2))
        self.wait()
        self.play(eq2[0].set_color, BLUE)
        self.wait()
        self.play(eq2.scale, 3)
        eq2aB = Brace(eq2[0])
        self.play(Write(eq2aB))
        ex1.next_to(eq2aB, DOWN)
        self.play(Write(ex1))
        self.wait()
        eq2bB = Brace(eq2[2])
        self.play(eq2[0].set_color, WHITE, eq2[2].set_color, RED)
        self.play(ReplacementTransform(eq2aB, eq2bB))
        ex2.next_to(eq2aB, DOWN)
        self.play(Transform(ex1,ex2))
        self.wait()
        vg1 = VGroup(ex1, eq2, eq2bB)
        self.play(ReplacementTransform(vg1,im))
        self.wait()
        self.play(Transform(im,imE))
        self.wait()