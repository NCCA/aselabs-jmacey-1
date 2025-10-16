from dataclasses import dataclass
from typing import Tuple


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
