from manim import *


RAW_INPUT = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
RANGES = [r for r in RAW_INPUT.split(",")]


class Day02(Scene):
    def construct(self):

        # # INTRO
        # title = Text('Advent of Code - 2025', font="Inter").scale(0.75)
        # subtitle = Text('Day 02', font="Inter").scale(0.65)
        # title_group = VGroup(title, subtitle).arrange(DOWN)

        # for line in title_group:
        #     self.play(Write(line))

        # self.wait(1)
        # self.play(FadeOut(title_group.submobjects.pop()))
        # self.play(FadeOut(title_group.submobjects.pop()))

        # Input data

        input_l1 = Tex(
            "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,", substrings_to_isolate=",")
        input_l2 = Tex(
            "1698522-1698528,446443-446449,38593856-38593862,565653-565659,", substrings_to_isolate=",")
        input_l3 = Tex("824824821-824824827,2121212118-2121212124",
                       substrings_to_isolate=",")

        input_l1.set_color_by_tex(",", RED)
        input_l2.set_color_by_tex(",", RED)
        input_l3.set_color_by_tex(",", RED)

        input_grp = VGroup(input_l1, input_l2, input_l3).arrange(
            direction=DOWN, aligned_edge=LEFT).scale(0.75).next_to(ORIGIN, UP)

        self.add(input_grp)
        self.wait(1)

        # Split string on comma
        str_split_grp = VGroup([Tex(r) for r in RANGES]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.5).scale(0.65).shift(5 * LEFT)
        self.play(ReplacementTransform(input_grp, str_split_grp))
        self.wait(1)
