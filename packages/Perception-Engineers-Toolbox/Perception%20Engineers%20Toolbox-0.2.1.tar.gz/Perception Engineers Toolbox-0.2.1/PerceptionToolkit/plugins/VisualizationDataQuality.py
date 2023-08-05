from PerceptionToolkit.PluginInterfaces import IVisualizationPlugin
import numpy as np
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
from typing import Dict, Any, Sequence

class VisualizationDataQuality(IVisualizationPlugin):
    """Plots a line where the good samples are in green, the bad ones are in red.

    This visualization provides a nice overview of the overall data quality and whether a tracking loss occurred at one
    point in time or is dispersed equally over the trial duration.

    Attributes:
        img_height: height of one line of validity (for one DataModel). If multiple models are present, blank lines will
                    be inserted in between and the total height will be 2*n_models*img_height-1
    """

    def __init__(self):
        super(VisualizationDataQuality, self).__init__()
        self.img_height = 1

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.img_height = parameters.get("img_height", self.img_height)

    @staticmethod
    def version() -> Version:
        return Version(0, 1, 0)

    def draw(self, data_models: Sequence[DataModel]) -> np.array:
        # allocate the image we draw the image with one pixel per sample. Averaging over a time window can also be
        # performed by resizing the image with interpolation afterwards.
        n_samples = [d.sample_count() for d in data_models]
        n_models = len(data_models)
        # leave a line empty after each entry
        img: np.array = np.zeros((self.img_height * n_models*2 - 1*self.img_height, max(n_samples), 3), dtype=np.uint8)

        # http://colorbrewer2.org/#type=diverging&scheme=RdYlGn&n=5
        color_valid = (26, 150, 65)
        color_invalid = (215, 25, 28)

        for j, data in enumerate(data_models):
            valid = data.valid()

            for i, v in enumerate(valid):
                if v:
                    img[(j*self.img_height*2):(j*self.img_height*2+self.img_height), i, :] = color_valid
                else:
                    img[(j*self.img_height*2):(j*self.img_height*2+self.img_height), i, :] = color_invalid

        return img
