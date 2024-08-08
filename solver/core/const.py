"""Constant definitions for the site."""

from typing import Any, Dict

CATEGORIES: Dict[str, str] = {
    "shade": "Shading",
    "loop": "Loop / Path",
    "region": "Region division",
    "num": "Number",
    "var": "Variety",
    "draw": "Drawing",
}


PUZZLE_TYPES: Dict[str, Dict[str, Any]] = {
    "aqre": {
        "name": "Aqre",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VZdb9pKEH3nV0R+3gfvro0/3tKU9CWlNyVVFFkoMsRJUAxODdxURvz3nNkdxza4urq6qporVcD6+Hh25szsjpf1921aZkK69NWhwBUfT4bmp8Kh+bn8uVps8iw+EafbzWNRAgjx5fxc3Kf5OhskbDUd7Koori5F9SlOHOkIR+EnnamoLuNd9TmuRqKa4JEjJLgLa6QARw28Ns8JnVlSusBjxoA3gPNFOc+z2wvL/BUn1ZVwKM4HM5ugsyz+zhzWQffzYjlbEDFLN0hm/bh45ifr7V3xtGVbOd2L6tTKnfTI1Y1cglYuoR65lMUvlhtN93uU/SsE38YJaf/WwLCBk3iHcRzvHO3S1BBa7No42idCt4iwrgUTviZi2BCBIsJriMhYYLlrQkrvwETaOC0v0jeB3mZBoDQyb8x4bkZlxitkISptxo9mdM3om/HC2IyQnPK1UD5CK2w+3wNGUIN94KHFnmqwwl73kA1hCXsFSYQj2EdsE6EXooBxAMw2IexrHLjolzou7ANUGVjrQGiqJ2HldbGy2rSUXSxZTxS+Ya0joWkZauyxfw/N60nGmMu54Ap7q1+rYWNPWNlctNRvWEXwKa1/g122d+Hftf5ViFxaWIV1HaDT5bgu4kqOKxGLdpvRTDptfXCFNq4D2chaD/zLmqfcI64t6lzHIhzwmgZYo4DXKKCacy5DrEXAa0F4yJo9aG5jj31q+Gxj2qhmP8An68cVmOdqCcxrpLGXNNdNRg2mvRHWOmHfxtQ9BmNuwPY+5tbYo73KuRP2OEeKZTA2+7XZ8mdm9Mw4NK0QULv/qxfCf++6f5SToHp0unQ//v+Pmw4SZ7It79N5hpfx6O4hOxkX5TLNcTfeLmdZWd/jLHTWRX67ZuvYHJV4eYNbGcsOlRfFc75Yde0WD6uizHofEZkhfI/9rCjvDry/pHneIezh36HsGdWhNiUOoNZ9WpbFS4dZppvHDtE6rDqestWmK2CTdiWmT+lBtGWT837g/HDML9H0J+XPH43f9EeDlsB9b2+X9ybH7N6i7G190D3dD7a3y5k/anTwRy1NAY+7GmxPY4M97G1Qx+0N8qjDwf2kycnrYZ+TqsNWp1BH3U6h2g2fTAev",
            },
            {
                "data": "m=edit&p=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",
            },
        ],
    },
    "aquarium": {
        "name": "Aquarium",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VZPb+O2E73nUyx05kEk9YfSbbtNeknTbpNisTCMQEm0G2PtaCvb3R8U5Lvvm+HQomQXPxRF0S1Q2Kaen98MZ8gZmtvf9k3fKq3pbZ1KFZDK8oI/Whv+pPK6We3Wbf1Kvd7vHrseQKmfLi7Uh2a9bc8Wmq3T5dnzUNXDWzX8UC8SnajE4KOTpRre1s/Dj/VwroZr/JQoDe7Siwzg+Qjf8e+E3nhSp8BXggHfA96v+vt1e3vpmZ/rxXCjEprnO7YmmGy639tE4qDv993mbkXEXbNDMtvH1Wf5Zbt/6D7tRauXL2p47cO9PhGuHcMl6MMldCJcyuJvDrdavrxg2X9BwLf1gmL/dYRuhNf1M8ar+jmxlkwzxOL3JrEZETYi8rmimBPl3MQRkUdENSOylIgqIvRcYYgoI2I+S8GKKI6SFaiyQFSsiJzqdC7RZu5F+3Riq5w1LmIK1kTRaceaQ0ZYXs2L/J7HCx4NjzfYAzVYHr/nMeUx5/GSNefYGuNKZRyW0qB1nAPGKhIusykusUOEi3TErlKmwiITrlJlU8/jCYwNZB6tHnBZQI89YJzDj/CFAUayzCMeWlK2NbD1PJ7AEmdlR1wi5gr1FWzLoIHPAw9NKbkUlEvIi+JHKbIefBXyQo4BF4jThRyBK4nZ6REXyMtJXhXlKLlAb7W3xRPYa/AEDjlmyMXHg6eyxseDJ7Csp4Ef4+di24BNoSzVNOEMPJVzsKVuIGzhkxqBNYjhoAfOxX8O/7n4xElsc1nzHH4K8VPAj5PYHHgntg62TmwdbF1kG/svJYYS8wZbmquUeEr6Sxj9ZKnn8VSZDnwO3vvBE3yIAXNVEmflJjjTvgYy/LMEbCvUUuXrxDrUmOwXYycahxoL+WJPDxraU9l3izrB9xFLDeAJLHsBfRZqgPY66KmGpfYs1bnUqkUv2CJgaArRoG6t1K1FPU9wsNXIS0teKWwFU1/ju9QD/NN5zBiaTPQZNFmoGcwVYzqdua6QY8CaalXySqHRoYapniO9kTVJsYYBG6wPHfDsn+pN+JxqMsKF+EEP2kL06LXDOhOmQ5Ixci8kl5zWLcK5rGGO3POQO/R05HI8tCbROUPHNWOsiRG9gZ/Qm7i7jP0FzD5xoL7jY/UNjxmPBR+3Jf0h/qm/zL9+sv/fcBbYcbp/TV+4h/3buOXZIrne9x+a+xbXlfOHj+2rq67fNGt8u9pv7to+fMdtMdl269utqGu+TOJ6A+6JlRNq3XWf16unqW718anr25M/Edli+hP6u65/mHn/0qzXE8JfjyeUv8VNqF2PK1r0ven77suE2TS7xwkRXecmntqn3TSAXTMNsfnUzGbbjDm/nCX/S/izsHSN/+8q/g9dxWkL0m/tdPnWwuHq7fqTrQ/6RPeDPdnlwh81OvijlqYJj7sa7InGBjvvbVDH7Q3yqMPB/UGTk9d5n1NU81anqY66naaKG36xPPsK",
            },
            {
                "data": "m=edit&p=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",
            },
        ],
    },
    "balance": {"name": "Balance Loop", "cat": "loop", "aliases": ["balanceloop"], "examples": []},
    "battleship": {"name": "Battleship", "cat": "var", "examples": []},
    "binairo": {
        "name": "Binairo",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VjNT/tGEL3nr6j2vAfvh+OPG6XQC9BSqBCyIuQEQyKcmNpOqRzlf2d2HCk4+6JKSD8VqSjxaPI8mX27M2/jTfPXOq8LqQP3NrEMpKJXlMR8xaHiK9i9bhdtWaQ/yZN1O69qcqT87fxcPuVlU4yyXdRktOmStLuW3a9pJpSQQtOlxER21+mmu0zFrFpOF0J2N3RfSEU3LvpITe7Z3r3j+8477UEVkH+188m9J7ctVm3Tf/w9zbpbKdxIP/NXnSuW1d+F2DFxn/vRCZiWb/Md1qwfq5f1LkpNtrI7YardDWBp9iyd27N0HmDpyDuWs0U9K4uHi88RzVta92a+eEV0k8l2S0v+BxF+SDPH/c+9G+/dm3RD9oqtYnufbsQ4ojSaBusJXjJlMU4IVYdoFKLYKIaxMEOsUYbYwljHzEMTl9fLoAKFYZcZwHDSKoCclXK5AWwwjHNrN3M/2gQw2sC5K4MJWjykdYXx4RAPGeKlCscYxrnHsL5qjHNHLrc/HW4dPzrBSRLXlF4SzQ0B4CPRsIc1bgiNK681XFitj0TDomkNF1YbPB0LlaO5IQCMp4MbQoewDDpy0X4S3hsAjJnEeMgYJ0ng5E0AF9awuH1YwWYzuGgGy9Vw0QAMi2Zw0Qyr2I+2UDuGSwxgWEuD5WoiuD0aFqAPx0dgKBITYyYJTGIDuLAW19JiuVosQItraTWcvNWwIayBtbS4OtY6JgDGubEuLd5M7Ri2j8WbqY0wwQgvFZarxQ1h8c+2jfHkcftYVrEHh3jrDflnFMCw2UIuMYAhwVCDydPj0Dk/FGm2t/TMJDvD9he2AduQ7QXHnLG9Y3vK1rIdc0zknro+/Vz2g+hkYf+A/++v8DvuO+7/FzcZZeK0Wr5WzaItBB1lRVOVD826fspndDjjky6dvwhbrZfToh5AZVW9lovVMG7xvKrqAt5yYPH4jOKnVf14kP0tL8sB0J/dB1C/ow2gtqYz5IfPeV1XbwNkmbfzAfDhvDnIRCftIYE2H1LMX/KD0Zb7OW9H4h/BV2Zoqe33/wT/wf8EbvmDr/ar9NXocOdWNZQ9wUD5hEKF73BP5IR7cnYD+oomFIia0ENdE+RLm0BP3YQdEbjLeqhxx+pQ5m4oT+luqI9izyajdw==",
            },
        ],
    },
    "box": {
        "name": "Box",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7ZVNc5s+EMbv/hQZnXVAvBm4pWnSS+o2f6eTyTBMBjskYQJWKuPmP3j83bO7giBeeuihrQ8dzM76xyPpEdKK7fddqjIuBP6cgFscMu56Pt1C2HRbzXWdV0UWnfDTXfUkFSScf7m44A9psc1mMbaEK5nt6zCqr3j9KYqZYJzZcAuW8Poq2tefo3rB6yU8YtwBdqlFNqTnXXpDzzE701BYkC+aHNJbSNe5WhfZ3aUmX6O4vuYMx/lArTFlpfyRscYH/l/LcpUjWKUVTGb7lL80T7a7e/m8a7QiOfD6VNtdtnZxlMYuOm/sYqrtYjZhF2fxm+2GyeEAr/0/MHwXxej9W5cGXbqM9hAX0Z45DjX1wIxeHOa4SGzHIB4SxzKIP9LMRyQgYvYcDjWuNSKCiG8Q6lngy2yIpwnjfgN8m4DbSeZEYMO1krluY7gJiMDQrSTUvUCjViIsQtBvqxHWyI0QhKDnd5FNzYw5CKcl7xr9wuBFdiI907kh8qhZT6TnGhgif9yTnm1oiAK9zibR62wSvc4moXU256/fmjnZgNbZnFpA62zOI6R1Nk2HtM7vDmE3CtqTtxQvKNoUr2HL8tqh+JGiRdGjeEmac4o3FM8ouhR90sxx0/9SWfwBO7Eb6HPSuObHRZJZzJY79ZCuMzhsFrtylamThVRlWjA43dlWFnfb5nlEhz8cR8A2pOyhQsqXIt/0dfnjRqps8hHC7P5xSr+S6n7Q+2taFD2gP2c9pE/dHqoUHKnG/1Qp+dojZVo99YBx/PZ6yjZV30CV9i2mz+lgtLKb82HG/md0xw5+dv99Ov/SpxOXwDq2k+LY7NDulWqy9AFPVD/QySpv+KjQgY9KGgccVzXQicIGOqxtQOPyBjiqcGA/KXLsdVjn6GpY6jjUqNpxKLPg42T2Bg==",
            },
        ],
    },
    "canal": {
        "name": "Canal View",
        "cat": "shade",
        "aliases": ["canalview"],
        "examples": [
            {
                "data": "m=edit&p=7ZVBc5s6EMfv/hQZnXVAEsSYW5omvbhuU+dNJsMwGeyQhAlYeTJuOnj83bO7kCIEPfTQNoeMzM76p9XqD2KX7f+71GRcSPypkHtcwPBnPl1qGtDlteMyr4osOuInu+pBG3A4/3J+zu/SYptN4jYqmezrWVRf8PpTFDPBOJNwCZbw+iLa15+jesHrJUwxroDNmyAJ7lnnXtE8eqcNFB74i9YH9xrcdW7WRXYzb8jXKK4vOcN9PtBqdFmpv2es1YH/17pc5QhWaQU3s33In9qZ7e5WP+7aWJEceH3SyF2+ysVdWrmovJWLbiMXvRG5eBd/WO4sORzgsX8DwTdRjNr/69ywc5fRHuwi2jPl41I4GdGcDVMzBH4HfA+BskDw+nBaMKWIYwsoBNMOCI9CQptMnbRCkBQrrxCuFiFdMUKSGjtGDWIUxQQ2OXZX+cJ5EMIP3bsIKI+dOZRuntDVI4WrRwqKsR6YFKTH2l1K0vNzFRyXoEO7JntOVpK9hDPltSL7kaxHNiA7p5gzsldkT8n6ZI8pZopvxW+9N39BTqx8akLDEbxzHMkkZsuduUvXGfSCxa5cZeZooU2ZFgyaL9vq4mbbzkfUm6FbANtQZA8VWj8V+aYfl99vtMlGpxBmt/dj8Sttbp3sz2lR9EDztemhpin2UGWg41n/U2P0c4+UafXQA1Z37GXKNlVfQJX2JaaPqbNb2d3zYcJ+MLpihV/F9y/bP/qy4RF4b61PvTU59PZqM1r6gEeqH+holbd8UOjAByWNGw6rGuhIYQN1axvQsLwBDioc2C+KHLO6dY6q3FLHrQbVjlvZBR8nkxc=",
            },
        ],
    },
    "castle": {"name": "Castle Wall", "cat": "loop", "aliases": ["castlewall"], "examples": []},
    "cave": {
        "name": "Cave (Corral)",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7ZXBbptAEIbvfopoz3tgwWDglqZJL6nb1KmiCCEL2yRBAW+6QFNh+d0zMxCxLPTQQ9uoqmxG429ndn68zFB+qxOVciHw6/jc4uDxuevRJYRNl9V9rrMqT8MTflpXD1KBw/mniwt+l+RlOou6qHh2aIKwueLNhzBignFmwyVYzJur8NB8DJslb1awxPgc2GUbZIN73rs3tI7eWQuFBf6y88G9BXebqW2eri9b8jmMmmvOsM47ykaXFfJ7yjod+Hsri02GYJNUcDPlQ/bUrZT1Tj7WXayIj7w5beWuXuVilU6u08tFt5WL3oRcvIvfLDeIj0f427+A4HUYofavvev37io8gF2GB+bYmBqAlvZsmDNHsOjB3ELgaYBSXA34RorrGRGemeJRFW3TBVXR9lhQihYR0KY6MMvCI2rcjLDNJGGPslxTnHBJnU48kicsHZkChUdbCzz2V7Sg+o5G/FGaT9V8jQTmnyGCYRYcnqAjvCV7QdYmew0nzBuH7HuyFlmX7CXFnJO9IXtGdk7Wo5gFPiO/9BT9ATmRAyNo4uP+uzSeRWxVq7tkm0KvL+tik6qTpVRFkjMYrqyU+brs1kOavTANgO0pcoByKZ/ybD+My+73UqWTSwjT3f1U/EaqnbH7c5LnA9C+TQaoHXoDVCmYaNrvRCn5PCBFUj0MgDb9Bjul+2oooEqGEpPHxKhW9Pd8nLEfjK7Iwbfe/zfXX3pz4RFYb23yvDU59PRKNdn6gCe6H+hkl3d81OjARy2NBcddDXSisYGavQ1o3N4ARx0O7CdNjruafY6qzFbHUqNux1J6w0fx7AU=",
                "config": {"product": False},
            },
            {
                "data": "m=edit&p=7ZXfb5swEMff81dUfvYDBkIob13X7CXL1jVTVSEUOQltUCHuDKwTUf733h1smB972MO2TpoIl8vHZ98Z53vkX0qpYy4s/Dg+h2+4XOHTbfse3VZzrZIijYMzflEWe6XB4fzDfM7vZZrHk7CJiibH6jyornn1LgiZYJzZcAsW8eo6OFbvg2rJqxsYYtwFtqiDbHCvWveWxtG7rKGwwF82Prh34G4TvU3j9aImH4OwWnGGed7QbHRZpr7GrKkDf29VtkkQbGQBm8n3yVMzkpc79Vg2sSI68eqiVy5macp12nLRrctFb6Rc3MVvLvc8Op3gsX+CgtdBiLV/bl2/dW+CI9hlcGSOi1NnUEt9NswlAEf1HUxtBG4LPKcHZjRFeAbxkPgGOO/N8QWCqQH6U4RFc2wjRgjKZCQSkBVzG/UKQfPMIJuSCXMlp78r4dK2hGWgKc0z1/aI/KgSHqKgR3lHdk7WJruCJ80rh+xbshbZKdkFxVyRvSV7SdYl61HMDM/ql07zD5QTOnVr6F7Tf49Fk5DdlPpebmNQ0rLMNrE+WyqdyZRB62K5Std5Mx5QZwOtATtQZAelSj2lyaEblzwclI5HhxDGu4ex+I3Su97qzzJNO6Du1R1Ut5QOKjT0C+O31Fo9d0gmi30HGL2ls1J8KLoFFLJbonyUvWxZu+fThH1jdIcOvlP+vxf+0nsBj8B6bf3ktZVD/16lR6UPeET9QEdV3vCB0IEPJI0Jh6oGOiJsoH1tAxrKG+BA4cB+InJcta9zrKovdUw1UDumMgUfRpMX",
                "config": {"product": True},
            },
        ],
        "parameters": {"product": {"name": "Product", "type": "checkbox", "default": False}},
    },
    "chocona": {
        "name": "Chocona",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=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",
            }
        ],
    },
    "country": {"name": "Country Road", "cat": "loop", "aliases": ["countryroad"], "examples": []},
    "doppelblock": {
        "name": "Doppelblock",
        "cat": "num",
        "examples": [
            {
                "data": "m=edit&p=7ZVfb9o8FMbv+RSVr33hxAFC7rqu7IaXroOpqqIIGUhL1ARTJ1knI757j0+y5S96tYuxXUwmRyc/H9uPneQhfc2FCukEGncpoxY07jK8XMf8WNmWURaH3hW9zrOdVJBQejed0icRp+HAt3AsCwZHPfH0PdWfPJ9YhBIbLosEVN97R/2fp+dUL6CLUAfYrCiyIb2t0gfsN9lNAS0G+bzMIX2EdBOpTRyuZgX57Pl6SYlZ5wOONilJ5LeQlDrM/UYm68iAtchgM+kuOpQ9ab6VL3lZawUnqq/Py+WVXJMWck3WI9fs4jfLnQSnExz7FxC88nyj/WuVulW68I4Q596RcGaGuqCleDaEWzgXPKufxDHEZjUybBOnGDWqyBBH8QqMxi3g4tLWpCITjsSpiMVGiMY1BCMA1Yu4jXp+ENiahRt8xDjFaGNcwv6p5hg/YmQYhxhnWHOL8QHjDUYH4whrxuYEf+mMLyDHd2z8XKs2uux9MPDJIldPYhPCeznPk3WoruZSJSImYAQklfEqLfs99Al4c4HtsbKBYikPcbRv1kXPe6nC3i4Dw+1zX/1aqm1r9jcRxw1QuF4DFR9oA2UKvr7avVBKvjVIIrJdA9S+1MZM4T5rCshEU6J4Ea3VkmrPpwH5TvDyORy8889l/5DLmkfA/jYf+B85vl5Qzqi+o+SQr8RqI2MCf9T0DL+4enzZpep1CsA9ZgG01xRK3vEF4B0HMAt2TQBojw8AbVsBoK4bAOwYArAznmBmbduCUdV2BrNUxxzMUnV/8Il4hb0Eg3c=",
            }
        ],
    },
    "easyasabc": {
        "name": "Easy As ABC",
        "cat": "num",
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
        "cat": "num",
        "examples": [
            {
                "data": "m=edit&p=7VZNb9s8DL7nVxQ662DJcWL71nXtLl3et2uHojCCwkndNqgTd/5YBwf576XIBKYl9zAM2HooHBP0I4p8RIaSqh9NWmZSBebnh9KTCp6JF+KrQviG9/Bcreo8i4/kcVM/FiUoUv53dibv07zKRsneaj7atlHcXsj2S5wILSS+SsxlexFv269xO5PtJQwJqQA7B00JqUE97dRrHDfaCYHKA32210G9AXW5Kpd5dntOyP9x0l5JYeJ8wtlGFeviZyZoGn4vi/ViZYBFWsNiqsfV836kau6Kp2Zvq+Y72R6/Tdfv6BqV6BptgK5ZxR/Tze4esqpZDHGN5rsd5PwbsL2NE0P8e6eGnXoZb0HO4q0Y68MyqTAiQCDogIlngJABaAGVPABTtJgwAC18BoQGmHZAaFuEgQHGDMApjFhkM43QgoVVHhJhTpTnW1yVh4FYZOWhHz5LoR8+S6ENy4rSyrbR9hKUxlk8lh/ZNk4B1Bj98FjB1J5FReHRnaqoCfrh+ZkiwsqgqDCcoVMZRaXhsyIXQT8suqZa9BCsBfOsFfrhNpRnlg1NeWbZ0L7NUPt25jXlmdtQnjkSIEPFEqTpz88dBY5rKganSMXgrqkYLEF64iyMmoT1laby8FhOeTSVh6eMGoUjkZN6Kg+L5VN52Np9agPG0LeKATuGwn3jBuUZSo3yCrYV2fooP6P0UAYoz9HmFOU1yhOUY5QTtJmajem3tq6/QCcZ0yH41gNH5cfo+x6djxJxCgfm0awo12kOh+asWS+y8vANVxRRFflt1ZT36RIOXLzBwLEK2AYte1BeFM/5atO3Wz1sijIbHDKgOa8H7BdFeWd5f0nzvAfQnawH0dWhB9Ul3AvYd1qWxUsPWaf1Yw9gV56ep2xT9wnUaZ9i+pRa0dbdmncj8Uvgm/iQ/PHH/e9f3P9M/r33tpW+Nzr41y3Kwb4HeKD1AR1s8T3udDngTj+bgG5LAzrQ1YDajQ2Q29sAOu0N2BsdbrzaTW5Y2X1uQjmtbkLxbk/mo1c=",
            },
            {
                "data": "m=edit&p=7VRBc5s8EL37V2R01gEBtjG3NLV7Sd2mSSeTYRiPbJOYCVj5BHzp4PF/z+5CDQJy6KGtDx3Bzr6nRVqteJv9V0gd8RkMx+MWFzAcz6LXc/Gx6nEX50nkX/DLIt8pDQ7nXxYL/iiTLBoFdVQ4OpQzv7zh5Sc/YDbj9AoW8vLGP5Sf/XLJy1uYYlwAdw2eYNwGd9649zSP3lVFCgv8Ze2D+wDuJtabJFpdV8xXPyjvOMN9PtDX6LJU/R+x6jPCG5WuYyTWMofDZLv4pZ7Jiq16LupYER55efl+uk6TLrpVuugNpIun+M3pzsLjEcr+DRJe+QHm/r1xvca99Q9gl/6BuS58KvCq6WqYO0Y8a/AEsHuCY4St6YnVwR7g6QlOcfXxCXrCjPamJp5huHeCwsLVJy2Mq7fihbA7hI1EGzvdADov/tw14eCJ7BpDUQSV5oHsgqxN9g4qx0uH7EeyFtkx2WuKmZO9J3tF1iU7oZgp1v6XbucPpBPYWG9z4IWdEROOAjbfPkUXS6VTmcB/vyzSdaR/Ymg0LFPJKiv0o9yAbKgPgTKA21OkQSVKvSTx3oyLn/ZKR4NTSEaw/UD8WultZ/VXmSQGUXVVg6oagEHlGtTdwlJr9Wowqcx3BtHqBMZK0T43E8ilmaJ8lp3d0ubMxxH7wegNHCi++6+L/6UujldgnVu3OLd06O9VelD6QA+oH9hBldd8T+jA9ySNG/ZVDeyAsIHtahuovryB7CkcuHdEjqt2dY5ZdaWOW/XUjlu1BR+Eozc=",
            },
        ],
        "parameters": {"fast_mode": {"name": "Fast Mode", "type": "checkbox", "default": True}},
    },
    "gokigen": {"name": "Gokigen (Slant)", "cat": "draw", "examples": []},
    "haisu": {"name": "Haisu", "cat": "loop", "examples": []},
    "hashi": {
        "name": "Hashiwokakero (Bridges)",
        "cat": "loop",
        "aliases": ["bridges", "hashiwokakero"],
        "examples": [],
    },
    "heteromino": {
        "name": "Heteromino",
        "cat": "region",
        "examples": [
            {
                "data": "m=edit&p=7ZdPb9tGEMXv/hQBzzxw/5O8pandi+s2tYsgEASDtplYiGSmlNQUMvzds9z5CTIlFWgPbVPAkLS7nJ2ZnbdvZqld/rZu+jbXbviaMi9yFT9VWaaf1UX6bT9Xs9W8rV/lr9er+66Pgzz/6ews/9DMl+3JBK3pyeOmqjdv880P9STTWZ5+Kpvmm7f14+bHenOZby7jVJbbKDuPI5XlOg5Pd8N3aX4YvRGhKuL4gnEcvo/D21l/O2+vz0Xycz3ZXOXZsM53yXoYZovu9zYTs/R82y1uZoPgpllFMMv72Wdmluu77tMaXTV9yjevJdzTI+GaXbjDUMIdRkfCHVD8w+FW06enuO2/xICv68kQ+6+7YbkbXtaPmS+z2uaZr1IXlHRaOiOdTV0lc5XMVS51qvD04kCpgl7UlOZZi7XSW7n4Vho/WuJQGj8GO4OdYR0TpLfM2+0zdk6CVQ6/DjuHnsefJw5PHB47NkIF7AJxlehX4kcXItdK9LRCDl6txZ8GnwaXNjyDQxvkVvxrK/Foiz34tGU9J/Frhz54NTi1Qw882mMfiAs8OrBuyTx86krmTSHrmELWMYX4M/BqlMRp1FYu6xv4NeA3Wvwb+DWGeYO9QY99MeyHgV9jiQOcBh4NOA18Gvg0njjAbchvQ2YbktmA35SsUxIP+2FK7CrkFXbsk2V/bCHzln2x7IdVYm/ZDwt+Sx5Y9sGC08K/hX8L/9ayHnlgyXPrsCPPLfxb9sOC35LPlpK2AXmJHnltwW/Jb1eIf0eeO+rbUd8O/h14nZI4nEJPSzwOvA6+HTw78t+B11n04dnBswOPg1/nsQefg08XkIPDlazLceXA5cHlObc8vHnweHB4+PPw58ljz7nkyUsPbx4cHt489eqpU++YB5f3+AGf5xzynLkeXB6+PPnq4cuTpx58vuIAJx9DIfMBfAF8gToNnFMBfgK4AjwFeApGcARwBnAGcAZwBvIybF8k6fyM75iL+jG2KrXvU3uWWp3aq/giyjcmtd+ntkitS+150jlN7bvUvkmtTa1POmF4lf3Fl92/Fs7Eyz+nv/NxLxYvFi8WLxb/D4vpySS7XPcfmts2XkFO7z62ry66ftHMs3jjy5bd/HrJbJ0uhPGKEmUP68VN249E8677PJ89jPVmHx+6vj06NQjbuNwR/Zuuv9vz/qWZz0cCueKORHITG4lWfbxmPXtu+r77MpIsmtX9SPDsSjby1D6sxgGsmnGIzadmb7XFDvPTSfZHln4TE7fdvlyn/6Pr9EBB8a39z/jWwknZ2/W70l/1a3I6SrfFPxIerXHkB2Ue5QcFPSx3WNNReqSso3S/sqPosLij8KC+o+xPSnzwul/lQ1T7hT4sdVDrw1LPy30yPfkK",
            }
        ],
    },
    "heyawake": {
        "name": "Heyawake",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VXfT9swEH7vX4H87Ic4dn6+MVb2wroxmBCKKpSWABVpw9J2TKn6v/OdfdCmDdqkaRqTpjb25+98vu8cnzP/tszrQiqP/jqW6PEzKraPH4f28fh3PlmURXogD5eLu6oGkPLT8bG8yct50ct41rC3apK0OZXNhzQTSkjh41FiKJvTdNV8TJu+bM5gEjIGd+Im+YD9DbywdkJHjlQe8IAx4CXgeFKPy+LqxDGf06w5l4LivLPeBMW0+l4I1kHjcTUdTYgY5QskM7+bPLBlvryu7pc8Vw3Xsjl8Xa7ukktkh1ya8IflJsP1Gtv+BYKv0oy0f93AeAPP0pUwoUhjKYLYdklgO+Ur1xtHq8BDD48BPDRwJiLodu/R+mbhyzAku9kMdduKeJl+GSrP35qNCCpdob207bFtfdueQ7JstG3f29azbWDbEzunD3W+UdIPkIaPk2YMMNRZHEk/RFqEgwA4YYyDHUEE4RC+EfuGCQ47tBOOfDr4jOEbs2+spZ9EjEOpPaRucQLMvkkktXJxYQc2jDWw84Vdat/FhR3YaYZdas2+fgDs4sIutXGaYQdmX424gYsLO7DTDDswa8Yc37BO4wHzntC+8ZrogVm/QY7Gabb7ybHQA/OeGFwMhveB9pmOjcXYW7O1VzGvE2OdmNeJaT9ZJ+WrnnNHjorzpRz1c77IS5M2vPAL+9qPbGtsG9rjENH5/sUKcKf690/eT+Vk2l2n7V/w73HDXibOlvVNPi5w+/Svb4uDQVVP8xKjwXI6KurnMS5/Ma/KqznPTu23AbcVuJmd2aLKqnooJ7P2vMntrKqLThORBcJ3zB9V9fXO6o95WbYI97VrUe5SblGLGjfu1jiv6+qxxUzzxV2L2LqdWysVs0VbwCJvS8zv851o003O6574Iexj70/z/8v6l76s9Aq8t3a7vDU59vRWdWfpg+6ofrCdVc78XqGD3ytpCrhf1WA7Chvsbm2D2i9vkHsVDu6VIqdVd+ucVO2WOoXaq3YKtV3w2bD3BA==",
            },
            {
                "data": "m=edit&p=7ZlbjxvH0Ybv91cYvJ6LOXF6mneOI+VGUeJIgWEsFgIl0dbCu6LD3Y0DCvrvfqrmrZnhkEHyIfgQAxF4qLeL1XXqqu4m+fC3p+1hV9SlPZu+KIuKR8q9v/p15a9Sj9e3j3e7zVfF10+PH/YHQFH86fnz4oft3cPu6lpSN1efjnlz/LY4/mFzvapWxarmVa1uiuO3m0/HP26Oz4rjKz5aFT28F4NQDXw2we/8c0PfDMyqBL8UBn4PfHd7eHe3e/Ni4Px5c318XazMzu98tsHV/f7vu5X8sPG7/f3bW2O83T4SzMOH25/1ycPT+/1PT5Ktbj4Xx68Hd19dcLe55K4xL7hrAv/P7uabz59J+19w+M3m2nz/6wT7Cb7afOL95ebTat1FpMParNbJGCxVMLp2ycgLRlWWCyVVWRmnnHGqM07jppsZZ71e6umdM7NVn9mqyzOZulnYquszmdajmOtZn3E6z8UJp19yktuac/plpE25TGFTLnPYNK55Pqt1PXOZ1m21M06/9LDJnp/5rLyMvcnLSNvKZ82st7Vbn8s0HsVcpllqbtv6jOOz5nra5bq362VW28HDma31ImOUb+VF/L2/P/f32t9fU+PFsfH33/t76e9rf3/hMs8o/a7NRbcm8JqaXpdgQnZcgQnEcQ0m7Y4bMOEYbkxeuOwKxpJp4ZMWlzE9wmVCJvSviy4RjuGED33MRU/gxuySKJ/bM1f+NPhgC+EYW7YEhitsVZIxHHzT08j/Hp+tOB0j00u+R6aPGM0f4QY/rSmC38m3Dj2d9HTo6aSnQ08Xc01euEJPIz0d/lvRul1y0rP0jomxl0zPXCtjlycngVvTr5xUyFuxGc5lkaohJ1CwYs+cYIE7bGX53OKDtbbrwZa1lc9dF0l+Qosk/6FFks/QoretDAwFDz5AwZInluCnDn8UY2rx03ZTt9UVjOVnjZ+KqyOurLha1tc2HMMcy4zHXKXQj90Udiv8HPMA3zZYjwVbjfxvElj+cM5P8SKj9YXis/T0bdGXgzwUPMhDiXGQh4456bLlWT5zc+iskb3OqYHA1l9pWJfUknPbEBxbTuRnTSzCzCsYSwb/W/lfk9vAJT7Xyk9Cjx0T0b9J+k3GDibH1EapHJbkqlSt0o+BoWDlocRWHXbJm/aHRCwTRr/2kMTewlgYeTtuQo8dWI6JvQzfzOfoC7OrPHToSdKT0J+kP2E3yW7CfzuGHDM3yeeErciz+RmYtUiRE/IzYpPX2vmtr1Zt19T5iFlrOxp83amBOmrAal61UVmPqGZq+kJrBwUPvvWsRWDsU1czPepraNGr36FFr32gZ38Yscmof92fwPR4rx6HIi+f2SsmTFzqNShYc8n5iKlPxlMe2iGHfI6MYsn0iB2yjpHP8pl1GTG12qtWoQWfOc70bFbPmm+BoUVWn0KLrD02s99OuC5yP+jP/XqGO+6dak7uZnk+olerUgeIAUZ2+vpo3TPSoWBKsjY9KFjOsPmgZRAyYOoGuwYYaRcxYOrClI90aiCZ5iOSYCwZcH+H9Nsga6mh4GEK1ISGnBuw+cMqGTDdgwKAeTiNbF7kj1AwEJ+YDxGwZVz6oEXWTg0Fy4XWVmLwADpqcr4qGApWKFRkVkVCp1A4CUK/VSFj8fEhOoEKYyxsnaDKZrft1bFQsCqVHTOro6BFVqdB0amFZCedsPkg36h4xsImrxjNf51ALqOugBKLYqQrWI1BkQFGSpcBS30sGRkj3VLBtKxmymxyIza3tPnBgy9XaLKsxso02YhpLMajDB7E6rI14EFUAaHgQbjJYlTlWFiYVHahfKDNzoCpCP/JADPH4rGmmEZe3EotSrKWCAqOmM0j7YwGTHl4xNJUpXZ6gHXOOCLdxpop0UIbsFEIcsLxFo3KGYeVaNTaGlXHkwFTGY3KCTIf2TwdLuaFjUIn5wVvkRFOFd7CAns6bxGQW9DRaMBGoYUTaDbP/dQBbMBG4QtnJ67HbsUpPGrJXG1HQRtk3XO9POQ+FBxlRjnJdSg4yslKTuufbBmUTxvkpHVMVmdaRy4MGBwwYY4GSDFjtSBOKPeZZWE8tWbot7nKEBQsGdKT9QUEOjlX40/IkybGky3lrzffAvOlg/GE9eUCCtZ2smY7UeKgzFWCuKjkWvHW6Ax/jK8LDJQtU/Hy5SjryxF0ypvx9SUIioz048+YT8PyDQqOLRl5fQmCgsMHZHRZgoJli8tqyPdcYoPfcw4xnrAOIY9dJyEUHLniMqAjzS+6Ojuhk7xdjMMWvo25NSw/oeNcu/AkrSMUrEsXuRoxuWI8XQ6VW5dR3hI5GTGxMx4vkJ1ihIL1JYhLQqdLgn9ZC4xMUn6g6NHFEv+TYsHOiJl38iUu6fIPZW74ZvK69JLPCSOvvKEPrDyQ56QvnlAuhKpJ4uoVF5TcxoWWueo7KPJxsbQvLLqMUZ+96hM66iTH5Fn+2IVfevxSqn6EgrWm9FQffUSvjbbsUme/LDnGlnocCg7/7dIrTM/yM6rqCv3agHo2owkjrz3EL5DavPgcHBdLq3n5zP4w8v1nWvlsfPUpFCyd1M+QQ34F+c5/C/nG31t/7/w3kmS/Ev6ffkf8z3+O+ZfuXNsh8m89OIi+yH2R+1+Tu7m6Xr16Ovywfbfjv4Fn73/cffVyf7jf3jF6+XT/dneIMX/NrB72d28eJL3xf274LwHeR5c8Yd3t9z/f3X48lbv98eP+sLv4kTF3mL8g/3Z/eL/Q/sv27u6EMfwXdcIa/jI5YT0e+D9kNt4eDvtfTjj328cPJ4zZfycnmnYfH08deNyeurj9abuwdj/F/Plq9Y+Vv665rRbtl/+9/kv/e9kSlL+1U+u35o5X7/5wsfVhX+h+uBe7XPyzRod/1tJm8Lyr4V5obLjL3oZ13t4wzzoc3j9pctO67HPzatnqZuqs283UvOGvb65+BQ=="
            },
        ],
    },
    "hitori": {
        "name": "Hitori",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=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"
            }
        ],
    },
    "hotaru": {"name": "Hotaru Beam", "cat": "loop", "examples": []},
    "jousan": {"name": "Jousan", "cat": "draw", "examples": []},
    "kakuro": {
        "name": "Kakuro",
        "cat": "num",
        "examples": [
            {
                "data": "m=edit&p=7VjNb9s2FL/7ryh01kEkJUr0reuaXTpvXTMUhWEUSuI2RuQok+11UJD/vY/vkbRIvVwGFCuGwrbA34/k+/oQLd21d6ehz4W2X9XkRS7go0uNv6ox+Cvc53J37LbLF/nL0/G2H2CQ579dXOSf2u6wXazdqs3icTTL8W0+/rJcZyLLMwk/kW3y8e3ycfx1Oa7y8R1MZbkA7g0tkjB8fR6+x3k7ekWkKGC8cmMYfoAhGU/49+V6vMwzq+Un3GuH2b7/e5s5Kyy+7vdXO0tctUdw5XC7e3Azh9NNf3dya8XmKR9fPm+sOhtrh2SsHTHGWh++qbFm8/QEIf8DzP24XFvL/zwPm/Pw3fIRriu8iuVjJuq6tCLKLC9BJsDGQu1hIy2UoIGwKVBhFTDuFmG9we3SONwIWn/GtL72WKJ81QSsERcel8bisFxXuF153BD25jQNbj9jU0+3G7LGG2PAzCksSdgZky3eN6NFFAujKTbedlOjMtDhMcZCuPWyALMn87JQiEGrx5QJaBTCZLyPDWCS5+yTQkb2AkZ7vX1S1KTP2Q8Y5btgSLBvkniAKF15a0DdJDhSUuh8YqWkxARnpCYc5mtaH+YNORtgZIsqorxJRZkRPhSqxNCXXpqCIEWYQu+VK4o8xMdhqlqvrSTXQKbDJB3S4TElNqwn24M1VYGBV15dRdb7opWVszZAqvGAXZ0EcQ2a4+tIVq7HfN60qxtvrnY95NfriuSF+SrqQamTOtBUB8E97ZoozMdNJGuq02B/TXUa1tekP4SvJv1efE3iQiU0LvpevGvxYE5TRclqqJCCd42LltdmKBnBWgP1P9lu1PQOII2LRcDku3NNFQW1uBOuClhoMc7DHfMD3DExmzIPt3K4tWellSoSzkYp5ay2lLPhSTmrNuVsVFPOxiLhMHwpZ91KOetHyjF+VIwfFeNHxfiBlZFweNdMOWYv5j3lGD+wmlOO0YsnWcoxerH7Uo7RIQpGoCiYCIqCSZ3Ak29Gctuh/OakYkIhsNhTEgt2RnKKuHISXJ0ILtmCy7bg0i00txJbc0Zyirj0wl8HjmQKFQ52jmRkSi7FdBKmJJdNyWUTTkqGhGN3TnKJk1zi4MTiSM4jrsMllyOp2ZWcIs2Ut+RaVXKJk1ziZMNpx1t/Shounlw2FZdNBccwQ3LbuRQrLpsK/gkwJBM6+h8zIxnfFXdMKK5hFXcAqPldHI6zC3wMkHi9hOeDfFR4/RmvBV4rvL7BNa/x+h6vr/Ba4lXjmto+YfyLZxA6V7+ROetS4sPs85/qx/z/eX6zWGer0/5qO7xY9cO+7eDp+d1t+7DN4BVFdui7j4fT8Km9hodufIMBz9XA3eOOiOr6/qHb3cfrdp/v+2HLTllye/OZW3/VDzeJ9C9t10XE4a9TO8Sbr3fDdRdTxwHeDUxwOwz9l4jZt8fbiJi8R4gkbe+PsQHHNjaxvWsTbfuzz0+L7J8Mf2sFYS9/vP/5D97/2PAX39sd+HszByu3H9i2B5rpfGDZDnf8rMmBn7WzVTjvaGCZpgY27Wug5q0N5Ky7gXumwa3UtMetVWmbW1WzTreqps0eKnmz+Ao="
            }
        ],
    },
    "kurodoko": {
        "name": "Kurodoko",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7ZXNb5tMEMbv/iuiPe+BNR823NI07iV1m9pVFCEUrW0So4A37wJNheX/PTMDKctHDz30bVRVNqPxb4edh10/S/5fKXXMhcCvPecWh4w7rkeXEFO6rOazToo0Ds74eVnslYaE80+LBb+XaR5PwqYqmhwrP6iuefUhCJlgnE3hEizi1XVwrD4G1ZJXKxhi3AF2VRdNIb1s0xsax+yihsKCfFnnHqS3kG4TvU3juysYBfI5CKs1Z9jnHd2NKcvUt5g1OvD3VmWbBMFGFvAw+T55akbycqcey6ZWRCdenddyVyNy7VYuprVczEbk4lP8Zrl+dDrBsn8BwXdBiNq/tum8TVfBEeIyODLbwVt9WMx6b5hjIZi3wHURzFrgedQNdvOVzKZEPIPMetP6NpVYLRGW359HCNFrLkR9H+72D0SCbIPYdJtJHOpvEpc0Go8h3DkSs71HisyaOS2PWePT+rivBJZR0GLeUlxQnFJcw1rzyqb4nqJF0aV4RTWXFG8oXlB0KHpUM8Pd+qX9/B/khDYcBiMf9++l0SRkq1Lfy20MrluW2SbWZ0ulM5kyOOZYrtK7vBkP6BQEXwI7UGUHpUo9pcmhW5c8HJSOR4cQxruHsfqN0rve7M8yTTugPtc7qD5+OqjQcLYYv6XW6rlDMlnsO8A4hzozxYeiK6CQXYnyUfa6Ze0znybsO6MrtPH98+8d8ofeIbgF1ls7ed6aHPr3Kj1qfcAj7gc66vKGD4wOfGBpbDh0NdARYwPtexvQ0N4ABw4H9hOT46x9n6OqvtWx1cDt2Mo0fBhNXgA="
            }
        ],
    },
    "kurotto": {
        "name": "Kurotto",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VVNb9swDL3nVxQ662D5I3V867pmlyxb1wxFYRiFkriNUTvqZHsdHOS/l6QNxJK9ww7bOmBwxFBPFPkU5dHlt1rqlAsHP17I4RseX4Q03HBKw+meVVblaXTGL+pqpzQ4nH+az/mDzMt0EndRyeTQzKLmmjcfopgJxpkLQ7CEN9fRofkYNUve3MAS4z5gizbIBffq5N7SOnqXLSgc8JetPwX3DtxNpjd5er+AVUA+R3Gz4gzrvKPd6LJCfU9ZxwPnG1WsMwTWsoLDlLvsuVsp6616qrtYkRx5c2HRxSodXe9EF92WLnojdPEUv5nuLDke4Wf/AoTvoxi5fz254cm9iQ5gl9GBeQ5uDeDHbO+GeQKB3tyzA3wbmFJ1p4fMzBx+aM4DmvdSnAd2ipCS9kLCcwuY2TyEY59FOJSlD1CWPkBU+3sEketREWIQ47o24tMJDMSuHdi1p+YeuBFB93JHdk7WJbuCa+ONR/Y9WYdsQHZBMVdkb8lekvXJTinmHC/+l/4af4BO7LV9xnyCfw9LJjG7qfWD3KQgy2VdrFN9tlS6kDmDPshKld+X3XpEbRKEC9ieIg0oV+o5z/ZmXPa4VzodXUIw3T6Oxa+V3lrZX2SeG0Db+A2o7U8GVGloPr251Fq9GEghq50B9BqVkSndVyaBSpoU5ZO0qhWnMx8n7AejEXv4gvr/kvlLLxm8Auet9ZO3Rof+vUqPSh/gEfUDOqryDh8IHfCBpLHgUNWAjggbUFvbAA3lDeBA4YD9ROSY1dY5srKljqUGasdSfcHHyeQV",
            },
            {
                "data": "m=edit&p=7VXPb5w8EL3vXxH57APm17Lc0jT5Lun2S5MqihCK2A1JUGCdGmgqVvu/Z2ZsFQxU6qVtKlUsM+PnwfPAfrP1lzZTORcO/ryIg4fLFxHdbhTS7ZjrqmjKPD7ix23zKBUEnH88O+P3WVnni8RkpYt9t4q7C979FydMMM5cuAVLeXcR77sPcbfm3SVMMe4Ddq6TXAhP+/Ca5jE60aBwIF7rOITwBsJtobZlfnsOs4D8HyfdFWdY5x09jSGr5NecGR443spqUyCwyRp4mfqxeDYzdXsnn1qTK9ID745HdLGKoev1dDHUdDGaoYtv8YvprtLDAT77JyB8GyfI/XMfRn14Ge+Zt2Sxz1ngaCe088iFxvnahdrpB5Z6tDSjFblIr7JytdOPCxe8Cz6EWRfKrrEsYAmLYPf0YWBegEA4ACIEXGeAQBFAcMsNsoRC+gwYIAL+kOL3iBDAPmHeAAmAur2yCOA1AIKj+R0Kae0+C4iLeA/2huwZWZfsFXxO3nlk35N1yAZkzynnlOw12ROyPtmQcpa4IT+5ZfoL/gY6iaf1b1/B34eli4Rdtuo+2+Ygl3VbbXJ1tJaqykoG/YnVsrytzXxM7QsEBdiOMi2olPK5LHZ2XvGwkyqfnUIwv3uYy99IdTda/SUrSwvQDdmCdN+woEZBUxiMM6Xki4VUWfNoAYMGYq2U7xqbQJPZFLOnbFSt6t/5sGDfGN2Jh38c/5r/H2r+uAXOW+snb40OnV6pZqUP8Iz6AZ1VucEnQgd8ImksOFU1oDPCBnSsbYCm8gZwonDAfiByXHWsc2Q1ljqWmqgdSw0Fn6SLVw==",
            },
        ],
    },
    "lightup": {"name": "Akari (Light Up)", "cat": "var", "aliases": ["akari"], "examples": []},
    "lits": {
        "name": "LITS",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VXNT9tOEL3nr0B7noN31/HXjdLQCz9aGiqErAg5wYCFk+XnOKVylP+dtx+uceKqh6qIQ2Vl8vJ2MjNvs2+z/n+TVTlxjwKSEXnE8fg8IhEEJDxhXp57Lou6zJMjOt7UD6oCIPp8ekp3WbnOR6nLmo22TZw0F9R8SlLGGTGBF2czai6SbfNf0kyomWKJEQd3ZpME4KSDV2ZdoxNLcg/43GHAa8BFUS3K/ObMMl+StLkkpvt8MN/WkC3V95y5OfTnhVrOC03Msxpi1g/Fk1tZb27V48bl8tmOmmM77rQdN+rGld24GtpxNRoYV6v483HLJzU0aDzb7bDhXzHqTZLqqb91MOrgNNkinpvITbw28dREYeIlUqmRJn400TNxbOKZyZkkW8bHIfGQs0Tgdw1wZELfYQkcWhziIEVjhwVw4DByojYnIB57DkfAwuJoDBw7jKPoOT72gF2vOCbBpcHmmHJbH+vAkcVckhC2l+DgRcvjaEvbV3DUka6OQH1p6+N7JHyrUQjk+C5HopffaoHG0M2mdbX7oHX93AfoClst4FvtEfYwsvNoXTx2+xmjptsHa79WI7Q47UYLt3uL9067ti23vYwu4TRqLa12raXVrrW02iVqSl0TP/KV+alPTPRNDMwRCPVZeuPT9ttxUmkvrf6DE/S3udkoZdNNdZctcjhzcnufH52rapmVDFcgW6vyZu1WE3NDwrngVpvlPK96VKnUU1ms+nnF/UpV+eCSJnO0G8ifq+p2r/pzVpY9wl75PcpeTT2qrnDvvPqcVZV67jHLrH7oEa+u1F6lfFX3B6iz/ojZY7bXbdlp3o3YD2ZeKSxG/r//lzf/f9Gb770337+3ccy5VdWg6UEP+B7soL8df2Bx8Adm1g0P/Qx2wNJg910N6tDYIA+8De4X9tZV9x2up9o3uW514HPd6rXVU1YW9ZrNRi8=",
            },
            {
                "data": "m=edit&p=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",
            },
        ],
    },
    "magnets": {"name": "Magnets", "cat": "var", "examples": []},
    "masyu": {"name": "Masyu", "cat": "loop", "examples": []},
    "mines": {
        "name": "Minesweeper",
        "cat": "var",
        "aliases": ["minesweeper"],
        "examples": [
            {
                "data": "m=edit&p=7ZRBb5swFMfv+RSVzz5gIClw67pmlyxb105VhVDkJG6DCnFnYJ2I8t37/KADG3bYYVEPE+Lp8fPD7x+T/yt+VFwJGsDlBdShDC7Pd/F2nRBvp71u0zIT0Rm9qMqdVJBQ+mU+pw88K8QkbquSyaEOo/qa1p+imDBCiQs3Iwmtr6ND/Tmql7S+gSVCA2CLpsiF9KpL73BdZ5cNZA7kyzaH9B7STao2mVgtGvI1iutbSnSfD/i2TkkufwrS6tDPG5mvUw3WvIQfU+zS53alqLbyqWprWXKk9YUl1+/kep1cnTZydfav5ObpXhRjSsPkeIQT/wZaV1GsZX/v0qBLb6IDxGV0IO65ftUBGc1nIV7w9qtb4Ds2cK1XfN8CM6zovTLDij6wu5yjDr8HsGLagQB1wN/nDYTYpQ88S0eIe/QrQg28DjAHd+31ZQ5uaxBbPWPM6sQY9v5dA6fL8IzvMc4xuhhv4RPQ2sP4EaODcYpxgTVXGO8wXmL0Mc6w5lx/xL/6zCeQE7szHBfdNT3tczKJyU2lHvhGgDWWVb4W6mwpVc4zAmOIFDJbFe16hFMKzANsj5UGyqR8zsBjBkwf91KJ0SUNxfZxrH4t1dba/YVnmQGaqWugZjwYqFTg/d4zV0q+GCTn5c4AvbFm7CT2pSmg5KZE/sStbnrktOA4Ib8I3rEHB+//n/Gnn/H69J33NgLemxz840o16nrAI8YHOmrwlg88DnzgZt1waGigI54Gatsa0NDZAAfmBvYHf+tdbYtrVbbLdauB0XWrvtfjZPIK",
                "config": {"mine_count": 10},
            },
            {
                "data": "m=edit&p=7VZfT9tADH/vp0D3fA+5S9qkeWMM9sLKWJkQiqoqLQEq0oYl7ZhS9btjO4E7X4MmHoZ4QG0s++c/57NzzlW/N2mZSdXHvx9JTyr4DbyIHhWBDM/z72KxzrP4QB5u1ndFCYyUZycn8ibNq6yXtFaT3rYexvW5rL/FiVBCCg2PEhNZn8fb+ntcj2U9BpWQEWCnjZEG9tiwl6RH7qgBlQf8qOWBvQJ2vijneTY9bZAfcVJfSIHrfCFvZMWy+JOJNg+U58VytkBglq5hM9Xd4qHVVJvr4n7T2qrJTtaHTrqBSdc36SLbpIvc/0p3uVhlVVemw8luBxX/CblO4wTT/mXYyLDjeAt0FG9F0AfXANpMTRHBkIkDD0TfiJqLAxD1ixiisfEN0diIkc9FXNf4RiGLPIxAHLyIysPQ8Fq+yAHzVp5jr3jeSitHxmQsf43ZWHof/S29z3eqfFzPbEYFGN/SB078AP2t+AH6W/vpY9kt+wH6W/YhL54KefVU6OQXYjktOXLqQc2w9U49ne4opz1qyGXt8f1rxV8UrTC+2a9WPD+t+P61dvy140/9weH0LPO3WPtOfB/jW/59/j7pPq5ny7yems6BFZ8OgiU7/dFOfzT1w4ofYf8t/ZC/b3rI+6HpPBjZp/Ng6uMrrL9Z31d2PeCkKzrvV0RPiGqiFzAOZO0T/UrUI9oneko2x0QviR4RDYgOyCbEgfKmkfMO6SRB8+l67Yed+NR+aO2kl4jxprxJ5xl86Eab5SwrD0ZFuUxzAZcKURX5tGr1Md054FMI2IosGZQXxUMOX0wGLm5XRZl1qhDMrm+77GdFee1Ef0zznAHNLYpBzceeQesSvuSWnJZl8ciQZbq+Y4B1SWGRstWaJ7BOeYrpfeqshheIFtj1xF9BDw2U4PPG9v43Nqy+99GG6D/SSeorGWhZn0nxsJmm03mRU2U6cShnJw5vyJvsoUWv2L97degcFWXnEAK4Yw4B2jlvWnxv5AC+N1xwwf35AmjHiAHUnTIA7Q8aAPdmDWCvjBuM6k4czModOrjU3tzBpezRk0x6Tw==",
            },
        ],
        "parameters": {"mine_count": {"name": "Mines", "type": "number", "default": ""}},
    },
    "moonsun": {"name": "Moon-or-Sun", "cat": "loop", "examples": []},
    "nagare": {"name": "Nagareru-Loop", "cat": "loop", "aliases": ["nagareru"], "examples": []},
    "nanro": {
        "name": "Nanro",
        "cat": "num",
        "examples": [
            {
                "data": "m=edit&p=7Vbfb9s2EH7PX1HomQ8iqR+U3rou2UuWrk2GojAMQ0nUxqhtZbK9Dgryv/e749EybRfFMGwrhsE28fF0ujvefXfm+rdt07dKa/pap1IFpLK84J/Whn+pfG7mm0Vbv1Avt5uHrgdQ6vXFhfrQLNbt2US0pmdPQ1UPb9TwUz1JdKISg59Opmp4Uz8NP9fDuRqu8ShRDrJLr2QAz0f4jp8TeuWFOgW+Egz4HvBu3t8t2tmll/xST4YblZCfH/htgsmy+71NJA7a33XL2zkJbpsNDrN+mD/Kk/X2vvu0FV09fVbDSx/u1Ylw7RguQR8uoRPh0in+znCR3mr6/Iy0v0XAs3pCsf86QjfC6/oJ61X9lNgcr1rUmiuT2BJbFFu2mYu3VaScF9HTgp6OW2eibUWOxq1OY9OgV2Rb69i4NrFvnR3o5/FBdHFgv6Tn2d6e7O/pu/jk2u37Q7I0p+w9rxe8Gl5vkFE1WF5/5DXlNef1knXOkWiTWWVyBGXQCFmhTKEFO2DrcZ4CI1DGGhhBMoZOGXQq4MzjAjp0EMawX4r9IgPGAQiXRhk6HGPI6WCMEUMlMZQlMBJK2CEGKhZj2K/EviuVTYNOBSwxVCmw6FcWWGKoMmDvC+8pq30MNoWO9jo2LZQ1Pgabwr7x9q2GTeNtWhpIxsdgNfxa79ca6BB7GcOmFZsGfq34tfCbiV8LHeIzY/jNxa+F31z8ZrBJRGIMv8RwxvBbiF/UyEqNbA6bRDTG8EstwBj2S7FfIIZSYkCNrNTIFtBxQQcxUL8whi8nvkoaxhJDCXklctTISo3wHrDYd4ihkhhcrrI09bgywKKDGmVSI9hQmQ46JbCPAe8BBx6Ce7lwhjgmeWCOBa7iLKYIHCNOCk+Ie4G3xD1qQsb5yFvioeSHeRg4jPOCiyMPJT/EPXBux70dh3FG8G/HvR2HccbAYeZh6nWYh8Jh8Bc46BDPAz/dHoeR/5Ar4qeW2mnUMXBbQ1+LPvEzcNsQh6W+xFUTOIx6BZ4b6oXAVehb0SfeBs5b4rboE4dpXAcOB/5bxJlJnMRhGpSMoRP4j5kDTo/czkWfuB36IkeucskVcTv0RY5chb4gbsvsYm6HHimgI7OLuR16pIDf0COo+64vSshlXjG3Q1+g7ru+IJ478eXgK/QIeL7rEUc9FXiOd2WmEed3vUNzKfROVUmPYEi/41H9iteM14JHeEl/mX/qT/Wv/1t8M5wJJhvd0A4/+X9XOj2bJNfb/kNz1+Lqc37/sX1x1fXLZoHd1XZ52/Zhj5tnsu4Ws7Vo13wxxVUJshVrRqJF1z0u5qtYb/5x1fXtyUckbOH+hP5t198fWP/cLBaRwF+1I5G/EUaiTY/r3t6+6fvucyRZNpuHSLB3NYwstatNHMCmiUNsPjUH3pbjmZ/Pkj8S/vFtKPv/Wv8vXeupBOn3Noe+Ec5kQOOmxik+coVzPW5nzeyuQ9MihbvHw+uvPfnuX/zHM84N2vUnpxvEJwYcpCcHmciPZhnkR1OLHB4PLkhPzC5ID8cXRMcTDMKjIQbZV+YYWT0cZRTV4TQjV0cDjVztz7RJsmpWfZdMz74A",
            },
            {
                "data": "m=edit&p=7Vddjxo3FH3nV0Tz7Ad/jT3DW5pu+pJumyZVFCG0YndJggI76QBNxWr/e861j4GBjVqpilpVFWCfe8Zj33t9rmdY/7ad9XNljHxdo7QCUr4O6WeMTT/Nz+vFZjkfP1FPt5sPXQ+g1E/Pn6t3s+V6Pppw1HR0v2vHu5dq98N4UplKVTb9pmr3cny/+3G8u1C7V7hUKQPuRR5kAS8O8E26LuhZJo0GvgR2+ba3gDeL/mY5v3qRB/48nuxeq0rW+S7dLbBadb/PK/oh9k23ul4IcT3bIJj1h8UnXllvb7uPW4410we1e/p1d93BXYHZXUGn7jKeb+xuO314QNp/gcNX44n4/usBvhrfo71MrRnfV0aHRu7LmYTZJLOmiQ0X0xezTub+ahxctSYcT2UbfWw6m2ZO+RTTp6vlXue9mFBHNts0VblaZzfKuuHoXsTxNkXzPLU2ta8RrNq51H6fWp3aOrUv0pgLRG+9UdZjbgtRegvsiB0wPErYA9fENTBcSzgAR+IIjPgSboBb4lbZGs4KrjWwIca6ksuEsW7gPAHzNOQb8C35NionOQBGr5zNPHrl6D965WryNXjZHMERfEO+icrrzKNX3mTeG9T4HtfAOUZvPHCO3RsHnHPi4QNsYpwR9M0bDZxj9LoFzrF73WDdnBOvxYecK6+xrqZvLebRzG1EfhriJiin85zokYfMo1fOkXfguS/olQvkA/hIPoJvybeIi/641oHPcbkWuWpzXC4ihy1zGMBH+om9hs11wVMDzoB3ZY+wFvPpkOeCLfIPmzFif7kvCUdqL0J7kdqL0F6k9iK0x1jQAxfNyL0FI2/0zQbojXmwNXQYig6hz5r6hE5gE2NO6idpvowRbe/nFK3SzwA/A/0MGB/oZ4CfgX6KzgsOmL+hPw14KfGkbckV90UePJb7ZcHvdQ7sOQY162qOgc8ukodmHDWDHvtbdCj6pJ419Fm01EKfOufEtQ32uuhB9j3nBMcQcNFnDcz5oR/Y3AvkJzKHEbmNzFtEzuUITPFiL8p4mYd1gR4xZh49YiTvwdfka/CRfAS/jxe44ZgG/uwx9NxQzzhDYBNLfqhP+AOb87TAZX7kgf477C/sg/657w7n2x47jOG55wx4R16DN8xJA15TM8C2YX4a5KdlflrJD7WBc8Cy7lJuC0ZtWtYmemBqT/ai1DLOHGcZuwXvyDvwNfkafCgxSuzkg8RVeKnxErucJ9QAtA2bWOZhznHOw+Za4Hn+p/w48gZjCtYYY4rP4j/n0ZifZyB64HKGyLnBfMp5RYwe8TLnVtYij7c3V5PH82WASyyoTdjEordylsIHPrOcBe/om/hvj3jL8VZqlvNYeTYVf4Ad13JyVpdaxnjHGIUvz0R5FrOu01lEnafncjqX8NB+kx7dz1LrUxvSIz2mtinvOV9//9kPOXsV+jsvEn/i2cNoggeFvEyffur/LjsdTapX2/7d7GaOt9SL2/fzJ5ddv5otYV1uV9fzvtj4k1Ctu+XVmqPH6T8E3mrB3aWRA2rZdZ+Wi7vhuMX7u66fP3pJyDmWf2T8ddffnsz+ebZcDoj8r2hA5Zf3AbXp8WZ+ZM/6vvs8YFazzYcBcfQWP5hpfrcZOrCZDV2cfZydrLY6xPwwqv6o0m8idaOM+/8/2D/0H0w2Qf/Vf2Lf8Pj5Nx+MufK7/lD8m35LVYMt5T8gH61y8meFDv6spGW586oG+0hhgz2tbVDn5Q3yrMLBfaXIZdbTOhevTktdljqrdlnquOAn09EX"
            },
        ],
    },
    "ncells": {
        "name": "N Cells",
        "cat": "region",
        "aliases": ["fivecells", "fourcells"],
        "examples": [
            {
                "data": "m=edit&p=7VVPb5swFL/nU1Q++4DDnyTcui7ZJcvWNVNVIRQ5CW1QIc4MrBNRvnufH3SxDT3ssKqaJsTj8fPP74/t91z8qLhMKHMoY9QdU/jC47Ex9fyAjlwPX6d9lmmZJeEFvazKnZCgUPplNqP3PCuSQdSy4sGxnoT1Na0/hREZEoovIzGtr8Nj/TmsF7S+gSFCGWBz0BihQ1CnZ/UWx5V21YDMAX3R6qDegbpJ5SZLVvMG+RpG9ZIS5ecDzlYqycXPhDTT8H8j8nWqgDUvIZlilx7akaLaiseq5bL4ROvL18N1z+EqtQlXaX8t3Owg+gKdxKcTLPg3CHUVRirq72d1fFZvwiPIRXgkXvCSY7MrxBspADbpNzBWgKsBE2uK71hTfGYBATK0KYFvMUae5WWMbjUGc4aWEea4HQ6aMTjoSTPMHDtl5tg5M4YcHRliTrod106KuXZWzOvE06yebse3F5j5yNHtNAuoc4JOPEFnfQJzfWDLGW78HcoZyiHKJZwLWrsoP6J0UPoo58iZorxFeYXSQxkgZ6RO1h+dvTcIJ3KbFmY+/r+BxYOITLcPycVCyJxn0A8WVb5O5Ms/tF5SiGxVVPKeb6CRYGeGjgHYHpkGlAlxyNK9yUsf9kImvUMKTMB9D38t5Nay/sSzzACau8aAmpZoQKWEfqf9cynFk4HkvNwZgNbKDUvJvjQDKLkZIn/klrf8nPNpQH4RfCNX3Yn/77U3v9fU4jvvrcO8t3Dw3ArZW/QA99Q9oL313eKdEge8U8zKYbeeAe0paUDtqgaoW9gAdmobsFfKW1m1K1xFZRe5ctWpc+VKL/UoHjwD",
            },
            {
                "data": "m=edit&p=7ZbfbpswFMbv8xSVr30B5k+Au65Ld9PRde1UVQhFTkpbVIgzB9bJUd69xweqFJtqqiZF01QRjg4/G5/PjvM5m58tlwV1Q/3xIupQF67QD/EOohhvp7+uyqYqkiN63DYPQkJC6fnpKb3j1aaYZH2vfLJVcaIuqPqSZIQRirdLcqoukq36mqiUqktoItQFdgaZSyiDdLZPr7FdZycddB3I0z6H9AbSZSmXVTE/68i3JFNXlOg6n/BtnZJa/CpI9xo+L0W9KDVY8AYms3ko133Lpr0Vj23f1813VB13cmcjcr29XJ12cnU2IlfP4u/lVmsxJjTOdztY8O8gdZ5kWvWPfRrt08tkCzFNtsSPX+bYfSsk8A0QWiAwgOtMTeIyi1hvMc8kfmiSwLGINc7UqjW19ERWrcgaJ4pMEpt9mDUvxsxazDM1M9+szqxVZtYs2NRcDWZpZrFZy3PMWp5jzsuzZuFZK+8FrkWG1WEDubiNbjCeYmQYr2CXUeVh/IzRwRhgPMM+M4zXGE8w+hhD7DPV+/RdO/kAcjKfoSG+fQUf7f9zez7JyOz2vjhKhax5BQ6ctvWikC/PcNiRjajmm1be8SVYN56F4NHAVthzgCoh1lW5GvYr71dCFqNNGhZQfqT/QshbY/QnXlUD0J3uA9QdQgPUSDhhXj1zKcXTgNS8eRiAV4fnYKRi1QwFNHwokT9yo1q9n/NuQn4TvDMPFt//+Cdx8H8SevGdf82F/yAnU5fUj6k6p2Tdzvl8KeB3Cqv2Nr95J081776B/mgc62C+ePBlwt+TkKNmBHjEj4CO+k7PLesBbpmMLmj7DNARqwFqug0g23AAWp4D7A3b0aOazqNVmeajS1n+o0u9tqAsnzwD",  # a bit slow to calculate
                "config": {"region_size": 4},
            },
        ],
        "parameters": {"region_size": {"name": "Region Size", "type": "number", "default": 5}},
    },
    "nonogram": {
        "name": "Nonogram",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7ZRBb5swFMfv+RSVzz5ASBriy9R1zS5dti6ZqgqhyEncBhXizsA6EeW7970HaWLDDjts62EivDx+fvb7Y/iTfy+lUXwERxByj/twBN6AznMPf4djnhSpEmf8oiw22kDC+efJhN/LNFe9KIAKOOPerhqL6oZXH0XEfMZZH06fxby6Ebvqk6imvJrBEOMBsOu6qA/p1TG9pXHMLmvoe5BPmxzSO0hXiVmlanFdky8iquacYZ/3NBtTlukfijU68Hqls2WCYCkLuJl8kzw1I3m51o9lU+vHe15d1HJnB7nYpZGLyhu5mNZyMeuQi3fxh+WO4/0etv0rCF6ICLV/O6bhMZ2JHcSp2LEgxKnvQEv9bFgwdsDAc4F/2JwDcKcM3SlDd8qwjwBeiFfg6hi6i47cRUMCJ4uGbpcxgZMpY2r7CmAPfNqJO4oTin2Kc9goXgUUP1D0KA4pXlPNFcVbipcUBxTPqWaEW/1bD+MvyInAxehrn4fd/3EvYrPS3MuVghdsWmZLZc6m2mQyZeBolut0kTfjggwPryCwLVVaKNX6KU22dl3ysNVGdQ4hVOuHrvqlNmtn9WeZphaoP18Wqp1mocKAjU6upTH62SKZLDYWOLGctZLaFraAQtoS5aN0umXHe9732E9GJ3wwfT74/7n8R59LfATeW/PpW5NDb682ndYH3OF+oJ0ub3jL6MBblsaGbVcD7TA2UNfbgNr2BthyOLBfmBxXdX2OqlyrY6uW27HVqeGjuPcC",
            },
            {
                "data": "m=edit&p=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",
            },
        ],
    },
    "norinori": {
        "name": "Norinori",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7ZfPbxPJE8Xv+SvQnPswP7rmh28sG74Xll02rBCyIuQEAxZOhnWSLytH+d/5dPfrMU684rAS4oAsdz/X1FTVtF+9nr76+2axWbq6dFXpmt4x8+mG3vmK71DFb6nPy9X1ejl75B7fXH8YNwDnfn/61L1brK+WR3N5nR7dbofZ9oXb/m82L6rCFTXfqjh12xez2+1vs+2x255wqXAVtmfJqQYe7+CreD2gJ8lYleDnwsDXwPPV5ny9fPMsWf6YzbcvXRHy/BLvDrC4GP+/LFRH+H0+XpytguFscc3DXH1YfdKVq5u348cb+Vand277OJV7ksvtd+U2h8oNxgPlBof/Xu7603io0OH07o4F/5NS38zmoeq/drDfwZPZLePzOFZxfB3Hp3Gs4/gSV7dt4vhrHMs4WhyfRZ/j2W3RtA1c6YpZ7cAGHoQ71wxVwl0FNuEa3Ap7cC8MxcpaeAA3CfeBfrL32CvZhxLshaFmpfhDA1Y9gw/UFTawahs652vVFuhdp/jkB6fayA9OcTz94JuUy1fkalIuagFnH3I1KRf5nfcpfmwdr/gV9ftUP/nBilMTxytOTRyvOHXrvJXCxDTFbLC3sjfY22wnfqv4nmdp9Sye+K3ie9ahTetAHuc71ea5t9O9Rm2dajN8evkYPr18Wtak15q0+Pfyhw9efPAtz9LrWeCGFzeoCylR/fAEWREm/qD4HfEHxYczXpzxcMaLM9TirFSuvnVWKWbfgRUTnph4EuTLxBM/1GDFhDMmzpDHWa048MTEE3KC0zpYScw6xbQS/yb5Uws4+VuJfyN/+GPij1XkbVJe6gKnZ6EucFof6nLmFRMumbhkcMnEJWoEKyb8MfGHusCK2fC8lp6X/OBsJ774Q05wWnNyghXTc2+re+GPiT/kBCsOXDJxiZzOxCVygmWHMybOkBOs+C3r0Gsd4IyJM+QHKz6cMXGG/M7EE/KDlQvOmDhjfeXaUjX3Hqw4vYEVB2604gZ5wIoDH1rxwdCNNusG/mjQpDmTpsEZ9GXSmUnf4A/6MmlLM2TNCZomXsEfX4pXJb0j3Ys6k3kbdEa1MU+6h86BxVt4krUODUOvsrbQI3XWFvyzpjVBr9QLDXbxEN0CqzeDhoh7zDsdgw+TjgUN8VlbqCFrlw+6p94MepK1y4iTtcuCjskn6EnWsaAV4lvs/U7+7B2TRgUdyBrV8Sxd1gfq6bI+UE+XNQH/rFfwYdIo+IBeTLox6RX/9aRXYa/JGhVffVQDPJk0Kuw1WaPCnpJ1Kewp+t+Z0aisD/C5FMeCPmROlvhIu9AtcNaNoFHiNntN1rGoA9rLmCe9ipogvUKrwLq3Cfoje9CErEv875PmhH7P2sLeQc/velz/NfNOZ4x6TPVY0Bb1Xeh9k7/hb9mf/s36w56CLuz0IWtR0AftZczg3OPUkzUq6EPWpdD7ne6FMybOMO+0CM6YOIMmoSfy74MWZR3AX3sc806v4MmkUfDBxAfmnRaFPSVrUdhHxIegISZNYAZnbWFNoj7wAvUqvkY9iaOPYxtfr7rwnvad3+S+Wc6cLg4Hgm9/7Kff9/A7PZoXJzebd4vzJaeB47fvl4+ej5uLxbrg2FVcjes3V7o6i6cyTgvYLm8uzpabPdN6HD+tV5f7fqv3l+NmefBSMC5Jd8D/bNy8vRf982K93jOkc+aeKR2H9kzXG846X/1ebDbj5z3LxeL6w57hq2PcXqTl5fV+AdeL/RIXHxf3sl3snvnuqPiniN95w7L7n2fa736mDYtf/mh6+KOVE3k7bg42PeYDfY/1YH/L/qDFsT9o5pDwYT9jPdDSWO93NaaHjY3xQW9j+5f2DlHvd3io6n6Th1QP+jyk+rrV5wUqtgrf4vToCw=="
            }
        ],
    },
    "numlin": {"name": "Numberlink", "cat": "loop", "aliases": ["numberlink"], "examples": []},
    "nuribou": {
        "name": "Nuribou",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VXPb5tMEL37r4j2vAeWH7bDpUrTuBfX/VK7iiKErLVNYhTwugs0FZb/98wMuHiBHlrpi3KIMKOZN+OZxy5vyX4UUkdcOPhzxtziAi7PsekWrku3VV+LOE8i/4JfFflWaXA4/zqZ8AeZZNEgqKvCwaG89MtbXn72AyYYZzbcgoW8vPUP5Re/nPFyDinGXcCmVZEN7k3j3lEevesKFBb4s9oH9x7cdazXSbScVsh/flAuOMM5H+nf6LJU/YxYzQPjtUpXMQIrmcPDZNt4X2eyYqOeirpWhEdeXlV05z10nYYuuhVd9P43usle9RG9DI9HWPBvQHXpB8j6e+OOG3fuH8DO/ANzhvBX3GXaE+YK7PQBSJ2AsZH3XAjh9ajDoRmOsNnodygs/DO8OKdY2GbsOBDDS3WKXas1XdB4A/E8Y6SgmWc9x9ijiW2aed7Btk3SttOKiUXzyLY7MljaHnY85WEZBS3mPdkJWZvsAtaalw7ZT2Qtsh7ZKdXckL0je03WJTukmhHu1l/t5yvQCZwhHQt9l/ee+ZdMOAjYvNAPch2BqmdFuor0xUzpVCYMDlCWqWSZ1XmfzlfQPWA7qjSgRKl9Eu/Muvhxp3TUm0Iw2jz21a+U3rS6P8skMYDqi2FA1cFmQLmGU+ssllqrZwNJZb41gLMD2egU7XKTQC5NivJJtqalzTMfB+wXo5sE775/nV7964SLb721M+2t0aH3Vule0QPco3tAe/Vd4x2JA94RMw7s6hnQHkkD2lY1QF1hA9jRNmB/kDd2bSscWbVFjqM6OsdR51IP2K7Q8UoVLBy8AA==",
            },
            {
                "data": "m=edit&p=7VVNb5tAEL37V0R73gPfBi5Vmsa9pG5Tu4oihCxskxgFvO4CTYXl/56ZARUWqNoeGuVgIcYzbx87zwtvN/9eRjLmhsZ1m5suh1+4pp7LHc0FzLProDXXMinS2L/gl2WxExISzj/PZvwhSvN4EjSscHKsPL+65dVHP2A648yAW2chr279Y/XJr+a8WsAQ4xZgNzXJgPS6Te9oHLOrGtQ1yOdNDuk9pJtEbtJ4dVMjX/ygWnKGfd7T05iyTPyIWaMD643I1gkC66iAP5PvkkMzkpdb8VQ2XD088eqylrsYkWu2cjGt5WL23+SmBzEm1AtPJ1jwryB15Qeo+lubum268I8Q5/6R2QY8Ci+2fifMwdL5Veqapda6BrXZqXG8W09VvoW11da2q9aug8rfwSI0iKHpgOj45TWAiZKmndpWWhouSminNDy1NmlCr60NdT7Txvk6fFqCriTT8VTGtPeEq45b1LHtYGnIN5oa1l2n1b+nOKNoUFzCy+GVSfEDRY2iTfGGONcU7yheUbQoOsSZ4uv9pw/gFeQEdr2T/PnC7/DMO/P+khdOArYo5UO0iWEznJfZOpYXcyGzKGVw7rBcpKu8GffpWILtErA9MRUoFeKQJnuVlzzuhYxHhxCMt49j/LWQ297sz1GaKkB91CpQfR4oUCFhs+/UkZTiWUGyqNgpQOccU2aK94UqoIhUidFT1OuWtf/5NGE/Gd208VrnQ/3VD3VcfO2t7exvTQ59t0KOmh7gEd8DOurvBh9YHPCBmbHh0M+Ajlga0L6rARoaG8CBtwH7jb1x1r7DUVXf5Nhq4HNs1bV6wPalTNaiZOHkBQ==",  # warning: this example is very hard to solve
            },
        ],
    },
    "nurikabe": {
        "name": "Nurikabe",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VVBb5w8EL3vr4h89gED2QUuVZomvaTbppsqihCKvBuSoMA6NdB8YrX/PTMDKTZQfeqhUQ4RYjTzZjx+xjy7/FlLnXIRcuFyL+AOF/As5g73Q5+HTkCv0z0XWZWn0QE/qqt7pcHh/OvpKb+VeZnO4q4qme2aMGrOefM5iplgnLnwCpbw5jzaNV+iZsmbFaQY9wE7a4tccE9695Ly6B23oHDAX3Y+uFfgbjK9ydPrsxb5FsXNBWc4z0cajS4r1K+UdTww3qhinSGwlhUsprzPHrtMWd+oh7qrFcmeN0ct3dUEXa+ni25LF71/Rjd/VFNEw2S/hw/+HaheRzGy/tG7Qe+uoh3YZbRjfghDD2GXaU9YeAih9zsUjoDYNWIfYt+I53YsXGTyARb1gnjeEPEdu6ePPc140HOBHAxOAY5fGDEuwcjTGox+YWD1c2lNRizs/q7A8UbexfmM/AL79f3dANdsxnbec/ALzI14kBe4/pc8bIugzbkie0rWJXsBe8cbj+wnsg7ZQ7JnVHNC9pLsMVmf7JxqFrj7f/V/vAKd2A/omPm/B3/S96o3XJXMYraq9a3cpHA2LetineqDpdKFzBlcA6xU+XXZ5SO6JeD0AmxLlRaUK/WYZ1u7LrvbKp1OphBMb+6m6tdK3wy6P8k8t4D23rOg9ni2oErD2WvEUmv1ZCGFrO4twLhWrE7ptrIJVNKmKB/kYLaiX/N+xv5j9NKx5L/fsa9+x+LHd97aSfrW6NB/q/Sk6AGe0D2gk/ru8JHEAR+JGScc6xnQCUkDOlQ1QGNhAzjSNmB/kDd2HSocWQ1FjlONdI5TmVKP2bbW2YNcpyyZPQM=",
            }
        ],
    },
    "nurimisaki": {
        "name": "Nurimisaki",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7ZXBb5swFMbv+Ssin33AhhDg1nXNLlm2LpmqCqHISWiDAnFmYJ2I8r/32TAltulhh1U5VMRPj58f9hfMZ5e/aiZSTEby5wbYwQQu3wlUIwHcQ/t7LbIqT6MhvqmrLReQYPxtMsFPLC/TQdxVJYNjE0bNPW6+RDEiCCMKjaAEN/fRsfkaNTPczKELYQ/YtC2ikN6d0wfVL7PbFhIH8lmXQ/oI6ToT6zxdTlvyPYqbBUZynk/qaZmigv9OUadD3q95scokWLEK/ky5zQ5dT1lv+K7uaklyws1NK3feI9c9y5VpK1dm/01ufuB9QsPkdIIX/gOkLqNYqv55ToNzOo+OEGfREfmOfHSIsN+uCvJdE/gmCA0wpgYgZGwSatXQkUXMgYklhow9kwSmPhIGBqGOOQ4l5jjUJRYxFVLXVEg9a+TAmj20Rg6t2UPzjbmOvjKwXkSt2qOKExWpigtYVNy4Kn5W0VFxpOJU1dyp+KDirYqeir6qGcvP4p8+nHeQE3vt/vPWBbvUR+919yaDGM1r8cTWKWxXs7pYpWI446JgOYKTAZU8X5Zdf6QODtjQgO1VpYZyzg95ttfrsuc9F2lvl4Tp5rmvfsXFxhj9heW5BtqjUEPtjq2hSsB2fHHPhOAvGilYtdXAxUmjjZTuK11AxXSJbMeM2Yrzfz4N0B+kWuzCi/c+jt13P3bly3eubQ+9Njnqu+Wi1/SAe3wPtNffHbcsDtwys5zQ9jPQHksDNV0NyDY2QMvbwN6wtxzVdLhUZZpcTmX5XE51afUY7WuRFVnJdhlKBq8=",
            },
            {
                "data": "m=edit&p=7VbfT9swEH7vX4H87If4R9o0b4zBXlg3ViaEogqlJUBEUjMnGVOq/u/cOYHETiZtDyAeUNTT3efL3WfHX+3iVxXrhHJOmU9FQD3K4Almkk69gLIZb43XPudpmSXhAT2syjulwaH028kJvYmzIplEbdZqsqvnYX1G6y9hRBihhMOPkRWtz8Jd/TWsF7RewhChErDTJomDe9y5F2YcvaMGZB74i9YH9xLcTao3WXJ12iDfw6g+pwT7fDJvo0ty9TshLQ+MNypfpwis4xImU9ylD+1IUV2r+6rNZas9rQ8bussRuqKji25DF71Xo5s9qDGi89V+Dwv+A6hehRGy/tm5Qecuwx3YRbgjfoCvHhA6bb4KCWYAiJdwzp3xue8AjE1dhA9yOFa1EOEWZgKpdJ2Z70EMm+85nmHVXhwM+s4FIPwl5gzf6CpyLq0KfMCKS0T8Xjy3K0yxQz/GcavCbFAzwHnYCM694yE8dy0Ec6sIbncW3J29EMxFJOb03vHd7yJ8e35iMB8R4Jr1EenZqyiZu4UkRyZdVWnW3c6wmUmBfZ9rwtZkZoNeGntiLDf2HPYvrYWxn431jPWNPTU5x8ZeGHtkrDR2anJmqID/0sgb0Il8af5s/+3xP3I/cl8/dzWJyLLSN/EmgbNmUeXrRB8slM7jjMCxTgqVXRXteGhOfTiNANuaTAvKlHrI0q2dl95ulU5GhxBMrm/H8tdKXzvVH+Mss4DmJmNBzXFrQaWGs7QXx1qrRwvJ4/LOAnrXBKtSsi1tAmVsU4zvY6db3s15PyF/iPnBXyKDi8XHnemt70y4+N57OxXeGx2zb5UeFT3AI7oHdFTfLT6QOOADMWPDoZ4BHZE0oK6qARoKG8CBtgH7i7yxqqtwZOWKHFsNdI6t+lKPyLbSaZ4W8X1KVpMn",
            },
        ],
    },
    "onsen": {"name": "Onsen-Meguri", "cat": "loop", "examples": []},
    "ripple": {
        "name": "Ripple Effect",
        "cat": "num",
        "aliases": ["rippleeffect"],
        "examples": [
            {
                "data": "m=edit&p=7ZdPb9tGEMXv/hQBz3sQyV3+0S1NnV5St2lSBIEgBLJDJ0Jky6XlppDh757fLN+Klq2gQIG2OQSSdp+Gw5kh983j8vqPm0Xfuby0b9m4icv5hLKIv9z7+Jvo83q5WXXTJ+7pzebjugc498vz5+58sbrujmbymh/dbtvp9qXb/jSdZXnmsoJfns3d9uX0dvvzdHvstq84lLkc24vBqQAej/BNPG7o2WDMJ+ATYeBb4NmyP1t1714Mll+ns+1rl1meH+LZBrOL9Z9dpjrs/9n64nRphtPFhou5/ri80pHrm/frTzfyzed3bvv06+WWh8o144FyzeFfLred391x23+j4HfTmdX++wibEb6a3jKexDGP49s4Po9jEcfXuLptGccf4ziJY4jji+hzPL3NyknjyiJk08JlZZ6DG+HKlWUp3IKrARfYvewF53qdW+Dj5VPCwjARDuBCmHODzvUFuBX2rqxyYXyq5FODvTDxK8UP1FmpzkCuWrkCPrV8qgm4FiZXrVwVuRrlqqitUW0VuRrlqojTKE5NnEZxanxa+dRce6trb/Bp5dNQW6vaGvK2ytt45yfK2wSw8jYVWNfb1GDFb/HP5d/in8u/xSdPPg14qIHY4CEvscFDXmI7Xwz3h9jgISaxwfJHNXwpnxyfMvmQtxzy+py85ZCXeODheokHVhz44MUHDx+8+EA8sHxK4gfFhw9efPBwwIsDxAArL3zw4oOHD158IB5YueCGFzeIDVauwH2odB/giRdPfCB+rfhww4sb5HG+kQ888eIJecDJn3oa1QNnvDhDHrBqgDNenPE19TSqpyZXo1zwx4s/5ATLH854cYbYLogzxAMrV9OClQtuBHHDtxVYtcGNIG4EOBDEgTDBvxj8OQ885MLXHhYDZn2D1hdfsDhc0C/FPR0oxPmCvki6YZqgmFETxCtmsPgMH0rlYh51xnRDHGMGq788/l7+phtJf0w3kv6YbnjVY7ohvjGDk85QT9KlQD3iIfo06pLpRtKiynQm6QM+SZfgyU6XTE/EQ/QJnDSHvOJeWXPfki7V+CRdMg1JumQaknTJdEMcYx51CT6gHTsN2WkUGrLTKHhSim9la/qjOC1xknbBjaRLUQcSf+ADWjBqgnQm9n7SFp4FOz2BA14cYB71xHo/6QnrvtMT04GkJ6y717ozj9pimpC0pTTNUUyPj0+9jz3piemA1jf2vp41sfeTtljvB50bTH/Ud6YDQX3Euu/0h3Xf6Y/1u9Y09nvSFuvrpCHWy0lDatMBXTvPgp1uWF8n3WBNd7ph+p+0wvQ/aYVpfpt6HLueKdbXO31oTQdSX9Oz0gpmsHqZZwH9P+qANCTqgDSEGax+Z92D1p151BDTh1z+7A1CnvzRJXGDGZz0hNqS5pie6LnDLP1hA/ImbkOexdHHsYrbk9r2Of/xTuhvy5nBTNtWH/qE70f+yZH50Sw7fv+he3Ky7i8WK/bEJzcXp12f/vMSkl2vV++ub/rzxRlb6viOwq4Z22X03DOt1uur1fJy32/54XLddwcPmbEj/QH/03X//kH0z4vVas8wvHXtmYaXgz3Tpmfnf+//ou/Xn/csF4vNxz3DvbeEvUjd5Wa/gM1iv8TFp8WDbBfjNd8dZX9l8TfjPdH57294/9Mbni3B5FtTt2+tnMjedX+w9TEf6H6sB7tc9keNjv1RS1vCx12N9UBjY33Y25getzfGRx2O7StNblEf9rlV9bDVLdWjbrdU9xt+lvXLq6tV96Q7P+/ONtn86As=",
            }
        ],
    },
    "shakashaka": {
        "name": "Shakashaka",
        "cat": "var",
        "examples": [
            {
                "data": "m=edit&p=7VhLb9tGEL7rVxh73gOXr6V4S127F1dpGhdBQAgCLTOxEMp0KakpaPi/Z14xZyUFKXIwGkCQtDvfPHZHOw9pufl7V/eNTSJ6FzayDl/OFzJ4l/MQyet6tW2b8sy+2m3vuh4Ia19fXtoPdbtpJpVozSePw7Qc3tjht7IysbH0cWZuhzfl4/B7Oczs8BZExqbAuwLKGRsDeTGS70iO1DkzXQT0jGkP5Hsgl6t+2TaLK5AC54+yGq6twX1+IWskzbr7pzFsRnjZrW9WyNjc1Z9qYW52t92nnai5+ZMdXpGnon3E3WR0F0l2F6kXd3c6f3qCE/8THF6UFfr+10gWI/m2fDQ+M2VqTeFpctmU5zzlWcTOC79IZGb9OJe5cDKzXTxlvXha0Jw4licx85M05jkXuaybFDnNacrrpuJPmrM8lf1S2T+LWD/zvF4m62Rf5VPeN4+YnyeCE/YzFz/ynGcfs9zHbO8TtvMJ7+MT9sdnkczsv/c8F2JfCL8Qvwvxu/Aifz521pvG7M80ZeyiiBWBkAhETkIUpRKDSA7JRTl7AwQqQ2RnEtkqtp4LjSJcJc+QIq3EFPHKjZjMNUZ9hfGkA4zrj5gyQ2PMELUfZYrGmDFaHzNHYcogjTGTNMZIYs08MzC1tAI5PG5IqaYwpZzSp9TTGEMZ4D19OoBxPUpNjTFFK3M2ekjJqlagpNUYk1dhSmKNMZlVSCmpNaYjGT2gJFf2lOxKn5JeyzH5tRyLIMDhCVFRBBgjMO5PRRKcAJWLsqCy0XjvzKmMNMZyCnCYtFRewY5UaEqDCk6XARVelWoGrqkKhwpRZz4VZLAGpZI2wQINTLBQnzWgYF35CON7Gi9pjGm8hk5th4TGX2mMaMxovCKdCxrf0XhOY0pjTjoee/1//DXgzvEC7lRe/ln80Cs72Z5sT7Yn25Ptyfbntp1PKvN213+olw3c5Ga79U3Tn826fl23gM+79UO3WW0bAzdos+naxUZ0S7pgw70PePdkFbDarntoV/eh3urjfdc3R0XIbG4/HtO/6frbvdU/120bMPixQcDim23A2vZwbVW47vvuc8BZ19u7gHFTb+HxwuZu9RCu1NxvQwe2degi3Iz3dluP3/lpYv419IG/YA7u8KfHEy/+eAJPP/q//S39jjsV5AFc42xlMoi0/Jd/2C3qxbKDcoUD/KoxvP6G4Cc0vfgRU3ic8B1T1Ng3ffF4U2fo+qNtFdhHOitwj3ZQ4R80UeAftEvc8LBjAvdI0wTuft8E1mHrBOZB9wTeNxoorrrfQ9Gr/TaKWx10UtxKN1Mpda73+eQL",
            }
        ],
    },
    "shikaku": {
        "name": "Shikaku",
        "cat": "region",
        "examples": [
            {
                "data": "m=edit&p=7VbNT9tKEL/nr0B73oP3w583oKEXmlcKTwhZUeQEAxFOTG2nVI7yvzMzzmN3HVdqD/RxQJZXM7/52N+sd7xbf99kVc6l5kJzFXGPC3hi3+N+6PFQC3q9/XO1bIo8OeLHm+ahrEDg/J+zM36XFXU+Svde09G2jZP2grefk5RJxukVbMrbi2TbfknaCW8vwcS4AOwcJMG4BHFsxGuyo3TagcIDedLJIYg3IC6W1aLIZ+ddoq9J2l5xhvOcUDSKbFX+yFkXRvqiXM2XCMyzBoqpH5ZPe0u9uS0fN3tfMd3x9rijOx6gqwxdFDu6KL0V3fz2Pq838yGu8XS3gzX/BmxnSYrE/zViZMTLZAvjJNmywMNQH6h1H4aFMQDBqxqFaDfmWIIeGVWjOTB24Qni4tmQAkhbeuTmFALnjI0uMcBMIiQGGE5CIQkroUZ/ZfQAWVn5QizSig/RbsWHmN/SI6zBt3Scz4qP/H7VEVZgZYiRkYmQnrts0qMMJoEUtJA2gAtvZfBdztJ3Z5Shy1GGGG/Zox6jCGu2GPU+rIyRoZAW4G4M5SEhE6Cku8iKPqKJVxrtlr8OnEVWvvvRFRVo6UFv16gQGZqvrCKcwFSs+ltXxZhBwL9sD2iBU9qAxBCraK3cnaUVFm2K1FTUawD0lKDOuoHO6nal4NbvZXaCPzKwn5GXpPEKWpK3isZPNHo0+jSek8+YxmsaT2nUNAbkE2JT/1Hb20TfiE7qR3SA/P7jf/h/+P89/+koZWM4So8mZbXKCjhOJ5vVPK/+0+HywuqymNWb6i5bwFFMdxs4cAFbk6cDFWX5VCzXrt/yfl1W+aAJQTzJB/znZXXby/6cFYUDdLc1B+ouFQ7UVHBjsPSsqspnB1llzYMDWJchJ1O+blwCTeZSzB6z3mwrU/NuxH4yeuFvKrj+uBn+HzdDXH/vvR0U740Obd2yGux7gAdaH9DBFt/jB10O+EE/44SHLQ3oQFcD2m9sgA57G8CD9gbsFx2OWftNjqz6fY5THbQ6TmV3ezodvQA=",
            }
        ],
    },
    "shimaguni": {
        "name": "Shimaguni (Islands)",
        "cat": "shade",
        "aliases": ["islands"],
        "examples": [
            {
                "data": "m=edit&p=7Zddb9tGE4Xv/SsCXrXAXvBjlx+6S/M6vUndN3WKIBCMgLYVR4hkppTUFDL83/Ps7lnLshUURQskF4Eg8nA4OzPkzDlarf7Y9OPMFM4Upalak5uCT523xnbWNC4P3/R5NV8vZpMn5ulm/X4YAcb8+vy5edcvVrOjqbzOjm623WT70mx/nkyzIjNZybfIzsz25eRm+8tke2y2p9zKTIvtRXQqgcc7+Drc9+hZNBY5+EQY+AZ4MR8vFrO3L6Ll/5Pp9pXJfJ6fwmoPs+Xw5yxTHf76Yliez73hvF/zMKv384+6s9pcDh828i3Obs32aSz39EC51aFyvfHrlNud3d7y2n+j4LeTqa/99x1sd/B0csPxZHKTFXnN2pJmh9ZkRZlzbe9dl1xX965brv1w+GuCFCHUm3B8Ho5lOL4ik9lW4fi/cMzD0YXji+BzTAFV2ZjKUkRpwB2YBB5XDKIrhC24Eq7BTrgFNxFb1tZa6wpTNTxIwKxttNaxttHaumLQebiAqaFVDTUxW8VscnAnTD2d6mmI2Slma43NE+7AqqHLwVrblcYWWttVYOWFW7bQ2s6BbcA2x15Gu81rcKzZ5g041mkL4pcxPvGMrWJ84oFjfOKBFafEv5J/WRhr4/shD1j+JTVY1UBfrPpCHnB8LvIY67SWHln1iNhg+Vh8avlYfGr5WOqpVY8lV61clly1clk0p47v39JTq56SE6z66a9Vf8kJln+NTyOfmryt8tbkapWr5n22ep/02qrXxAYrV0M9neppsHeyt4VxufK2JVjxWwdW/LYBa23bghW/q40rlLfDXkQ78cCxZpdXxnnCBWzB8V25nPhljE88cIzv0GdXKk5B/CrGdwX2Snb67tR3R9+d+k4MsPzptVOvXclaq7VwzYlrDq45cY0YYMWkp049JQZY/vTUqafwG14nnnq+iyP0Gt6Km/DRxWcMnE0c95xNHKen8HbHX80PZ3DitQMnLrNWsxS43CT+en0QBz2vkz54Xid9aIjTKE7jdUNx6HvVJr57DVEN6EClueK805OWtUlPmI1KM8Z5py1oxZ22oBV32oI+oAvivtcTzVvO/OfibM6cS384g+9pSJ7WMv9pJr2epJn0eiK94nynV5zRIs251xlpV9AZ6VXQk1J2ryeaW8477WLG0BHpg9elxHfW2qQJXnMS9/HXnATuJ52pvZ4ovud10hBm4E5DmAF4Luz1RM/leZ20wnO5TfylhqQP9NSqp5x3WuG1PWkF/bLqF2c0QXG8zqt3nuO2S3z3GhJrQCfQgcRrrxuJ1/Bd/QocV48Cx9UXh4Yn3QgcT7pR4FMknw4dSLwmV9IQtP1ONzzH/Y934DK5KuWqsFfJTpykD57j6hFnsGKi584mvhNfvxdBB4Ke8MP+Ovy8PwtHG451+Nlv/PbjH21Q/v0O42/LmfKkfkPzpQ974u93/4u7Z0fT7HQzvusvZmxejy+vZk9OhnHZL7g62SzPZ2O65r9DthoWb1fynoS/Fmx2sV0Hzz3TYhg+LubX+37zq+thnB285Y0z0h/wPx/GywfRP/WLxZ4h/lnaM8U9/Z5pPbJhv3fdj+Pwac+y7Nfv9wz3Nvd7kWbX6/0C1v1+if2H/kG25e6Zb4+yv7LwDft4+/2P2Vf6Y+ZbkH9r6vetlROmdxgPUh/zAfZjPchy2R8RHfsjSvuEj1mN9QCxsT7kNqbH9Mb4iOHYvkByH/Uhz31VD6nuUz1iu091n/DTjPjL/mpzPX/yw3y16K8vVz9mZ0efAQ==",
            }
        ],
    },
    "simpleloop": {"name": "Simple Loop", "cat": "loop", "examples": []},
    "skyscrapers": {
        "name": "Skyscrapers",
        "cat": "num",
        "examples": [
            {
                "data": "m=edit&p=7VTBcpswEL37KzI664AA24Rbmsa9uG7TuJPJMIxHtknMGCxXQNPi8b9nd6EBGXLooa0PHdDO7tsV+yT0lH0rpI64EPg6Hrc4eNwdjmgIYdOw6mce50nkX/CrIt8oDQ7nnyYT/iiTLBoEOBOecHAoL/3ylpcf/IAJxpkNQ7CQl7f+ofzolzNe3kGKQS0vp1WRDe5N495THr3rChQW+LPaB/cB3FWsV0m0mFbIZz8o55xhn3c0G12Wqu8Rq3lgvFLpMkZgKXNYTLaJ93UmK9ZqW9S1Ijzy8uptuk5DF92KLno9dHEVf5iuHR6PsO1fgPDCD5D718b1GvfOP4Cd+QfmuDDVhf9Ff4Y5IwjHTehBOHwNXcsIRzaEzmvojY25l5iFc1OHQmDaa2Ib863YxXyrfoh5OHu/Ym9oMBXUriEjvMtWe1idoDU+kJ2QtcnOYQt46ZB9T9YiOyQ7pZobsvdkr8m6ZEdUM8ZN/K1t/gt0Ahf30nxwN84ICQcBmxXpMtIXM6VTmTC4I1imkkVW6Ee5ghNPVwgcasB2VGlAiVL7JN6ZdfHTTumoN4VgtH7qq18qvT75+rNMEgOoLkUDqrRrQLkGYbZiqbV6NpBU5hsDaInY+FK0y00CuTQpyq086ZY2az4O2A9Gg0Tp/r+A/9EFjL/AOrf74dzo0OlVulf6APeoH9Beldd4R+iAdySNDbuqBrRH2ICeahugrrwB7CgcsDdEjl891TmyOpU6tuqoHVu1BR+wbPszW2m5j3TGwsEL",
            }
        ],
    },
    "slither": {"name": "Slitherlink", "cat": "loop", "aliases": ["slitherlink"], "examples": []},
    "starbattle": {
        "name": "Star Battle",
        "cat": "var",
        "examples": [
            {
                "data": "m=edit&p=7VhNbxs3EL3rVwR75mFJ7pJc3dLU7sV1msZFYAiCsbaVWIjkTVdSU6zh/5435ND6IoF+oEEPgqTV03A4MxzNI2d39fum7WdCWnprJ0oh8TKu8h+lSv+Jr6v5ejEbvxKvN+uHrgcQ4u35ufjYLlaz0YRm4jUdPQ3NeHgnhp/Gk0IVwn9kMRXDu/HT8PN4OBPDewwVwkF2ASQLoQDPtvCDHyf0JghlCXzJGPAa8G7e3y1mNxdB8st4MlyJgvz84GcTLJbdH7MiTPO/77rl7ZwEq3Xbs2y1ue8+b1hLTp/F8NoHysqJaHUqWhImoiWF/yzaZvr8jHz/inhvxhMK/bctdFv4fvyE6+X4qagdTdWIwv8pkEo/dk1jDcYUXHhvigbP/aDy1yvYEoP21x/9tfTX2l8vvM4ZzFSuEbUsizFMVU0JLBnXwIaxAbYe1yX0ddCvpQLWjKGvg34tHTDiI6ygX7O+roBrxtCvWb+CXxP81hX0LevX0LGsUyMGyzEY+HXs18JmwzYtdBrWsYih4RhsI0zJNh0oUyrGCpjtNJBLljeglGSbWLuJa28sMP4Tjx0w229gXwX7poQdFezAD3CwDz/AFWPYV8G+kZBrliOHhnNoJPzq4Nco2KzYpsLciudq6NSsoxEb1QvhCn4N+62gb1gf+TScT8wDZv0a8TuOH7k1nFtjaGvhuQa+HPuysNOwHeTWcm4Ncms5twa5tZxb2p5syXacAw55s8iV5VxZ5MRyTiz2N6tDbFZpYauQH4u1W1671aWwdagZqxGDCTFAF5h1qho4xGlr6FvWN/Dr2C/WaHmN1sCvY78W+g3rOy1cyTFgLY7XYsEdx9yx4I5j7niOsBx8Aua6Io4wp8AnYK4l4kjklNbAwZfnSOQU1giebDkSOYW1gA+Md7hDvLCRFzs8Io5EHhFHLNcw/jvwgTFicBwD7QmcB+LFC9doT4hcAxci18AzcCro+zqP/zv2CtT6traZU+DTC4/AIfCC56od7lDNR75gDzE64h2+UJ1HXlCd896C7y1HaviifTPWeeQI1XnkiMFcrhlf55EvyBVqnWsYcTqOk/aQyBd/FMc6B7+4lgz20sgXcAX1z3WF/SFyBN/AXGPEhVhjqCUbawx5AzeYC5jL+fG8iNwhXujIC3CN92HPi8gd4kLkjgHmvddzIXIHfAcftlyI3CFe83qJCy/cIV479oWaCdzBIfPBHzVv/LXyV+OPIEuH3ek4PB2Hp+PwdByejsPTcXg6Dp9HE7jhW/PkC7f+p9H/9+h0NCneb/qP7d0MDwEuN8vbWf/qsuuX7aLA45Zi1S1uVjw+9k9j0LRA9ug190SLrvuymD/u680/PXb9LDlEwtn9p5T+bdffH1j/2i4We4LwfGlPFJ6D7InWPR5y7Pxu+777uidZtuuHPcFtu8azqNXD/Mu+pdnjej8A6t32bH9uD7wtt2t+HhV/Fv4z0Uh8dXqW9b2fZVHuy7/Vwu+27P+sQ/+3dxST4Vpgzx7eiuLL5qa9uesWPjFeLg/kSGFSjiwn7bBcooFJDqChSjo4kkcHLufgcAA1kB7IhlSx60yoUmcWLdG5JAcanbNkMhPqvyjnvyenL9EzJQdsJq3o0TNJyq05tzaFlis9gN4kPYCbpuSARkebHqgyUSn0YOkZaIbSM3Bnk56BNi9jKrfAXPEr3L1mkngYLle/RG+enoHGNWMqk8RjH3EglyuV/c9zuVJoU9MzcO+RSUlmgQodYybtuSrJ8VXbjHONjjk9UGfWoXGPlllHZts5HogzcuGq3JancgUnXW4gsdt+90PHNyddn+zsIE40d5AmmziWH/VxkB91bOTwuGmDNNG3QXrYukF03L1BeNTAQZbp4cjqYRtHUR12cuTqqJkjV7v93GQ6+gY=",
                "config": {"stars": 3},
            }
        ],
        "parameters": {"stars": {"name": "Stars", "type": "number", "default": 2}},
    },
    "statuepark": {"name": "Statue Park", "cat": "var", "examples": []},
    "stostone": {
        "name": "Stostone",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VZNb9tGEL3rVwQ874HcD+6SNze1e3HVpHYRBIRgUDYTC6HMlKKagob/e97szkKixKIoekgKFJJWj8O3s498M0vuft/XfSOyTGSpUE6kAkhokwudOWEy638pf243Q9uUr8TFfnjsegAhfrm6Eh/qdtcsKmatFs9jUY5vxfhTWSVZIhKJX5asxPi2fB5/LsdLMd7gVCIcYteBJAEvD/CdP0/odQhmKfCSMeB7wPtNf982d9ch8qasxluR0Do/+NkEk233R5OwDjq+77brDQXW9YCL2T1uPvOZ3f6h+7RnbrZ6EeNFkLuckavm5FLw28gtVi8vuO2/QvBdWZH23w7QHeBN+YxxWT4nucZUA6/JGcQyf+a9H6/8KP14i4liVH780Y+pH40frz3nEvmkLITUSCrht1LAjrEGLgLWwCbiXMg8Y+yAFWPkIXGETQacMwbHMieXwJYxclrOmSOn45wWHMccCz2O9VjwHfMt+EXkW2DJGBoK1uCgoWANzgqVMsc5YNbjCmDmFxkw8wsJzBoKDczrFrlQWVgX+YADB/mAg07kAw58lRqhZMoYc2WcCz0y6EFu4KAB+YRSHEcbKxV0Ih8wcyT6XRnG0KyCZiWxlua1FLRp1gZPFXuKHMCsTWEtw2sp5DecXyOecxz+KvYX84CZA38V+4scwLyWgQbLGuC1Yq/BxR7F154jv+P8lvaucC2+xnTEBjjWD3xknb6WYh0aqrewFv4PNZlT7TGf6i3Wp0XcxjqhOoxx1JjlGqAas6zBQoM91IMsmF+AzzXmvU7ZC/Ka6wc1gho48jHWg8Q9kXw/JXyJvkvkkdFTqpnoKdVM9BFzYz0ocKLvChwVOVQ/0Wuqn+g1vIu1oXHPNXuhoVNHr6kGmGPAMcwx0GZYG/lrou9Y10R/qQZYW47r8nWCDead32Ze+1H7Mffbj6Vd7R/te/9+p/tbORXuMD1ETz+02f7no6tFldzs+w/1fYPn0OXDx+bVsuu3dYuj5X67bvp4jNeAZNe1dztml/4tAc8txJ48cxJqu+5zu3ma8jYfn7q+mT1FwQbLz/DXXf9wkv1L3baTQHjvmYTC43kSGno8e4+O677vvkwi23p4nASOntOTTM3TMBUw1FOJ9af6ZLXt4ZpfFsmfif9Vit7P/n/H+kbvWGRB+r3tON+bHF+9XT/b+gjPdD+is13O8bNGR/yspWnB865GdKaxET3tbYTO2xvBsw5H7C+anLKe9jmpOm11Wuqs22mp44avkt3Q4YvQavEV",
            }
        ],
    },
    "sudoku": {
        "name": "Sudoku",
        "cat": "num",
        "examples": [
            {
                "data": "m=edit&p=7VXRTtswFH3vVyA/+yF2EjfJG2OwF9aNwYRQVKG0BKhIG5a2Y0rVf+fcG0OctNM0TdN4mNK6pyfOOdf3+sbL9U35sJYxLj+SnlS4/MjjbxTQx7PXxWxV5MmBPFyv7ssKQMpPJyfyNiuW+SC1s8aDTR0n9ZmsPySpUEIKja8SY1mfJZv6Y1KPZH2OW0IqcKfNJA143MJLvk/oqCGVBzyyGPAKcDqrpkV+fdown5O0vpCCfN7x0wTFvPyeCxsH/Z+W88mMiEm2wmKW97NHe6dJg52rxltZH/bCpXBsuH4bLsEmXEJ7wqXH/nK48Xi7Rdq/IODrJKXYv7YwauF5ssE4SjbC919W2tRG+AERfksEhgjU7pUYEjFsiZAfCRwi7M9gDeMQcc/FeETEDsEukUNEvTgMa4QtETPhPKI8VnUiU57qrVd5fV3lsY4Ti1K6Z6UU581ZgFKcBddd73hp1nHnNOl2vXxO3muuUCfF1bri8YRHzeMFiilrn8f3PHo8hjye8pxj1FhFRipKjoZiHEtNywHGr9QadoR1KLWPVBBG++sQwRMOldQGQRI2gdRD1IXwcCh1jPQSjvGS8JAQ0o+g71l9D/rK6ivoa6uvoR9Y/QD6tIHYC/pUd/aCfmT18QLScaOPX3hhO7EOxW957QNbHQ0dd136Zb4Btvoa+m48uskPfpEH6+vD17dxGsqDXZeBr7G+Br5ufoz1NfA11tfA110XbWXG8KVdzBi+Q/JF0S65dEc8BjwaLumQuve3+vvPd88vw0mRPToq3Ct8W8x4kIrRej7Jq4NRWc2zQuBwEsuyuF6uq9tsilctn114m4Jb8MwOVZTlYzFbdOfN7hZlle+9RWR+c7dv/qSsbnrqT1lRdIjlt3VWdR9uDo0OtapwIjj/s6oqnzrMPFvddwjn9Ogo5YtVN4BV1g0xe8h6bvN2zduB+CH4m/pId/D/5P9HJz+VwHtr74e3Fg7v3rLa2/qg93Q/2L1dbvmdRge/09JkuNvVYPc0Nth+b4PabW+QOx0O7idNTqr9Pqeo+q1OVjvdTlZuw6fjwTM=",
            },
            {
                "data": "m=edit&p=7VbLbuM2FN37KwKuuRBJiXrs0jTpJnUnkxRBIBiB7CiJEdlKZbsZyPC/59wrOnrYg2IwKJpFIZs+OiLPffGKXm0eypeNjHGZSHpS4TKRx9/Ip48CS/zNfF3kyYk83ayfywpAyj8uLuRjVqzyUUpzcE1G2zpO6itZ/5akQgkpNL5KTGR9lWzr35N6LOtrPBJSgbtsJmnA8xbe8nNCZw2pPOCxw4B3gLN5NSvy+8uG+ZKk9Y0UZOcXXk1QLMq/c+H8oPtZuZjOiZhmawSzep6/uidNGtxcNdnJ+nTgLrnj3DWtuwQbdwkdcZeW/cvuxpPdDmn/Cofvk5R8/7OFUQuvky3GcbIVRu0jbWojTECEbQmfZ6B2H4QmIu4QIRF+h4iICFsiYFHTIeKBqGWisyT0Bn6ErBG0RGyGBJuNOsRQVHkHjBqqKM2WewynoBOx0naQNqU5CR3jyrByj+E5HzoogeJC3PF4waPm8QZ1krXh8VcePR4DHi95zjnKpyIrFYWpoRjHUisUBxi/UmtkjLAOpDbIDWF0tg4QDuFASW39Bltf6hDuEQ5DqWMkgXCM/vcQCOlH0Pecvgd95fQV9LXT19CnHUPYh37g9APoW6dvoR85fbxbNBWSbRnYQmJZh/x3vDbATkdDpxsXFYKxBXb6Gvpdf3STH/wiD86ugV3a++wP5cHFZWHXOrsWdrv5sc6uhV3r7FrY7cZlnV0Lu7SnGcMubWfOoUG9MB/1QcGwQMEJugFoIuMbLhmW843B+gA+8U1ATjmBJpN7gQgC8V4gDpDLvYCHV3eMABs78NhDVI0duKkQCt/4yAnlrbGDRPhwurGD6IO9QEgh7wUiCIROwHgQiFgA2/OWN+kZjz6PljdvSK+gH3pJ/Xyf/KM7KRJB5133Cj4XMxmlYrxZTPPqZFxWi6wQOGHFqizuV5vqMZvhvOADGEcCuCXP7FFFWb4W82V/3vxpWVb50UdE5g9Px+ZPy+phoP6WFUWPWP21yar+4ubk61HrCsda5z6rqvKtxyyy9XOP6ByBPaV8ue47sM76LmYv2cDaoo15NxLfBH9TtKj0///78h/9faESeJ/t/fDZ3OHdW1ZHWx/0ke4He7TLHX/Q6OAPWpoMHnY12CONDXbY26AO2xvkQYeD+06Tk+qwz8mrYauTqYNuJ1Pdhk8no3c=",
                "config": {"diagonal": True},
            },
            {
                "data": "m=edit&p=7VVNb9s4FLz7VwQ88yBSEvVxy6ZJL6m3abIIAsEIZEdJjMhWVrY3hQz/98x7YmpKVlEUxaI5FLKp8YicGZJ69GpzVz1tZILLj6UnFS4/9vgbB/Tx7HU1X5dFeiSPN+vHqgaQ8u+zM3mfl6tilNlek9G2SdLmQjYf00woIYXGV4mJbC7SbfMpbcayucQjIRW487aTBjzdw2t+TuikJZUHPLYY8AZwNq9nZXF73jKf06y5koJ8/uLRBMWi+q8QNgf9nlWL6ZyIab7GZFaP82f7pF0G21dNdrI57sWlODauv49LsI1LaCAuDfuf4yaT3Q7L/gWBb9OMsv+zh/EeXqZbtON0K3xFQ7Ezqt0b4YdvU7dE4BPhO0TUGxLykMAhkt4Q5TFjHEaxbOgwmqNELsPC7iifR8Uuw2m+jcK0FE/uhtszbjW3V5i7bHxuP3DrcRtye859TrEkKjZSJQisoZgkUivNGHepKRJhHUrtxy1GtegQ4QmHSmoTtNgEUkeIRziKpE68FieoKQ8TIf0Y+p7V96CvrL6Cvrb6GvqB1Q+gH1r9EPrG6hvox1Yf9aqTVh93eBmrQ/ktr31gq6Oh485Lv/U3wFZfQ9/No9v1wR3rYH19+NL7xHloHey8DHyN9TXwddfHWF8DX2N9DXzdeRnra+BrrK+Bb0S+2LRr3roTbgNuDW9pRC/7T5XDr789P4yTYfXoZHWv8H0xk1EmxpvFtKiPxlW9yEuBs1ysqvJ2tanv8xlOJj7qcfiAW3LPDlVW1XM5X3b7zR+WVV0MPiKyuHsY6j+t6rue+ktelh1i9e8mr7uD2zO2Q61rHKDO77yuq5cOs8jXjx3COWw7SsVy3Q2wzrsR86e857bYz3k3El8FfzMfyx38+aP8TX+UtAXeezsf3lscfnurerD0QQ9UP9jBKrf8QaGDPyhpMjysarADhQ22X9ugDssb5EGFg/tOkZNqv84pVb/Uyeqg2snKLfhsMnoF",
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
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7ZbRT9s+EMff+1cgP/shtpM0ycvEj8FeWDdWJoSiCrklQEVad2k6plT93zmf81tsJ5s2TUI8oKin68d3vq9dX53tt52sCsoZZSEVCQ0oeDQRMY3G4DPGjQna53JZl0V2RI939YOqwKH009kZvZPlthjlbdRstG/SrLmgzYcsJ4xQwuHDyIw2F9m++Zg1E9pMYYjQENi5CeLgnnbuFY5r78RAFoA/AT8EH9xrcBfLalEWN+eGfM7y5pISXec/zNYuWanvBWl16O8LtZovNZjLGhazfVhu2pHt7lY97tpYNjvQ5tjInQ7IFZ1c7Rq52vPltuv5d7nlRg0JTWeHA2z4F5B6k+Va9dfOTTp3mu3BTrI9iWKd+g5UUNhMmC9KNIAf6X+QIBAdSJkHWCCQ2IhhFpwXi3FM5NyqxkTLbBQiclJjU9OuEGOYW2Hsi2dpX1qKS7YIDwyx8niQ+rq4GBtdNsIoWEOHor56HmGYtWwe41y2hhhj7Kyxv888MQosUSLAcroNfhJcjB3DMMZWKRjO5BCzYBuJyJ8pxDRrISIy+2sRszR7niTwsxLMsvdI9I6ZSLG8Q9yp4QgzPMjXaM/QcrSXcM5pI9C+RxugjdCeY8wp2iu0J2hDtDHGjHWn/FUvvYCcPIL/4D98orfIt8jfPbNRTqa76k4uCrhLJrvVvKiOJqpayZLAtU22qrzZtuMZ3upw2wBbY6SDSqU25XLtxi3v16oqBoc0LG7vh+Lnqrr1Zn+SZekA86biIHOdOqiu4K60vsuqUk8OWcn6wQHWa4AzU7GuXQG1dCXKR+lVW3VrPozID4KfXMDGh2/vRC/+TqQ3P3ht/+avTQ6eW1UNNj3ggb4HOtjfLe+1OPBeM+uC/X4GOtDSQP2uBtRvbIC93gb2i/bWs/odrlX5Ta5L9fpcl7JbPSe13EgyGz0D",
            }
        ],
    },
    "tasquare": {
        "name": "Tasquare",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7Zffb9s2EMff/VcEfOaDSFGyrLeua/aSpWudoQgEw5AdtTEqR55sr4OC/O+9O6qjSN6wDciKPQSGiONHp+Pxx30tHX87130jtZIqk2khEwmWLNJc5kkhdTqnKxl/N7tT25QX8tX5dN/1YEj59vJSfqzbYzOrRq/V7HFYlMM7OfxUVkIJKTRcSqzk8K58HH4uh1s5LOGWkAbYlXXSYL5x5ge6j9ZrC1UC9vVog3kLpk1+fWXJL2U13EiB4/xAT6Mp9t3vjRjzwP622292CDb1CSZzvN8dxjvH8133+Tz6qtWTHF7ZdJdMuqlLF02bLlpMuvmzpNseOi7RxerpCRb8PaS6LivM+ldnFs5clo/QXpePIkvx0QvIwu6KyBYByJMQ5ADMn925Du4vsgCoJHRRCcYoXF8p6GvX1/PwCYOJulGVQY/JE1nh93P0V3iCR1CE81BFMGiBITyPBXpMiVboMwmrNQI3E53iXKd9XI2F6xtMww2qTTREbnAI148WWBcYcxKjCFdLL8LJ6kXok9IeuChpgjufuj7ticsjVf6Kpwr93Y6kKcbzRjBIJhEynNlkhCzKKQ9XI6XT5pE5PuWimmAeJsEdcXkZFa6fUeGhNyo8s4Zm5xHtx4ECUlRGt9/KCLhX1baWIkoFFVO7VgGlvY8oVVhEbZkxmI1sSy7GVHkxpvJjMO9NxRhjW5MRpspkMJ8gVWmMqVQjPNZrhKlqY0zFy2B2vW0pM5jPZCzrEPM7bEucwex623JnMOttC5/B7Gn9JgMR5mNT2cSYtCHGo0CEmHSCwfyQpBkM5mOP6hFgKyIMZs+JlRQGs+fbiguD2aWyMhNgUJlL0hpN7Q38i8shpfZHahNqM2qvyOcNtR+ofU2toTYnnzm+B/yrN4Wp3P1H6VQZqvg/+2Uvni+ez+O5mlViee4/1tsG3qmvz/tN019cd/2+bqG/vK8PjYDPGHHs2vVx9CvpKweKFNgDPeGhtusO7e7B99t9euj6hr2FsLn7xPlvuv4uiP6lblsPWKnw0HbXb1sfnXr4dpj0677vvnhkX5/uPTD5LPIiNQ8nP4FT7adYf66D0fZuzk8z8Yegi14Gzcs34nf/RsTFT/5v+v836VRwDHIlh7dSHM7rer3toD5h1Z6Jf/fZUll0PaspgBlZAcrKx8gjBQEeaQUOGMsFUEYxgIaiASjWDYCRdAD7C/XAqKGAYFahhuBQkYzgUFMlqcSpHuezmn0F",
            }
        ],
    },
    "tatamibari": {
        "name": "Tatamibari",
        "cat": "region",
        "examples": [
            {
                "data": "m=edit&p=7VTBbptAEL37K6K9diuxYLuYS5Wmdi+u2zSuogihaG2TGAW86QJNhet/z8xA612ghx7a+lCtGT0eszOPxW/yL6XUMZ/A8nzucAHL8x26/CH+nGYtkyKNgzN+XhZbpQFw/mE243cyzeNB2GRFg301CapLXr0LQuYyTpdgEa8ug331PqgWvLqCR4wL4OaABOMuwOkRXtNzRBc1KRzAiwYDvAG4TvQ6jW/nNfMxCKslZ9jnDe1GyDL1NWb1Nrpfq2yVILGSBbxMvk0emyd5uVEPZZMrogOvzmu50x653lEuwlouoj8lN97cx3m56tM6iQ4HOPNPoPY2CFH45yP0j/Aq2ENcBHvm+rj1OwipPwzzHCReGoSLxGuDGCLxwiDGrRqjdsaYahgZPnUxivrtLT4JMzKEQ22MFCHam0Qt1mIox2gtarlmZa99CGJI+n7WgcMSdGQ3FGcUXYpLOFFeeRTfUnQojijOKWdK8ZriBcUhxTHlvMJv8ltf7S/ICV2f3G+u0Wkx0SBkU/DC2ULpTKbgh0WZrWL94x6mD8tVepuX+k6uwUs0nMAxwO0o06JSpR7TZGfnJfc7pePeR0iiFXvyV0pvWtWfZJpaRD1qLaqeChZVaLC8cS+1Vk8Wk8liaxHGNLMqxbvCFlBIW6J8kK1u2fGdDwP2jdEVenD4w/+j/V+Mdjx/59RGxanJob+u0r2+B7rH+sD2WrzhOy4HvuNnbNi1NLA9rga2bWygut4GsmNv4H7hcKzaNjmqavscW3Wsjq1Mt4fR4Bk=",
            }
        ],
    },
    "tentaisho": {
        "name": "Tentaisho (Spiral Galaxies)",
        "cat": "region",
        "aliases": ["spiralgalaxies"],
        "examples": [
            {
                "data": "m=edit&p=7VZbb5tMEH33r4j2eR9Ylpt5S9O0L6nT1KkiC1nW2iGxFex1uTQVlv97Zmb55ACLWqnq5ZMqzMxwGGbPDstZF18qladcOPiTEQcPhyciOt0ooNNpjttNmaXxGT+vyrXOIeD8esIfVFako6RJmo8O9Tiub3j9Pk6Yyzidgs15fRMf6g9xPeP1FG4x7gF2BZFg3IXw8hTe0X2MLgwoHIgnTQzhDMLVJl9l6WI6NdDHOKlvOcOB3tDjGLKt/poy8xxdr/R2uUFgqUqYTLHe7Js7RXWvn6omV8yPvD7v8MVRGr7yxBdDwxcjC1+cxs/zTe8f06Ja2siO58cjdP0T0F3ECTL/fAqjUziNDywQLPY4C1zjpHEeubBxY3JRRG5sUoRjnhBOaLwIGm+yhWsKC/mfb/Jl87w0xYWH+UBmEh/ACrIzICYBTwRM+NQlaBzzoYwFDhyA3T7sW+EIOFmKRDhkP1tIexUhYco23Ee8X15gd235Edbv50vPPleJ78WCe+4ATjwteIT5fT6+O9D6gT74A132Q3ubAxfnZXlZA/0MBuYbhLAibXhk71vo2HmGApawDQ/xfXXrwPJ8R4vUJXsLnxKvJdm3ZB2yPtkryrkke0f2gqxHNqCcED/GH/xc+9/JL6KTSKP87cP//2HzUcKmVf6gVilI5SWI5tlE51uVwdV0rfYpgw2KFTpbFE1WTPsXSCpgu2q7TPMWlGm9zza7dt7mcafz1HoLQdRqS/5S5/ed6s8qy1qA2ZBbkFmOLajMYU94da3yXD+3kK0q1y3g1X7XqpTuyjaBUrUpqifVGW17mvNxxL4xOhOJfxz+7f5/ZvfHN+D8baLyHToJ9FaEgtfXnO2rhVqsNHyl0LqhG7+dP612nVulAmCLWgBqVYUG7wkD4D0JwAH7KgCoRQgA7WoBQH05ALCnCIANiAJW7eoCsupKAw7VUwcc6rVAJPPRCw==",
            },
            {
                "data": "m=edit&p=7Vjfb9tGDH73X1Ho+R7Eu9PPt6zL9tK565yhCAwjkBO1MSpHmWyvg4L87+VRBhxZHzFgw7A+BIIJ+iPF+8Q78nTa/XGoutpQYaw1LjexIb6yNDZ55g353A0iPl5Xm31Tl2/MxWF/33asGPN+bj5Vza6eLY9Oq9lTX5T9B9P/XC4jGxn5UbQy/Yfyqf+l7K9Nv2BTZDxj71ijyFhWL0/qR7EH7e0AUsz6/Kizes3q7aa7beqbxWKAfi2X/ZWJwkA/yO1Bjbbtn3U03Cf/b9vtehOAdbXnh9ndbx6Plt3hrv1yOPrS6tn0Fzpfd+Ib1IFv0ADf8Bj/nm9997neHdaIbLF6fuas/8Z0b8plYP77Sc1P6qJ8YjkXSSKvy6fIFxyGeKQTPWYcJZZhO4Uz6J0mEM5CEAA7GDsLsadwjmNTjKkQKbjFo5IP8QGeKP4ppklpjsdVHosKj/2LFPrbmBQ8TCDAKfhP41tS4tsY+1ucH+vx81pZUMA/UfyVtWNz7O8czoNzIZ8ID3EAnmCeLsWL1mWYp8sVPgp/H+N15SnkH+GYp7d4fr3F/L1T8Azz9xleJz7DDcPnwR80EsJ5S2RdAVzmEbQYrZl47J9J/U7xIsfrvChwPimOtQakzDBRjFNBJLWHelOijGFzpUu4WBncEa4DcsrCoKFCgMHL1KGWKb0U3eFwcslL10SGTKHrC7wDUSITDg1KElMtJalkFxkK5QHTAq9+ypW2TYWy/qmQ+UB3WCVXhaQEGvAdNlY2MTbglWjjVN1m8JNbUhoaGxRWZJXBh70YGrRNTl5IkKFQQlmn3GGVRsIGvIPwzqikxCoTZZ3UBwjlHArFr2g/yYuaFXnF73GmdyJ/FBmLTES+E59LkR9FvhXpRabik4U3wX/8rvgf0Vn6XA4ef3clr16vXq9e+FrNltHi0H2qbms+I17yafHNvO22VcP/FvfVYx3xyTzatc3N7uhVysGdz5KMPRy267obQU3bPjabh7Hf5vND29XQFMBwSAX+67a7O4v+tWqaETB8ixhBQyscQfuOD8Mv/ldd134dIdtqfz8CXhz0R5Hqh/2YwL4aU6y+VGejbU/P/DyL/orkt+SPJPxp4PWzx//y2SPMQPy9bWjfGx1ZvG0HK59hUPyMwiI/4pM6Z3xS0WHAaVEzCuqa0fPSZmha3QxOCpwxpcZD1PMyD6zOKz0MNSn2MNTLel+uZt8A",
            },
        ],
    },
    "tents": {"name": "Tents", "cat": "var", "examples": []},
    "tapaloop": {
        "name": "Tapa-Like Loop",
        "cat": "loop",
        "aliases": ["tapalikeloop", "tapa-like-loop", "tapalike", "tapa-like"],
        "examples": [],
    },
    "yajilin": {"name": "Yajilin", "cat": "loop", "examples": []},
    "yajikazu": {
        "name": "Yajisan-Kazusan",
        "cat": "shade",
        "aliases": ["yk", "yajisan-kazusan"],
        "examples": [
            {
                "data": "m=edit&p=7VVNb5tMEL77V0R7aqWttAvYxtzSNOkldZvaVRQhC60dkvAGm5SPNy2W/3tmho3YBXrooW1UVYjx7LPz8ex6Zii+ViqPufT4jLs+F1zCM54KWAjuS59eoZ9lUqZxcMSPq/Iuy0Hh/OPZGb9RaRGPQm21Gu3rWVBf8Pp9EDKHcXolW/H6ItjXH4J6zusFbDEuATsHTTLugHraqpe0j9pJA0oB+rwJiG5XoG6SfJPG0XmDfArCeskZ5nlL3qiybfZ/zJoQtN5k23WCwFqVcJjiLnnQO0V1nd1X2lauDrw+bugunun6LV23pYtqQxe1Ll2K9cvpzlaHA1z7ZyAcBSFy/9Kqfqsugj3IebBnnoOuXuQCG/yHIKI3RsiJ8IafoRkliPAUGhoLhIRpNfF6jhOK5Zrhp9PGyog1pfCe6ei7PccZOdqQ5mU4SiF7xKSgaI7pKiXZOZEwscmAnU5rxnP8vp1DXGzMpUuSNjbAxR3I6w7k8CheB9PnsDDytS5UTvS9m+edai6mnU8VYdv5dDbjDqB6JNXQFckzkg7JJZQYr12S70gKkmOS52RzSvKS5AlJj+SEbKZYpD9Vxr+BTghTEWfi8DP+u/dWo5AtqvxGbWIYO/Nqu47zo3mWb1XKYM6zIkujQu8H9BmAwQTYjiwtKM2yhzTZ2XbJ7S7L48EtBOPr2yH7dZZfd6I/qjS1gOa7ZkHN/LWgMofhaqxVnmePFrJV5Z0FGIPYihTvSptAqWyK6l51sm3bMx9G7BujN3Th4r1/H9E/9BHFv0C8tBn00uhQ9Wb5YOsDPND9gA52ucZ7jQ54r6UxYb+rAR1obEC7vQ1Qv70B7HU4YD9ocoza7XNk1W11TNXrdkxlNnzIvqv/kntVV0evUCvU7g2u4Pc1W42eAA==",
            }
        ],
    },
    "yinyang": {
        "name": "Yin-Yang",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7ZVNb9pAEIbv/Ipqz1vJa2M+fEtp6IWkTUMVRZaFFnDAiu2l/iiNEf89M2NLxHiqSpWiRlUFHg2Ph5nXsO9u/r3UWSiVwrczkpaETPbdAV1K2XRZzWseFXHovZMXZbE1GSRSfp5O5YOO87DnN1VB71CNvepGVp88XyghhQ2XEoGsbrxDdeWJlUmWkZDVLdwXUsGNWV1pQ3p5Su/oPmaTGioL8usmh/Qe0lWUreJwMavJF8+v5lLgsA/0bUxFYn6EohGDn2sBAJbxftuwvFybx7KpUsFRVhe/Ueuc1GJaq8WMUYsP8Wpqx8HxCD/6V9C78HyU/u2Ujk7prXeAeE1RUbz3DsIZQhsbxtTSrkiacG2WDjg66LOU7TsYc3RksZSdNmY7KIsdp6wRj/kmSvGY/TGUcnnMylaKF2hjtepghxfYd9jqPj/S5QW6vBIXR3Z7D/mHH2LvbvWI6Q0LbUrLzaY4h9UoK4fiR4oWRZfijGouKd5RnFDsUxxQzRDX8x+v+FeS4zuwWTIv99+lQc8XE5PsTB4VoYCNX+QmXuRl9qBXsIXRuQB7FbC0TJZh1kKxMbs4Stt10SY1WcjeQhiuN1z90mTrs+57HcctUJ90LVSv0RYqMthpX3zWWWb2LZLoYtsCS13AqZhvo127U5gWbQGFbkvUj/psWnJ65mNP/BR0+Q6eyP9P1b9yquIfYL21neatyaG1azLW+IAZ7wNlPd7wjs2BdwyNA7ueBsrYGui5swF1zQ2w429gv7A4dj13Oao6NzqO6ngdR720uy+eovT9k043Iug9Aw==",
            }
        ],
    },
}

# pylint: skip-file
