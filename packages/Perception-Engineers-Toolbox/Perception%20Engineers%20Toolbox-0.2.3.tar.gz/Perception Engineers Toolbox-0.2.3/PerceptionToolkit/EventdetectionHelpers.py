import math
import numpy as np
from typing import Sequence, Tuple, List


class Geometry3D:
    """Calculates the 3D geometry between viewer and screen (or stimulus presentation plane).

    An eye-tracker often reports gaze estimates as pixels on a screen. Here, we perform the necessary calculations to
    convert them to degrees of visual angle. Such a measure is more useful for many methods, especially for event
    detection. It allows us to determine eye movement velocity thresholds that are stable across different viewing
    distances and screen sizes / DPI.

    For our calculations we assume the global coordinate system center at the center of the screen (0,0,0) and square
    pixels (the height of a pixel on the screen equals its width).
    """

    def __init__(self, eye: Tuple[float, float, float], stimulus_pixel_size: float):
        """
        Args:
            eye: the 3D position of the eye in world coordinates (= relative to the screen center). If you don't have a
            3D estimate, proceed with the other constructor that simply uses a distance estimate towards the screen.
            stimulus_pixel_size: the physical size of one pixel on the screen in [mm] (you can measure the screen width
            and divide it by the resolution of the screen in that dimension, e.g., 500 mm / 1920 px). In case your gaze
            data contains gaze estimates in millimeters already, you can set this value to 1.0.
        """
        self.eye = eye
        self.stimulus_pixel_size = stimulus_pixel_size

    def __init__(self, eye_distance: float, stimulus_pixel_size: float):
        """
        Args:
            eye_distance: the distance in [mm] between the observer's eye and the stimulus.
            stimulus_pixel_size: the physical size of one pixel on the screen in [mm] (you can measure the screen width
            and divide it by the resolution of the screen in that dimension, e.g., 500 mm / 1920 px).
        """
        self.eye = (0, 0, eye_distance)
        self.stimulus_pixel_size = stimulus_pixel_size

    def degrees_between(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """Calculates the gaze angle change between stimulus location [x1, y1] and [x2, y2] in degrees."""
        v1: Sequence[float, float, float] = (p1[0] * self.stimulus_pixel_size, p1[1] * self.stimulus_pixel_size, 0.)
        v2: Sequence[float, float, float] = (p2[0] * self.stimulus_pixel_size, p2[1] * self.stimulus_pixel_size, 0.)
        v1 -= np.array(self.eye)
        v2 -= np.array(self.eye)
        # cross and norm are performance bottlenecks!
        angle_rad = np.arctan2(np.linalg.norm(Geometry3D.python_cross_product(v1, v2)), np.dot(v1, v2))
        return math.degrees(angle_rad)

    @staticmethod
    def python_cross_product(left, right):
        # For non-vectorized operations, this is the faster option.
        # https://stackoverflow.com/questions/1988091/poor-numpy-cross-performance
        x = ((left[1] * right[2]) - (left[2] * right[1]))
        y = ((left[2] * right[0]) - (left[0] * right[2]))
        z = ((left[0] * right[1]) - (left[1] * right[0]))
        return x, y, z

    def degree2pixels(self, degrees: float) -> float:
        """converts degrees of visual angles to pixels on the screen"""
        distance_to_eye: float = np.linalg.norm(self.eye)
        target_millimeter: float = math.tan(math.radians(degrees)) * distance_to_eye
        return target_millimeter / self.stimulus_pixel_size


class VelocityCalculator:
    """Calculates the velocity at which the eye moves in °/s.

    - We assume a stable sampling frequency. This allows us to implement the calculations much faster than with varying
      frame rate. Therefore, the actually used length of the velocity_calculator_window is reduced to the average
      duration covering an integer number of samples. E.g., when one sample is recorded each 10ms on average, a window
      of 22ms will be reduced to 20 ms.
    - No estimates are delivered in case data that is labeled invalid in contained within the window (nan instead).
    - Velocity estimates are determined from the eye position at the beginning of the window directly to the position at
      the end (as opposed to piece-wise through summing up the inter-sample distances).

    These procedures are consistent with those described by Tobii
    (https://www.tobiipro.com/siteassets/tobii-pro/learn-and-support/analyze/how-do-we-classify-eye-movements/tobii-pro-i-vt-fixation-filter.pdf)

    Attributes:
        velocity_calculator_window: length of the window in [ms] over which the velocity is estimated. Has to span at
            least the duration between two sample points. Longer windows will result in a more stable estimate while
            they will also result in an underestimation of maximum velocity. So, noise reduction can be achieved at the
            cost of typical average filter smoothing effects that might make event detection harder, if exaggerated.
        geometry: conversion functions between pixel coordinates and degrees of visual angle
        sampling_frequency: the number of samples per second that can be expected.
    """

    def __init__(self, velocity_calculator_window: float, geometry: Geometry3D, sampling_frequency: float):
        self.velocity_calculator_window = velocity_calculator_window
        self.geometry = geometry
        self.sampling_frequency = sampling_frequency

    def calculate(self, t: Sequence[float], x: Sequence[float], y: Sequence[float], v: Sequence[float]) -> Sequence[float]:
        """Calculates velocity estimates over a moving window.

        Returned velocity sequence might contain nan, if data marked as invalid is encountered! Calling code must handle
        these correctly.
        """
        assert len(t) == len(x) == len(y) == len(v)

        # Reserve memory for the velocity list
        velocities = [None] * len(t)

        if len(t) < 3:
            print("Number of rows unreasonably small! Calculating velocities is not possible.")
            return velocities

        window_width: int = int(math.ceil(self.velocity_calculator_window / (1000 / self.sampling_frequency)))

        # The plus one makes sure there are at least 2 samples in the time window. It also accounts for integer
        # dividing by 2 in the next steps.
        i = 0
        for i in range(0, len(x)):
            if i > window_width / 2:
                window_start = int(i - window_width / 2)
            else:
                window_start = 0

            window_end: int = int(min(i + window_width / 2, len(x) - 1))

            # calculate no velocities, if the window overlaps with a gap or the beginning or end of recording (Tobii
            # doesn't)
            if any(v[window_start:window_end + 1]) > 1.0:
                velocities[i] = float("nan")  # Comparisons against nan (2 < nan / 2 > nan) will always result in False.
            else:
                # Tobii I-VT actually considers the whole span at once (as opposed to stitching it from the
                # individual sample distances)
                velocities[i] = self.geometry.degrees_between((x[window_start], y[window_start]),
                                                              (x[window_end], y[window_end])) / (
                                            t[window_end] - t[window_start]) * 1000.0
                # *1000 so that we get degree per second instead of milliseconds

        return velocities


class VelocityCalculatorPixels:
    """Calculates the velocity at which the eye moves in Pixels/s.

    - We assume a stable sampling frequency. This allows us to implement the calculations much faster than with varying
      frame rate. Therefore, the actually used length of the velocity_calculator_window is reduced to the average
      duration covering an integer number of samples. E.g., when one sample is recorded each 10ms on average, a window
      of 22ms will be reduced to 20 ms.
    - No estimates are delivered in case data that is labeled invalid in contained within the window (nan instead).
    - Velocity estimates are determined from the eye position at the beginning of the window directly to the position at
      the end (as opposed to piece-wise through summing up the inter-sample distances).

    These procedures are consistent with those described by Tobii
    (https://www.tobiipro.com/siteassets/tobii-pro/learn-and-support/analyze/how-do-we-classify-eye-movements/tobii-pro-i-vt-fixation-filter.pdf)

    Attributes:
        velocity_calculator_window: length of the window in [ms] over which the velocity is estimated. Has to span at
            least the duration between two sample points. Longer windows will result in a more stable estimate while
            they will also result in an underestimation of maximum velocity. So, noise reduction can be achieved at the
            cost of typical average filter smoothing effects that might make event detection harder, if exaggerated.
        sampling_frequency: the number of samples per second that can be expected.
    """

    def __init__(self, velocity_calculator_window: float, sampling_frequency: float):
        self.velocity_calculator_window = velocity_calculator_window
        self.sampling_frequency = sampling_frequency

    def calculate(self, t: Sequence[float], x: Sequence[float], y: Sequence[float], v: Sequence[float]) -> Sequence[float]:
        """Calculates velocity estimates over a moving window.

        Returned velocity sequence might contain nan, if data marked as invalid is encountered! Calling code must handle
        these correctly.
        """
        assert len(t) == len(x) == len(y) == len(v)

        # Reserve memory for the velocity list
        velocities = [float("nan")] * len(t)

        if len(t) < 3:
            print("Number of rows unreasonably small! Calculating velocities is not possible.")
            return velocities

        window_width: int = int(math.ceil(self.velocity_calculator_window / (1000 / self.sampling_frequency)))

        # The plus one makes sure there are at least 2 samples in the time window. It also accounts for integer
        # dividing by 2 in the next steps.
        i: int = 0
        for i in range(0, len(x)):
            if i > window_width / 2:
                window_start = int(i - window_width / 2)
            else:
                window_start = 0

            window_end: int = int(min(i + window_width / 2, len(x) - 1))

            # calculate no velocities, if the window overlaps with a gap or the beginning or end of recording (Tobii
            # doesn't)
            if any(v[window_start:window_end + 1]) > 1.0:
                velocities[i] = float("nan")  # Comparisons against nan (2 < nan / 2 > nan) will always result in False.
            else:
                # Tobii I-VT actually considers the whole span at once (as opposed to stitching it from the
                # individual sample distances)
                velocities[i] = math.sqrt(
                    pow(x[window_start] - x[window_end], 2) + pow(y[window_start] - y[window_end], 2)) / (
                                            t[window_end] - t[window_start]) * 1000.0
                # *1000 so that we get degree per second instead of milliseconds

        return velocities
