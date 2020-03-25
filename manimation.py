#!/usr/bin/env python3

from manimlib.imports import *
import typing
import itertools
import collections

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