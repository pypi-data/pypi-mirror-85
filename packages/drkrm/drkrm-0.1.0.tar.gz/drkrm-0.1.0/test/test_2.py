# test reading in an image
# should return no errors

import pytest
import sys
sys.path.insert(0, 'src')
from base import *


p = get_path()


def test_path():
    assert (p != None)
