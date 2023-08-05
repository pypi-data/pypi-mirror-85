from PerceptionToolkit.CommandProcessor import *
from PerceptionToolkit.PEPluginManager import PEPluginManager
from importlib import import_module
from PerceptionToolkit.Version import version_str

import argparse
                 
"""Perception Engineer's toolbox

A toolbox of easily programmable and adjustable functions for eye-tracking data processing and analysis.

The program is separated into a very minimalistic main program with the responsibility to load and call plugins as well
as to manage their interconnections.
The plugins perform all heavy lifting, such as importing and processing data. Some plugins might require others to be 
run before their functionality is accessible (such as calculating metrics on fixations and detecting fixations). They
also assert these assumptions.

This work is published under CC0 1.0 license. https://creativecommons.org/publicdomain/zero/1.0/deed.de
You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.
Published from Germany.
This work is dual licensed under the MIT license. You can simply use it with the MIT license instead of CC0, if you 
prefer to do so.

For a manual full installation of all dependencies run:
    git clone https://bitbucket.org/fahrensiesicher/perceptionengineerstoolkit.git
    python setup.py install

Optional for profiling:
    pip install snakeviz cprofilev profile-viewer
    run with -B -m cProfile -o output.prof
    snakeviz output.prof or runsnake.exe

Optional for publishing to PyPi:
    pip install twine
    python setup.py sdist
    twine upload dist/*
"""

# MAIN PROGRAM ENTRY #
# Parse command line arguments
parser = argparse.ArgumentParser(description='Perception Engineer\'s Toolkit for eye-tracking data analysis',
                                 epilog='Licensed CC0 v1.0')
parser.add_argument("-C", "--commands", help="CommandList file")
parser.add_argument("-S", "--scriptfile", help="Python script file")
parser.add_argument("-v", "--version", help="Show version string", action='version',
                    version='Perception Engineer\'s Toolkit ' + version_str)
args = parser.parse_args()

# Initialize main components
plugin_manager = PEPluginManager()  # setup_plugins()

if args.commands:
    # read commands from file
    controller = CommandProcessor()
    controller.parse_command_file(args.commands, plugin_manager)

if args.scriptfile:
    # execute a custom script that implements a run function
    module = import_module(args.scriptfile)
    module.run(plugin_manager)
