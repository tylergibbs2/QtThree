from typing import Dict, Union

import pyqtgraph.opengl as gl
from pyqtgraph.opengl.GLGraphicsItem import GLGraphicsItem
from PySide2 import QtCore
from PySide2.QtGui import QMouseEvent

from qtthree.shapes import AbstractShape


class ExtendedGLViewWidget(gl.GLViewWidget):
    wireframe_status: bool = False
    grid_status: bool = True
    shapes: Dict[str, AbstractShape] = {}

    selectMesh = QtCore.Signal(gl.GLMeshItem)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setBackgroundColor('k')

        self.setCameraPosition(distance=30)
        self.addGrid()

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        """
        Override mousePressEvent to emit a signal when a mesh is clicked.

        Parameters
        ----------
        ev : QMouseEvent
            The mouse event.
        """
        pos = ev.pos()
        items = self.itemsAt(region=(pos.x(), pos.y(), 5, 5))
        for item in items:
            if isinstance(item, gl.GLMeshItem):
                self.selectMesh.emit(item)
                break

        return super().mousePressEvent(ev)

    def addGrid(self) -> None:
        """
        Add a grid to the scene.
        """
        self.addItem(gl.GLGridItem())

    def removeGrid(self) -> None:
        """
        Remove the grid from the scene.
        """
        for item in self.items:
            if not isinstance(item, gl.GLGridItem):
                continue

            self.items.remove(item)
            break

    def addItem(self, item: Union[AbstractShape, GLGraphicsItem]) -> None:
        """
        Add an item to the scene, whether it is a shape or a GLGraphicsItem.

        Maintains the existing settings for wireframe.

        Parameters
        ----------
        item : Union[AbstractShape, GLGraphicsItem]
            The item to add to the scene.
        """

        mesh = None
        if isinstance(item, AbstractShape):
            mesh = item.mesh_item
            mesh.opts["drawEdges"] = self.wireframe_status
            self.shapes[item.uuid] = item
        elif isinstance(item, GLGraphicsItem):
            mesh = item
        else:
            raise TypeError("Item must be of type AbstractShape or GLGraphicsItem.")

        self.items.append(mesh)

        if self.isValid():
            mesh.initialize()

        mesh._setView(self)
        self.update()

    def removeShape(self, shapeId: str) -> None:
        """
        Remove a shape from the scene.

        Parameters
        ----------
        shapeId : str
            The UUID of the shape to remove.
        """
        item = self.shapes.pop(shapeId)
        self.items.remove(item.mesh_item)
        self.update()

    def toggleGrid(self, status: bool) -> None:
        """
        Toggle the grid on or off.

        Parameters
        ----------
        status : bool
            The new status of the grid.
        """
        if status:
            self.addGrid()
        else:
            self.removeGrid()

        self.grid_status = status
        self.update()

    def toggleWireframe(self, status: bool) -> None:
        """
        Toggle the wireframe on or off.

        Parameters
        ----------
        status : bool
            The new status of the wireframe.
        """
        for item in self.items:
            if not isinstance(item, gl.GLMeshItem):
                continue

            md = item.opts["meshdata"]
            if not md.hasFaceIndexedData():
                item.edges = md.edges()
                item.edgeVerts = md.vertexes()
            else:
                item.edges = md.edges()
                item.edgeVerts = md.vertexes(indexed='faces')

            item.opts["drawEdges"] = status

        self.wireframe_status = status
        self.update()

    def clearScene(self) -> None:
        """
        Clear the scene of all shapes.

        This does not remove the grid.
        """
        self.items.clear()
        self.shapes.clear()
        self.update()

        if self.grid_status:
            self.addGrid()
