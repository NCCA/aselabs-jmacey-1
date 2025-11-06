from dataclasses import dataclass, field

from Vec3 import Vec3


@dataclass
class Particle:
    position: Vec3 = field(default_factory=Vec3)
