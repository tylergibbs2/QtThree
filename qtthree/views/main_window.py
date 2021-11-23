from typing import Optional

import pyqtgraph.opengl as gl
from PySide2 import QtCore
from PySide2.QtWidgets import (QAction, QDialog, QFileDialog, QMainWindow,
                               QToolBar)

from qtthree.shapes import Box, CustomShape, Sphere
from qtthree.shapes.abstract_shape import AbstractShape
from qtthree.utils.serializer import Serializer
from qtthree.views.editor import Editor
from qtthree.views.extended_glviewwidget import ExtendedGLViewWidget


class MainWindow(QMainWindow):
    graphics: ExtendedGLViewWidget
    toolbar: QToolBar
    editor: Optional[Editor] = None

    serializer: Serializer

    def __init__(self, serializer: Serializer) -> None:
        super().__init__()
        self.serializer = serializer

        self.setGeometry(50, 50, 1600, 800)

        self.setup_toolbar()
        self.setup_views()
        self.statusBar()

        self.setWindowTitle('qtthree')

        loaded = 0
        for shape in self.serializer.restore_all_shapes():
            loaded += 1
            self.graphics.addItem(shape)
            if self.editor is not None:
                self.editor.add_shape_to_list(shape)

        if loaded:
            self.statusBar().showMessage(f"{loaded} shapes loaded")

    def clone_shape(self, shape: AbstractShape) -> None:
        """
        Clones the given shape and adds it to the scene.

        Parameters
        ----------
        shape : AbstractShape
            The shape to clone.
        """
        new_shape = shape.clone()
        self.graphics.addItem(new_shape)
        if self.editor is not None:
            self.editor.add_shape_to_list(new_shape)

        self.serializer.save_shape(new_shape)
        self.statusBar().showMessage("Shape cloned")

    def delete_shape(self, shape: str) -> None:
        """
        Deletes the shape with the given UUID from the scene.

        Parameters
        ----------
        shape : str
            The UUID of the shape to delete.
        """
        self.statusBar().showMessage("Shape deleted")
        self.graphics.removeShape(shape)
        self.serializer.remove_shape(shape)

    def setup_scene_editor(self) -> None:
        """
        Sets up the scene editor. Spawns the instance,
        and then hooks into the events that are called
        upon shape deletion or clone.
        """
        if self.editor is not None:
            self.editor.show()
            return

        self.editor = Editor(self, self.serializer)
        self.editor.deleteShape.connect(self.delete_shape)
        self.editor.cloneShape.connect(self.clone_shape)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.editor, QtCore.Qt.Orientation.Horizontal)

    def setup_views(self) -> None:
        """
        Sets up the views. Spawns the graphics widget, and then
        also sets up the scene editor docked widget.
        """
        self.graphics = ExtendedGLViewWidget()
        self.graphics.selectMesh.connect(self.onSelectMesh)
        self.setup_scene_editor()

        self.setCentralWidget(self.graphics)

    def setup_toolbar(self) -> None:
        """
        Sets up the toolbar. Creates all of the menus,
        dropdown items, and hooks into their events.
        """
        menu = self.menuBar()

        new_button = QAction("New Scene", self)
        new_button.triggered.connect(self.onNewButtonClick)

        wireframe_button = QAction("Object Wireframes", self)
        wireframe_button.triggered.connect(self.onWireframeButtonClick)
        wireframe_button.setCheckable(True)

        grid_button = QAction("Grid", self)
        grid_button.triggered.connect(self.onGridButtonClick)
        grid_button.setCheckable(True)
        grid_button.setChecked(True)

        file_menu = menu.addMenu("File")
        file_menu.addAction(new_button)
        file_menu.addAction(wireframe_button)
        file_menu.addAction(grid_button)

        box_button = QAction("New Box...", self)
        box_button.triggered.connect(self.onBoxButtonClick)
        sphere_button = QAction("New Sphere...", self)
        sphere_button.triggered.connect(self.onSphereButtonClick)
        custom_button = QAction("New shape from STL...", self)
        custom_button.triggered.connect(self.onCustomButtonClick)

        new_menu = menu.addMenu("Create")
        new_menu.addAction(box_button)
        new_menu.addAction(sphere_button)
        new_menu.addAction(custom_button)

        scene_editor_button = QAction("Scene Editor", self)
        scene_editor_button.triggered.connect(self.onSceneEditorButtonClick)

        views_menu = menu.addMenu("Views")
        views_menu.addAction(scene_editor_button)

    def onSelectMesh(self, mesh: gl.GLMeshItem) -> None:
        """
        Called when a mesh is clicked on in the 3D space.

        Forwards the event to the editor, where it can highlight
        the mesh's shape in the object list.

        Parameters
        ----------
        mesh : gl.GLMeshItem
            The mesh that was clicked on.
        """
        if self.editor is None:
            return

        self.editor.select_mesh(mesh)

    def onNewButtonClick(self) -> None:
        """
        Called when the new scene button is clicked.

        Resets the scene and empties the stored data.
        """
        self.graphics.clearScene()

        if self.editor is not None:
            self.editor.reset()

        self.serializer.clear_data()

    def onBoxButtonClick(self) -> None:
        """
        Called when the new Box button is clicked.

        Creates a new Box and adds it to the scene.
        """
        new_shape = Box()
        self.graphics.addItem(new_shape)
        if self.editor is not None:
            self.editor.add_shape_to_list(new_shape)

        self.serializer.save_shape(new_shape)
        self.statusBar().showMessage("Box added")

    def onSphereButtonClick(self) -> None:
        """
        Called when the new Sphere button is clicked.

        Creates a new Sphere and adds it to the scene.
        """
        new_shape = Sphere()
        self.graphics.addItem(new_shape)
        if self.editor is not None:
            self.editor.add_shape_to_list(new_shape)

        self.serializer.save_shape(new_shape)
        self.statusBar().showMessage("Sphere added")

    def onCustomButtonClick(self) -> None:
        """
        Called when the new Custom Shape button is clicked.

        Queries the user for a file path, and then loads,
        a new Custom Shape and adds it to the scene.
        """
        file_dialog = QFileDialog(self, "Custom STL file")
        file_dialog.setNameFilter("STL files (*.stl)")
        if file_dialog.exec_() != QDialog.Accepted:
            return

        file_path = file_dialog.selectedFiles()[0]
        if not file_path.lower().endswith(".stl"):
            self.statusBar().showMessage("Invalid file type")
            return

        new_shape = CustomShape(file_path)
        self.graphics.addItem(new_shape)
        if self.editor is not None:
            self.editor.add_shape_to_list(new_shape)

        self.serializer.save_shape(new_shape)
        self.statusBar().showMessage("Custom shape added")

    def onWireframeButtonClick(self, status: bool) -> None:
        """
        Called when the wireframe toggle button is clicked.

        Parameters
        ----------
        status : bool
            The new status of the button.
        """
        self.graphics.toggleWireframe(status)

    def onSceneEditorButtonClick(self) -> None:
        """
        Called when the scene editor button is clicked.

        Shows the scene editor.
        """
        self.setup_scene_editor()

    def onGridButtonClick(self, status: bool) -> None:
        """
        Called when the grid toggle button is clicked.

        Parameters
        ----------
        status : bool
            The new status of the button.
        """
        self.graphics.toggleGrid(status)
