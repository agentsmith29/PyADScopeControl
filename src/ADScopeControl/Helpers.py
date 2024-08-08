# ======================================================================================================================
# EposCMD64.dll is needed, thus, try to copy it
# ======================================================================================================================
import os
import pathlib
import shutil

def get_pyprojecttoml() -> pathlib.Path:
    # is found in ../../pyconfig.toml
    pytoml_via_git = pathlib.Path(__file__).parent.parent.parent / "pyproject.toml"
    # found in ./pyconfig.toml: Copied to the root dir
    pytoml_via_pip = pathlib.Path(__file__).parent / "pyproject.toml"

    if pytoml_via_git.exists():
        #print("pytoml_via_git:", pytoml_via_git)
        return pytoml_via_git.resolve().absolute()
    elif pytoml_via_pip.exists():
        #print("pytoml_via_pip:", pytoml_via_pip)
        return pytoml_via_pip.resolve().absolute()

