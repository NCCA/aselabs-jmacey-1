import pytest

from Particle import Particle
from Vec3 import Vec3


def test_particle_creation():
    particle = Particle()
    assert particle
    assert particle.position == Vec3()
