"""The Dosun-Fuwari solver."""

from typing import Set, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, count, display, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs, validate_direction


def dosufuwa_gravity(float_color: str = "white", drown_color: str = "black") -> str:
    """
    Generates a constraint to fill the colors according to gravity.

    A grid rule should be defined first.
    """
    rule = f":- grid(R, C), {float_color}(R, C), grid(R - 1, C), not {float_color}(R - 1, C).\n"
    rule += f":- grid(R, C), {drown_color}(R, C), grid(R + 1, C), not {drown_color}(R + 1, C).\n"

    return rule.strip()


class DosuFuwaSolver(Solver):
    """The Dosun-Fuwari solver."""

    name = "Dosun-Fuwari"
    category = "var"
    aliases = ["dosunfuwari"]
    examples = [
        {
            "data": "m=edit&p=7VRdT+pKFH3nV5h5dZLTmYKWJvehInj1IKJCuNI0pOAA1Zbx9AM8Jfx390zH0Jbq9eXe+HBSurO69mbN3tPOin4lbshwAy7dwBomcFFqyLuuid/7NfBin5lH2EriJQ8BYHzT6eC560cMXz0suy1ubc6tf9ZGPB6TCy251EZPnafju+DnpaeHpNMz+tf9a48urL9bZ7cn7eOTfhINY7a+DcjZ03A8mPdHiyb93e6N6+n4Rmtcjec/1tbwr5qtenBq27RpphZOL0wbEYQRhZsgB6e35ja9NtM2Tu8hhXDdwShI/NibcZ+HSHIE6rrZHynA9h6OZF6gVkYSDXBPYYAPAGdeOPPZpJsxfdNOBxiJtc/kvwVEAV8zsZjoTTzPeDD1BDH1N0uEdaCi5JE/J6qIODucWrJ3VfvFAUDpfQABswEEqhhAzPVfDdB0djt4K3cwwsS0xTTDPTT28N7cQuzJSGR8kLEjI5VxAKU41WU8l1GTsSFjV9a0zS0iWhMToiGTwsvX4IvNY40qTAHrCuuA6wrXATcyTAz4b1Nh0KRKh4BOHhOlSUCTKE0CmkRp0lOoNxQGTao0KWjqSoeCTh5TpUlBUycZ1kWN4GHQkRy3JWNdxhO5DadiP//nHf/XdmyaOYe4Gl9DTs1G90k4d2cMPrX244Id9XgYuD48tXjwwiMvZghOPIq4P4myygl7dWcxMjPTyWcK3CoJpgzOTI7yOX/xvVWVwnuqQHqLFQ9ZZUqQDPr9QEqkKqSmPHws9bRxfb84izTjApWd2QIVh3Agc89uGPJNgQnceFkgpm4M5h0tvZeiEluVNjN2iy26z25ptWC/HbsaekXytnVM/9jzd7Vn8Ya072YZ360d+XHz8BOn2SfLdIXfAPuJ5eSyVfwH7pLLlvkDKxHNHroJsBWGAmzZU4A6tBUgD5wFuA/MRaiW/UV0VbYYsdSBy4il8kZjO7U3",
        },
        {
            "data": "m=edit&p=7VZrT9tIFP3Or6jma0daz4zf0n4INHTb5VlALImiyAQDoQ5mHRu6Rvz3njsP8qRF1Xa1K60SzxyfuffOfYyvPf2zyaqcC4/+KuaY8fNFrC8Zh/ry7O94XBd5+oZ3mvq6rAA439/e5pdZMc35x7Prna2y8/Cu88d9XPd64r3XfPBOb7Zv3n6a/P5hrCqxvRcf7B7sjuVV57etzcOw+zY8aKYndX5/OBGbNye948uD06tE/tXd6/ltb98LPvYuf7nvnPy60bc+DDYe2yRtO7x9n/aZYJxJXIINeHuYPra7advl7RGWGPcHnE2aoh6PyqKsmOYE5HaMogTszuCpXie0ZUjhAe9ZDHgGOBpXoyIf7hjmIO23x5zR3ptamyCblPc5bUa+0f2onJyPiTgvHq4ZV6CmzUX5ubFCYvDE24723cq+MgBYcgEQNAEQWhMAxfWzAkgGT0+oyieEMEz7FM3JDMYzeJQ+MiVZ6nPmx3oKAz3FwkyRnhIjIjxlZyMrhG9m5ZnZN+IiJDmY30sfMQo9nulxW49Sj8fwgbdKj+/06Okx0OOOlunCQSkDLmXIUomTJXH8JbbROAKGK4SFP8MSj4kPlwn7ksvA6gbQDaxuAN3AygeQDxIrj70cVgJ2kA9tH/IKSXE8ZU1j2FcIV2MFjJRoDH+U1SVM6dX2sVdodUPoRta3CPs+Y8hHVjeCzcjaDBJguxfJxNZmHHPlGZuYuRLGDmZgEy9mYCOvPP8ZywQ9xrP2gWViYsQ6VzZGzFz51qYPm1RmjcHb3CrkHPczLE0OMcMOjoe2g71sDjHP7PvAgYlXoaa4tz4o2HH+A9Nx05j8t/IedC2WMXQ9WyPKG51ejVGv2Mkgz4mtbwLfPOubR3lwupCPbI0iqpHLOfITWZmQamF0ZQCboTs/0LWxSB/yNhZ9bn0nD98CV1PU0cknOBvPvuG8Ja5GVDuXE/jpsAf/hfVfUq5sfiTyI10+A2B3HihXrkZUR1cX2HnGVHdbO8KBqxH2fa4L6q5t4gE91Y/plh59PYb68Y2owbyyBa12CsSGTibQ6Exz3NXtEjuDhQfz7I81le963sdhpffu4i/473GDjT47aqrLbJTj5dG9uMrf7JXVJCtwt1VO7srpuM4Z3uFsWhbDqZEc5l+yUc1S8xkxv7LA3TaT8xxvwTmqKMu7Yny7zoJbWiDHV7dlla9dIjKHvy+YoqU1ps7L6mLJp4esKBZj0Z9YC5Q5UgtUXeEVO3efVVX5sMBMsvp6gTjPanyOTa/Hd4uW8tulZNbZoovZ52xpt8ksHU8b7AvTVx+d4/8Prn/rBxdVyPvhnveTGtl33Om3Z3jx8Xafs7tmmA2RZoYTxv9WXrya/8ezo5+1svpG45stLtNr2h/Yb3TAudV1/AvNbm51mV/pbOTsanMDu6a/gV1ucaBWuxzIlUYH7oVeR1aX2x15tdzxaKuVpkdbzfe9/mDjKw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_cc(colors=["circle_M__1", "circle_M__2", "empty"]))
        self.add_program_line(dosufuwa_gravity(float_color="circle_M__1", drown_color="circle_M__2"))

        exclude: Set[Tuple[int, int]] = set()
        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")
            exclude.add((r, c))

        areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, exclude=exclude)
        for i, ar in enumerate(areas):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(count(1, color="circle_M__1", _type="area", _id=i))
            self.add_program_line(count(1, color="circle_M__2", _type="area", _id=i))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_M__1":
                self.add_program_line(f"circle_M__1({r}, {c}).")
                self.add_program_line(f"not empty({r}, {c}).")

            if symbol_name == "circle_M__2":
                self.add_program_line(f"circle_M__2({r}, {c}).")
                self.add_program_line(f"not empty({r}, {c}).")

        self.add_program_line(display(item="circle_M__1"))
        self.add_program_line(display(item="circle_M__2"))

        return self.program
