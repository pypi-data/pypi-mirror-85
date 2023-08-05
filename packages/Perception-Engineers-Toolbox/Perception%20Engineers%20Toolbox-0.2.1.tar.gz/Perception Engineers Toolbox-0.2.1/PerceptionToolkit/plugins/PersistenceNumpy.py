from PerceptionToolkit.PluginInterfaces import IPersistencePlugin
import numpy as np
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
from typing import List, Dict, Any
import tabel as tb

# TODO figure out how to save the header and aliases and stuff as well
# Also how to save the strings. Making them objects is kind of nonsense as we loose a lot of the speed advantage.
# IN DEVELOPMENT. DO NOT USE IN PRODUCTION.

class PersistenceNumpy(IPersistencePlugin):
    def __init__(self):
        super(PersistenceNumpy, self).__init__()
        self.filename: str = ""

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.filename = parameters["filename"]

    @staticmethod
    def version() -> Version:
        return Version(0, 0, 1)

    def read(self) -> List[DataModel]:
        assert len(self.filename) > 0

        model = DataModel()
        loaded_data = np.load(self.filename, allow_pickle=True)

        assert 'header' in loaded_data
        assert 'raw' in loaded_data
        assert 'alias' in loaded_data

        model.column_alias = loaded_data['alias'].item()
        model.header = loaded_data['header']
        model.raw = loaded_data['raw']
        # check consistency
        assert np.size(model.raw, 1) == np.size(model.header)  # header columns = data columns
        for alias in model.column_alias:  # aliases point to existing columns
            assert (model.column_alias[alias] >= 0) and model.column_alias[alias] < np.size(model.raw, 1)

        if 'events' in loaded_data:
            model.events = loaded_data['events']
        if 'metrics' in loaded_data:
            model.metrics = loaded_data['metrics']

        IPersistencePlugin.report(model)

        return [model]

    def write(self, data: DataModel) -> None:
        data.raw.save(self.filename, 'npz', False)
        # TODO save other fields too, especially care about headers
