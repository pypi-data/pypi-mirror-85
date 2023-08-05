from PerceptionToolkit.PluginInterfaces import *
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.Version import Version
from typing import Dict, List
from yapsy.PluginManager import IPlugin, PluginManager
from PIL import Image
import yaml


class Command:
    """A Command contains all the information required to call a specific action from a plugin through its execute
    function. It is usually instantiated via parsing of a CommandList file. But you can also create them manually and
    push them to the CommandProcessor stack or call their execute function."""

    def __init__(self, plugin: IToolboxPlugin, action: str = "", parameters=None):
        """
        Args:
            plugin: the plugin object that should be invoked action: tells the CommandProcessor which method from
        the plugin to invoke parameters: a collection of parameters that the plugin might require. Some parameters
        are required by the plugin, while others are provided with reasonable defaults.
        """
        assert plugin
        if parameters is None:
            parameters = {}
        self.plugin = plugin
        self.action = action
        self.parameters = parameters

    def execute(self, data: List[DataModel]):
        """Executes a plugin's functionality on the data

        Which function is called is determined via the Interface implemented by the plugin and the action string,
        in case multiple actions are available (such as loading and saving data to/from a file)

        Args:
            data: a list of all currently loaded datasets
        """

        # Apply parameters, if any
        if len(self.parameters) > 0:
            self.plugin.apply_parameters(self.parameters)

        if isinstance(self.plugin, IPersistencePlugin):
            assert self.action in ["read", "write"]
            if self.action == "read":
                for trial in self.plugin.read():
                    data.append(trial)
            if self.action == "write":
                self.plugin.write(data)

        if isinstance(self.plugin, ITrialFilterPlugin):
            # We need to use mutable list operations here in order to change the original object, not a copy.
            filtered_data = self.plugin.filter(data)
            data.clear()
            for d in filtered_data:
                data.append(d)

        if isinstance(self.plugin, IPreprocessingPlugin):
            for model in data:
                model = self.plugin.process(model)

        if isinstance(self.plugin, IEventdetectionPlugin):
            for model in data:
                self.plugin.detect(model)

        if isinstance(self.plugin, IVisualizationPlugin):
            img = self.plugin.draw(data)
            im = Image.fromarray(img)
            im.save("img.png")

        if isinstance(self.plugin, IClassificationPlugin):
            assert self.action in ["fit", "predict"]

            if self.action == "fit":
                self.plugin.fit(data)

            # TODO how to determine which one to predict?
            if self.action == "predict":
                self.plugin.predict(data[0])

        if isinstance(self.plugin, IMetricPlugin):
            for model in data:
                self.plugin.calculate(model)


class CommandProcessor:
    """Holds and executes a sequence of commands.

    Commands are processed in sequence (not in parallel). Commands later on the stack can access data written to the
    model in earlier steps (e.g., access eye movements detected via an event detection method).
    """

    def __init__(self):
        self.model: List[DataModel] = []
        self.queue: List[Command] = []

    def reset(self):
        self.model = []
        self.queue = []

    def append_command(self, command: Command) -> None:
        """Appends a command to the end of the command queue. The command is not automatically executed,
        but only when the CommandProcessor's execute function is called. """
        self.queue.append(command)

    def execute(self) -> None:
        """Executes the current command queue in order."""
        for command in self.queue:
            command.execute(self.model)
        self.queue = []

    def execute_command(self, cmd: Command) -> None:
        """Executes a command right now, out of the command queue. The command queue is not executed through this."""
        cmd.execute(self.model)

    def parse_command_file(self, filename: str, plugin_manager: PluginManager) -> None:
        """Reads and parses a YAML-formatted commandlist file

        Args:
            filename: the file to load and parse
            plugin_manager: the PluginManager used for acquiring plugin handles
        """
        with open(filename, 'r') as file:
            doc = yaml.load(file, Loader=yaml.FullLoader)
            for command in doc:
                plugin: IPlugin
                action: str = ""
                version: Version = Version()
                parameters: dict = {}
                if "plugin" not in command:
                    print("WARNING! No plugin specified.")
                    continue
                if "action" in command:
                    action = command["action"]
                if "parameters" in command:
                    parameters = command["parameters"]
                if "version" in command:
                    version = Version.from_str(command["version"])

                plugin: IToolboxPlugin = CommandProcessor.find_plugin(plugin_manager, command["plugin"])

                # If this assertion triggers, you are trying to use a plugin that is not available at run-time.
                # Check whether the name of the plugin is written correctly and whether its *.toolbox-plugin in sane and
                # placed in the plugins sub folder.
                assert plugin is not None

                if version:
                    assert version == plugin.version()

                # print("CMD %s:%s"%(command["plugin"], action))
                self.append_command(Command(plugin, action, parameters))
        self.execute()

    @staticmethod
    def find_plugin(plugin_manager: PluginManager, name: str) -> IToolboxPlugin:
        """Get a plugin by name.

        For some reason the standard plugin manager does not offer a possibility to search by name only (instead it
        always requires a category as well). We could move this to a class deriving from PluginManager to get a cleaner
        interface.

        Args:
            plugin_manager: the initialized PluginManager
            name: description string of the plugin

        Returns:
            The plugin with the name search for, or None if not found.
        """
        for pluginInfo in plugin_manager.getAllPlugins():
            if pluginInfo.name == name:
                return pluginInfo.plugin_object
        return None
