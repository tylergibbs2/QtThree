from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np
import pyqtgraph.opengl as gl
from PySide2 import QtCore
from PySide2.QtWidgets import QLabel, QWidget
from stl import mesh as stl_mesh

from qtthree.shapes import AbstractShape
from qtthree.widgets import SpinboxGroup


class CustomShape(AbstractShape):
    scale: np.ndarray

    file_path: str
    custom_mesh_file: Optional[stl_mesh.Mesh] = None

    def __init__(self, file_path: str, **kwargs) -> None:

        self.scale = kwargs.pop("scale", np.array([1.0, 1.0, 1.0], dtype=float))
        if isinstance(self.scale, list):
            self.scale = np.array(self.scale, dtype=float)

        self.file_path = file_path

        mesh = self.generate_meshdata()

        self.mesh_item = gl.GLMeshItem(
            meshdata=mesh,
            smooth=True,
            edgeColor=(0, 0, 0, 1),
            computeNormals=False
        )
        self.sync_transformation_matrix()

        kwargs["name"] = kwargs.get("name", "Custom Shape")
        super().__init__(**kwargs)

    @classmethod
    def deserialize(cls, data: dict) -> CustomShape:
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
        return cls(**data)

    def generate_meshdata(self) -> gl.MeshData:
        """
        Generate the mesh data for the shape.

        Returns
        -------
        gl.MeshData
            The mesh data for the shape.
        """
        if self.custom_mesh_file is None:
            self.custom_mesh_file = stl_mesh.Mesh.from_file(self.file_path)

        return gl.MeshData(
            vertexes=self.custom_mesh_file.vectors * self.scale
        )

    def update_translation(self, property_: str, axis: int, value: float) -> None:
        """
        Update the scale of the shape.

        Parameters
        ----------
        property_ : str
            The name of the property to be edited.
        axis : int
            The axis of scale.
        value : float
            The value of the scale.
        """
        super().update_translation(property_, axis, value)
        if self.mesh_item is None or property_ != "scale" or value <= 0.0:
            return

        self.scale[axis] = value
        self.mesh_item.setMeshData(meshdata=self.generate_meshdata())

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
            *super().get_form_components(),
            ("scale", QLabel("Scale", alignment=QtCore.Qt.AlignBaseline), SpinboxGroup(self.scale[0], self.scale[1], self.scale[2])),
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
            **super().serialize(),
            "type": "custom",
            "file_path": self.file_path,
            "scale": self.scale.tolist()
        }
