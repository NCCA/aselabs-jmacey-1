import pytest

from Particle import Particle
from Vec3 import Vec3


def test_particle_creation():
    particle = Particle()
    assert particle
    assert particle.position == Vec3()
    assert particle.colour == Vec3()
    assert particle.direction == Vec3()
    assert particle.life == 0
    assert particle.max_life == 100
    assert particle.size == pytest.approx(1.0)


def test_particle_value():
    pos = Vec3(1, 2, 3)
    dir = Vec3(4, 5, 6)
    colour = Vec3(7, 8, 9)
    max_life = 10
    life = 20
    scale = 2.0
    particle = Particle(pos, dir, colour, life, max_life, scale)

    assert particle.position == pos
    assert particle.colour == colour
    assert particle.direction == dir
    assert particle.max_life == max_life
    assert particle.life == life
    assert particle.size == pytest.approx(scale)
