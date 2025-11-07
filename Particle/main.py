#!/usr/bin/env -S uv run --script

from Emitter import Emitter
from Vec3 import Vec3

emitter = Emitter(Vec3(0, 0, 0), 1)
# emitter.render()
for _ in range(100):
    emitter.update(0.01)
    # emitter.render()
    pos = emitter.particles[0].position
    print(f"{pos.x},{pos.y},{pos.z}")
