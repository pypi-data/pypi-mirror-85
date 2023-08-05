from yapsy.PluginManager import IPlugin, PluginManager
from PerceptionToolkit.PluginInterfaces import *


class PEPluginManager(PluginManager):
    def __init__(self):
        PluginManager.__init__(self)
        self.setup_plugins()

    def setup_plugins(self):
        """Initializes the PluginManager, which makes all plugin functionality available to the main program.

        It searches the sub folder "plugins" for *.toolbox-plugin definitions and activates the found plugins.
        """
        self.setPluginPlaces(["PerceptionToolkit/plugins"])
        self.setPluginInfoExtension("toolbox-plugin")

        self.setCategoriesFilter({
            "Persistence": IPersistencePlugin,
            "TrialFilter": ITrialFilterPlugin,
            "Preprocessing": IPreprocessingPlugin,
            "Eventdetection": IEventdetectionPlugin,
            "Visualization": IVisualizationPlugin,
            "Classification": IClassificationPlugin,
            "Metric": IMetricPlugin
        })

        self.collectPlugins()

        print("##### PLUGINS ######")
        for pluginInfo in self.getAllPlugins():
            print("Registering plugin ", pluginInfo.name)
            self.activatePluginByName(pluginInfo.name)
        print("##### PLUGINS ######")
