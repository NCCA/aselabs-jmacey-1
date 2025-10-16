import pytest

from image import rgba


@pytest.fixture
def red() -> rgba:
    return rgba(255, 0, 0)


def test_rgba_defaults():
    """Test that we default to black with full alpha"""
    c = rgba()
    assert (c.r, c.g, c.b, c.a) == (0, 0, 0, 255)


def test_rgba_custom():
    """test init from other values"""
    c = rgba(255, 0, 128, 56)
    assert (c.r, c.g, c.b, c.a) == (255, 0, 128, 56)


def test_as_tuple(red):
    assert red.as_tuple() == (255, 0, 0, 255)


@pytest.mark.parametrize(
    "component,value", [("r", -1), ("g", 256), ("b", 1000), ("a", -1000), ("r", 25.0), ("b", "one")]
)
def test_invalid_values(component, value):
    with pytest.raises(ValueError):
        kwargs = {component: value}
        rgba(**kwargs)
