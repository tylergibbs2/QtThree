from typing import Any, Optional

from PySide2 import QtCore
from PySide2.QtGui import QColor
from PySide2.QtWidgets import (QButtonGroup, QDial, QDoubleSpinBox,
                               QFormLayout, QHBoxLayout, QLineEdit,
                               QPushButton, QWidget)

from qtthree.shapes import AbstractShape
from qtthree.utils.serializer import Serializer
from qtthree.widgets.color_picker import ColorPicker
from qtthree.widgets.rotation_dial import RotationDialGroup
from qtthree.widgets.translation_spinbox import SpinboxGroup


class PropertiesForm(QWidget):
    serializer: Serializer
    layout: QFormLayout
    target: Optional[AbstractShape] = None

    shapeNameChanged = QtCore.Signal(AbstractShape, str)
    deleteShape = QtCore.Signal(str)
    cloneShape = QtCore.Signal(AbstractShape)

    def __init__(self, parent, serializer: Serializer):
        super().__init__(parent)
        self.serializer = serializer

        self.layout = QFormLayout(self)

    def handle_property_update(self, property_: str, value: Any):
        """
        This function handles generic property updates.

        It updates the shape in memory, and then saves the shape.

        Parameters
        ----------
        property_ : str
            The name of the property to be edited.
        value : Any
            The value of the property.
        """
        if self.target is None:
            return

        if property_ == "name":
            self.shapeNameChanged.emit(self.target, value)

        self.target.update_property(property_, value)
        self.serializer.save_shape(self.target)

    def handle_color_update(self, color: QColor) -> None:
        """
        This function handles events from the color picker.

        It updates the shape in memory, and then saves the shape.

        Parameters
        ----------
        color : QColor
            The color to be applied to the shape.
        """
        if self.target is None:
            return

        self.target.update_color(color)
        self.serializer.save_shape(self.target)

    def handle_translation_update(self, property_: str, axis: int, value: float) -> None:
        """
        This function handles events from the translation spinboxes.

        It updates the shape in memory, and then saves the shape.

        Parameters
        ----------
        property_ : str
            The name of the property to be edited.
        axis : int
            The axis of translation.
        value : float
            The value of the translation.
        """
        if self.target is None:
            return

        self.target.update_translation(property_, axis, value)
        self.serializer.save_shape(self.target)

    def handle_rotation_update(self, axis: int, value: float) -> None:
        """
        This function handles events from the rotation dials.

        It updates the shape in memory, and then saves the shape.

        Parameters
        ----------
        axis : int
            The axis of rotation.
        value : float
            The value of the rotation in degrees.
        """
        if self.target is None:
            return

        self.target.update_rotation(axis, value)
        self.serializer.save_shape(self.target)

    def hook_component_input(self, property_: Optional[str], component: QWidget) -> None:
        """
        Setups up all of the necessary event handlers for
        the target shape's given fields.

        Parameters
        ----------
        property_ : Optional[str]
            The name of the property to be edited.
        component : QWidget
            The widget that is being edited.
        """
        if self.target is None or property_ is None:
            return

        if isinstance(component, QLineEdit):
            component.textChanged.connect(lambda text: self.handle_property_update(property_, text))
        elif isinstance(component, (QDoubleSpinBox, QDial)):
            component.valueChanged.connect(lambda value: self.handle_property_update(property_, value))
        elif isinstance(component, ColorPicker):
            component.colorChanged.connect(self.handle_color_update)
        elif isinstance(component, SpinboxGroup):
            component.spinboxGroupMemberChanged.connect(lambda index, value: self.handle_translation_update(property_, index, value))
        elif isinstance(component, RotationDialGroup):
            component.rotationDialGroupMemberChanged.connect(self.handle_rotation_update)

    def set_target(self, shape: AbstractShape) -> None:
        """
        When the selected shape is changed, this function
        populates the properties form with all of the fields
        necessary for editing the new target shape.

        Parameters
        ----------
        shape : AbstractShape
            The shape to be edited.
        """
        self.target = shape

        while self.layout.rowCount():
            self.layout.removeRow(0)

        for property, label, component in shape.get_form_components():
            self.layout.addRow(label, component)
            self.hook_component_input(property, component)

        button_group = QWidget()
        button_group_layout = QHBoxLayout(button_group)

        clone_button = QPushButton("Clone Object")
        clone_button.clicked.connect(lambda: self.cloneShape.emit(shape))

        delete_button = QPushButton("Delete Object")
        delete_button.clicked.connect(lambda: self.deleteShape.emit(shape.uuid))

        button_group_layout.addWidget(clone_button)
        button_group_layout.addWidget(delete_button)

        self.layout.addRow(button_group)

        self.update()

    def clear_target(self) -> None:
        """
        When the selected shape is changed or removed,
        this function handles the removal of the fields
        in the properties form.
        """
        self.target = None

        while self.layout.rowCount():
            self.layout.removeRow(0)

        self.update()