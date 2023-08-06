import pytest
import sys
sys.path.insert(0, 'src')
from base import *
import pathlib
print("path: ", pathlib.Path().absolute())


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0
