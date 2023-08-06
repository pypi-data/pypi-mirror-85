__author__ = "Dilawar Singh"
__email__ = "dilawar.s.rajput@gmail.com"

import math

def argmax(ls : list) -> int:
    """argmax: Returns the index i such that max(ls) == ls[i]
    """
    _m, _mi = -math.inf, 0
    for i, v in enumerate(ls):
        if v > _m:
            _m = v
            _mi = i
    return _mi


def test_argmax():
    import random
    a = [ random.randint(-1000, 1000) for x in range(1000)]
    assert max(a) == a[argmax(a)]
