# test changing image highlights - works well for manga panels

import pytest
import sys
sys.path.insert(0, 'src')
from utils import *
from base import *
from arr import *


def test_highlights():
    i2 = read_img("examples/hq.jpg")
    npa = get_nparray_from_img(i2)
    a = highlights(npa)
    b = get_img_from_nparray(a)
    b.show()
