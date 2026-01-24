import pytest

from Emitter import Emitter
from Vec3 import Vec3


def test_emitter_creation():
    pos = Vec3(0, 0, 0)
    num_particles = 10
    emitter = Emitter(pos, num_particles)
    assert emitter
    assert emitter.position == pos
    assert emitter.num_particles == num_particles
    assert isinstance(emitter.particles, list)
    assert len(emitter.particles) == num_particles
