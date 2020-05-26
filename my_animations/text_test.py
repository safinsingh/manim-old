from manimlib.imports import *

class Proxima(Scene):
    def construct(self):
        text1 = Code("hi.go",language="go")
        self.wait()
        self.play(Write(text1),run_time=3)
        self.wait()