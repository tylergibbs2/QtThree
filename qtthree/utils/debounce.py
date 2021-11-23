from threading import Timer
from typing import Optional

from qtthree.shapes.abstract_shape import AbstractShape


# Credit: https://gist.github.com/walkermatt/2871026
def debounce(wait: float):
    """
    Decorator that will postpone a functions
    execution until after wait seconds
    have elapsed since the last time it was invoked.

    Parameters
    ----------
    wait : float
        The number of seconds to wait before executing.
    """
    def decorate(fn):
        def get_shape(self, *args, **kwargs) -> Optional[AbstractShape]:
            for arg in (*args, *kwargs.values()):
                if isinstance(arg, AbstractShape):
                    return arg

        def wrapped(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)

            argument_shape = get_shape(*args, **kwargs)
            try:
                if argument_shape == wrapped.shape:
                    wrapped.timer.cancel()
            except AttributeError:
                pass

            if argument_shape is not None:
                wrapped.timer = Timer(wait, call_it)
                wrapped.shape = argument_shape
                wrapped.timer.start()

        return wrapped

    return decorate