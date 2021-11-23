import json
from typing import Generator

from qtthree.shapes import AbstractShape, Box, CustomShape, Sphere
from qtthree.utils.debounce import debounce


class Serializer:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data: dict) -> None:
        """
        Saves the passed data to the serializer's filename.

        Parameters
        ----------
        data : dict
            The data to save.
        """
        with open(self.filename, 'w') as f:
            f.write(json.dumps(data))

    def load(self) -> dict:
        """
        Loads the data from the serializer's filename.

        Returns
        -------
        dict
            The data loaded from the serializer's filename.
        """
        try:
            with open(self.filename, 'r') as f:
                return json.loads(f.read())
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def restore_all_shapes(self) -> Generator[AbstractShape, None, None]:
        """
        Restores all shapes from the serializer's filename.

        Yields
        ------
        AbstractShape
            The shape that was restored.
        """
        data = self.load()
        for shape_data in data.values():
            if shape_data["type"] == "box":
                yield Box.deserialize(shape_data)
            elif shape_data["type"] == "sphere":
                yield Sphere.deserialize(shape_data)
            elif shape_data["type"] == "custom":
                yield CustomShape.deserialize(shape_data)

    @debounce(0.5)
    def save_shape(self, shape: AbstractShape) -> None:
        """
        Saves the passed shape to the serializer's filename.

        0.5 seconds debounce to prevent saving excessively.

        Parameters
        ----------
        shape : AbstractShape
            The shape to save.
        """
        shape_data = shape.serialize()
        data = self.load()
        data[shape_data["uuid"]] = shape_data
        self.save(data)

    def remove_shape(self, shape: str) -> None:
        """
        Removes the shape with the given UUID from the serializer's filename.

        Parameters
        ----------
        shape : str
            The UUID of the shape to remove.
        """
        data = self.load()
        data.pop(shape, None)
        self.save(data)

    def clear_data(self) -> None:
        """
        Clears the data from the serializer's filename.
        """
        self.save({})
