"""Constant definitions for the site."""

import logging
from typing import Any, Dict

logger = logging.getLogger("uvicorn.error")

PUZZLE_TYPES: Dict[str, Dict[str, Any]] = {
    "akari": {
        "name": "Akari",
        "category": "var",
        "aliases": ["akari"],
        "examples": [
            {
                "url": "https://puzz.link/p?akari/20/20/................................h............h1...h............i...i...........i1.bg........t.....i6cn...hbibi1b..kbl1b0.g6bgc..l..k.j1.l..hciam...i6.q...v0...bs....b.b..h2..h....i..h..i..h....i..h..b..h....h1..h...h..h....................../",
            }
        ],
    },
    "aqre": {
        "name": "Aqre",
        "category": "shade",
        "examples": [
            {
                "url": "https://puzz.link/p?aqre/18/18/aba2qqg6mi2nhodt6jfc57m8qt96l6a1828b1j6ucn7p5bspeseknpl0od86h00o00svvhe3e41s3g8r2gr3v9u0241vvvrufs3gf3soc0m1g21c3o3k3sn000s0g1g1g22g11g2g22g1g2212g1g1112233355g555355g3g3g355",
            },
            {
                "url": "https://puzz.link/p?aqre/21/17/144g3ab85s7kb44ql7sl61gc600ccc66cc66ic69c286i1g9cfu6nlltag1a4g1420081q5816tq1dvmh850l248h00g0321300001800kkbkaa18552l2lllllcdhkbvvk2fv404g7411g0115111339001112000182",
            },
            {
                "url": "https://puzz.link/p?aqre/25/18/g60o30c1g4000014o20vtofvvrgvu971vt1e30o0820g0gs1o1g2fg2g8v8d0hm1q138jk32r7cfdn6ouo0280000000vvvvvvuvo194fis9001014000vu07svufnsvv0nu80fu4nvfvq1u0011s000707to603oo0c000vvvvvg2g2g2h346g31gf1221g11311dg22451-10c9g36420505",
            },
        ],
    },
    "aquarium": {
        "name": "Aquarium",
        "category": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VZPb+O2E73nUyx05kEk9YfSbbtNeknTbpNisTCMQEm0G2PtaCvb3R8U5Lvvm+HQomQXPxRF0S1Q2Kaen98MZ8gZmtvf9k3fKq3pbZ1KFZDK8oI/Whv+pPK6We3Wbf1Kvd7vHrseQKmfLi7Uh2a9bc8Wmq3T5dnzUNXDWzX8UC8SnajE4KOTpRre1s/Dj/VwroZr/JQoDe7Siwzg+Qjf8e+E3nhSp8BXggHfA96v+vt1e3vpmZ/rxXCjEprnO7YmmGy639tE4qDv993mbkXEXbNDMtvH1Wf5Zbt/6D7tRauXL2p47cO9PhGuHcMl6MMldCJcyuJvDrdavrxg2X9BwLf1gmL/dYRuhNf1M8ar+jmxlkwzxOL3JrEZETYi8rmimBPl3MQRkUdENSOylIgqIvRcYYgoI2I+S8GKKI6SFaiyQFSsiJzqdC7RZu5F+3Riq5w1LmIK1kTRaceaQ0ZYXs2L/J7HCx4NjzfYAzVYHr/nMeUx5/GSNefYGuNKZRyW0qB1nAPGKhIusykusUOEi3TErlKmwiITrlJlU8/jCYwNZB6tHnBZQI89YJzDj/CFAUayzCMeWlK2NbD1PJ7AEmdlR1wi5gr1FWzLoIHPAw9NKbkUlEvIi+JHKbIefBXyQo4BF4jThRyBK4nZ6REXyMtJXhXlKLlAb7W3xRPYa/AEDjlmyMXHg6eyxseDJ7Csp4Ef4+di24BNoSzVNOEMPJVzsKVuIGzhkxqBNYjhoAfOxX8O/7n4xElsc1nzHH4K8VPAj5PYHHgntg62TmwdbF1kG/svJYYS8wZbmquUeEr6Sxj9ZKnn8VSZDnwO3vvBE3yIAXNVEmflJjjTvgYy/LMEbCvUUuXrxDrUmOwXYycahxoL+WJPDxraU9l3izrB9xFLDeAJLHsBfRZqgPY66KmGpfYs1bnUqkUv2CJgaArRoG6t1K1FPU9wsNXIS0teKWwFU1/ju9QD/NN5zBiaTPQZNFmoGcwVYzqdua6QY8CaalXySqHRoYapniO9kTVJsYYBG6wPHfDsn+pN+JxqMsKF+EEP2kL06LXDOhOmQ5Ixci8kl5zWLcK5rGGO3POQO/R05HI8tCbROUPHNWOsiRG9gZ/Qm7i7jP0FzD5xoL7jY/UNjxmPBR+3Jf0h/qm/zL9+sv/fcBbYcbp/TV+4h/3buOXZIrne9x+a+xbXlfOHj+2rq67fNGt8u9pv7to+fMdtMdl269utqGu+TOJ6A+6JlRNq3XWf16unqW718anr25M/Edli+hP6u65/mHn/0qzXE8JfjyeUv8VNqF2PK1r0ven77suE2TS7xwkRXecmntqn3TSAXTMNsfnUzGbbjDm/nCX/S/izsHSN/+8q/g9dxWkL0m/tdPnWwuHq7fqTrQ/6RPeDPdnlwh81OvijlqYJj7sa7InGBjvvbVDH7Q3yqMPB/UGTk9d5n1NU81anqY66naaKG36xPPsK",
            },
        ],
    },
    "balance": {
        "name": "Balance Loop",
        "category": "loop",
        "aliases": ["balanceloop"],
        "examples": [
            {"url": "https://puzz.link/p?balance/10/10/q1i8k8k0i1g8h1g9k9h0j1h8k8g0h9g0i1k9k9i0q"},
            {"url": "https://puzz.link/p?balance/15/9/l-111do080o199o000o111o000o711o008ob1bo808o919l"},
        ],
    },
    "battleship": {
        "name": "Battleship",
        "category": "var",
        "examples": [
            {
                "data": "m=edit&p=7VVBb9s6DL7nVxQ662DFjuP41va1u3R569qhCAyjUFK3MWpHneKsg4P895K0W8uydthhWwcMjgnmI0V+okR6+3UndcaFwJ8fcY+DxoNJSK8QY3q99rnOqyKLj/jxrlorDQrn/5+f83tZbLNRImi1l4729SyuL3n9IU6YYJyN4RUs5fVlvK8/xvWc11dgYlwAdtE4jUE969QbsqN22oDCA33e6qAuQF3KCvhs1/nT7UmDfoqT+pozzHVCEVBlpfqWsZYL/l+pcpkj0AVoLdvdnXrctb4iPfD6uKG8cFD2O8qoNpRRc1DGnfwGyrP0cIDyfwbSt3GC/L90atSpV/Ee5DzeM9/HpT5wac6I+cHr9l+BCQJwhm9AaANTBDwDiBAIDGBmLQk8K0sgLB7B2F5CWYygoe0xJQ8j6Iw8DGLCIxdjjRiTjxFWNNsxwoiJnUmEA5+IfN42AOUVVOQFFDnEioV8ePoswvI7LcLDmvlOE62aOk0zrKPDBEzOic+Y5DXcA177JP8j6ZGckLwgnzOSNyRPSQYkQ/KZ4k36qbtmluQX0UmCiAZY/4FB9rdh6Shh8125zPTRXOlSFtDtV2v5lDEYr2yritvtTt/LFQwJmr4wBwDb0IoeVCj1VOSbvl/+sFE6c5oQzO4eXP5Lpe+s6M+yKHpA8z3pQatcr4o+VGmYZcZ/qbV67iGlrNY9wJh7vUjZpuoTqGSfonyUVray2/NhxL4zeqHT4Lv379v1h79deBTee5sq740O3WKlnSMAYMcUANTZ7S0+aHjAB62NCYfdDaijwQG1exygYZsDOOh0wH7Q7BjV7ndkZbc8php0PaYyGz9JRy8=",
            }
        ],
    },
    "binairo": {
        "name": "Binairo",
        "category": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VjNT/tGEL3nr6j2vAfvh+OPG6XQC9BSqBCyIuQEQyKcmNpOqRzlf2d2HCk4+6JKSD8VqSjxaPI8mX27M2/jTfPXOq8LqQP3NrEMpKJXlMR8xaHiK9i9bhdtWaQ/yZN1O69qcqT87fxcPuVlU4yyXdRktOmStLuW3a9pJpSQQtOlxER21+mmu0zFrFpOF0J2N3RfSEU3LvpITe7Z3r3j+8477UEVkH+188m9J7ctVm3Tf/w9zbpbKdxIP/NXnSuW1d+F2DFxn/vRCZiWb/Md1qwfq5f1LkpNtrI7YardDWBp9iyd27N0HmDpyDuWs0U9K4uHi88RzVta92a+eEV0k8l2S0v+BxF+SDPH/c+9G+/dm3RD9oqtYnufbsQ4ojSaBusJXjJlMU4IVYdoFKLYKIaxMEOsUYbYwljHzEMTl9fLoAKFYZcZwHDSKoCclXK5AWwwjHNrN3M/2gQw2sC5K4MJWjykdYXx4RAPGeKlCscYxrnHsL5qjHNHLrc/HW4dPzrBSRLXlF4SzQ0B4CPRsIc1bgiNK681XFitj0TDomkNF1YbPB0LlaO5IQCMp4MbQoewDDpy0X4S3hsAjJnEeMgYJ0ng5E0AF9awuH1YwWYzuGgGy9Vw0QAMi2Zw0Qyr2I+2UDuGSwxgWEuD5WoiuD0aFqAPx0dgKBITYyYJTGIDuLAW19JiuVosQItraTWcvNWwIayBtbS4OtY6JgDGubEuLd5M7Ri2j8WbqY0wwQgvFZarxQ1h8c+2jfHkcftYVrEHh3jrDflnFMCw2UIuMYAhwVCDydPj0Dk/FGm2t/TMJDvD9he2AduQ7QXHnLG9Y3vK1rIdc0zknro+/Vz2g+hkYf+A/++v8DvuO+7/FzcZZeK0Wr5WzaItBB1lRVOVD826fspndDjjky6dvwhbrZfToh5AZVW9lovVMG7xvKrqAt5yYPH4jOKnVf14kP0tL8sB0J/dB1C/ow2gtqYz5IfPeV1XbwNkmbfzAfDhvDnIRCftIYE2H1LMX/KD0Zb7OW9H4h/BV2Zoqe33/wT/wf8EbvmDr/ar9NXocOdWNZQ9wUD5hEKF73BP5IR7cnYD+oomFIia0ENdE+RLm0BP3YQdEbjLeqhxx+pQ5m4oT+luqI9izyajdw==",
            },
        ],
    },
    "box": {
        "name": "Box",
        "category": "shade",
        "examples": [
            {
                "data": "m=edit&p=7ZVNc5s+EMbv/hQZnXVAvBm4pWnSS+o2f6eTyTBMBjskYQJWKuPmP3j83bO7giBeeuihrQ8dzM76xyPpEdKK7fddqjIuBP6cgFscMu56Pt1C2HRbzXWdV0UWnfDTXfUkFSScf7m44A9psc1mMbaEK5nt6zCqr3j9KYqZYJzZcAuW8Poq2tefo3rB6yU8YtwBdqlFNqTnXXpDzzE701BYkC+aHNJbSNe5WhfZ3aUmX6O4vuYMx/lArTFlpfyRscYH/l/LcpUjWKUVTGb7lL80T7a7e/m8a7QiOfD6VNtdtnZxlMYuOm/sYqrtYjZhF2fxm+2GyeEAr/0/MHwXxej9W5cGXbqM9hAX0Z45DjX1wIxeHOa4SGzHIB4SxzKIP9LMRyQgYvYcDjWuNSKCiG8Q6lngy2yIpwnjfgN8m4DbSeZEYMO1krluY7gJiMDQrSTUvUCjViIsQtBvqxHWyI0QhKDnd5FNzYw5CKcl7xr9wuBFdiI907kh8qhZT6TnGhgif9yTnm1oiAK9zibR62wSvc4moXU256/fmjnZgNbZnFpA62zOI6R1Nk2HtM7vDmE3CtqTtxQvKNoUr2HL8tqh+JGiRdGjeEmac4o3FM8ouhR90sxx0/9SWfwBO7Eb6HPSuObHRZJZzJY79ZCuMzhsFrtylamThVRlWjA43dlWFnfb5nlEhz8cR8A2pOyhQsqXIt/0dfnjRqps8hHC7P5xSr+S6n7Q+2taFD2gP2c9pE/dHqoUHKnG/1Qp+dojZVo99YBx/PZ6yjZV30CV9i2mz+lgtLKb82HG/md0xw5+dv99Ov/SpxOXwDq2k+LY7NDulWqy9AFPVD/QySpv+KjQgY9KGgccVzXQicIGOqxtQOPyBjiqcGA/KXLsdVjn6GpY6jjUqNpxKLPg42T2Bg==",
            },
        ],
    },
    "canal": {
        "name": "Canal View",
        "category": "shade",
        "aliases": ["canalview"],
        "examples": [
            {
                "url": "https://puzz.link/p?canal/17/17/r11q33h33m31h13m31h16q42q16u81z14u21q21u43z16u31q31q62h41m54h31m12h15q21r",
            },
        ],
    },
    "castle": {
        "name": "Castle Wall",
        "category": "loop",
        "aliases": ["castlewall"],
        "examples": [
            {
                "url": "https://puzz.link/p?castle/13/13/224e227u20.d124b223k224g10.10.k122e133b247k20.b146e115k135121g211k213b10.d233u242e211",
            },
            {
                "url": "https://puzz.link/p?castle/16/11/f032k222d022e133a00.d143f041i023c011b023b00.b130d232f033e20.e212a040r035b20.c20.a00.b033a00.f131i034d013b10.a00.a00.e014m037a",
            },
        ],
    },
    "cave": {
        "name": "Cave",
        "category": "shade",
        "aliases": ["corral", "bag"],
        "examples": [
            {"url": "https://puzz.link/p?cave/11/11/9g7k6g5g7m5g5g6k7g6u6g7o9o6g7u5g5kag6gbm3g6g8k7g6"},
            {"url": "https://puzz.link/p?cave/10/10/l.j2h2h2h.h.h.q2i2h2g.l.k.h.h.g2h2i.i.j2h2j.i.i"},
            {
                "url": "https://puzz.link/p?cave/10/10/j7k2m4l4l-10g8h4g58x56gch6gfl4lam2k8j",
                "config": {"product": True},
            },
        ],
        "parameters": {"product": {"name": "Product", "type": "checkbox", "default": False}},
    },
    "chocona": {
        "name": "Chocona",
        "category": "shade",
        "examples": [
            {
                "url": "https://puzz.link/p?aqre/26/22/885kcco5lc912qccuksc8u9k8cdbs24ujt2ctre2ifbuagd77ah6bbjpubmjvt7n57t4gldt0oa6t0gi3uci41s4icrs32ar3j7cqhjpkk2lik3g3302fuitovkgv3g7tge73ifv7jejuc0r4v3ei4e1o79r01jpqune0kg1ov1f300bf783vukb00fg2mvvvggs0tvovs0g3frku1s0tg7v270064a13422432332444724242322633942221232249322222423462242621324325398321344611532442412253236225",  # hack aqre as chocona
            }
        ],
    },
    "country": {
        "name": "Country Road",
        "category": "loop",
        "aliases": ["countryroad"],
        "examples": [
            {
                "url": "https://puzz.link/p?country/17/17/4si5d6t8fa2heg0ch42pfar88vioeikf7s4665a6g69g2bo2rc2qk0g5jrmll2p6kk62qsfhflvrakghu0pq13l87qg5huhgj407o09p0557vg4g4j-19o-362k2q1g",
            }
        ],
    },
    "doppelblock": {
        "name": "Doppelblock",
        "category": "num",
        "examples": [
            {
                "data": "m=edit&p=7ZVfb9o8FMbv+RSVr33hxAFC7rqu7IaXroOpqqIIGUhL1ARTJ1knI757j0+y5S96tYuxXUwmRyc/H9uPneQhfc2FCukEGncpoxY07jK8XMf8WNmWURaH3hW9zrOdVJBQejed0icRp+HAt3AsCwZHPfH0PdWfPJ9YhBIbLosEVN97R/2fp+dUL6CLUAfYrCiyIb2t0gfsN9lNAS0G+bzMIX2EdBOpTRyuZgX57Pl6SYlZ5wOONilJ5LeQlDrM/UYm68iAtchgM+kuOpQ9ab6VL3lZawUnqq/Py+WVXJMWck3WI9fs4jfLnQSnExz7FxC88nyj/WuVulW68I4Q596RcGaGuqCleDaEWzgXPKufxDHEZjUybBOnGDWqyBBH8QqMxi3g4tLWpCITjsSpiMVGiMY1BCMA1Yu4jXp+ENiahRt8xDjFaGNcwv6p5hg/YmQYhxhnWHOL8QHjDUYH4whrxuYEf+mMLyDHd2z8XKs2uux9MPDJIldPYhPCeznPk3WoruZSJSImYAQklfEqLfs99Al4c4HtsbKBYikPcbRv1kXPe6nC3i4Dw+1zX/1aqm1r9jcRxw1QuF4DFR9oA2UKvr7avVBKvjVIIrJdA9S+1MZM4T5rCshEU6J4Ea3VkmrPpwH5TvDyORy8889l/5DLmkfA/jYf+B85vl5Qzqi+o+SQr8RqI2MCf9T0DL+4enzZpep1CsA9ZgG01xRK3vEF4B0HMAt2TQBojw8AbVsBoK4bAOwYArAznmBmbduCUdV2BrNUxxzMUnV/8Il4hb0Eg3c=",
            }
        ],
    },
    "easyasabc": {
        "name": "Easy As ABC",
        "category": "num",
        "examples": [
            {
                "data": "m=edit&p=7ZXPb5swFMfv+Ssqn33AQBPg1nVtL122rqmqCqGKpLRFhbgzsE5E+d/73gMN27DDDttymIifHh/844ud76P61qQq40Lgzwu4wyHj/vGcmhAuNae/VnldZNERP2nqZ6kg4fzz+Tl/TIsqm8U4Eq5ktmvDqL3i7UUUM8E4c6EJlvD2Ktq1n6J2ydtreMS4D+yy6+RCejakt/Qcs9MOCgfyZZ9DegfpJlebIru/7MiXKG5XnOE6H2g0pqyU3zPW68D7jSzXOYJ1WsPLVM/5a/+kah7kS9P3FcmetyeWXJTTy/UGuZh2cjGbkIvD/rDcMNnvYdu/guD7KEbtN0MaDOl1tIO4jHbM83HoCWjpzoZ5cwQ3GljYIEBwPQDfQbDSgLABzaGBhQ0CApqO0EVwMQDh2GOEsKUJdzSqk69NLDox+qj5iAS0LQahfdHeWowki4B2xiChrSekzdJnDmm3fo6CgxF0PHcUzym6FFdwerz1KH6k6FA8pnhJfc4o3lI8pehTnFOfBZ7/b/1D/oKc2A+6kqFdi8MiySxmy6ZcZ+poKVWZFgzKG6tkcV816jHdgFmp+oEfgW2pp4EKKV+LfGv2y5+2UmWTjxBmD09T/ddSPVizv6VFYYCunhuoKzsGqhXUFO0+VUq+GaRM62cDaPXHmCnb1qaAOjUlpi+ptVo5vPN+xn4warGH353/345/9O3AI3AOrT4cmhz690o1aX3AE+4HOunyno+MDnxkaVxw7GqgE8YGansb0NjeAEcOB/YLk+Osts9RlW11XGrkdlxKN3yczN4B",
                "config": {"letters": "AUGST"},
            }
        ],
        "parameters": {"letters": {"name": "Letters", "type": "text", "default": "ABC"}},
    },
    "fillomino": {
        "name": "Fillomino",
        "category": "num",
        "examples": [
            {
                "url": "http://pzv.jp/p.html?fillomino/13/13/i3j3k3h1g3g1h3k3j3k3j3j331g1g3h1g31j3p3j1j3p3j13g1h3g1g133j3j3k3j3k3h1g3g1h3k3j3i",
            },
            {
                "url": "https://puzz.link/p?fillomino/15/15/h1o5i8g2m6g3g7i3h4h1i1g6g4h2g3h4g2i5h2i4h3l4k5m4m6k7o7k7m3m2k5l3h4i3h3i-10g4h4g1h3g7g1i8h4h3i2g2g2m8g6i1o1h",
            },
            {
                "url": "https://puzz.link/p?fillomino/9/9/rb-134k-13i-13i7k5h-13k-13h8k6i-13i-13k9-13am2j",
            },
        ],
        "parameters": {"fast_mode": {"name": "Fast Mode", "type": "checkbox", "default": True}},
    },
    "firefly": {
        "name": "Hotaru Beam",
        "category": "loop",
        "aliases": ["hotaru", "hotarubeam"],
        "examples": [
            {
                "url": "https://puzz.link/p?firefly/13/13/2.e43e33b13g31g42a23h13b23b32g44c22f4.g13g41h13a41e3.a4.h43g25g11f4.c13e1.d30d23g41f",
            }
        ],
    },
    "fivecells": {
        "name": "FiveCells",
        "category": "region",
        "examples": [
            {
                "data": "m=edit&p=7VbNbtpAEL7zFNGe9+AZ29jrW5pCL5Q2DVUUWVYExG1QQU75qSoj3j2zs1CW2ebQQyMOkdnR+NuZ3W9+dvHq52a8rDWk9hfnOtJATzfKeUBO7zQOz2i2ntfFhb7crB+bJSlaf+r39bfxfFV3yr1V1dm2pmivdfuhKBUqzQNUpdvrYtt+LNqhbm9oSmkgbEAaKI2k9o7qLc9b7cqBEJE+3Ouk3pE6nS2n8/p+4JDPRdmOtLL7vGNvq6pF86tWzo3fp81iMrPAZLymYFaPs6f9zGrz0PzY7G2h2un28mW68ZGuVR1dq/03uvOn5m9ETbXbUcK/ENX7orSsvx7V/KjeFFuSw2KrutEhRlcV1QULUJH+ACiB2AKxByQWiDwglRZduUsmLXJpYYRFxkw9HplkmkmmGa/hAYZdvEUNb+tZAMiEAEiugLyubxPLACEJ1kl48xOECfsrJ5xbn0/CyT1BmLPvlcp8QyqzB0HVwNXA55PxXr5NFuQnZ85esSHn2H0vE+xlZA4xkqXAiKPw9kKQ+UGQeUZXnRMv2UoIsg8QZTMhytgxDhi66nixY8rr+Ig7Lr5X0MmYy87FXNYU84CzCTi7dvYjNfIIYFALNPK4opH9gybIc1hBd3ZObGSkcXTKmS4d4KvnjmWfJbIc0c2k25jle5YRy5TlgG16LG9ZXrFMWHbZJrN32z/dfq9Ap0zcn+hLD/3Vvs2e92zVKVXv4Xt9MWyWi/Gc/neHm8WkXh7e6RNn11G/FY8yJpfk7avn1b96bPKjczv950aH7qOq8ww=",
            },
        ],
    },
    "fourcells": {
        "name": "FourCells",
        "category": "region",
        "examples": [
            {
                "data": "m=edit&p=7ZbfbpswFMbv8xSVr30B5k+Au65Ld9PRde1UVQhFTkpbVIgzB9bJUd69xweqFJtqqiZF01QRjg4/G5/PjvM5m58tlwV1Q/3xIupQF67QD/EOohhvp7+uyqYqkiN63DYPQkJC6fnpKb3j1aaYZH2vfLJVcaIuqPqSZIQRirdLcqoukq36mqiUqktoItQFdgaZSyiDdLZPr7FdZycddB3I0z6H9AbSZSmXVTE/68i3JFNXlOg6n/BtnZJa/CpI9xo+L0W9KDVY8AYms3ko133Lpr0Vj23f1813VB13cmcjcr29XJ12cnU2IlfP4u/lVmsxJjTOdztY8O8gdZ5kWvWPfRrt08tkCzFNtsSPX+bYfSsk8A0QWiAwgOtMTeIyi1hvMc8kfmiSwLGINc7UqjW19ERWrcgaJ4pMEpt9mDUvxsxazDM1M9+szqxVZtYs2NRcDWZpZrFZy3PMWp5jzsuzZuFZK+8FrkWG1WEDubiNbjCeYmQYr2CXUeVh/IzRwRhgPMM+M4zXGE8w+hhD7DPV+/RdO/kAcjKfoSG+fQUf7f9zez7JyOz2vjhKhax5BQ6ctvWikC/PcNiRjajmm1be8SVYN56F4NHAVthzgCoh1lW5GvYr71dCFqNNGhZQfqT/QshbY/QnXlUD0J3uA9QdQgPUSDhhXj1zKcXTgNS8eRiAV4fnYKRi1QwFNHwokT9yo1q9n/NuQn4TvDMPFt//+Cdx8H8SevGdf82F/yAnU5fUj6k6p2Tdzvl8KeB3Cqv2Nr95J081776B/mgc62C+ePBlwt+TkKNmBHjEj4CO+k7PLesBbpmMLmj7DNARqwFqug0g23AAWp4D7A3b0aOazqNVmeajS1n+o0u9tqAsnzwD",
            },
        ],
    },
    "gokigen": {
        "name": "Gokigen",
        "category": "draw",
        "examples": [
            {
                "url": "http://pzv.jp/p.html?gokigen/40/25/hbg1bha6ah66bcbh7c98d8cdjdk672817chc717die62b8dcg8c26di32ck3d287271617262bg31222c88e2bddcc3bkdeg87dc777228ddg1cehdch6cb2cb122b73d3c26b31377c7e71cc8clbg8bh317677c6d7b63716eh26d2b8c9ch31c7ddj28277d77bg732cg27c61cg83268871ci626b8681cieicg2ddjdi6277226ch8d3d7dgec2cg73dd63622d3cb172b62667cc1c66d37226263c7cdg8d7bg7273cg78cb9c77cg22dg061661668dge71b778c76bgcg717c7cd376677173bgdg81b9dc8dgch231ch8ce897cg7b631682cgcckcjdg318277cg4ceh6166cgb6cc268173cgeg2173c27d367328cgc267di6bi7bg77dg769cg78d8d22ba656776bgb1bibajb",
            }
        ],
    },
    "haisu": {
        "name": "Haisu",
        "category": "loop",
        "examples": [
            {"url": "https://puzz.link/p?haisu/7/7/335594i94i94g07u003v00n1g3m3i2i3i2m2g1n"},
            {"url": "https://puzz.link/p?haisu/9/9/199103msp7vvv4pre00bs6poj0068sr1ugp2g2g2g2u2g2k2k2g2u2g2g2g2p"},
            {"url": "https://puzz.link/p?haisu/13/9/5948l0l2la55d8220gg44110000vg305c0cc00000000fvol3t1k3h25g5y5r6i7jao5zq"},
        ],
    },
    "hashi": {
        "name": "Hashiwokakero",
        "category": "loop",
        "aliases": ["bridges", "hashiwokakero"],
        "examples": [
            {
                "url": "https://puzz.link/p?hashi/19/14/2g2g3g3g2i2g3g2q2g2g1h3g2g3h2v2i3g2h1g2h1g2g3p2g23g2g2g2j2g2i2h2g3g3g33zh2h3g1h2g32h1g2g2h2j4g3h1h2l2g1j23g2h4g2g1h2h3g2o1g2h2p2g2i2k1g2g3g4j3h22g3h2",
            },
            {
                "url": "https://puzz.link/p?hashi/15/21/.g3g2g3g3g2g3g3w3h.i3h3zh2g3g3m4i3g.i2h2i2h.h3i.l.g2q2i2m3i4g.i2l2h.h3l2i.g2i4m2i2q.g2l.i3h.h2i2h2i4g.i3m1g2g3zh2h2i.h2w2g3g4g4g2g4g2g./",
            },
        ],
    },
    "heteromino": {
        "name": "Heteromino",
        "category": "region",
        "examples": [
            {
                "data": "m=edit&p=7ZdPb9tGEMXv/hQBzzxw/5O8pandi+s2tYsgEASDtplYiGSmlNQUMvzds9z5CTIlFWgPbVPAkLS7nJ2ZnbdvZqld/rZu+jbXbviaMi9yFT9VWaaf1UX6bT9Xs9W8rV/lr9er+66Pgzz/6ews/9DMl+3JBK3pyeOmqjdv880P9STTWZ5+Kpvmm7f14+bHenOZby7jVJbbKDuPI5XlOg5Pd8N3aX4YvRGhKuL4gnEcvo/D21l/O2+vz0Xycz3ZXOXZsM53yXoYZovu9zYTs/R82y1uZoPgpllFMMv72Wdmluu77tMaXTV9yjevJdzTI+GaXbjDUMIdRkfCHVD8w+FW06enuO2/xICv68kQ+6+7YbkbXtaPmS+z2uaZr1IXlHRaOiOdTV0lc5XMVS51qvD04kCpgl7UlOZZi7XSW7n4Vho/WuJQGj8GO4OdYR0TpLfM2+0zdk6CVQ6/DjuHnsefJw5PHB47NkIF7AJxlehX4kcXItdK9LRCDl6txZ8GnwaXNjyDQxvkVvxrK/Foiz34tGU9J/Frhz54NTi1Qw882mMfiAs8OrBuyTx86krmTSHrmELWMYX4M/BqlMRp1FYu6xv4NeA3Wvwb+DWGeYO9QY99MeyHgV9jiQOcBh4NOA18Gvg0njjAbchvQ2YbktmA35SsUxIP+2FK7CrkFXbsk2V/bCHzln2x7IdVYm/ZDwt+Sx5Y9sGC08K/hX8L/9ayHnlgyXPrsCPPLfxb9sOC35LPlpK2AXmJHnltwW/Jb1eIf0eeO+rbUd8O/h14nZI4nEJPSzwOvA6+HTw78t+B11n04dnBswOPg1/nsQefg08XkIPDlazLceXA5cHlObc8vHnweHB4+PPw58ljz7nkyUsPbx4cHt489eqpU++YB5f3+AGf5xzynLkeXB6+PPnq4cuTpx58vuIAJx9DIfMBfAF8gToNnFMBfgK4AjwFeApGcARwBnAGcAZwBvIybF8k6fyM75iL+jG2KrXvU3uWWp3aq/giyjcmtd+ntkitS+150jlN7bvUvkmtTa1POmF4lf3Fl92/Fs7Eyz+nv/NxLxYvFi8WLxb/D4vpySS7XPcfmts2XkFO7z62ry66ftHMs3jjy5bd/HrJbJ0uhPGKEmUP68VN249E8677PJ89jPVmHx+6vj06NQjbuNwR/Zuuv9vz/qWZz0cCueKORHITG4lWfbxmPXtu+r77MpIsmtX9SPDsSjby1D6sxgGsmnGIzadmb7XFDvPTSfZHln4TE7fdvlyn/6Pr9EBB8a39z/jWwknZ2/W70l/1a3I6SrfFPxIerXHkB2Ue5QcFPSx3WNNReqSso3S/sqPosLij8KC+o+xPSnzwul/lQ1T7hT4sdVDrw1LPy30yPfkK",
            }
        ],
    },
    "heyawake": {
        "name": "Heyawake",
        "category": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VXfT9swEH7vX4H87Ic4dn6+MVb2wroxmBCKKpSWABVpw9J2TKn6v/OdfdCmDdqkaRqTpjb25+98vu8cnzP/tszrQiqP/jqW6PEzKraPH4f28fh3PlmURXogD5eLu6oGkPLT8bG8yct50ct41rC3apK0OZXNhzQTSkjh41FiKJvTdNV8TJu+bM5gEjIGd+Im+YD9DbywdkJHjlQe8IAx4CXgeFKPy+LqxDGf06w5l4LivLPeBMW0+l4I1kHjcTUdTYgY5QskM7+bPLBlvryu7pc8Vw3Xsjl8Xa7ukktkh1ya8IflJsP1Gtv+BYKv0oy0f93AeAPP0pUwoUhjKYLYdklgO+Ur1xtHq8BDD48BPDRwJiLodu/R+mbhyzAku9kMdduKeJl+GSrP35qNCCpdob207bFtfdueQ7JstG3f29azbWDbEzunD3W+UdIPkIaPk2YMMNRZHEk/RFqEgwA4YYyDHUEE4RC+EfuGCQ47tBOOfDr4jOEbs2+spZ9EjEOpPaRucQLMvkkktXJxYQc2jDWw84Vdat/FhR3YaYZdas2+fgDs4sIutXGaYQdmX424gYsLO7DTDDswa8Yc37BO4wHzntC+8ZrogVm/QY7Gabb7ybHQA/OeGFwMhveB9pmOjcXYW7O1VzGvE2OdmNeJaT9ZJ+WrnnNHjorzpRz1c77IS5M2vPAL+9qPbGtsG9rjENH5/sUKcKf690/eT+Vk2l2n7V/w73HDXibOlvVNPi5w+/Svb4uDQVVP8xKjwXI6KurnMS5/Ma/KqznPTu23AbcVuJmd2aLKqnooJ7P2vMntrKqLThORBcJ3zB9V9fXO6o95WbYI97VrUe5SblGLGjfu1jiv6+qxxUzzxV2L2LqdWysVs0VbwCJvS8zv851o003O6574Iexj70/z/8v6l76s9Aq8t3a7vDU59vRWdWfpg+6ofrCdVc78XqGD3ytpCrhf1WA7Chvsbm2D2i9vkHsVDu6VIqdVd+ucVO2WOoXaq3YKtV3w2bD3BA==",
            },
            {
                "url": "https://puzz.link/p?heyawake/19/15/201480mhg2i40a8s192816704r503gk0m2g2oa0a18085010k046g0003hu0104000400fbvgvo005fu1800o0000000800600000003s0003c-1c140411g81ah8233",  # this case will TLE
            },
        ],
    },
    "hitori": {
        "name": "Hitori",
        "category": "shade",
        "examples": [
            {
                "url": "https://puzz.link/p?hitori/11/10/2b17123259583b698a764b75327b56287428b368ab69a141532195317984768731362985b5428b475297b8725853b14931a6964a4131b6",
            }
        ],
    },
    "juosan": {
        "name": "Juosan",
        "category": "draw",
        "examples": [
            {
                "url": "https://puzz.link/p?juosan/21/12/4ql08qtg9qt59ul5bunltnn9tntd72ta72h636h5b641bm04vmcvjo0fu1vo3s6fhuv1u0gf7fvpjo0fvjro0fs3vu0tvvgg33g42554342h553444g2g24211g121g2221341225h121g252442224465g25g1g2425g273",
            }
        ],
    },
    "kakuro": {
        "name": "Kakuro",
        "category": "num",
        "examples": [
            {
                "url": "https://puzz.link/p?kakuro/15/15/m-dm.ffl-7l9-mQjmIBmbam-anWZs.jSpBjo.7goP4lJ9m..nAjo74lf-.lUUrF9l7-qHNq-clKTrO4l.-clgIoibn.JbmHglfgo.gOo7NpA-.s7Hnb-m-fm-7m-7m-hl-4l.-Dm-Em46BfgJjhSK79acVZD"
            }
        ],
    },
    "kurodoko": {
        "name": "Kurodoko",
        "category": "shade",
        "examples": [{"url": "https://puzz.link/p?kurodoko/10/10/3h2h5h3r3j6h2n5z8n2h3j4r6h2h5h2"}],
    },
    "kurotto": {
        "name": "Kurotto",
        "category": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VXPb5w8EL3vXxH57APm17Lc0jT5Lun2S5MqihCK2A1JUGCdGmgqVvu/Z2ZsFQxU6qVtKlUsM+PnwfPAfrP1lzZTORcO/ryIg4fLFxHdbhTS7ZjrqmjKPD7ix23zKBUEnH88O+P3WVnni8RkpYt9t4q7C979FydMMM5cuAVLeXcR77sPcbfm3SVMMe4Ddq6TXAhP+/Ca5jE60aBwIF7rOITwBsJtobZlfnsOs4D8HyfdFWdY5x09jSGr5NecGR443spqUyCwyRp4mfqxeDYzdXsnn1qTK9ID745HdLGKoev1dDHUdDGaoYtv8YvprtLDAT77JyB8GyfI/XMfRn14Ge+Zt2Sxz1ngaCe088iFxvnahdrpB5Z6tDSjFblIr7JytdOPCxe8Cz6EWRfKrrEsYAmLYPf0YWBegEA4ACIEXGeAQBFAcMsNsoRC+gwYIAL+kOL3iBDAPmHeAAmAur2yCOA1AIKj+R0Kae0+C4iLeA/2huwZWZfsFXxO3nlk35N1yAZkzynnlOw12ROyPtmQcpa4IT+5ZfoL/gY6iaf1b1/B34eli4Rdtuo+2+Ygl3VbbXJ1tJaqykoG/YnVsrytzXxM7QsEBdiOMi2olPK5LHZ2XvGwkyqfnUIwv3uYy99IdTda/SUrSwvQDdmCdN+woEZBUxiMM6Xki4VUWfNoAYMGYq2U7xqbQJPZFLOnbFSt6t/5sGDfGN2Jh38c/5r/H2r+uAXOW+snb40OnV6pZqUP8Iz6AZ1VucEnQgd8ImksOFU1oDPCBnSsbYCm8gZwonDAfiByXHWsc2Q1ljqWmqgdSw0Fn6SLVw==",
            },
            {
                "url": "https://puzz.link/p?kurotto/17/13/7i4i-1ai4iay1i6ibi0y3ibi9i-14iay4i7i-10i4y-11iei6ici3y1ibi7i2y-10i8i0i4i1",  # this example will probably TLE
            },
        ],
    },
    "lits": {
        "name": "LITS",
        "category": "shade",
        "examples": [
            {
                "url": "https://puzz.link/p?lits/24/24/0000000o01lnmg5dvc0dntsq94ia94i814i914i976i94i294i294i8t4i90ci94ki94s294j094ia14i9pki944i94o1mregamtm0rddc00010002002dhm02i14080044vvvk6001os0001vvvq1g00a4000sfvvvsc003p80073fvvq700080000g3vvu100021g0087vvv8114102295g296oo",
            },
        ],
    },
    "magnets": {
        "name": "Magnets",
        "category": "var",
        "examples": [
            {
                "data": "m=edit&p=7VZNb6RGEL3Pr1hx7gPdzfdt49i5OJNs1tFqhUYWtll7ZBgcYLIRlv/7viqqPQNDFEVRNnuIGJrHm+qq6lddQPfbvmhLpX362UThiiPQCZ8mifj05bja9lWZvVFv9/1D0wIo9dPFhfpUVF25ymkmjs3qeUiz4Z0afshyT3vKMzi1t1HDu+x5+DEb1mp4j7882KrhcjQygOcH+IH/J3Q2ktoHXgsG/Ah4u21vq/L6cmR+zvLhSnkU5zueTdCrm99LT/Kg+9umvtkSURf3u7LvhO72d83jXgz15kUNbzlXsV9I2B4SJjgmTGghYVrHv5lwunl5geq/IOXrLKfsfz3A5ADfZ88Y19mzZw1NRWH0WBrPBkTYIyJyajgimU0JeMoREVoiggMRz6MkekZo35/F1X46C6wNRz5mbDyfFc6z0xF7njDzdHTES3jNGOJolugjjxc8Gh6voKAaLI/f8+jzGPJ4yTbnENYEvjIBlmmw7wMNjKCEDdrJYeLDcMRhqEyEJROOYPOKU7QeBCWcWGVSLJlwipZ8xTEwFs44UVaP/q3WRxh9rcd8mDdjXFyVtWMsxgb1ZhwBj/5xVVbWAn/wM+aD66sNxTWp5JymylJBycanuJDX2QvmtSQOB8CiQwIdnJ8Y+jieMO0jxoYeR2KPPCUWaxgKH0KfWPgYtXCxiA8l5xC6xa5GyMfxAfwHojnxtMMJW6qp4AA502ZjP1i75Ib1QZORxxW6CU/YOJ2hjxV94NOKT8ZWdLaoEXUn+6S6yFzCWmqksXYtNdKokZvrU92lvqS/73jSX+wJ+xLXp5o6PZGnLzon0CeRNQI7P2RjEqlRQrUWraguscNUX9EzRl2cPeFYYpFNLHrG0DOWWkfQ2fEh9j+1sNM5dH0Bm0jyibA3qKm5LrQHxAYa4l54rMXZW6qpqzXsA8knwN5gHk38gVv5jMeAx4hbPKZH6N96yP7zp8lfppNjFfLalSP+uvebVe6d392Xb9ZNWxcVXk7rfX1Ttof7s6Z+arptX3r4MPC6prru9u2n4hYvOf5uwKsM3I5nTaiqaZ6q7W5qt73fNW25+BeRJVJZsL9p2ruZ989FVU2I8UtoQo2v6wnVt3gXH90Xbdt8njB10T9MiJuix1dT97B9mnoqd/00gb6Yplg8FrNo9WHNLyvvD4/P3NIX2/9fXf/NVxdVwP/WHgvfWjq8eZt2sfNBLzQ/2MUmF/6kz8GfdDQFPG1qsAt9DXbe2qBOuxvkSYOD+5MeJ6/zNqes5p1OoU6anUId93u+WX0B",
            },
        ],
    },
    "masyu": {
        "name": "Masyu",
        "category": "loop",
        "aliases": ["mashu"],
        "examples": [
            {
                "url": "https://puzz.link/p?masyu/21/15/000a0l2943300030l00200i10j0063c60091000670303010606j3600133013ia16l0110000600306b2063000300020960ai301030"
            }
        ],
    },
    "mines": {
        "name": "Minesweeper",
        "category": "var",
        "aliases": ["minesweeper"],
        "examples": [
            {
                "url": "https://puzz.link/p?mines/8/8/g0l1g1g0g0o1g1i1j45g2m20234g4g1h0g1j",
                "config": {"mine_count": 10},
            },
            {
                "url": "https://puzz.link/p?mines/15/15/h5i3g1g2h5g4i5h44h6i3i43n4g5h4h3g3g3g5h5l5j4g3h5m43i3g4h6h7h3g2g2g3h4j4h30g1g4g32g45p3o1g2g5h5h7g7i5j4m3j3h34g44h4i3g34g3h56j2j3l",
            },
        ],
        "parameters": {"mine_count": {"name": "Mines", "type": "number", "default": ""}},
    },
    "moonsun": {
        "name": "Moon-or-Sun",
        "category": "loop",
        "examples": [
            {
                "url": "http://pzv.jp/p.html?moonsun/15/15/928i4h492940i814g28h2h25248g0h01208g0h01200000000vvv0000003vvs00000fvvg0000vvv0000001800jn33l000f6ig100109inb6i4003a3f00600fclh01i0910032f31ii290003631lk5ai100"
            }
        ],
    },
    "nagare": {
        "name": "Nagareru-Loop",
        "category": "loop",
        "aliases": ["nagareru"],
        "examples": [
            {
                "data": "m=edit&p=7VdNb9tGEL37VwQ888D94OctTuNeXLeJXRgGIRi0zcRCJNOlpCag4f+enZmnSBQnaHtoEaCGxP14Ozv7drRvqF39sWn6NrYJfV0RJ7EJn7ws+ClSw0+Cz8V8vWirV/Hrzfq+60Mjjn89OYk/NItVe1TDanb0NJTV8C4efq7qyEYxnlk8vKuehl+q4SoezsNQFPuAnYaWiWIbmm93zUsep9YbAU0S2mdoh+ZVaDZ9332+Pr4+Fsvfqnq4iCNa6JinUzNadn+2kczj/m23vJkTcNOsw25W9/NHjKw2d92nDWzN7DkeXgvf0y1fWhh83Y4vNYUvtRS+RI743s7720V7fSqO/iHd9u5j+0VjWs6en0PI3weu11VNtH/fNYtd87x6itI8qnwcZYarXHpFKpX0ykSqgiuTiKlJxMgkpdTGSW0tapltLMaduDEO4w72Dn4c7D3sfCY1GJoc83LMyzGeg1eOdQqMF8AL4KWsYxMZt+BtjaxnrezLWtiBv7Xix4Kn9ZjvvdSp8LI5+uBlEUsLXraAHYLrwMMlMs8hns6gb7Z98eOM+HFW+DrwdYi3s/DngPttjfkp5oGvy7BOJnwd4uRKjJcYLzFeyrhPZNwjbt7IOh6/vwdvbyRuHvw84ukRT+/gDzx9in4GvxnmZZiXA89hj3PgEWePY+pL6afglxrhn4JPijimHK+ggrPqKZSGy6ugCPJXm/hbLrlkuUb0M9bpDpYUw+JQrCmImjU5cROYNVXnEy+sIRUnPwpOZ1Rhw9rS7Elrmj39Jvv2W56kyf1tbe3pzGv+SZv7+93iBfmfhoe1qNizJhX/rFENp1yjxNmSNpR9WcpF+3H4hh/43+J0JjX7jPar4JQbNJ7fiRtrXokD5wANp5yg4rRfDafjqeEU52ncOKcovzvnGA2n3KKcK1cQz2k8HWlWwTnXKDw5tyj+OdcofDinKHH2ma5Hzi2aH3qnKOeWc4/Gk945ynlIE/38cE6a+Al56YSzk+XyIry848Fx+ROXCZcpl6ds85bLSy7fcOm5zNgmp9f/3/yDME2Q/xKdOpV/mn/9SV/sXuz+f3azozo63/Qfmts2/Ok/nT+0r866ftksQu/8vnlso3DPilbd4noFq4qvYeFyELCHzfKm7UfQouseF8HNCJx/fOj6Vh0ikO4civ1N198deP/cLBYjQC6WI0iuPyNo3Ye7zV6fM+EIWTbr+xGwd20beWof1mMC62ZMsfnUHKy23O35+Sj6EvETErIJF9OXS+x/f4ml8Cc/2pvqR6PDJ7frVdkHWFF+QFWFA5+IPOATOdOCU0UHVBF1QA91HaCptAM4UXfAviNw8nqocWJ1KHNaaqJ0Wmpf7PXs6Cs=",  # unsolvable now
            }
        ],
    },
    "nanro": {
        "name": "Nanro",
        "category": "num",
        "examples": [
            {
                "url": "https://puzz.link/p?nanro/11/11/9bdcljmcpj6cpj6dpl6mqi46tt8qpltbdmqnljb2nnc4i3g2l23l2n2n2n2n2i3i2n3n3n3n2l43l2g3i",
            },
            {
                "data": "m=edit&p=7Vddjxo3FH3nV0Tz7Ad/jT3DW5pu+pJumyZVFCG0YndJggI76QBNxWr/e861j4GBjVqpilpVFWCfe8Zj33t9rmdY/7ad9XNljHxdo7QCUr4O6WeMTT/Nz+vFZjkfP1FPt5sPXQ+g1E/Pn6t3s+V6Pppw1HR0v2vHu5dq98N4UplKVTb9pmr3cny/+3G8u1C7V7hUKQPuRR5kAS8O8E26LuhZJo0GvgR2+ba3gDeL/mY5v3qRB/48nuxeq0rW+S7dLbBadb/PK/oh9k23ul4IcT3bIJj1h8UnXllvb7uPW4410we1e/p1d93BXYHZXUGn7jKeb+xuO314QNp/gcNX44n4/usBvhrfo71MrRnfV0aHRu7LmYTZJLOmiQ0X0xezTub+ahxctSYcT2UbfWw6m2ZO+RTTp6vlXue9mFBHNts0VblaZzfKuuHoXsTxNkXzPLU2ta8RrNq51H6fWp3aOrUv0pgLRG+9UdZjbgtRegvsiB0wPErYA9fENTBcSzgAR+IIjPgSboBb4lbZGs4KrjWwIca6ksuEsW7gPAHzNOQb8C35NionOQBGr5zNPHrl6D965WryNXjZHMERfEO+icrrzKNX3mTeG9T4HtfAOUZvPHCO3RsHnHPi4QNsYpwR9M0bDZxj9LoFzrF73WDdnBOvxYecK6+xrqZvLebRzG1EfhriJiin85zokYfMo1fOkXfguS/olQvkA/hIPoJvybeIi/641oHPcbkWuWpzXC4ihy1zGMBH+om9hs11wVMDzoB3ZY+wFvPpkOeCLfIPmzFif7kvCUdqL0J7kdqL0F6k9iK0x1jQAxfNyL0FI2/0zQbojXmwNXQYig6hz5r6hE5gE2NO6idpvowRbe/nFK3SzwA/A/0MGB/oZ4CfgX6KzgsOmL+hPw14KfGkbckV90UePJb7ZcHvdQ7sOQY162qOgc8ukodmHDWDHvtbdCj6pJ419Fm01EKfOufEtQ32uuhB9j3nBMcQcNFnDcz5oR/Y3AvkJzKHEbmNzFtEzuUITPFiL8p4mYd1gR4xZh49YiTvwdfka/CRfAS/jxe44ZgG/uwx9NxQzzhDYBNLfqhP+AOb87TAZX7kgf477C/sg/657w7n2x47jOG55wx4R16DN8xJA15TM8C2YX4a5KdlflrJD7WBc8Cy7lJuC0ZtWtYmemBqT/ai1DLOHGcZuwXvyDvwNfkafCgxSuzkg8RVeKnxErucJ9QAtA2bWOZhznHOw+Za4Hn+p/w48gZjCtYYY4rP4j/n0ZifZyB64HKGyLnBfMp5RYwe8TLnVtYij7c3V5PH82WASyyoTdjEordylsIHPrOcBe/om/hvj3jL8VZqlvNYeTYVf4Ad13JyVpdaxnjHGIUvz0R5FrOu01lEnafncjqX8NB+kx7dz1LrUxvSIz2mtinvOV9//9kPOXsV+jsvEn/i2cNoggeFvEyffur/LjsdTapX2/7d7GaOt9SL2/fzJ5ddv5otYV1uV9fzvtj4k1Ctu+XVmqPH6T8E3mrB3aWRA2rZdZ+Wi7vhuMX7u66fP3pJyDmWf2T8ddffnsz+ebZcDoj8r2hA5Zf3AbXp8WZ+ZM/6vvs8YFazzYcBcfQWP5hpfrcZOrCZDV2cfZydrLY6xPwwqv6o0m8idaOM+/8/2D/0H0w2Qf/Vf2Lf8Pj5Nx+MufK7/lD8m35LVYMt5T8gH61y8meFDv6spGW586oG+0hhgz2tbVDn5Q3yrMLBfaXIZdbTOhevTktdljqrdlnquOAn09EX"
            },
        ],
    },
    "ncells": {
        "name": "N Cells",
        "category": "region",
        "aliases": ["fivecells", "fourcells"],
        "examples": [
            {
                "data": "m=edit&p=7VVPb5swFL/nU1Q++4DDnyTcui7ZJcvWNVNVIRQ5CW1QIc4MrBNRvnufH3SxDT3ssKqaJsTj8fPP74/t91z8qLhMKHMoY9QdU/jC47Ex9fyAjlwPX6d9lmmZJeEFvazKnZCgUPplNqP3PCuSQdSy4sGxnoT1Na0/hREZEoovIzGtr8Nj/TmsF7S+gSFCGWBz0BihQ1CnZ/UWx5V21YDMAX3R6qDegbpJ5SZLVvMG+RpG9ZIS5ecDzlYqycXPhDTT8H8j8nWqgDUvIZlilx7akaLaiseq5bL4ROvL18N1z+EqtQlXaX8t3Owg+gKdxKcTLPg3CHUVRirq72d1fFZvwiPIRXgkXvCSY7MrxBspADbpNzBWgKsBE2uK71hTfGYBATK0KYFvMUae5WWMbjUGc4aWEea4HQ6aMTjoSTPMHDtl5tg5M4YcHRliTrod106KuXZWzOvE06yebse3F5j5yNHtNAuoc4JOPEFnfQJzfWDLGW78HcoZyiHKJZwLWrsoP6J0UPoo58iZorxFeYXSQxkgZ6RO1h+dvTcIJ3KbFmY+/r+BxYOITLcPycVCyJxn0A8WVb5O5Ms/tF5SiGxVVPKeb6CRYGeGjgHYHpkGlAlxyNK9yUsf9kImvUMKTMB9D38t5Nay/sSzzACau8aAmpZoQKWEfqf9cynFk4HkvNwZgNbKDUvJvjQDKLkZIn/klrf8nPNpQH4RfCNX3Yn/77U3v9fU4jvvrcO8t3Dw3ArZW/QA99Q9oL313eKdEge8U8zKYbeeAe0paUDtqgaoW9gAdmobsFfKW1m1K1xFZRe5ctWpc+VKL/UoHjwD",
            },
        ],
        "parameters": {"region_size": {"name": "Region Size", "type": "number", "default": 5}},
    },
    "nonogram": {
        "name": "Nonogram",
        "category": "shade",
        "examples": [
            {
                "data": "m=edit&p=7ZRBb5swFMfv+RSVzz5ASBriy9R1zS5dti6ZqgqhyEncBhXizsA6EeW7970HaWLDDjts62EivDx+fvb7Y/iTfy+lUXwERxByj/twBN6AznMPf4djnhSpEmf8oiw22kDC+efJhN/LNFe9KIAKOOPerhqL6oZXH0XEfMZZH06fxby6Ebvqk6imvJrBEOMBsOu6qA/p1TG9pXHMLmvoe5BPmxzSO0hXiVmlanFdky8iquacYZ/3NBtTlukfijU68Hqls2WCYCkLuJl8kzw1I3m51o9lU+vHe15d1HJnB7nYpZGLyhu5mNZyMeuQi3fxh+WO4/0etv0rCF6ICLV/O6bhMZ2JHcSp2LEgxKnvQEv9bFgwdsDAc4F/2JwDcKcM3SlDd8qwjwBeiFfg6hi6i47cRUMCJ4uGbpcxgZMpY2r7CmAPfNqJO4oTin2Kc9goXgUUP1D0KA4pXlPNFcVbipcUBxTPqWaEW/1bD+MvyInAxehrn4fd/3EvYrPS3MuVghdsWmZLZc6m2mQyZeBolut0kTfjggwPryCwLVVaKNX6KU22dl3ysNVGdQ4hVOuHrvqlNmtn9WeZphaoP18Wqp1mocKAjU6upTH62SKZLDYWOLGctZLaFraAQtoS5aN0umXHe9732E9GJ3wwfT74/7n8R59LfATeW/PpW5NDb682ndYH3OF+oJ0ub3jL6MBblsaGbVcD7TA2UNfbgNr2BthyOLBfmBxXdX2OqlyrY6uW27HVqeGjuPcC",
            },
            {
                "url": "https://puzz.link/p?nonogram/31/13/m513j1111i531q55k11111h5111p55k111j131q55k11k55k11k135j1l55k111j55r35k311j35r51k115j51zn3353133o11111111111k131113133m11111111111k11111111333zg3113313311l111111111111111g3331111133l111112121111j11111111111111x",
            },
        ],
    },
    "norinori": {
        "name": "Norinori",
        "category": "shade",
        "examples": [
            {
                "url": "http://pzv.jp/p.html?norinori/20/10/ahkcfeorctdhkqdffmk9jprqnqd57ea6us16ok4jboec2oku7ck43rbqseje3kc16cvv8f7i7f",
            }
        ],
    },
    "norinuri": {
        "name": "Norinuri",
        "category": "shade",
        "examples": [
            {
                "url": "https://puzz.link/p?nuribou/10/10/g6p8l.n-14zzhan4lap.g",  # hack nuribou as norinuri
            }
        ],
    },
    "numlin": {
        "name": "Numberlink",
        "category": "loop",
        "aliases": ["numberlink"],
        "examples": [
            {
                "data": "m=edit&p=7ZTPb5swFMfv+Ssqn33gR9Kl3NK02yVj65qpqhCKnMRtUCHuDKyVo/zvfe9BBwYmbZq09TA5eXp8/Gx/jf0l/1YKLfkEmj/lDnehed6U/mMHf69tmRSpDE74rCx2SkPC+aeQ34k0l6OoLopHB3MWmCtuPgQRcxlnHvxdFnNzFRzMx8CE3FxDF+MusEVV5EF62aQ31I/ZvIKuA3lY55DeQrpJ9CaVq0VFPgeRWXKG65zTaExZpr5LVuvA543K1gmCtShgL/kueax78nKrHsq61o2P3MxIbj1kQLPfaMa00ozZgGbcyh9rTpO9fB6SexYfj/Dav4DgVRCh9q9NOm3S6+AAMQwOzHNx6AxkVGfDfAfBeQt4CC5a4AzBvAFjGtKqmBBoVUxoldakp1TxY1kQ45KkW4rvKXoUl6CYG5/iBUWH4oTigmouKd5QnFMcUzylmne45996K39BTuRV/sI2+bUsHkVsASd/EiqdiRTOPyyztdSvz2A4lqt0lZf6Tmzg5pAf4YYA21OlhVKlHvEiWTC53ystB7sQyu39UP1a6W1n9ieRphaoPi4WqjxgoULDBW89C63Vk0UyUews0DKwNZPcF7aAQtgSxYPorJY1ez6O2DOjf+TDyx///5r9o68ZHoHz1tz71uTQ7VV60PqAB9wPdNDlNe8ZHXjP0rhg39VAB4wNtOttQH17A+w5HNhPTI6zdn2OqrpWx6V6bsel2oaP4tEL",
                "config": {"visit_all": False, "no_2x2": False},
            },
            {
                "url": "https://puzz.link/p?numlin/26/26/zz-15gdx-12nfs-16j8x4v-11zxes9kfs8zg4lbm6k5ubv2r-14n1q-10z5v7zeq3n3r1v-13u9k-11mdl6zgas2k-10sczxav-16x7jcs-15n-13x-14g-12zz",
            },
        ],
        "parameters": {
            "visit_all": {"name": "Visit all cells", "type": "checkbox", "default": True},
            "no_2x2": {"name": "No 2x2 path", "type": "checkbox", "default": True},
        },
    },
    "nuribou": {
        "name": "Nuribou",
        "category": "shade",
        "examples": [
            {"url": "https://puzz.link/p?nuribou/13/13/1j.l1g3o3m7zi2i2v4h.m.h3v2i2zi.m3o3g1l4j1"},
            {"url": "https://puzz.link/p?nuribou/20/15/h5o6zs6k3i3h6zg4p4zi.pbzl7h3zz4k4l9v7zn4h.l4k4o4q7i2"},
        ],
    },
    "nurikabe": {
        "name": "Nurikabe",
        "category": "shade",
        "examples": [{"url": "https://puzz.link/p?nurikabe/19/12/g5zw3k2h4g4k.v.h2i2g4z3n7j3k2h4h4k3i4j3zzk2i2k2p6j2k6k"}],
    },
    "nurimisaki": {
        "name": "Nurimisaki",
        "category": "shade",
        "examples": [
            {
                "url": "https://puzz.link/p?nurimisaki/15/15/v.h.h.h.h.zr.j.h.i.zk.l.q.m.j.l.r.i.i.i.zr.h.h.h.h.v",
            },
            {
                "url": "https://puzz.link/p?nurimisaki/22/15/j.zj3j.h.v.n.g..k3q4z4l.l2w3n4h.u5g3o3k.m.h.g4u.p.k3h.j.p3n.i3k.t.u4o.h3h.g3r4",
            },
        ],
    },
    "nuriuzu": {
        "name": "Nuri-uzu",
        "category": "shade",
        "examples": [
            {
                "url": "https://pzprxs.vercel.app/p?tentaisho/15/15/znezzqezu6esezzzoezzzzzqereztcel0ezzkezzweztezzzzjezzezzzueu",  # hack tentaisho as nuriuzu
            },
        ],
    },
    "onsen": {
        "name": "Onsen-Meguri",
        "category": "loop",
        "examples": [
            {
                "url": "http://pzv.jp/p.html?onsen/10/10/akkh92j6mt9pjvfti91svv1vvovv3g3f04ti3m2n1j1x1zq2v3n3",
            },
            {
                "url": "https://puzz.link/p?onsen/15/15/9018m2kqm9jbr3a9f853qcfj996k6esa8alac2v892cvv0sj4086g5lb4a6qqeh7q2404c5nvq8cvi30m098zzzzzzj.u..zzzzi",
            },
        ],
    },
    "ripple": {
        "name": "Ripple Effect",
        "category": "num",
        "aliases": ["rippleeffect"],
        "examples": [
            {
                "url": "https://puzz.link/p?ripple/13/13/i2aonbatddnfdjqt6qafrlvfl9egl450fvjbt3t9lfu2072jfj8pvgojecbvcvu0zzzzzzzzo",
            },
            {
                "url": "https://puzz.link/p?ripple/10/10/2gpr9dbqk5bqmcr9186cbi7sg3fuk1bsa26s....h......g1j...n..n.z.n..n...j6g......h..../",
            },
        ],
    },
    "shakashaka": {
        "name": "Shakashaka",
        "category": "var",
        "examples": [
            {
                "url": "https://puzz.link/p?shakashaka/30/30/kcodzzzgchbjbgbgbgbzzzobmcclbhblbobr.zkbncczzpbobgbgbscvczzu.lbgbgbobzgddkcsbzzndibiddbjbkcw.ztbzpbhbgbgbgb.zwbzgczzhegdobycgdlbhdx",
            }
        ],
    },
    "shikaku": {
        "name": "Shikaku",
        "category": "region",
        "examples": [
            {
                "url": "https://puzz.link/p?shikaku/24/14/h5x6i.j8g6lag4j.l9i8j6i4l3z9g6i4i4h56h6i4i6j8h4n3h6zn4j4r6j4g6j8i8hci6j8q6h2r8k5l8k8j.l9j4l.lataock36kck",
            }
        ],
    },
    "shimaguni": {
        "name": "Shimaguni",
        "category": "shade",
        "aliases": ["islands"],
        "examples": [
            {
                "url": "https://puzz.link/p?shimaguni/15/12/55a19a6l11nhcnqlddnqkr5cmajmaoeahc3gqv3nftavvke414681sk3e7cekml25fok2o43g1s",
            }
        ],
    },
    "simpleloop": {
        "name": "Simple Loop",
        "category": "loop",
        "examples": [
            {
                "url": "https://puzz.link/p?simpleloop/20/20/124000044004i000200120018l001000000200000084000080220000o00g000080020h224008400p",
            }
        ],
    },
    "skyscrapers": {
        "name": "Skyscrapers",
        "category": "num",
        "examples": [{"url": "https://puzz.link/p?skyscrapers/9/9/g4g7g5g5i4g5g7i3g2g8g6i7g8g2h"}],
    },
    "slitherlink": {
        "name": "Slitherlink",
        "category": "loop",
        "aliases": ["slither"],
        "examples": [
            {
                "data": "m=edit&p=7VZRT9swEH7vr0B+9oPtJG2SN8bKXlg3BhNCUYXSEqAirZmbDJSq/53zJR32pbCHadOkTWlOly93n8/nfHbX3+rcFDyBK4y44BKuMBJ4x6H9ie46X1RlkR7ww7q60wYczj8dH/ObvFwXg6yLmg42TZI2p7z5kGYsYJxJuBWb8uY03TQf02bCmzN4xbgE7AQ8CAjAHbeuAvcC31vwqI0U4E7a9zbrEtz5wszL4uqkzficZs05Z3aYd5hiXbbU3wvWpuHzXC9nCwvM8grmsr5bPHRv1vW1vq+7WDnd8uawrXb8drXWfataW9svV1tc3xZP+wpNptst9PsLlHqVZrbqry/uWboBO0k3TMU2HtZC2tUAEpXsZtoBgbTAGePxDggoENGUIQFC5FAOoCxwYRuyQ5DVzRlRAEv1crBWp/iIVhJhJW4EsrokEdI6tUXI6oYMBQkZ0vkMkdbpybBHMqIkI+yBC2ALvBycj0MbY44zwTikEXTGCV2uBEndYRK6Xgn2xAV605GCfhdS0BWTgn5dUvSJJDZGOEESqf0g2iwpcV4egtwuopDaI1J06aSiH41U2A8/rTe3oFdRKwwPoesnA/qhyIAKToZ+Q0CpEvV6ifYYrUJ7DnLmTYD2PVqBNkJ7gjFjtBdoj9CGaIcYM0Ib77aG17eMHyHO7vHbK9sOMhXjseNe0d+FTAcZG8M2fDDRZpmXsBlP6uWsMLtnOPbYWpdX69rc5HPYxvFUhO0asBVGelCp9UO5WPlxi9uVNsXeVxa0pwBLK1N74TNtrgn5Y16WHtAe8R7UnkceVBk4bJzn3Bj96CHLvLrzAOcY9ZiKVeUXUOV+ifl9TkZbvkx5O2BPDO9McRXByfr/P8Uf/k9hmy9+/s/in961WsFrs1fzAO+RPaB75d3hrcJ9vCdmO2Bfz4DukTSgVNUA9YUNYE/bgL0ib8tKFW6roiK3Q/V0bodypZ5NB88=",
            },
            {
                "url": "http://pzv.jp/p.html?slither/25/15/i5di5di6bg3ad13dc13bd3cg5bi7ci7dhai6bi6ci7b02bd33cc23d8ci8ai6cibh6di6bi7dg1ca31ab10dc3dg6bi6ai6chai7ci7ci8d33dc33cc20d8bi7di7cidh8di5ci6cg3dd03cb02ad3dg6bi7ci6bg",
            },
        ],
    },
    "starbattle": {
        "name": "Star Battle",
        "category": "var",
        "examples": [
            {
                "url": "https://puzz.link/p?starbattle/15/15/3/31g94h1gk30glmiuum28c52kl8mh0i10o51gh4i1go2h84a4802gt5hah8la6046hc9aign1ga18424a42h8",
                "config": {"stars": 3},
            }
        ],
        "parameters": {"stars": {"name": "Stars", "type": "number", "default": 2}},
    },
    "statuepark": {
        "name": "Statue Park",
        "category": "var",
        "examples": [
            {
                "data": "m=edit&p=7ZZPb5tMEIfv/hTVnvewy/LHcEvzJr0kaVOniiKEIuyQGAV7U8DNKyx/98wMVA7e6aVV1RwizGj4MZ55jGd2ab5v8rqQ2sOPmUolNRx+7NNpooBONRxXZVsVyQd5tGmXtgZHys+np/I+r5pikg5R2WTbxUl3KbtPSSq0kMKDU4tMdpfJtjtPxMKu5qWQ3QzuCzmFG2d9pAfuyd69pvvoHfeiVuBfDD64N+AuynpRFbdnvfIlSbsrKbDYR/o2umJlfxRigMHrHgCEefW8HLRmc2cfN0OUznayOyLabvYTFPMPoGYPim4Pih4Divx/Dpq38OibZfnE4cbZbgdP/SsA3yYpsn/bu9O9O0u2YC/IarI3yVaYANJoKNYDnhOyMBGrTkH1HDXmYn3NqoZVfS6vz5IFmNeJDVnekOWNWLKIJYtYsoitFrPPQSu2nFZsPa3Yglqxz0IrFkQrnkRjtJvb8ICGBzQ8IN9Gmu8jzbeM5ntGB0jilgx5wJAH5DtEhzxJpNgkfJPoCJO40TH/TGKeJGabVfNd5fFd5fFd5XHtA/N/SquAR/YKFgnZGbL/kVVkA7JnFHNC9prsMVmfbEgxES4zv70Q/SWc1Pi0qblH8K7jkU1SMdvU9/migM3l2K6ebFO2hYCNXDS2um2Gewnt87D1gLberOZFPZIqa5+qcj2OKx/Wti7YWygWdw9c/NzWdwfZn/OqGgn9m8tI6nt7JLU1bJ+vrvO6ts8jZZW3y5HwaqsdZSrW7RigzceI+WN+UG21/827ifhf0JkafMN6f0v6N29J+A+ot7ZEvTUcal5bs5MPMjP8oLJDPujOnIPuTDQWdIcaVGauQT0cbZDc6QbRGXDQfjHjmPVwzJHqcNKxlDPsWOr1vKfZ5AU=",
                "config": {"shapeset": "pento"},
            }
        ],
        "parameters": {
            "shapeset": {
                "name": "Shape Set",
                "type": "select",
                "default": {"tetro": "Tetrominoes", "pento": "Pentominoes", "double_tetro": "Double Tetrominoes"},
            }
        },
    },
    "stostone": {
        "name": "Stostone",
        "category": "shade",
        "examples": [{"url": "https://puzz.link/p?stostone/11/10/4c5d8ltltlvkv2sktihi30js7o01g614fkvootg0l5t"}],
    },
    "sudoku": {
        "name": "Sudoku",
        "category": "num",
        "examples": [
            {
                "url": "https://puzz.link/p?sudoku/9/9/k13m27h476h39h825zg841h29h538h18m96k",
            },
            {
                "url": "https://puzz.link/p?sudoku/9/9/i1i6g29j47h3i2k76j5o5j87k7i5h59j18g8i9i",
                "config": {"diagonal": True},
            },
            {
                "url": "https://puzz.link/p?sudoku/9/9/i2i1i3i2i4i3zs6i5i7i6i8i7i",
                "config": {"untouch": True, "antiknight": True},
            },
        ],
        "parameters": {
            "diagonal": {"name": "Diagonal", "type": "checkbox", "default": False},
            "untouch": {"name": "Untouch", "type": "checkbox", "default": False},
            "antiknight": {"name": "Antiknight", "type": "checkbox", "default": False},
        },
    },
    "tapa": {
        "name": "Tapa",
        "category": "shade",
        "examples": [
            {
                "url": "https://puzz.link/p?tapa/21/14/j.g2zk3h3maltblhc4kaehc1zhalhblo2talh3kakhaeziadgajpc1j.m3g1g3qaer4g2majh1gadq2q.g3s1n.ha7j3l3g1",
            }
        ],
    },
    "tasquare": {
        "name": "Tasquare",
        "category": "shade",
        "examples": [
            {
                "url": "https://puzz.link/p?tasquare/21/15/g.k..k4k.x.h.i8j2q.u4i2l2jar.2l.h.zhak8i8h9j2.x1m.n2g.h.l.j2h3g1k2g4r.o1i3h.i.j.l1zj2g4i..g.i.h./",
            }
        ],
    },
    "tatamibari": {
        "name": "Tatamibari",
        "category": "region",
        "examples": [
            {
                "data": "m=edit&p=7VTBbptAEL37K6K9diuxYLuYS5Wmdi+u2zSuogihaG2TGAW86QJNhet/z8xA612ghx7a+lCtGT0eszOPxW/yL6XUMZ/A8nzucAHL8x26/CH+nGYtkyKNgzN+XhZbpQFw/mE243cyzeNB2GRFg301CapLXr0LQuYyTpdgEa8ug331PqgWvLqCR4wL4OaABOMuwOkRXtNzRBc1KRzAiwYDvAG4TvQ6jW/nNfMxCKslZ9jnDe1GyDL1NWb1Nrpfq2yVILGSBbxMvk0emyd5uVEPZZMrogOvzmu50x653lEuwlouoj8lN97cx3m56tM6iQ4HOPNPoPY2CFH45yP0j/Aq2ENcBHvm+rj1OwipPwzzHCReGoSLxGuDGCLxwiDGrRqjdsaYahgZPnUxivrtLT4JMzKEQ22MFCHam0Qt1mIox2gtarlmZa99CGJI+n7WgcMSdGQ3FGcUXYpLOFFeeRTfUnQojijOKWdK8ZriBcUhxTHlvMJv8ltf7S/ICV2f3G+u0Wkx0SBkU/DC2ULpTKbgh0WZrWL94x6mD8tVepuX+k6uwUs0nMAxwO0o06JSpR7TZGfnJfc7pePeR0iiFXvyV0pvWtWfZJpaRD1qLaqeChZVaLC8cS+1Vk8Wk8liaxHGNLMqxbvCFlBIW6J8kK1u2fGdDwP2jdEVenD4w/+j/V+Mdjx/59RGxanJob+u0r2+B7rH+sD2WrzhOy4HvuNnbNi1NLA9rga2bWygut4GsmNv4H7hcKzaNjmqavscW3Wsjq1Mt4fR4Bk=",
            }
        ],
    },
    "tentaisho": {
        "name": "Tentaisho",
        "category": "region",
        "aliases": ["spiralgalaxies"],
        "examples": [
            {
                "data": "m=edit&p=7VZbb5tMEH33r4j2eR9Ylpt5S9O0L6nT1KkiC1nW2iGxFex1uTQVlv97Zmb55ACLWqnq5ZMqzMxwGGbPDstZF18qladcOPiTEQcPhyciOt0ooNNpjttNmaXxGT+vyrXOIeD8esIfVFako6RJmo8O9Tiub3j9Pk6Yyzidgs15fRMf6g9xPeP1FG4x7gF2BZFg3IXw8hTe0X2MLgwoHIgnTQzhDMLVJl9l6WI6NdDHOKlvOcOB3tDjGLKt/poy8xxdr/R2uUFgqUqYTLHe7Js7RXWvn6omV8yPvD7v8MVRGr7yxBdDwxcjC1+cxs/zTe8f06Ja2siO58cjdP0T0F3ECTL/fAqjUziNDywQLPY4C1zjpHEeubBxY3JRRG5sUoRjnhBOaLwIGm+yhWsKC/mfb/Jl87w0xYWH+UBmEh/ACrIzICYBTwRM+NQlaBzzoYwFDhyA3T7sW+EIOFmKRDhkP1tIexUhYco23Ee8X15gd235Edbv50vPPleJ78WCe+4ATjwteIT5fT6+O9D6gT74A132Q3ubAxfnZXlZA/0MBuYbhLAibXhk71vo2HmGApawDQ/xfXXrwPJ8R4vUJXsLnxKvJdm3ZB2yPtkryrkke0f2gqxHNqCcED/GH/xc+9/JL6KTSKP87cP//2HzUcKmVf6gVilI5SWI5tlE51uVwdV0rfYpgw2KFTpbFE1WTPsXSCpgu2q7TPMWlGm9zza7dt7mcafz1HoLQdRqS/5S5/ed6s8qy1qA2ZBbkFmOLajMYU94da3yXD+3kK0q1y3g1X7XqpTuyjaBUrUpqifVGW17mvNxxL4xOhOJfxz+7f5/ZvfHN+D8baLyHToJ9FaEgtfXnO2rhVqsNHyl0LqhG7+dP612nVulAmCLWgBqVYUG7wkD4D0JwAH7KgCoRQgA7WoBQH05ALCnCIANiAJW7eoCsupKAw7VUwcc6rVAJPPRCw==",
            },
            {
                "url": "https://puzz.link/p?tentaisho/19/22/hafheneweo2ffneneyerfgezy0eg4fifhafnezgfnfmegepel3epfzzt6989ezq7ehfehfwfnezk2dezq4b88fzveweofznfhefezzu54ffzzmedb4b3ezuejflexezg4fl7ezel72eregfztflefzzheifhbeztewen9ekejemer6eret8fpe",
            },
        ],
    },
    "tents": {
        "name": "Tents",
        "category": "var",
        "examples": [{"url": "https://puzz.link/p?tents/13/13/23g3g1i333g2j2g2j3i1517617151695114b322hi33g00100100e"}],
    },
    "tapaloop": {
        "name": "Tapa-Like Loop",
        "category": "loop",
        "aliases": ["tapalikeloop", "tapa-like-loop", "tapalike", "tapa-like"],
        "examples": [
            {
                "url": "https://puzz.link/p?tapaloop/16/16/y+72zg+5qrb0q+10n+10h+6wl-g8ha0zvb0j-10m-g8q-g8k-10zo+10ha0ka0i-g8q+10n+10zna0l",
                "config": {"visit_all": True},
            },
            {
                "url": "https://puzz.link/p?tapaloop/17/17/g2h3h2yarhajh2x4h2haiyaihaih3xabhajh+2lyaihaih2w3h3h2y3haihabx2hajhaiyajhaihajx2hajhajy2h2h3g",  # a bit slow example
            },
        ],
        "parameters": {
            "visit_all": {"name": "Visit all cells", "type": "checkbox", "default": False},
        },
    },
    "yajilin": {
        "name": "Yajilin",
        "category": "loop",
        "aliases": ["yajirin"],
        "examples": [
            {"url": "https://puzz.link/p?yajilin/10/10/0.p31g23l21g33f42g42l13g12p0./"},
            {"url": "https://puzz.link/p?yajilin/19/13/g24g33f45o23d30g32z43k41y11a11a42zo33a14a12b11d31a32c21e11t36g31e21y"},
        ],
    },
    "yajikazu": {
        "name": "Yajisan-Kazusan",
        "category": "shade",
        "aliases": ["yk", "yajisan-kazusan"],
        "examples": [
            {
                "url": "https://puzz.link/p?yajikazu/14/9/d24b42c3140i4223g32a44c23i23a41a40a22c12d2243f222221b22b22a22a2222b44n12e42d12f43f",
            }
        ],
    },
    "yinyang": {
        "name": "Yin-Yang",
        "category": "shade",
        "examples": [
            {
                "url": "https://puzz.link/p?yinyang/11/11/02000620ik00i0i00i8kiq030061206j002100600",
            },
            {
                "url": "https://puzz.link/p?yinyang/22/18/00000000000000030190030000900003000000900130020006000l0000090000i0020009400030200060000002empf01900001009901030130900031009a00009000",  # this example will TLE
            },
        ],
    },
}

# pylint: skip-file
