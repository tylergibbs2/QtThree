from typing import List, Tuple

import numpy as np
import pyqtgraph.opengl as gl
from PySide2.QtWidgets import QDoubleSpinBox, QLabel, QLineEdit, QWidget

from qtthree.shapes import AbstractShape


class Box(AbstractShape):
    length: float
    width: float
    height: float

    def __init__(self, **kwargs) -> None:

        self.length = kwargs.pop("length", 1.0)
        self.width = kwargs.pop("width", 1.0)
        self.height = kwargs.pop("height", 1.0)

        mesh = self.generate_meshdata()

        self.mesh_item = gl.GLMeshItem(
            meshdata=mesh,
            smooth=True,
            edgeColor=(0, 0, 0, 1),
            computeNormals=False
        )
        self.sync_transformation_matrix()

        kwargs["name"] = kwargs.get("name", "Box")
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
        vertices = np.array([
            [self.length,   0,          0          ],
            [0,             0,          0          ],
            [0,             self.width, 0          ],
            [0,             0,          self.height],
            [self.length,   self.width, 0          ],
            [self.length,   self.width, self.height],
            [0,             self.width, self.height],
            [self.length,   0,          self.height]
        ], dtype=float)

        faces = np.array([
            [1, 0, 7], [1, 3, 7],
            [1, 2, 4], [1, 0, 4],
            [1, 2, 6], [1, 3, 6],
            [0, 4, 5], [0, 7, 5],
            [2, 4, 5], [2, 6, 5],
            [3, 6, 5], [3, 7, 5]
        ], dtype=int)

        return gl.MeshData(
            vertexes=vertices,
            faces=faces
        )

    def update_property(self, property_: str, value: float) -> None:
        """
        Update the property of the shape.

        Parameters
        ----------
        property_ : str
            The property to update.
        value : float
            The value to update the property to.
        """
        if property_ == "length":
            self.length = value
        elif property_ == "width":
            self.width = value
        elif property_ == "height":
            self.height = value
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
            ("length", QLabel("Length"), QDoubleSpinBox(value=self.length)),
            ("width", QLabel("Width"), QDoubleSpinBox(value=self.width)),
            ("height", QLabel("Height"), QDoubleSpinBox(value=self.height))
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
            "type": "box",
            "length": self.length,
            "width": self.width,
            "height": self.height
        }
