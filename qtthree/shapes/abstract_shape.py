from __future__ import annotations

import uuid
from typing import Any, List, Tuple, Union

import numpy as np
import pyqtgraph.opengl as gl
from PySide2 import QtCore
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QLabel, QLineEdit, QWidget

from qtthree.utils.color import hex_to_rgba
from qtthree.widgets import ColorPicker, RotationDialGroup, SpinboxGroup


class AbstractShape:
    uuid: str
    name: str
    color: QColor

    # Used temporarily to store differences in the transformation matrix
    translation: np.ndarray
    rotation: np.ndarray

    transformation_matrix: np.ndarray
    mesh_item: gl.GLMeshItem

    def __init__(self, **kwargs):
        self.uuid = kwargs.pop("uuid", str(uuid.uuid4()))

        self.name = kwargs.pop("name", "AbstractShape")
        self.translation = kwargs.pop("translation", np.array([0, 0, 0], dtype=float))
        if isinstance(self.translation, list):
            self.translation = np.array(self.translation, dtype=float)

        self.rotation = kwargs.pop("rotation", np.array([0, 0, 0], dtype=int))

        color = kwargs.pop("color", "#00a0ff")
        self.update_color(color)

        transformation_matrix = kwargs.pop("transformation_matrix", None)
        if transformation_matrix is not None:
            self.update_transformation_matrix(np.array(transformation_matrix))

    @classmethod
    def deserialize(cls) -> AbstractShape:
        """
        Deserialize the shape from a dictionary.

        Parameters
        ----------
        data : dict
            The serialized shape.

        Returns
        -------
        AbstractShape
            The deserialized shape.
        """
        raise NotImplementedError("Cannot deserialize an AbstractShape.")

    def clone(self) -> AbstractShape:
        shape_data = self.serialize()
        shape_data["uuid"] = str(uuid.uuid4())
        return self.deserialize(shape_data)

    def set_name(self, name: str) -> None:
        """
        Set the name of the shape.

        Parameters
        ----------
        name : str
            The new name.
        """
        self.name = name

    def update_color(self, color: Union[QColor, str]) -> None:
        """
        Update the color of the shape.

        Can be a QColor instance or a hex color string.

        Parameters
        ----------
        color : Union[QColor, str]
            The new color.
        """
        if self.mesh_item is None:
            return

        if isinstance(color, QColor):
            self.color = color
        elif isinstance(color, str):
            rgba = hex_to_rgba(color)
            self.color = QColor(rgba[0], rgba[1], rgba[2], rgba[3])

        self.mesh_item.setColor(self.color.getRgbF())
        self.mesh_item.update()

    def update_transformation_matrix(self, transformation_matrix: np.ndarray) -> None:
        """
        Update the transformation matrix of the shape.

        Parameters
        ----------
        transformation_matrix : np.ndarray
            The new transformation matrix.
        """
        if self.mesh_item is None:
            return

        self.transformation_matrix = transformation_matrix
        self.mesh_item.setTransform(transformation_matrix)

    def sync_transformation_matrix(self) -> None:
        """
        Sync the transformation matrix with the mesh item.

        This is necessary because the local copy of the transformation matrix
        is not updated when the mesh item is rotated/translated/etc.
        """
        if self.mesh_item is None:
            return

        self.transformation_matrix = self.mesh_item.transform().matrix()

    def update_property(self, property_: str, value: Any) -> None:
        """
        Update the property of the shape.

        Parameters
        ----------
        property_ : str
            The property to update.
        value : Any
            The value to update to.
        """
        if property_ == "name":
            self.set_name(value)

        self.mesh_item.update()

    def update_translation(self, property_: str, axis: int, value: float) -> None:
        """
        Update the translation of the shape.

        Parameters
        ----------
        property_ : str
            The property to update.
        axis : int
            The axis to translate along.
        value : float
            The value to translate to.
        """
        if self.mesh_item is None or property_ != "translation":
            return

        old_value = self.translation[axis]
        difference = value - old_value

        self.translation[axis] = value
        if axis == 0:
            self.mesh_item.translate(difference, 0, 0)
        elif axis == 1:
            self.mesh_item.translate(0, difference, 0)
        elif axis == 2:
            self.mesh_item.translate(0, 0, difference)

        self.sync_transformation_matrix()

    def update_rotation(self, axis: int, value: float) -> None:
        """
        Update the rotation of the shape.

        Parameters
        ----------
        axis : int
            The axis to rotate around.
        value : float
            The value to rotate to in degrees.
        """
        if self.mesh_item is None:
            return

        old_value = self.rotation[axis]
        difference = value - old_value

        self.rotation[axis] = value
        if axis == 0:
            self.mesh_item.rotate(difference, 1, 0, 0, local=True)
        elif axis == 1:
            self.mesh_item.rotate(difference, 0, 1, 0, local=True)
        elif axis == 2:
            self.mesh_item.rotate(difference, 0, 0, 1, local=True)

        self.sync_transformation_matrix()

    def get_form_components(self) -> List[Tuple[str, QLabel, QWidget]]:
        """
        Get the form components for the shape.

        Returns
        -------
        List[Tuple[str, QLabel, QWidget]]
            The form components. (property, label, widget)
        """
        return [
            ("uuid", QLabel("UUID"), QLineEdit(self.uuid, readOnly=True)),
            ("name", QLabel("Name"), QLineEdit(self.name)),
            ("color", QLabel("Color"), ColorPicker(self.color)),
            ("translation", QLabel("Translation", alignment=QtCore.Qt.AlignBaseline), SpinboxGroup(self.translation[0], self.translation[1], self.translation[2])),
            ("rotation", QLabel("Rotation", alignment=QtCore.Qt.AlignBaseline), RotationDialGroup(self.rotation[0], self.rotation[1], self.rotation[2])),
        ]

    def serialize(self) -> dict:
        """
        Serialize the shape to a dictionary.

        Returns
        -------
        dict
            The serialized shape.
        """
        return {
            "uuid": self.uuid,
            "name": self.name,
            "color": self.color.name(),
            "transformation_matrix": self.transformation_matrix.tolist(),
            "translation": self.translation.tolist()
        }
