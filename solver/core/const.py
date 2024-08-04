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
                "config": {"Product": False},
            },
            {
                "data": "m=edit&p=7ZXfb5swEMff81dUfvYDBkIob13X7CXL1jVTVSEUOQltUCHuDKwTUf733h1smB972MO2TpoIl8vHZ98Z53vkX0qpYy4s/Dg+h2+4XOHTbfse3VZzrZIijYMzflEWe6XB4fzDfM7vZZrHk7CJiibH6jyornn1LgiZYJzZcAsW8eo6OFbvg2rJqxsYYtwFtqiDbHCvWveWxtG7rKGwwF82Prh34G4TvU3j9aImH4OwWnGGed7QbHRZpr7GrKkDf29VtkkQbGQBm8n3yVMzkpc79Vg2sSI68eqiVy5macp12nLRrctFb6Rc3MVvLvc8Op3gsX+CgtdBiLV/bl2/dW+CI9hlcGSOi1NnUEt9NswlAEf1HUxtBG4LPKcHZjRFeAbxkPgGOO/N8QWCqQH6U4RFc2wjRgjKZCQSkBVzG/UKQfPMIJuSCXMlp78r4dK2hGWgKc0z1/aI/KgSHqKgR3lHdk7WJruCJ80rh+xbshbZKdkFxVyRvSV7SdYl61HMDM/ql07zD5QTOnVr6F7Tf49Fk5DdlPpebmNQ0rLMNrE+WyqdyZRB62K5Std5Mx5QZwOtATtQZAelSj2lyaEblzwclI5HhxDGu4ex+I3Su97qzzJNO6Du1R1Ut5QOKjT0C+O31Fo9d0gmi30HGL2ls1J8KLoFFLJbonyUvWxZu+fThH1jdIcOvlP+vxf+0nsBj8B6bf3ktZVD/16lR6UPeET9QEdV3vCB0IEPJI0Jh6oGOiJsoH1tAxrKG+BA4cB+InJcta9zrKovdUw1UDumMgUfRpMX",
                "config": {"Product": True},
            },
        ],
        "parameters": [{"name": "Product", "type": "checkbox", "default": False}],
    },
    "chocona": {
        "name": "Chocona",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VZdb9tGEHzXrwj4fA88Hr/f3MTui6s2tYsgEASDtplYCGWmlNQUNPzfM7Ncmh9SURRF0RQoJJHD0d7u7O3t8Xa/HoqmNNbn16UGd3xCm8ovSGP5+fq53uyrMn9lzg77h7oBMObHiwvzoah25WKlVuvFU5vl7VvTfp+vPOsZL8DPemvTvs2f2h/y9ty0V/jLMym4y84oADwf4Dv5n+h1R1ofeKkY8D3g3aa5q8qby475KV+118ZjnO9kNKG3rX8rPdXB57t6e7shcVvskczuYfNZ/9kd7utPB7W162fTnnVyl71cRlG5bpBL2MklOiGXWfzDcrP18zOm/WcIvslX1P7LANMBXuVPuC7zJ8/5HIrK2K42ngtIRCMiJOGPiJREOBChEMxWiWhOxG4WJU5mURIJO4qSSNiRjySeWaRCjCysb2derT8PbP25Nmsl0niUzci4EROIvFHOtpuWsU0YzZlZ2phyKxP/Xq4Xcg3keo26mNbJ9Y1cfblGcr0Um3OUK3CZCULULEA7BejKHtvA4LnDoQ8eUyE2yYCtgw0mnjgCjpCC4NAEMaaFOEa3x0hf+GjAoYU9EhQb+Bzbp5gc4hQaMtWQYewLjo2znU7cjQu6uLgbx8VEjD3HuS4W7sZFmLoea44O+Q44gp/Ov7MWuNMm2KqeDD57nCLHTDWnyD3V3Kk57WKJTao5ptDPBSYYcX2N60M/F4zEclOscys6X3ACrDkG0BN2enBHjqqfPrl0BVN/nwtz1Dnh2B6Tt33unFuNZRHLqR8HP1yQEgvzPMZsT8HwE6qfEH7iPkfmpT6Jfc3Rx1irY/FWcNwqJBZycVov2vj9HKJ2bEDFQaZrNcP6zPp8MfbFBj59rVfCWmi9EtSL24Fg1CtR+whrj/uGYKxJzUtwoms+Qawx7uvOta3zjztsVFvIvtAeCdhrGgtzjueB575J7Nhr6hNz+6KBWOccd/B9T2Fsr585JmqTwIY7nPQUc+wx+i7WHGPEijUX1AvPqgH2WseAb2uti/Bal8BSs2KHuE7jEnP/Fp8YG/b9zn2AfrDxvJPt57VcQ7nGsi0lfJn8pdfN398B/1TOChXh2WX6if573Hqx8q4OzYfirsSr/vz+Y/lqWTfbosLT8rC9LZv+GSctb1dXNzu1zuUghqMBuEexnFBVXX+uNo9Tu83Hx7opT/5FskT4E/a3dXM/8/6lqKoJ0R0tJ1R3AppQ+wbHm9Fz0TT1lwmzLfYPE2J0FJp4Kh/3UwH7Yiqx+FTMom2HnJ8X3u+e/FaOR+D/j7H/0jGWJfC/td3lW5Mjq7duTrY+6BPdD/Zklyt/1Ojgj1qaAY+7GuyJxgY7721Qx+0N8qjDwf1Bk9PrvM+pat7qDHXU7Qw1bvjVevEV",
            }
        ],
    },
    "country": {"name": "Country Road", "cat": "loop", "aliases": ["countryroad"], "examples": []},
    "doppelblock": {"name": "Doppelblock", "cat": "num", "examples": []},
    "easyas": {"name": "Easy As", "cat": "num", "examples": []},
    "fillomino": {"name": "Fillomino", "cat": "num", "examples": []},
    "gokigen": {"name": "Gokigen (Slant)", "cat": "draw", "examples": []},
    "haisu": {"name": "Haisu", "cat": "loop", "examples": []},
    "hashi": {"name": "Hashiwokakero (Bridges)", "cat": "loop", "aliases": ["bridges"], "examples": []},
    "heteromino": {"name": "Heteromino", "cat": "region", "examples": []},
    "heyawake": {
        "name": "Heyawake",
        "cat": "shade",
        "examples": [
            {
                "data": "m=edit&p=7VXfT9swEH7vX4H87Ic4dn6+MVb2wroxmBCKKpSWABVpw9J2TKn6v/OdfdCmDdqkaRqTpjb25+98vu8cnzP/tszrQiqP/jqW6PEzKraPH4f28fh3PlmURXogD5eLu6oGkPLT8bG8yct50ct41rC3apK0OZXNhzQTSkjh41FiKJvTdNV8TJu+bM5gEjIGd+Im+YD9DbywdkJHjlQe8IAx4CXgeFKPy+LqxDGf06w5l4LivLPeBMW0+l4I1kHjcTUdTYgY5QskM7+bPLBlvryu7pc8Vw3Xsjl8Xa7ukktkh1ya8IflJsP1Gtv+BYKv0oy0f93AeAPP0pUwoUhjKYLYdklgO+Ur1xtHq8BDD48BPDRwJiLodu/R+mbhyzAku9kMdduKeJl+GSrP35qNCCpdob207bFtfdueQ7JstG3f29azbWDbEzunD3W+UdIPkIaPk2YMMNRZHEk/RFqEgwA4YYyDHUEE4RC+EfuGCQ47tBOOfDr4jOEbs2+spZ9EjEOpPaRucQLMvkkktXJxYQc2jDWw84Vdat/FhR3YaYZdas2+fgDs4sIutXGaYQdmX424gYsLO7DTDDswa8Yc37BO4wHzntC+8ZrogVm/QY7Gabb7ybHQA/OeGFwMhveB9pmOjcXYW7O1VzGvE2OdmNeJaT9ZJ+WrnnNHjorzpRz1c77IS5M2vPAL+9qPbGtsG9rjENH5/sUKcKf690/eT+Vk2l2n7V/w73HDXibOlvVNPi5w+/Svb4uDQVVP8xKjwXI6KurnMS5/Ma/KqznPTu23AbcVuJmd2aLKqnooJ7P2vMntrKqLThORBcJ3zB9V9fXO6o95WbYI97VrUe5SblGLGjfu1jiv6+qxxUzzxV2L2LqdWysVs0VbwCJvS8zv851o003O6574Iexj70/z/8v6l76s9Aq8t3a7vDU59vRWdWfpg+6ofrCdVc78XqGD3ytpCrhf1WA7Chvsbm2D2i9vkHsVDu6VIqdVd+ucVO2WOoXaq3YKtV3w2bD3BA==",
            },
            {
                "data": "m=edit&p=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"
            },
        ],
    },
    "hitori": {"name": "Hitori", "cat": "shade", "examples": []},
    "hotaru": {"name": "Hotaru Beam", "cat": "loop", "examples": []},
    "jousan": {"name": "Jousan", "cat": "draw", "examples": []},
    "kakuro": {"name": "Kakuro", "cat": "num", "examples": []},
    "kurotto": {"name": "Kurotto", "cat": "shade", "examples": []},
    "kurodoko": {"name": "Kurodoko", "cat": "shade", "examples": []},
    "lits": {"name": "LITS", "cat": "shade", "examples": []},
    "lightup": {"name": "Light Up (Akari)", "cat": "var", "aliases": ["akari"], "examples": []},
    "magnets": {"name": "Magnets", "cat": "var", "examples": []},
    "masyu": {"name": "Masyu", "cat": "loop", "examples": []},
    "mines": {"name": "Minesweeper", "cat": "var", "aliases": ["minesweeper"], "examples": []},
    "moonsun": {"name": "Moon-or-Sun", "cat": "loop", "examples": []},
    "nagare": {"name": "Nagareru-Loop", "cat": "loop", "aliases": ["nagareru"], "examples": []},
    "nanro": {"name": "Nanro", "cat": "num", "examples": []},
    "ncells": {"name": "N Cells", "cat": "region", "aliases": ["fivecells", "fourcells"], "examples": []},
    "nonogram": {"name": "Nonogram", "cat": "shade", "examples": []},
    "norinori": {"name": "Norinori", "cat": "shade", "examples": []},
    "numlin": {"name": "Numberlink", "cat": "loop", "aliases": ["numberlink"], "examples": []},
    "nuribou": {"name": "Nuribou", "cat": "shade", "examples": []},
    "nurikabe": {"name": "Nurikabe", "cat": "shade", "examples": []},
    "nurimisaki": {"name": "Nurimisaki", "cat": "shade", "examples": []},
    "onsen": {"name": "Onsen-Meguri", "cat": "loop", "examples": []},
    "ripple": {"name": "Ripple Effect", "cat": "num", "aliases": ["rippleeffect"], "examples": []},
    "shakashaka": {"name": "Shakashaka", "cat": "var", "examples": []},
    "shikaku": {"name": "Shikaku", "cat": "region", "examples": []},
    "shimaguni": {"name": "Shimaguni (Islands)", "cat": "shade", "aliases": ["islands"], "examples": []},
    "simpleloop": {"name": "Simple Loop", "cat": "loop", "examples": []},
    "skyscrapers": {"name": "Skyscrapers", "cat": "num", "examples": []},
    "slither": {"name": "Slitherlink", "cat": "loop", "aliases": ["slitherlink"], "examples": []},
    "spiralgalaxies": {"name": "Spiral Galaxies", "cat": "region", "examples": []},
    "starbattle": {"name": "Star Battle", "cat": "var", "examples": []},
    "statuepark": {"name": "Statue Park", "cat": "var", "examples": []},
    "stostone": {"name": "Stostone", "cat": "shade", "examples": []},
    "sudoku": {"name": "Sudoku", "cat": "num", "examples": []},
    "tapa": {"name": "Tapa", "cat": "shade", "examples": []},
    "tasquare": {"name": "Tasquare", "cat": "shade", "examples": []},
    "tatamibari": {"name": "Tatamibari", "cat": "region", "examples": []},
    "tents": {"name": "Tents", "cat": "var", "examples": []},
    "tapaloop": {
        "name": "Tapa-Like Loop",
        "cat": "loop",
        "aliases": ["tapalikeloop", "tapa-like-loop", "tapalike", "tapa-like"],
        "examples": [],
    },
    "yajilin": {"name": "Yajilin", "cat": "loop", "examples": []},
    "yajikazu": {"name": "Yajisan-Kazusan", "cat": "shade", "aliases": ["yk", "yajisan-kazusan"], "examples": []},
    "yinyang": {"name": "Yin-Yang", "cat": "shade", "examples": []},
}

# pylint: skip-file
