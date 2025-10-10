import pytest

from vec3 import Vec3


def test_create_vec3():
    v = Vec3()
    assert v.x == pytest.approx(0.0)
    assert v.y == pytest.approx(0.0)
    assert v.z == pytest.approx(0.0)


def test_create_with_values():
    v = Vec3(1, 2, 3)
    assert v.x == 1
    assert v.y == 2
    assert v.z == 3
