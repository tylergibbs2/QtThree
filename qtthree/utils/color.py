from typing import Tuple


def hex_to_rgba(hex_color: str) -> Tuple[int, ...]:
    """
    Convert a hex color string to a tuple of RGBA values.

    Parameters
    ----------
    hex_color : str
        The hex color string.

    Returns
    -------
    Tuple[int, ...]
        The RGBA values.
    """
    hex_color = hex_color.lstrip('#').lower()
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (255,)
