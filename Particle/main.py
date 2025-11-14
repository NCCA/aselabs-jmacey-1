#!/usr/bin/env -S uv run --script

from pathlib import Path

from Emitter import Emitter
from Vec3 import Vec3

OUTPUT_DIR = "/transfer/Particle"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

emitter = Emitter(Vec3(0, 0, 0), 1000)
# emitter.write_geo("test.geo")
# emitter.render()
for i in range(250):
    emitter.write_geo(f"{OUTPUT_DIR}/Particle.{i:04}.geo")
    emitter.update(0.01)

    # emitter.render()
