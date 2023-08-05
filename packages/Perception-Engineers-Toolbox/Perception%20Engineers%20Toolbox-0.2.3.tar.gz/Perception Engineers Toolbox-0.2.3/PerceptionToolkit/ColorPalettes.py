from typing import Sequence, Tuple
import numpy as np


def interpolate_colors(scale: Sequence[float], guide_colors: Sequence[Tuple[int, int, int, int]], n_steps: int) \
        -> Sequence[Tuple[int, int, int]]:
    """Generates a color gradient via linear interpolation between the provided colors

    Args:
        scale: the position along the axis where the specified color should be placed
        guide_colors: a color sequence that is placed on the axis and between which is interpolated (RGBA)
        n_steps: how many equally-spaced interpolation steps should be performed. For n_steps = 2, the first and last
                 color along the axis are returned

    Returns:
        interpolated_colors: a sequence of colors interpolated at equally spaced intervals on the color axis defined by
        the provided guide_colors and their position (=scale) on the color axis
    """
    assert len(guide_colors) == len(scale)
    steps = np.linspace(min(scale), max(scale), n_steps)
    interpolated_colors = np.apply_along_axis(lambda x: np.interp(steps, scale, x), 0, np.array(guide_colors))
    return interpolated_colors


def heatmap_palette(n_steps):
    """Typical heatmap color palette from cold colors (blue, green) to warmer ones (yellow, red)

    Args:
        n_steps: how many distinct colors the palette should contain.

    Returns:
        interpolate_colors: a color palette in RGBA format
    """

    scale = (0, 3, 5, 8)
    guide_colors = [
        (50, 136, 189, 255), (230, 245, 152, 255), (254, 224, 139, 255), (213, 62, 79, 255)]  # blue, green, yellow, red
    return interpolate_colors(scale, guide_colors, n_steps)


def alpha_heatmap_palette(n_steps):
    """Typical heatmap color palette with transparency from cold, transparent colors (blue, green) to warmer,
    opaque ones (yellow, red)

    Args:
        n_steps: how many distinct colors the palette should contain.

    Returns:
        interpolate_colors: a color palette in RGBA format
    """

    scale = (0, 3, 5, 8)
    guide_colors = [
        (50, 136, 189, 0), (230, 245, 152, 210), (254, 224, 139, 230), (213, 62, 79, 255)]  # red, yellow, green, blue
    return interpolate_colors(scale, guide_colors, n_steps)


def shadowmap_palette(n_steps):
    """A shadowmap of black color with increasing transparency

    Args:
        n_steps: how many distinct colors the palette should contain.

    Returns:
        interpolate_colors: a color palette in RGBA format
    """

    scale = (0, 1)
    guide_colors = [
        (0, 0, 0, 255), (0, 0, 0, 0)]  # red, yellow, green, blue
    return interpolate_colors(scale, guide_colors, n_steps)
