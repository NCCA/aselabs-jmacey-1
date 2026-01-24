#!/usr/bin/env -S uv run --script

import sys
import traceback

from ncca.ngl import Vec3, logger
from ncca.ngl.widgets import Vec3Widget
from PySide6.QtCore import QFile
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from PyNGLScene import PyNGLScene


class Loader(QUiLoader):
    def createWidget(self, class_name, parent=None, name=""):
        if class_name == "Vec3Widget":
            return Vec3Widget(parent)
        return super().createWidget(class_name, parent, name)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui("MainWidget.ui")
        self.resize(1024, 720)
        self.scene = PyNGLScene()
        self.centralWidget().layout().addWidget(self.scene, 0, 0, 2, 2)
        self._set_custom_widgets()
        self._connect_signals_and_slots()

    def _set_custom_widgets(self):
        self.emitter_pos.set_name("Emitter Pos")
        self.emitter_pos.set_range(-20, 20)
        self.emitter_pos.set_single_step(1.0)

    def _connect_signals_and_slots(self):
        self.max_alive.valueChanged.connect(self.scene.update_max_alive)
        self.num_per_frame.valueChanged.connect(self.scene.update_num_per_frame)
        self.emitter_pos.valueChanged.connect(self.scene.update_emitter_pos)

    def load_ui(self, ui_file_name: str) -> None:
        """load ui from a file"""
        try:
            loader = Loader()
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


class DebugApplication(QApplication):
    """
    A custom QApplication subclass for improved debugging.

    By default, Qt's event loop can suppress exceptions that occur within event handlers
    (like paintGL or mouseMoveEvent), making it very difficult to debug as the application
    may simply crash or freeze without any error message. This class overrides the `notify`
    method to catch these exceptions, print a full traceback to the console, and then
    re-raise the exception to halt the program, making the error immediately visible.
    """

    def __init__(self, argv):
        super().__init__(argv)
        logger.info("Running in full debug mode")

    def notify(self, receiver, event):
        """
        Overrides the central event handler to catch and report exceptions.
        """
        try:
            # Attempt to process the event as usual
            return super().notify(receiver, event)
        except Exception:
            # If an exception occurs, print the full traceback
            traceback.print_exc()
            # Re-raise the exception to stop the application
            raise


if __name__ == "__main__":
    # --- Application Entry Point ---

    # Create a QSurfaceFormat object to request a specific OpenGL context
    format: QSurfaceFormat = QSurfaceFormat()
    # Request 4x multisampling for anti-aliasing
    format.setSamples(4)
    # Request OpenGL version 4.1 as this is the highest supported on macOS
    format.setMajorVersion(4)
    format.setMinorVersion(1)
    # Request a Core Profile context, which removes deprecated, fixed-function pipeline features
    format.setProfile(QSurfaceFormat.CoreProfile)
    # Request a 24-bit depth buffer for proper 3D sorting
    format.setDepthBufferSize(24)
    # Set default format for all new OpenGL contexts
    QSurfaceFormat.setDefaultFormat(format)

    # Apply this format to all new OpenGL contexts
    QSurfaceFormat.setDefaultFormat(format)

    # Check for a "--debug" command-line argument to run the DebugApplication
    if len(sys.argv) > 1 and "--debug" in sys.argv:
        app = DebugApplication(sys.argv)
    else:
        app = QApplication(sys.argv)

    # Create the main window
    window = MainWindow()
    # Set the initial window size
    window.resize(1024, 720)
    # Show the window
    window.show()
    # Start the application's event loop
    sys.exit(app.exec())
