# funity

![PyPI](https://img.shields.io/pypi/v/funity)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/funity)
![PyPI - Status](https://img.shields.io/pypi/status/funity)
![PyPI - License](https://img.shields.io/pypi/l/funity)
![PyPI - Format](https://img.shields.io/pypi/format/funity)
![PyPI - Downloads](https://img.shields.io/pypi/dm/funity)

A Unity3d installation finder and command line helper.

## Installation

```sh
pip install funity
```

## Usage

### In Terminal

```sh
python -m funity

# Outputs a JSON-formatted file containing all Unity3d editors found in the current working directory.

# editor.cache
# [
#   "/Applications/Unity/Hub/Editor/2019.2.6f1"
# ]
```

### In Python

```python
from os import getcwd
from pathlib import Path

from funity import UnityEditor, UnityProject, UnityVersion


cache_dir = Path(getcwd()) / 'editor.cache'

# Find all Unity editor installations and cache the results into 'cache_dir'.
editors = UnityEditor.find_in(cache=str(cache_dir))

version = UnityVersion(2019, 2)

# Filter results to only Unity 2019.2.xfx versions.
editors_2019_2 = [e for e in editors if e.version.is_equal_to(version, fuzzy=True)]

# Throw an exception if no compatible Unity version is found.
if not editors_2019_2:
    raise Exception(f'No Unity {version} found.')

# Get the first Unity 2019.2.xfx editor.
editor = editors_2019_2[0]

# Create a UnityProject instance.
project = UnityProject('/Users/you/Projects/HelloWorld')

# Run 'executeMethod' on the Unity project using the Unity editor CLI.
return_code = editor.run(
    '-projectPath', str(project),
    '-buildTarget', 'Win64',
    '-executeMethod', 'BuildPlayerCommand.Execute',
    cli=True,  # Shorthand for '-batchmode', '-nographics', '-quit', '-silent-crashes'.
    log_func=lambda l: print(l, end='')  # Prints all logs from Unity.
)
```