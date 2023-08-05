from PerceptionToolkit.CommandProcessor import *
from yapsy.PluginManager import PluginManager
from typing import Dict


def add_command(controller: CommandProcessor, plugin_manager: PluginManager, plugin_name: str, plugin_action: str,
                plugin_parameters: Dict):
    plugin = CommandProcessor.find_plugin(plugin_manager, plugin_name)
    controller.append_command(Command(plugin, plugin_action, plugin_parameters))


# Runs I-DT with different parameter settings
def brute_force_idt(controller: CommandProcessor, plugin_manager: PluginManager):
    IDTplugin = CommandProcessor.find_plugin(plugin_manager, "EventdetectionIDT")
    for dispersion in range(15, 25, 1):
        for duration in range(50, 70, 1):
            print("Dispersion %i px, min_duration %i ms:"%(dispersion, duration))
            cmd = Command(IDTplugin, "", {"max_fixation_dispersion": dispersion, "min_fixation_duration": duration,
                                          "merge_adjacent_fixations": False})
            controller.execute_command(cmd)


# This function initializes the script.
def run(plugin_manager: PluginManager) -> None:
    print("Executing scripttest.py")

    # Usage of the CommandProcessor is completely optional, you can call plugin function directly as well.
    # However, it is very convenient.
    controller = CommandProcessor()

    add_command(controller, plugin_manager, "PersistenceCSV", "read",
                {"filename": "test/data/TobiiSpectrum120Hz.tsv",
                 "preset": "Tobii"})

    add_command(controller, plugin_manager, "PreprocessGapFill", "", {"max_gap_length": 70})
    add_command(controller, plugin_manager, "PreprocessMedianFilter", "", {"time_window": 30})
    controller.execute()

    brute_force_idt(controller, plugin_manager)
