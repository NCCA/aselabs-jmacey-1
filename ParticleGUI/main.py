#!/usr/bin/env -S uv run --script

import sys

from PySide6.QtCore import QFile
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from PyNGLScene import PyNGLScene


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui("MainWidget.ui")
        self.resize(1024, 720)
        self.scene = PyNGLScene()
        self.centralWidget().layout().addWidget(self.scene, 0, 0, 2, 2)
        self._connect_signals_and_slots()

    def _connect_signals_and_slots(self):
        self.max_alive.valueChanged.connect(self.scene.update_max_alive)
        self.num_per_frame.valueChanged.connect(self.scene.update_num_per_frame)

    def load_ui(self, ui_file_name: str) -> None:
        """load ui from a file"""
        try:
            loader = QUiLoader()
            ui_file = QFile(ui_file_name)
            ui_file.open(QFile.ReadOnly)
            loaded_ui = loader.load(ui_file, self)
            self.setCentralWidget(loaded_ui)
            # add all children with object names as attributes of this class
            for child in loaded_ui.findChildren(QWidget):
                name = child.objectName()
                if name:
                    setattr(self, name, child)
            ui_file.close()
        except Exception:
            print(f"Error loading ui file {ui_file_name}")
            raise


def main():
    app = QApplication(sys.argv)
    format = QSurfaceFormat()
    format.setMajorVersion(4)
    format.setMinorVersion(6)
    format.setProfile(QSurfaceFormat.CoreProfile)
    QSurfaceFormat.setDefaultFormat(format)
    print(f"{format.profile()} OpenGL {format.majorVersion()} {format.minorVersion()}")
    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Application error {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
