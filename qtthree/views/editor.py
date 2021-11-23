from typing import Any

import pyqtgraph.opengl as gl
from PySide2 import QtCore
from PySide2.QtWidgets import (QDockWidget, QListWidget, QListWidgetItem,
                               QVBoxLayout, QWidget)

from qtthree.shapes.abstract_shape import AbstractShape
from qtthree.utils.serializer import Serializer
from qtthree.views.properties_form import PropertiesForm


class ObjectListItem(QListWidgetItem):
    def __init__(self, shape: AbstractShape, parent: QWidget = None) -> None:
        super().__init__(shape.name, parent)
        self.shape = shape

    def text(self) -> str:
        return self.shape.name


class Editor(QDockWidget):
    serializer: Serializer
    list_view: QListWidget
    properties_form: PropertiesForm

    deleteShape = QtCore.Signal(str)
    cloneShape = QtCore.Signal(AbstractShape)

    def __init__(self, parent, serializer: Serializer) -> None:
        super().__init__("Scene Editor", parent)
        self.serializer = serializer

        self.setWindowTitle("Scene Editor")
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)

        self.onDockLocationChanged(None)
        self.dockLocationChanged.connect(self.onDockLocationChanged)

        self.setup_child_widgets()

    def onDockLocationChanged(self, area: QtCore.Qt.DockWidgetArea) -> None:
        """
        Called when the dock location changes.

        Parameters
        ----------
        area : QtCore.Qt.DockWidgetArea
        """
        self.setMinimumSize(self.parent().width() / 3, self.parent().height())

    def setup_child_widgets(self) -> None:
        """
        Sets up the child widgets of this dock widget.
        """
        multi_widget = QWidget()
        layout = QVBoxLayout(multi_widget)

        self.list_view = QListWidget()
        self.list_view.setMinimumSize(0, int(self.height() * 0.25))
        self.list_view.itemSelectionChanged.connect(self.update_properties_form)

        self.properties_form = PropertiesForm(self, self.serializer)
        self.properties_form.setMinimumSize(0, int(self.height() * 0.75))
        self.properties_form.shapeNameChanged.connect(self.update_shape_name)
        self.properties_form.deleteShape.connect(self.delete_shape)
        self.properties_form.cloneShape.connect(self.cloneShape.emit)

        layout.addWidget(self.list_view)
        layout.addWidget(self.properties_form)

        self.setWidget(multi_widget)

    def select_mesh(self, mesh: gl.GLMeshItem) -> None:
        """
        Selects the given mesh in the object list.

        Parameters
        ----------
        mesh : gl.GLMeshItem
            The mesh to select.
        """
        for i in range(self.list_view.count()):
            item = self.list_view.item(i)
            if item.shape.mesh_item == mesh:
                self.list_view.setCurrentItem(item)
                break

    def reset(self) -> None:
        """
        Clears the object list and properties form.
        """
        self.list_view.clear()
        self.properties_form.clear_target()

    def delete_shape(self, shape: str) -> None:
        """
        Removes the shape with the given UUID from the object list.

        Emits an event that signal the graphics widget to delete the shape.

        Parameters
        ----------
        shape : str
            The UUID of the shape to remove.
        """
        self.deleteShape.emit(shape)
        self.remove_shape_from_list(shape)

    def update_properties_form(self) -> None:
        """
        Updates the properties form to reflect the currently selected shape.

        If no shape is selected, the properties form is cleared.
        """
        selected = self.list_view.selectedItems()
        if not selected:
            self.properties_form.clear_target()
            return

        selected_item = selected[0]
        self.properties_form.set_target(selected_item.shape)

    def update_shape_name(self, shape: AbstractShape, new_name: str) -> None:
        """
        Updates the name of the given shape in the object list.

        Parameters
        ----------
        shape : AbstractShape
            The shape whose name to update.
        new_name : str
            The new name to give the shape.
        """
        for i in range(self.list_view.count()):
            item = self.list_view.item(i)
            if item.shape == shape:
                item.setText(new_name)
                break

    def add_shape_to_list(self, shape: AbstractShape) -> None:
        """
        Adds the given shape to the object list.

        Parameters
        ----------
        shape : AbstractShape
            The shape to add to the list.
        """
        self.list_view.addItem(ObjectListItem(shape, self.list_view))

    def remove_shape_from_list(self, shape: str) -> None:
        """
        Removes the shape with the given UUID from the object list.

        Parameters
        ----------
        shape : str
            The UUID of the shape to remove.
        """
        for i in range(self.list_view.count()):
            item = self.list_view.item(i)
            if item.shape.uuid == shape:
                self.list_view.takeItem(i)
                break
