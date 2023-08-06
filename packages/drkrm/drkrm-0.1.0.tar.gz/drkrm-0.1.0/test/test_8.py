# test adjusting individual reds/greens/blues channels

import pytest
import sys
sys.path.insert(0, 'src')
from utils import *
from base import *
from arr import *


def test_np():
    i2 = read_img("examples/kakashi.jpg")
    npa = get_nparray_from_img(i2)
    a = reds(npa, 140)
    a = greens(npa, 140)
    a = blues(npa, 90)
    b = get_img_from_nparray(a)
    b.show()
