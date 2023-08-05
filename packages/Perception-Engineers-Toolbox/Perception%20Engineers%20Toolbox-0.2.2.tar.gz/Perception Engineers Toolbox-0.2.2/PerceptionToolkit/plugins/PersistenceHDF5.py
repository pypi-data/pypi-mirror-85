from PerceptionToolkit.PluginInterfaces import IPersistencePlugin
from PerceptionToolkit.Version import Version
import numpy as np
from PerceptionToolkit.DataModel import DataModel
from typing import List, Dict, Any, Sequence
import tabel as tb
import h5py
from ast import literal_eval
from enum import IntEnum


class PersistenceHDF5(IPersistencePlugin):
    """Import a hdf5 file

    IN DEVELOPMENT! DO NOT USE IN PRODUCTION!

    Attributes:
        filename: Which file to load. Can be relative or absolute path.
    """

    VALIDITY_DISABLED: int = -91827  # some random value that is unlikely to appear in reality

    def __init__(self):
        super(PersistenceHDF5, self).__init__()
        self.filename: str = ""

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.filename = parameters["filename"]

    @staticmethod
    def version() -> Version:
        return Version(0, 0, 2)

    def read(self) -> List[DataModel]:
        assert len(self.filename) > 0

        models = []

        data = tb.Tabel()
        model = DataModel()
        with h5py.File(self.filename, 'r') as f:

            for key in list(f.keys()):
                assert isinstance(f[key], h5py.Group)
                # parse aliases for each group (= recording)
                if not data.shape[0] == 0:
                    model.raw = data
                    assert PersistenceHDF5.test_data_assertions(model)
                    models.append(model)
                    model = DataModel()
                    data = tb.Tabel()
                assert key + "/aliases" in f.keys()
                model.accessors = literal_eval(f[key + "/aliases"][()])
                for key_column in list(f[key]):
                    if not key_column == "aliases":
                        data[key_column] = f[key + "/" + key_column][()]

        if not data.shape[0] == 0:
            model.raw = data
            models.append(model)

        [IPersistencePlugin.report(model) for model in models]
        IPersistencePlugin.report_final(models)

        return models

    @staticmethod
    def test_data_assertions(data: DataModel) -> bool:
        duration_ok = data.duration() > 0
        """Makes sure all assumptions we have on the data do hold. (e.g., time is always increasing)"""
        is_sorted = lambda a: np.all(a[:-1] <= a[1:])
        timestamps_ok = is_sorted(data.time())
        return duration_ok and timestamps_ok

    def write(self, data: Sequence[DataModel]) -> None:
        assert len(self.filename) > 0
        # this does not save the aliases.
        for i, d in enumerate(data):
            with h5py.File(self.filename, "w") as f:
                f.create_group("rec_" + str(i))
                for column in d.raw.columns:
                    # if the type is object, it's most likely a string. Save it as such.
                    if d.raw[column].dtype == object:
                        f.create_dataset("rec_" + str(i) + "/" + column, data=d.raw[column], dtype=h5py.string_dtype())
                    else:
                        f.create_dataset("rec_" + str(i) + "/" + column, data=d.raw[column])
                # add the aliases as a separate dataset
                f.create_dataset("rec_" + str(i) + "/" + "aliases",
                                 data=PersistenceHDF5.serialize_enum_dict(d.accessors), dtype=h5py.string_dtype())

    @staticmethod
    def serialize_enum_dict(mydict: Dict[IntEnum, str]) -> str:
        new_dict: Dict[int, str] = {}
        for key, value in mydict.items():
            new_dict[int(key)] = value
        return str(new_dict)
