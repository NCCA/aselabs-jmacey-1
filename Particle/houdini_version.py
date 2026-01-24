#!/opt/hfs20.5.332/bin/hython
#
import hou

from Emitter import Emitter
from Vec3 import Vec3

OUTPUT_DIR = "/transfer/Particle"


def write_particles(emitter, filename):
    geo = hou.Geometry()
    geo.addAttrib(hou.attribType.Point, "Cd", hou.Vector3(0, 0, 0))
    geo.addAttrib(hou.attribType.Point, "pscale", 1.0)
    point_objects = []
    for particle in emitter.particles:
        p = geo.createPoint()
        pos = particle.position
        p.setPosition(hou.Vector3(pos.x, pos.y, pos.z))
        colour = particle.colour
        p.setAttribValue("Cd", hou.Vector3(colour.x, colour.y, colour.z))
        p.setAttribValue("pscale", particle.size)
        point_objects.append(p)
    geo.saveToFile(filename)


def main():
    emitter = Emitter(Vec3(0, 0, 0), 10000)
    for frame in range(250):
        write_particles(emitter, f"{OUTPUT_DIR}/HouParticles.{frame:04}.bgeo")
        emitter.update(0.1)


if __name__ == "__main__":
    main()
