from manimlib.imports import *
from ThetaCreature.ThetaCreature import *

class test1(Scene):
    def construct(self):
        Theta = SVGMobject("ThetaCreature_plain")
        Theta[4].set_color(BLUE)
        self.add(Theta)

class OmegaDice(Scene):
    def construct(self):
        Ale=Alex().to_edge(DOWN)
        palabras_ale = TextMobject("Learn to do \\\\animations with me!!")
        self.add(Ale)
        self.play(ThetaCreatureSays(
            Ale, palabras_ale, 
            bubble_kwargs = {"height" : 4, "width" : 6},
            target_mode="speaking"
        ))
        self.wait()
        self.play(Blink(Ale))
        self.wait(1)
        self.play(Blink(Ale))
        self.wait(1)
        self.play(Blink(Ale))
        self.wait(1)
        self.play(Blink(Ale))
        self.wait(1)