from typing import List, Tuple

import pyqtgraph.opengl as gl
from PySide2.QtWidgets import QDoubleSpinBox, QLabel, QWidget

from qtthree.shapes import AbstractShape


class Sphere(AbstractShape):
    radius: float

    def __init__(self, **kwargs) -> None:
        self.radius = kwargs.pop("radius", 1.0)

        mesh = self.generate_meshdata()

        self.mesh_item = gl.GLMeshItem(
            meshdata=mesh,
            smooth=True,
            edgeColor=(0, 0, 0, 1)
        )
        self.sync_transformation_matrix()

        kwargs["name"] = kwargs.get("name", "Sphere")
        super().__init__(**kwargs)

    @classmethod
    def deserialize(cls, data: dict) -> AbstractShape:
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
        return gl.MeshData.sphere(rows=20, cols=20, radius=self.radius)

    def update_property(self, property_: str, value: float) -> None:
        """
        Update a property of the shape.

        Parameters
        ----------
        property_ : str
            The property to update.
        value : float
            The value to update the property to.
        """
        if property_ == "radius":
            self.radius = value
        else:
            super().update_property(property_, value)
            return

        self.mesh_item.setMeshData(meshdata=self.generate_meshdata())
        self.mesh_item.meshDataChanged()

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
            ("radius", QLabel("Radius"), QDoubleSpinBox(value=self.radius))
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
            "type": "sphere",
            "radius": self.radius
        }
