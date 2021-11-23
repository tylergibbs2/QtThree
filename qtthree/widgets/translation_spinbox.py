from typing import List

from PySide2 import QtCore
from PySide2.QtWidgets import (QDoubleSpinBox, QHBoxLayout, QLabel,
                               QVBoxLayout, QWidget)


class TranslationSpinbox(QDoubleSpinBox):
    index: float

    spinboxGroupMemberChanged = QtCore.Signal(int, float)

    def __init__(self, value: float = 0, index: int = 0, parent=None):
        super().__init__(parent)

        self.index = index

        self.setMinimum(-100)
        self.setMaximum(100)
        self.setValue(value)
        self.valueChanged.connect(lambda value: self.spinboxGroupMemberChanged.emit(self.index, value))


class SpinboxGroup(QWidget):
    layout: QHBoxLayout

    spinBoxes: List[TranslationSpinbox]

    spinboxGroupMemberChanged = QtCore.Signal(int, float)

    def __init__(self, x: int, y: int, z: int, parent=None):
        super(SpinboxGroup, self).__init__(parent)

        self.layout = QHBoxLayout(self)

        for i, value in enumerate((x, y, z)):
            spinbox_group = QWidget()
            spinbox_group_layout = QVBoxLayout(spinbox_group)

            label_text = "X" if i == 0 else "Y" if i == 1 else "Z"
            label = QLabel(label_text, alignment=QtCore.Qt.AlignCenter)
            spinbox_group_layout.addWidget(label)
            spinbox = TranslationSpinbox(value, i)
            spinbox_group_layout.addWidget(spinbox)
            spinbox.spinboxGroupMemberChanged.connect(lambda index, value: self.spinboxGroupMemberChanged.emit(index, value))

            self.layout.addWidget(spinbox_group)

