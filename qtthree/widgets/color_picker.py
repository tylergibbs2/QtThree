from typing import Optional

from PySide2.QtCore import Signal
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QColorDialog, QHBoxLayout, QPushButton, QWidget


class ColorPicker(QWidget):
    layout: QHBoxLayout
    color: QColor

    color_preview: QWidget
    dialog: Optional[QColorDialog]

    colorChanged = Signal(QColor)

    def __init__(self, color: QColor, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout(self)
        self.color = color

        self.setup_children()

    def setup_children(self):
        self.color_preview = QWidget()
        self.update_preview()

        self.layout.addWidget(self.color_preview)

        choose_button = QPushButton("Choose Color")
        choose_button.clicked.connect(self.launch_color_picker)

        self.layout.addWidget(choose_button)

    def update_preview(self):
        self.color_preview.setStyleSheet(f"background-color: rgba{self.color.getRgb()}")

    def on_color_changed(self, color: QColor):
        self.color = color
        self.colorChanged.emit(color)
        self.update_preview()
        self.update()

    def launch_color_picker(self):
        self.dialog = QColorDialog()
        self.dialog.currentColorChanged.connect(self.on_color_changed)
        self.dialog.setOption(QColorDialog.NoButtons, True)
        self.dialog.show()


