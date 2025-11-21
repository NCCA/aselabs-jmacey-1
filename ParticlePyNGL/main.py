#!/usr/bin/env -S uv run --script


import sys

import OpenGL.GL as gl
from ncca.ngl import Primitives, Prims, ShaderLib, Transform, Vec3, look_at, perspective
from PySide6.QtCore import Qt
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtOpenGL import QOpenGLWindow
from PySide6.QtWidgets import QApplication

from Emitter import Emitter


class MainWindow(QOpenGLWindow):
    def __init__(self):
        super().__init__()
        self.setTitle("PyNGL Demo")

    def initializeGL(self):
        gl.glClearColor(0.4, 0.4, 0.4, 1.0)
        ShaderLib.load_shader("Pass", "shaders/Vertex.glsl", "shaders/Fragment.glsl")
        ShaderLib.use("Pass")
        Primitives.load_default_primitives()
        self.view = look_at(Vec3(0, 0, 20), Vec3(0, 0, 0), Vec3(0, 1, 0))
        self.project = perspective(45.0, 1, 0.01, 200)
        self.emitter = Emitter(Vec3(0, 0, 0), 10000)
        Primitives.create(Prims.SPHERE, "sphere", 0.1, 20)
        self.startTimer(16)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_MULTISAMPLE)

    def resizeGL(self, w: int, h: int):
        print(f"Resize {w} {h}")
        self.project = perspective(45.0, w / h, 0.1, 200)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_W:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        elif key == Qt.Key_S:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

        self.update()

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glViewport(0, 0, self.width(), self.height())
        tx = Transform()
        for p in self.emitter._particles:
            tx.set_position(p.position.x, p.position.y, p.position.z)
            tx.set_scale(p.size, p.size, p.size)
            ShaderLib.set_uniform("MVP", self.project @ self.view @ tx.get_matrix())
            ShaderLib.set_uniform("colour", p.colour.x, p.colour.y, p.colour.z)
            Primitives.draw("sphere")
        print("paint")

    def timerEvent(self, event):
        self.emitter.update(0.01)
        self.update()


if __name__ == "__main__":
    app = QApplication()
    format = QSurfaceFormat()
    format.setMajorVersion(4)
    format.setMinorVersion(6)
    format.setProfile(QSurfaceFormat.CoreProfile)
    QSurfaceFormat.setDefaultFormat(format)
    print(f"{format.profile()} OpenGL {format.majorVersion()} {format.minorVersion()}")

    win = MainWindow()

    win.resize(1024, 720)
    win.show()
    sys.exit(app.exec())
