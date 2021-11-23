import pyqtgraph as pg
from PySide2.QtWidgets import QApplication

from qtthree.utils.serializer import Serializer
from qtthree.views.main_window import MainWindow

app = pg.mkQApp(__name__)


def create_application(data_file: str) -> QApplication:
    """
    Creates an instance of the Qt app.

    Parameters
    ----------
    data_file: str
        The path to the data file.
    """
    serializer = Serializer(data_file)
    main_window = MainWindow(serializer)
    main_window.show()

    app = pg.mkQApp(__name__)

    # Prevents views from being garbage collected
    setattr(app, "main_window", main_window)

    return pg.mkQApp(__name__)
