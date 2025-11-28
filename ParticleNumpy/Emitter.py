import random

import numpy as np
from ncca.ngl import Vec3


class Emitter:
    _GRAVITY = np.array((0.0, -9.81, 0.0), dtype=np.float32)

    def __init__(self, position: Vec3, num_particles: int):
        self._position = position
        self._position_np = position.to_numpy()
        self._num_particles = num_particles
        self.position = np.zeros((self._num_particles, 3), dtype=np.float32)  # x,y,z
        self.direction = np.zeros((self._num_particles, 3), dtype=np.float32)  # x,y,z
        self.colour = np.zeros((self._num_particles, 3), dtype=np.float32)  # r,g,b

        self.life = np.zeros((self._num_particles,), dtype=int)  # r,g,b
        self.max_life = np.zeros((self._num_particles,), dtype=int)  # r,g,b
        self.size = np.zeros((self._num_particles,), dtype=np.float32)  # r,g,b

        self._init_particles()

    def _init_particles(self):
        indices = np.arange(self._num_particles)
        self._respawn_particles(indices)

    def _respawn_particles(self, indices):
        # init particles vectorized.
        if len(indices) == 0:
            return

        idx = np.asarray(indices, dtype=int)
        count = idx.size
        EMIT_DIR = np.array((0.0, 1.0, 0.0), dtype=np.float32)
        SPREAD = 15.0
        rand_pos = np.random.rand(count, 1)
        # Now create a direction vector.
        rand_normals = np.random.normal(size=(count, 3))
        norms = np.linalg.norm(rand_normals, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        rand_unit = rand_normals / norms
        # build our dir
        directions = EMIT_DIR * rand_pos + rand_unit * SPREAD
        directions[:, 1] = np.abs(directions[:, 1])

        # positions at start so from pos
        positions = np.tile(self._position_np.reshape(1, 3), (count, 1))
        colours = np.random.rand(count, 3)
        life = np.zeros(count, dtype=int)
        max_life = np.random.randint(10, 51, size=count, dtype=int)
        size = np.full(count, 0.01, dtype=np.float32)

        self.position[idx] = positions
        self.direction[idx] = directions
        self.colour[idx] = colours
        self.life[idx] = life
        self.max_life[idx] = max_life
        self.size[idx] = size

    def update(self, dt: float):
        self.direction += Emitter._GRAVITY * (dt * 0.5)
        self.position += self.direction * dt
        self.life += 1
        self.size += 0.1
        # now respawn dead particles
        dead_mask = self.life > self.max_life
        if np.any(dead_mask):
            dead_indices = np.nonzero(dead_mask)[0]
            self._respawn_particles(dead_indices)

    @property
    def num_particles(self):
        return self._num_particles
