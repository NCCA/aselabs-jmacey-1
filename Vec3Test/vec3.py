class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, rhs: "Vec3") -> "Vec3":
        return Vec3(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)
