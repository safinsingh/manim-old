#!/usr/bin/env python3

from manimlib.imports import *

class DrawLogo(Scene):
    def construct(self):
        svg = SVGMobject("logo", fill_opacity=0)
        introText = TextMobject("S", "a", "f", "i", "n", " ", "S", "i", "n", "g", "h")
        
        self.play(Write(svg), run_time=4)
        self.play(Transform(svg, introText))
        self.wait()