#!/usr/bin/env -S uv run --script


import sys

import OpenGL.GL as gl
from ncca.ngl import (
    Primitives,
    Prims,
    ShaderLib,
    Transform,
    VAOFactory,
    VAOType,
    Vec3,
    VertexData,
    look_at,
    perspective,
)
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
        self.view = look_at(Vec3(0, 0, 20), Vec3(0, 0, 0), Vec3(0, 1, 0))
        self.project = perspective(45.0, 1, 0.01, 200)
        self.emitter = Emitter(Vec3(0, 0, 0), 10000)
        self.startTimer(16)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_MULTISAMPLE)
        self.vao = VAOFactory.create_vao(VAOType.MULTI_BUFFER, gl.GL_POINTS)
        with self.vao:
            data = VertexData(data=[], size=0)
            self.vao.set_data(data, index=0)  # index 0 is positions
            self.vao.set_data(data, index=1)  # index 1 is colours

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
        gl.glPointSize(4)
        ShaderLib.set_uniform("MVP", self.project @ self.view)
        with self.vao:
            data = VertexData(data=self.emitter.position.flatten(), size=self.emitter.position.nbytes)
            self.vao.set_data(data, index=0)
            self.vao.set_vertex_attribute_pointer(0, 3, gl.GL_FLOAT, 0, 0)

            data = VertexData(data=self.emitter.colour.flatten(), size=self.emitter.colour.nbytes)
            self.vao.set_data(data, index=1)
            self.vao.set_vertex_attribute_pointer(1, 3, gl.GL_FLOAT, 0, 0)

            self.vao.set_num_indices(len(self.emitter.position))
            self.vao.draw()

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
