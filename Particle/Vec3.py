import math


class Vec3:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, rhs):
        if not isinstance(rhs, Vec3):
            return NotImplemented
        return math.isclose(self.x, rhs.x) and math.isclose(self.y, rhs.y) and math.isclose(self.z, rhs.z)

    def __str__(self):
        return f"[{self.x},{self.y},{self.z}]"

    def __mul__(self, rhs):
        if isinstance(rhs, Vec3):
            return Vec3(self.x * rhs.x, self.y * rhs.y, self.z * rhs.z)
        elif isinstance(rhs, (int, float)):
            return Vec3(self.x * rhs, self.y * rhs, self.z * rhs)
        else:
            raise TypeError("Unsupported type for * and Vec3")

    def __add__(self, rhs):
        if isinstance(rhs, Vec3):
            return Vec3(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)
        else:
            raise TypeError("Unsupported Type for Vec3 +")

    def copy(self) -> "Vec3":
        return Vec3(self.x, self.y, self.z)
