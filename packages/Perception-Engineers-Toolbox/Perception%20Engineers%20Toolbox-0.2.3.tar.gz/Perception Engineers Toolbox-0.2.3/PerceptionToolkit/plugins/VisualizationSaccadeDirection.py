from PerceptionToolkit.PluginInterfaces import IVisualizationPlugin
from PerceptionToolkit.EyeMovements import Saccade
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
import numpy as np
from matplotlib.pyplot import figure, show
from typing import Dict, Any, Sequence


class VisualizationSaccadeDirection(IVisualizationPlugin):
    """Plots a line where the good samples are in green, the bad ones are in red.

    This visualization provides a nice overview of the overall data quality and whether a tracking loss occurred at one
    point in time or is dispersed equally over the trial duration.
    """

    def __init__(self):
        super(VisualizationSaccadeDirection, self).__init__()
        self.img_dimension = 600  # px
        self.n_bins = 8

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.img_dimension = parameters.get("img_dimension", self.img_dimension)
        self.n_bins = parameters.get("n_bins", self.n_bins)
        pass

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    def draw(self, data: Sequence[DataModel]) -> np.array:
        # adapted from https://matplotlib.org/1.2.1/examples/pylab_examples/polar_bar.html
        # force square figure and square axes looks better for polar, IMO
        fig = figure(figsize=(8, 8))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
        theta = np.linspace(0.0, 2 * np.pi, self.n_bins + 1)[:-1]  # as 0 and 360 overlap

        radii = 10 * np.random.rand(self.n_bins)
        bin_counts = np.zeros(self.n_bins)
        bin_upper_boundary = np.linspace(0, 360, self.n_bins)
        print(bin_upper_boundary)
        saccades_total = 0  # we need to count, as some saccades might not have a good direction
        for d in data:
            saccades = d.saccades()
            for s in range(0, saccades.shape[0]):
                saccade_direction = Saccade(d, saccades[s, 1], saccades[s, 2]).direction
                if saccade_direction < 0:
                    saccade_direction = 360 + saccade_direction
                if not np.isnan(saccade_direction):
                    assigned_bin = np.argmax(saccade_direction <= bin_upper_boundary)
                    bin_counts[assigned_bin] += 1
                    saccades_total += 1

        # norm to frequencies [0,1]
        bin_counts = bin_counts / saccades_total

        width = 6.3 / self.n_bins * np.ones(self.n_bins)  # np.random.rand(self.n_bins)
        bars = ax.bar(theta, bin_counts, width=width, bottom=0.0, align="edge", linewidth=1, color=(0.6, 0.6, 0.6),
                      edgecolor=(0, 0, 0))
        ax.grid(linestyle='dotted')
        ax.set_rlabel_position(0)
        for r, bar in zip(radii, bars):
            bar.set_alpha(0.5)
        show()

        return np.ones((10, 10)).astype(np.uint8)
