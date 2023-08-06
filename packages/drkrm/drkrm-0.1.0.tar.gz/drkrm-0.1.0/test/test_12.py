# test coversion from hex color to rgb

import pytest
import sys
sys.path.insert(0, 'src')
from utils import *
from base import *
from arr import *


def test_hex_to_rgb():
    p = hex_to_rgb("#e2d9ff")
    print(p)
