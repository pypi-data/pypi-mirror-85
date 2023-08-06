# test centrally square cropping a vertical image

import pytest
import sys
sys.path.insert(0, 'src')
from base import *
from utils import *


def test_square_vertical():
    i2 = read_img("examples/hq.jpg")
    sq2 = square(i2)
    sq2.show()
