from PySide2 import QtCore
from PySide2.QtWidgets import QDial, QHBoxLayout, QLabel, QVBoxLayout, QWidget


class RotationDial(QDial):
    rotationDialGroupMemberChanged = QtCore.Signal(int, float)

    def __init__(self, value: int = 0, index: int = 0, parent=None):
        super(RotationDial, self).__init__(parent)

        self.index = index

        self.setNotchesVisible(True)
        self.setWrapping(True)
        self.setMinimum(0)
        self.setMaximum(360)
        self.setValue(value)

        self.valueChanged.connect(lambda value: self.rotationDialGroupMemberChanged.emit(self.index, value))


class RotationDialGroup(QWidget):
    layout: QHBoxLayout

    rotationDialGroupMemberChanged = QtCore.Signal(int, float)

    def __init__(self, x: int, y: int, z: int, parent=None):
        super(RotationDialGroup, self).__init__(parent)

        self.layout = QHBoxLayout(self)

        for i, value in enumerate((x, y, z)):
            dial_group = QWidget()
            dial_group_layout = QVBoxLayout(dial_group)

            label_text = "X" if i == 0 else "Y" if i == 1 else "Z"
            label = QLabel(label_text, alignment=QtCore.Qt.AlignCenter)
            dial_group_layout.addWidget(label)
            dial = RotationDial(value, i)
            dial_group_layout.addWidget(dial)
            dial.rotationDialGroupMemberChanged.connect(self.rotationDialGroupMemberChanged.emit)

            self.layout.addWidget(dial_group)
