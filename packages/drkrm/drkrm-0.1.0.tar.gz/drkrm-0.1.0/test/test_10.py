# test adjusting shadows

import pytest
import sys
sys.path.insert(0, 'src')
from utils import *
from base import *
from arr import *


def test_shadows():
    i2 = read_img("examples/kakashi.jpg")
    npa = get_nparray_from_img(i2)
    a = shadows(npa)
    b = get_img_from_nparray(a)
    b.show()
