from manimlib.imports import *

class Proxima(Scene):
    def construct(self):
        text1 = Text("Hello World!",font="Proxima Nova Soft W03 Regular")
        self.play(Write(text1),run_time=4)