import pytest

from image import Image, ImageAccessError, rgba


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


@pytest.mark.parametrize("arg,value", [("r", -1), ("g", 256), ("b", 1000), ("a", -1000), ("r", 25.0), ("b", "one")])
def test_invalid_values(arg, value):
    with pytest.raises(ValueError):
        kwargs = {arg: value}
        rgba(**kwargs)


@pytest.fixture
def small_image() -> Image:
    return Image(10, 10)


def test_default_image_ctor():
    img = Image(20, 40)
    assert img.width == 20
    assert img.height == 40


def test_size_change_exception(small_image):
    with pytest.raises(ImageAccessError):
        small_image.width = 100
    with pytest.raises(ImageAccessError):
        small_image.height = 100


def test_save():
    img = Image(1024, 1024)
    img.save("test.png")
    img = Image(1024, 1024, (255, 0, 0, 255))
    img.save("red.png")
    img = Image(1024, 1024, rgba(0, 255, 0, 255))
    img.save("green.png")
