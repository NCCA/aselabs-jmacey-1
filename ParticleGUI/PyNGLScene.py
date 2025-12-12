#!/usr/bin/env -S uv run --script


import sys

import numpy as np
import OpenGL.GL as gl
from ncca.ngl import (
    FirstPersonCamera,
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
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QApplication

from Emitter import Emitter


class PyNGLScene(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.animate = True
        self.keys_pressed = set()
        self.rotate: bool = False
        self.original_x_pos: int = 0
        self.original_y_pos: int = 0

    @Slot(int)
    def update_max_alive(self, value):
        print("update max alive", value)
        self.emitter.max_alive = value

    def initializeGL(self):
        gl.glClearColor(0.4, 0.4, 0.4, 1.0)
        ShaderLib.load_shader("Pass", "shaders/Vertex.glsl", "shaders/Fragment.glsl")
        ShaderLib.use("Pass")
        self.camera = FirstPersonCamera(Vec3(0, 5, 20), Vec3(0, 0, 0), Vec3(0, 1, 0), 45.0)
        self.emitter = Emitter(Vec3(0, 0, 0), 5000, 2, 1, (30, 200))
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_MULTISAMPLE)
        self.vao = VAOFactory.create_vao(VAOType.MULTI_BUFFER, gl.GL_POINTS)
        with self.vao as vao:
            data = VertexData(data=[], size=0)
            vao.set_data(data, index=0)  # index 0 is positions
            vao.set_data(data, index=1)  # index 1 is colours
        self.startTimer(16)

    def resizeGL(self, w: int, h: int):
        ratio = self.devicePixelRatio()
        self.camera.set_projection(45.0, (w * ratio / h * ratio), 0.05, 200)

    def keyReleaseEvent(self, event):
        key = event.key()
        self.keys_pressed.discard(key)
        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        self.keys_pressed.add(key)
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_W:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        elif key == Qt.Key_S:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        elif key == Qt.Key_A:
            self.animate ^= True
        elif key == Qt.Key_1:
            self.emitter.update(0.01)

        self.update()

    def _process_camera_movements(self):
        x_dir = 0.0
        y_dir = 0.0
        for key in self.keys_pressed:
            if key == Qt.Key_Left:
                y_dir = -1.0
            elif key == Qt.Key_Right:
                y_dir = 1.0
            elif key == Qt.Key_Up:
                x_dir = 1.0
            elif key == Qt.Key_Down:
                x_dir = -1.0

        if x_dir != 0.0 or y_dir != 0.0:
            self.camera.move(x_dir, y_dir, 0.1)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glViewport(0, 0, self.width(), self.height())
        gl.glEnable(gl.GL_PROGRAM_POINT_SIZE)
        self._process_camera_movements()
        ShaderLib.use("Pass")
        ShaderLib.set_uniform("MVP", self.camera.get_vp())
        with self.vao as vao:
            pos_size = np.concatenate([self.emitter.position, self.emitter.size[:, np.newaxis]], axis=1)
            data = VertexData(data=pos_size.flatten(), size=pos_size.nbytes)
            vao.set_data(data, index=0)
            vao.set_vertex_attribute_pointer(0, 4, gl.GL_FLOAT, 0, 0)

            data = VertexData(data=self.emitter.colour.flatten(), size=self.emitter.colour.nbytes)
            vao.set_data(data, index=1)
            vao.set_vertex_attribute_pointer(1, 3, gl.GL_FLOAT, 0, 0)

            vao.set_num_indices(len(self.emitter.position))
            vao.draw()

    def timerEvent(self, event):
        if self.animate:
            self.emitter.update(0.01)
            self.update()

    def mousePressEvent(self, event):
        position = event.position()
        if event.button() == Qt.LeftButton:
            self.original_x_pos = position.x()
            self.original_y_pos = position.y()
            self.rotate = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rotate = False

    def mouseMoveEvent(self, event):
        if self.rotate and event.buttons() == Qt.LeftButton:
            position = event.position()
            diff_x = position.x() - self.original_x_pos
            diff_y = position.y() - self.original_y_pos
            self.original_x_pos = position.x()
            self.original_y_pos = position.y()
            self.camera.process_mouse_movement(diff_x, -diff_y)
            self.update()
