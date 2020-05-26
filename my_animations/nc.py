from manimlib.imports import *
from ThetaCreature.ThetaCreature import *

class test1(Scene):
    def construct(self):
        Theta = SVGMobject("ThetaCreature_plain")
        Theta[4].set_color(BLUE)
        self.add(Theta)

class TC(Scene):
    def construct(self):
        bruh = Bruh().to_edge(DOWN)
        bruh2 = CoolBruh().next_to(bruh,LEFT,buff=MED_LARGE_BUFF)
        
        self.wait()

        self.play(FadeInFromDown(VGroup(bruh,bruh2)))

        self.wait()

        self.play(Blink(bruh))
        self.play(Blink(bruh2))

        bruhText = TextMobject("bruh")

        self.play(
            ThetaCreatureSays(bruh, bruhText, bubble_kwargs = {"height" : 3, "width" : 4}, target_mode="speaking", look_at_arg=bruhText),
            bruh2.look_at, bruhText
        )

        self.wait()

        self.play(
            RemovePiCreatureBubble(bruh),
            bruh2.look_at, RIGHT,
        )

        self.wait()