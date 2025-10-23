from dataclasses import dataclass
from typing import Tuple, Union

import numpy as np
from PIL import Image as PILImage


@dataclass
class rgba:
    """A class to represent an RGBA colour."""

    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 255

    def as_tuple(self) -> tuple[int, int, int, int]:
        """Get the rgba as a tuple for easy use.

        Returns:
            A tuple of (r, g, b, a).
        """
        return (self.r, self.g, self.b, self.a)

    def __post_init__(self) -> None:
        """Validate the RGBA values after initialization."""
        for component in ("r", "g", "b", "a"):
            value = getattr(self, component)
            if not isinstance(value, int) or not (0 <= value <= 255):
                raise ValueError(f"RGBA component {component} must be an int 0 - 255")


class ImageAccessError(Exception):
    """This exception is thrown when trying to change the size of an image."""

    pass


class Image:
    """A class to represent an image."""

    def __init__(self, width: int, height: int, fill_colour: Union[rgba, tuple, None] = None) -> None:
        """
        Initialize the Image.

        Args:
            width: The width of the image.
            height: The height of the image.
            fill_colour: The colour to fill the image with.
        """
        self._width = width
        self._height = height
        fill = self._validate_rgba(fill_colour)

        self._rgba_data = np.full((self._height, self._width, 4), fill, dtype=np.uint8)

    def _validate_rgba(self, value: Union[rgba, tuple, None]) -> Tuple[int, int, int, int]:
        """
        Check to see if a value is correct and return a tuple of RGBA values.

        Args:
            value: The value to check.

        Returns:
            A tuple of RGBA values.
        """
        if value is None:
            return (255, 255, 255, 255)
        elif isinstance(value, rgba):
            return value.as_tuple()
        elif isinstance(value, tuple):
            if len(value) == 3:
                return (value[0], value[1], value[2], 255)
            elif len(value) == 4:
                return value
            else:
                raise ValueError("fill_colour not the correct size!")
        else:
            raise ValueError("wrong type")

    @property
    def width(self) -> int:
        """The width of the image."""
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        """Set the width of the image."""
        raise ImageAccessError("Trying to set read only Property Width")

    @property
    def height(self) -> int:
        """The height of the image."""
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        """Set the height of the image."""
        raise ImageAccessError("Trying to set read only Property Height")

    def save(self, name: str) -> None:
        """
        Save the image to a file.

        Args:
            name: The name of the file to save the image to.
        """
        img = PILImage.fromarray(self._rgba_data)
        img.save(name)

    def _check_bounds(self, x: int, y: int) -> None:
        """
        Check if the given x,y coordinates are within the bounds of the image.

        Args:
            x (int): The x coordinate to check.
            y (int): The y coordinate to check.

        Raises:
            IndexError: If the coordinates are out of range.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"x,y values out of range {x=} {self.width=} {y=} {self.height=}")

    def get_pixel(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """
        Get the pixel at x,y and return as a tuple.

        Args:
            x: The x coordinate of the pixel.
            y: The y coordinate of the pixel.

        Returns:
            The r,g,b,a of the pixel if the range is valid.
        """
        self._check_bounds(x, y)
        return tuple(self._rgba_data[y, x])

    def set_pixel(self, x: int, y: int, value: Union[tuple, rgba]) -> None:
        """
        Set the pixel at x,y to the given value.

        Args:
            x: The x coordinate of the pixel.
            y: The y coordinate of the pixel.
            value: The value to set the pixel to.
        """
        self._check_bounds(x, y)
        validated_value = self._validate_rgba(value)
        self._rgba_data[y, x] = validated_value
