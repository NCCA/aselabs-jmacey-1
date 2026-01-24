import pytest

from Vec3 import Vec3


def test_vec3_ctor():
    a = Vec3()
    assert a.x == pytest.approx(0.0)
    assert a.y == pytest.approx(0.0)
    assert a.z == pytest.approx(0.0)
