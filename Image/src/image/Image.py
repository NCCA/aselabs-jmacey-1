from dataclasses import dataclass
from typing import Tuple, Union

import numpy as np
from PIL import Image as PILImage


@dataclass
class rgba:
    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 255

    def as_tuple(self) -> tuple[int, int, int, int]:
        """get the rgba as a tuple for easy use"""
        return (self.r, self.g, self.b, self.a)

    def __post_init__(self):
        for component in ("r", "g", "b", "a"):
            value = getattr(self, component)
            if not isinstance(value, int) or not (0 <= value <= 255):
                raise ValueError(f"RGBA component {component} must be and int 0 - 255")


class ImageAccessError(Exception):
    """This exception is thrown when trying to change size of image"""

    pass


class Image:
    def __init__(self, width: int, height: int, fill_colour: Union[rgba, tuple, None] = None) -> None:
        self._width = width
        self._height = height
        if fill_colour is None:
            fill = rgba(255, 255, 255)
        elif isinstance(fill_colour, tuple):
            if len(fill_colour) == 3:
                fill = rgba(r=fill_colour[0], g=fill_colour[1], b=fill_colour[2], a=255)
            elif len(fill_colour) == 4:
                fill = rgba(r=fill_colour[0], g=fill_colour[1], b=fill_colour[2], a=fill_colour[3])
            else:
                raise ValueError("fill_colour not the correct size!")

        elif isinstance(fill_colour, rgba):
            fill = fill_colour

        else:
            raise ValueError("wrong type")

        self._rgba_data = np.full((self._height, self._width, 4), fill.as_tuple(), dtype=np.uint8)

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value) -> None:
        raise ImageAccessError("Trying to set read only Property Width")

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value) -> None:
        raise ImageAccessError("Trying to set read only Property Height")

    def save(self, name: str):
        img = PILImage.fromarray(self._rgba_data)
        img.save(name)

    def get_pixel(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """
        Get the pixel at x,y and return as tuple

        Args :
            x (int) : x cord of the pixel
            y (int) : y cord of the pixel

        Returns current r,g,b,a of the pixel if range valid
        """
        if 0 <= x < self.width and 0 <= y and self.height:
            return self._rgba_data[y, x]
        else:
            raise IndexError(f"x,y values out of range {x=} {self.width=} {y=} {self.height=} ")

    def set_pixel(self, x: int, y: int, value: Union[tuple, rgba]) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            if isinstance(value, rgba):
                self._rgba_data[y, x] = value.as_tuple()
            elif isinstance(value, tuple):
                if len(value) == 3:
                    self._rgba_data[y, x] = (*value, 255)
                elif len(value) == 4:
                    self._rgba_data[y, x] = value
                else:
                    raise ValueError("list not valid size")
            else:
                raise ValueError("Wrong datatype for pixel data")
        else:
            raise IndexError(f"x,y values out of range {x=} {self.width=} {y=} {self.height=} ")
