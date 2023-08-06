"""
.. module:: test_viewer
   :synopsis: Unit tests for viewer module
"""

import numpy as np

from nutsflow import Consume
from nutsflow.common import Redirect
from nutsml import PrintColType, PrintType

expected_col_info1 = """
item 0: <tuple>
  0: <ndarray> shape:10x20x3 dtype:float64 range:0.0..0.0
  1: <int> 1
item 1: <tuple>
  0: <str> text
  1: <int> 2
item 2: <int>
  0: <int> 3
"""

expected_col_info2 = """
item 0: <tuple>
  1: <int> 2
item 1: <tuple>
  1: <int> 4
"""

expected_col_info3 = """
item 0: <tuple>
  0: <int> 1
  1: <int> 2
item 1: <tuple>
  0: <int> 3
  1: <int> 4
"""

expected_type_info1 = """
(<ndarray> 3x4:uint8, <ndarray> 1x2:float32)
<float> 1.1
[[<ndarray> 3x4:uint8], <int> 2]
"""

expected_type_info2 = """
data: <float> 1.1
data: [[<ndarray> 3x4:uint8], <int> 2]
"""


def test_PrintColType():
    with Redirect() as out1:
        data = [(np.zeros((10, 20, 3)), 1), ('text', 2), 3]
        data >> PrintColType() >> Consume()
    assert out1.getvalue() == expected_col_info1[1:]

    with Redirect() as out2:
        data = [(1, 2), (3, 4)]
        data >> PrintColType(1) >> Consume()
    assert out2.getvalue() == expected_col_info2[1:]

    with Redirect() as out3:
        data = [(1, 2), (3, 4)]
        data >> PrintColType((0, 1)) >> Consume()
    assert out3.getvalue() == expected_col_info3[1:]


def test_PrintType():
    a = np.zeros((3, 4), dtype='uint8')
    b = np.zeros((1, 2), dtype='float32')
    with Redirect() as out:
        data = [(a, b), 1.1, [[a], 2]]
        data >> PrintType() >> Consume()
    assert out.getvalue() == expected_type_info1[1:]

    with Redirect() as out:
        data = [1.1, [[a], 2]]
        data >> PrintType('data:') >> Consume()
    assert out.getvalue() == expected_type_info2[1:]
