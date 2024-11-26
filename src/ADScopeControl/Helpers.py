import os
from pathlib import Path
import shutil
import sys

def toml_exists(path: Path):
    return (path / 'pyproject.toml').exists()

def resolve_path(path):
    if getattr(sys, "frozen", False):
        # If the 'frozen' flag is set, we are in bundled-app mode!
        p = Path(sys._MEIPASS) / path
    else:
        # Normal development mode. Use os.getcwd() or __file__ as appropriate in your case...
        p = path
    return p.resolve()

def get_pyprojecttoml() -> Path:
    # is found in ../../pyconfig.toml
    pytoml_via_git = resolve_path(Path('../..'))
    if toml_exists(pytoml_via_git):
        return pytoml_via_git
    pytoml_via_pip = resolve_path(Path('.'))
    if toml_exists(pytoml_via_pip):
        return pytoml_via_pip
    pytoml_as_submodule = resolve_path(Path('./.venv/Lib/site-packages/ADScopeControl'))
    if toml_exists(pytoml_as_submodule):
        return pytoml_as_submodule
    return None

