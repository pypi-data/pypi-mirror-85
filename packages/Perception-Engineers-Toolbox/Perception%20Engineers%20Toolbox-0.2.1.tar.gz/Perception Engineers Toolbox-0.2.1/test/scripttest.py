from PerceptionToolkit.CommandProcessor import *
from yapsy.PluginManager import PluginManager
from typing import Dict


def add_command(controller: CommandProcessor, plugin_manager: PluginManager, plugin_name: str, plugin_action: str,
                plugin_parameters: Dict):
    plugin = CommandProcessor.find_plugin(plugin_manager, plugin_name)
    controller.append_command(Command(plugin, plugin_action, plugin_parameters))


def unroll_events(events, len):
    evt = np.zeros(len)
    for i in range(0, len):
        current_event = np.logical_and(events[:, 1] <= i, events[:, 2] >= i)
        if np.any(current_event):
            idx = np.where(current_event)[0][0]
            evt[i] = events[idx, 0]
    return evt


def compare_events_SMI(baseline, events) -> float:
    testline = unroll_events(events, len(baseline))
    # this modifies the original data matrix in a not so good way, but we honestly don't care right now.
    baseline[baseline == "0"] = EyeMovementTypes.SACCADE
    baseline[baseline == "Fixation"] = int(EyeMovementTypes.FIXATION)
    baseline[baseline == "Saccade"] = int(EyeMovementTypes.SACCADE)
    print("Matched %d of %d" % (sum(baseline == testline), len(baseline)))
    return sum(baseline == testline) / len(baseline)


def compare_events_Tobii(baseline, events) -> float:
    testline = unroll_events(events, len(baseline))
    # this modifies the original data matrix in a not so good way, but we honestly don't care right now.
    baseline[baseline == "Fixation"] = int(EyeMovementTypes.FIXATION)
    baseline[baseline == "Saccade"] = int(EyeMovementTypes.SACCADE)
    print("Matched %d of %d" % (sum(baseline == testline), len(baseline)))
    return sum(baseline == testline) / len(baseline)


# Prepare data


# Runs I-DT with different parameter settings
def brute_force_idt():
    IDTplugin = CommandProcessor.find_plugin(plugin_manager, "EventdetectionIDT")
    with open("idt.txt", "w") as file:
        for dispersion in range(15, 25, 1):
            for duration in range(50, 70, 1):
                cmd = Command(IDTplugin, "", {"max_fixation_dispersion": dispersion, "min_fixation_duration": duration,
                                              "merge_adjacent_fixations": False})
                controller.executeCommand(cmd)
                score = compare_events_Tobii(controller.model[0].get("Eye movement type"), controller.model[0].events)
                file.write(str(score) + " ")
        file.write("\n")


# Runs I-DT with different parameter settings
def brute_force_ivt(controller: CommandProcessor, plugin_manager: PluginManager):
    IDTplugin = CommandProcessor.find_plugin(plugin_manager, "EventdetectionIVT")
    with open("ivt.txt", "w") as file:
        for distance_eye_to_stimulus in np.arange(100., 1000., 10.):
            for stimulus_pixel_size in np.arange(0.1, 0.4, 0.02):
                cmd = Command(IDTplugin, "", {"distance_eye_to_stimulus": distance_eye_to_stimulus,
                                              "stimulus_pixel_size": stimulus_pixel_size,
                                              "merge_adjacent_fixations": False})
                controller.executeCommand(cmd)
                score = compare_events_Tobii(controller.model[0].get("Eye movement type"), controller.model[0].events)
                file.write(str(score) + " ")
        file.write("\n")


# This function initializes the script.
def run(plugin_manager: PluginManager) -> None:
    print("Executing scripttest.py")

    # Usage of the CommandProcessor is completely optional, you can call plugin function directly as well.
    # However, it is very convenient.
    controller = CommandProcessor()

    add_command(controller, plugin_manager, "PersistenceCSV", "read",
                {"filename": "test/data/TobiiSpectrum120Hz.tsv", "separator": "\t", "skip_header_lines": 0,
                 "comment_symbol": "#", "trial_split_symbol": "", "timestamp_to_ms_factor": 0.001,
                 "invalid_value": -999,
                 "aliases": {"TIME": "Computer timestamp", "LEFT_EYE_X": "Gaze point left X",
                             "LEFT_EYE_Y": "Gaze point left Y",
                             "RIGHT_EYE_X": "Gaze point right X", "RIGHT_EYE_Y": "Gaze point right Y"}})

    add_command(controller, plugin_manager, "PreprocessGapFill", "", {"max_gap_length": 70})
    add_command(controller, plugin_manager, "PreprocessMedianFilter", "", {"time_window": 30})
    controller.execute()

    brute_force_ivt(controller, plugin_manager)
