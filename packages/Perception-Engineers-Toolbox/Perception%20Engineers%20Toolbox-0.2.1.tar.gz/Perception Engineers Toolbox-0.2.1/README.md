# Perception Engineer's Toolbox

A toolbox of easily programmable and adjustable functions for eye-tracking data processing and analysis.

The program is separated into a very minimalistic main program with the responsibility to load and call plugins as well
as to manage their interconnections.
The plugins perform all heavy lifting, such as importing and processing data. Some plugins might require others to be
run before their functionality is accessible (such as calculating metrics on fixations and detecting fixations). They
also assert these assumptions.

## Installation from source
The sourcecode is available via git at https://bitbucket.org/fahrensiesicher/perceptionengineerstoolkit/src
1. Install dependencies\
    `python setup.py install`
    You can get rid of a relevant part of the dependencies if you deactivate certain plugins that require those. The core library does not make direct use of them. For a list of plugin dependencies see `toolbox.py`

2. Running the examples\
    `python toolbox.py -C test/commandlist.yaml`\
    `python toolbox.py -S test.scripttest`

## Interfacing with the toolbox
You can run your own analysis either through a YAML command file (see `test/commandlist.yaml` for an example) or through a custom python script (see `test/scripttest.py` for an example).

## License
This work is double-licensed. You can use it with either of the two licenses. 

Perception Engineer's Toolbox is published under CC0 1.0 license. https://creativecommons.org/publicdomain/zero/1.0/deed.de\
* You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.\
* There are no warranties about the work and no liability for all uses of the work, to the fullest extent permitted by applicable law.

Perception Engineer's Toolbox is published under MIT license.
Copyright 2020 Thomas Kübler
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contributing
All contributions (including pull requests) are required to comply with both of the above licenses.

## Building the documentation
`pip install pdoc3`\
`pdoc --html PerceptionToolkit plugins`

## Publishing to PyPi
Check the version number and push a tag to git that starts with release-*.*.*, containing the current version number
