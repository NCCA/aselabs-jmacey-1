import random

from Particle import Particle
from Random import Random
from Vec3 import Vec3

GRAVITY = Vec3(0, -9.81, 0)


class Emitter:
    def __init__(self, position: Vec3, num_particles: int):
        self._position = position
        self._num_particles = num_particles
        self._particles = []
        self._init_particles()

    def _init_particles(self):
        for _ in range(self.num_particles):
            particle = self._create_particle()
            self._particles.append(particle)

    def _create_particle(self):
        EMIT_DIR = Vec3(0.0, 1.0, 0.0)
        SPREAD = 15
        direction = EMIT_DIR * Random.random_positive_float() + Random.random_vector_on_sphere() * SPREAD
        direction.y = abs(direction.y)
        max_life = random.randint(10, 50)
        colour = Random.random_positive_vec3()
        pos = self._position.copy()
        particle = Particle(pos, direction, colour, 0, max_life, 1.0)
        return particle

    def update(self, dt: float):
        for i, particle in enumerate(self._particles):
            particle.direction += GRAVITY * dt * 0.5
            particle.position += particle.direction * dt
            particle.life += 1
            if particle.life > particle.max_life:
                self._particles[i] = self._create_particle()

    def render(self):
        for particle in self._particles:
            print(particle)

    @property
    def position(self):
        return self._position

    @property
    def num_particles(self):
        return self._num_particles

    @property
    def particles(self):
        return self._particles
