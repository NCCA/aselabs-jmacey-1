from dataclasses import dataclass, field

from Vec3 import Vec3


@dataclass
class Particle:
    position: Vec3 = field(default_factory=Vec3)
    direction: Vec3 = field(default_factory=Vec3)
    colour: Vec3 = field(default_factory=Vec3)
    life: int = 0
    max_life: int = 100
    size: float = 1.0

    def __str__(self):
        return f"Particle(position={self.position} dir={self.direction} )"
