# test adding noise to image 

import pytest
import sys
sys.path.insert(0, 'src')
from utils import *
from base import *
from arr import *


def test_noise():
    i2 = read_img("examples/kakashi.jpg")
    npa = get_nparray_from_img(i2)
    a = noise(npa, 50)
    b = get_img_from_nparray(a)
    b.show()
