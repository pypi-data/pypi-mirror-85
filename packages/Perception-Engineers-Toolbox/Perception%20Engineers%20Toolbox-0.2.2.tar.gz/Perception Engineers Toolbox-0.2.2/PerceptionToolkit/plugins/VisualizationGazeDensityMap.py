from PerceptionToolkit.PluginInterfaces import IVisualizationPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovements import Fixation
from PerceptionToolkit.Version import Version
import PerceptionToolkit.ColorPalettes
import numpy as np
from scipy.stats import multivariate_normal
from typing import Dict, Any, Sequence
import sklearn.neighbors


class VisualizationGazeDensityMap(IVisualizationPlugin):
    """Draws a heatmap (the beautiful way)

    We actually pour Gaussians on top of each other, which is more computationally demanding than producing a fixation
    count map and convolving it with a Gaussian. Somehow I find this way more beautiful, although this is entirely
    personal taste. Live rendering is not possible this way once we aggregate over multiple trials.

    Attributes:
        img_height: height of the heatmap in pixels. Should match your stimulus. Samples outside of the heatmap area
            will be discarded!
        img_width:  width of the heatmap in pixels.
        spread: sigma (covariance) of the Gaussians that are put on top of each other for each sample. Larger values
            produce more smooth heatmaps, smaller ones create more detailed resolution heatmaps. Depends mainly on the
            stimulus resolution and the eye-tracker's precision.
        sample_type: heatmaps can be calculated either based on individual eye-tracker samples (default) or based on
            fixations. When calculating on all samples, samples from saccades are included as well. When calculated on
            fixations, one can either produce a fixation count heatmap or a fixation duration heatmap. The later one
            weights each fixation's contribution to the heatmap by its duration. However, the distribution of samples
            within the fixation is lost for this type of heatmap.
        # TODO how about a heatmap that plots each sample of a fixation, so the spread remains present, yet saccades are excluded?
        show_color_legend: include a color bar in the heatmap image (the resulting image will be larger than the source)
        color_palette: Whether to produce a heatmap, a shadowmap or a heatmap with transparency (default).
    """

    def __init__(self):
        super(VisualizationGazeDensityMap, self).__init__()
        self.img_height: int = int(600)
        self.img_width: int = int(800)
        self.spread: float = 20
        self.sample_type = "sample_count"  # one of ["sample_count", "fixation_count", "fixation_duration"]
        self.show_color_legend = True
        self.color_palette = PerceptionToolkit.ColorPalettes.alpha_heatmap_palette(256)

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.img_height = parameters.get("img_height", self.img_height)
        self.img_width = parameters.get("img_width", self.img_width)
        self.spread = parameters.get("spread", self.spread)
        self.sample_type = parameters.get("sample_type", self.sample_type)
        assert self.sample_type in ["sample_count", "fixation_count", "fixation_duration"]

        self.show_color_legend = parameters.get("show_color_legend", self.show_color_legend)

        palette_switcher = {
            "alpha_heatmap": PerceptionToolkit.ColorPalettes.alpha_heatmap_palette(256),
            "heatmap": PerceptionToolkit.ColorPalettes.heatmap_palette(256),
            "shadowmap": PerceptionToolkit.ColorPalettes.shadowmap_palette(256)
        }
        assert parameters.get("palette", "alpha_heatmap") in palette_switcher
        self.color_palette = palette_switcher[parameters.get("palette", "alpha_heatmap")]

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    @staticmethod
    def cutoff_frequency(eccentricity):
        alpha = 0.106
        e2 = 2.3
        ct0 = 1. / 64
        return (e2 * np.log(1 / ct0)) / (alpha * (eccentricity + e2))

    @staticmethod
    def cutoff_frequency_function(box):
        x = np.linspace(-np.pi, np.pi, box)
        y = VisualizationGazeDensityMap.cutoff_frequency(abs(x))
        # norm to 0,1
        y -= min(y)
        y = y / max(y)
        # outer product
        return np.outer(y, y)

    def draw(self, data: Sequence[DataModel]) -> np.array:
        aggregated_img: np.array = np.zeros((self.img_height, self.img_width), dtype=np.float64)
        for d in data:
            # allocate the density image
            img: np.array = np.zeros((self.img_height, self.img_width), dtype=np.float64)

            x = []
            y = []
            w = []
            if self.sample_type == "sample_count":
                x = d.x()
                y = d.y()

            if self.sample_type == "fixation_count" or self.sample_type == "fixation_duration":
                fixation_centroids = np.apply_along_axis(lambda f: Fixation(d, f[1], f[2]).centroid, 1,
                                                         d.fixations())
                x = fixation_centroids[:, 0]
                y = fixation_centroids[:, 1]
                w = np.apply_along_axis(lambda f: Fixation(d, f[1], f[2]).duration, 1, d.fixations())

            if max(x) >= self.img_width or max(y) >= self.img_height or min(x) < 0 or min(y) < 0:
                print("WARNING! Some samples are outside of the heatmap area. They will be omitted.")

            # norm to image coordinate system ([0,1] if within image)
            x = x / self.img_width
            y = y / self.img_height

            patch_x, patch_y = np.mgrid[-self.spread:self.spread:1, -self.spread:self.spread:1]
            rv = multivariate_normal(mean=None, cov=np.eye(2) * self.spread)
            pos = np.empty(patch_x.shape + (2,))
            pos[:, :, 0] = patch_x
            pos[:, :, 1] = patch_y
            patch = rv.pdf(pos)

            for i in range(0, len(x)):
                # insert patch centered at (x,y)
                xi = patch_y.flatten() + y[i] * self.img_height
                yi = patch_x.flatten() + x[i] * self.img_width
                patch_i = patch.flatten()
                if self.sample_type == "fixation_duration":
                    patch_i = patch_i * w[i]
                valid = np.logical_and(np.logical_and(xi >= 0, xi < self.img_height),
                                       np.logical_and(yi >= 0, yi < self.img_width))
                x_v = np.array(xi[valid]).astype(dtype=int)
                y_v = np.array(yi[valid]).astype(dtype=int)
                img[x_v, y_v] += patch_i[valid]

            aggregated_img += img

        # norm the frequencies as a transfer function to the color scale
        aggregated_img = aggregated_img / np.max(aggregated_img) * 255
        aggregated_img = np.array(aggregated_img).astype(dtype=np.uint8)
        color_img = self.apply_palette(aggregated_img)

        # make the legend available (e.g., imprint on the final image on demand)
        if self.show_color_legend:
            legend_width: int = 30
            legend: np.array = np.zeros((self.img_height, legend_width, 4), dtype=np.float64)
            padding_vertical = int((1. / 7) * legend.shape[0])
            padding_horizontal = int(0.3 * legend.shape[1])
            legend_height = legend.shape[0] - padding_vertical * 2 + 1
            for x in range(padding_horizontal, legend.shape[1] - padding_horizontal):
                for y in range(padding_vertical, legend.shape[0] - padding_vertical):
                    legend[y, x, :] = self.color_palette[256 - int(y / (legend_height + padding_vertical) * 256)]
            color_img = np.concatenate((color_img, legend), axis=1)
        return np.array(color_img).astype(np.uint8)

    def draw_kde(self, data: Sequence[DataModel]) -> np.array:
        # Uses sklearn's KernelDensity estimate. As of now not recommended due to speed issues.
        aggregated_img: np.array = np.zeros((self.img_height, self.img_width), dtype=np.float64)
        for d in data:
            # allocate the density image
            img: np.array = np.zeros((self.img_height, self.img_width), dtype=np.float64)

            x = []
            y = []
            v = d.valid()
            w = []
            if self.sample_type == "sample_count":
                x = d.x()
                y = d.y()
                w = np.ones(len(x))

            if self.sample_type == "fixation_count" or self.sample_type == "fixation_duration":
                fixation_centroids = np.apply_along_axis(lambda f: Fixation(d, f[1], f[2]).centroid, 1,
                                                         d.fixations())
                x = fixation_centroids[:, 0]
                y = fixation_centroids[:, 1]
                w = np.apply_along_axis(lambda f: Fixation(d, f[1], f[2]).duration, 1, d.fixations())

            if max(x) >= self.img_width or max(y) >= self.img_height or min(x) < 0 or min(y) < 0:
                print("WARNING! Some samples are outside of the heatmap area. They will be omitted.")

            # norm to image coordinate system ([0,1] if within image)
            x = x / self.img_width
            y = y / self.img_height

            kd_estimator: sklearn.neighbors.KernelDensity = sklearn.neighbors.KernelDensity(self.spread)
            density_data = np.vstack([x, y])
            kd_estimator.fit(density_data[:, v].T, sample_weight=w[v])
            xv, yv = np.meshgrid(np.arange(0, self.img_height), np.arange(0, self.img_width), sparse=False, indexing='ij')
            xy = np.vstack([xv.ravel() / self.img_width, yv.ravel() / self.img_height]).T
            # this one is slow as ###. Therefore, use of this function does currently not make sense.
            scores = np.exp(kd_estimator.score_samples(xy))
            scores = scores.reshape(xv.shape)
            aggregated_img += scores

        # norm the frequencies as a transfer function to the color scale
        aggregated_img = aggregated_img / np.max(aggregated_img) * 255
        aggregated_img = np.array(aggregated_img).astype(dtype=np.uint8)
        color_img = self.apply_palette(aggregated_img)

        # make the legend available (e.g., imprint on the final image on demand)
        if self.show_color_legend:
            legend_width: int = 30
            legend: np.array = np.zeros((self.img_height, legend_width, 4), dtype=np.float64)
            padding_vertical = int((1. / 7) * legend.shape[0])
            padding_horizontal = int(0.3 * legend.shape[1])
            legend_height = legend.shape[0] - padding_vertical * 2 + 1
            for x in range(padding_horizontal, legend.shape[1] - padding_horizontal):
                for y in range(padding_vertical, legend.shape[0] - padding_vertical):
                    legend[y, x, :] = self.color_palette[256 - int(y / (legend_height + padding_vertical) * 256)]
            color_img = np.concatenate((color_img, legend), axis=1)
        return np.array(color_img).astype(np.uint8)

    def apply_palette(self, img: np.array) -> np.array:
        # convert to RGBA
        color_img = np.stack((img,) * 4, axis=-1)
        for x in range(0, img.shape[0]):
            for y in range(0, img.shape[1]):
                color_img[x, y, :] = self.color_palette[img[x, y]]
        return color_img
