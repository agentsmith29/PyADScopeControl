# ADScopeControl: Python Project for Digilent Analog Devices USB Oscilloscope Control

PyADScopeControl (*A*nalog *D*iscovery Scopes) is a Python project developed to control Digilent's [Analog Discovery 
Essentials](https://digilent.com/reference/test-and-measurement/start) USB oscilloscopes.
The following models are fully supported, however only the *Analog Discovery 2* has been tested for use:
- [Analog Discovery 2](https://digilent.com/reference/test-and-measurement/analog-discovery-2/start) (**Tested**)
- [Analog Discovery 3](https://digilent.com/reference/test-and-measurement/analog-discovery-3/start) (**Not** Tested)
- [Analog Discovery Studio](https://digilent.com/reference/test-and-measurement/analog-discovery-studio/start) (**Not** Tested)
- [Digital Discovery](https://digilent.com/reference/test-and-measurement/digital-discovery/start) (**Not** Tested)	

#  Installation

# Using pip
```bash
pip install PyADScopeControl
```


    Clone the repository:
```bash
git clone https://github.com/agentsmith29/fs.lasercontrol.git
```
## Install dependencies:
## Place the Sacher Laser Library in your working directory
```bash

# Create a virtual environment
python -m venv .venv
# Activate the virtual environment
. .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

# Usage

Run the main script:

```bash
python examples/main.py
```
Use the graphical interface to adjust laser parameters, monitor data, and control the laser.
Refer to the user manual or documentation for detailed instructions on specific operations and functionalities.

# Contributing

Contributions to Laser Control are welcome! If you have suggestions for improvements, encounter any issues, or would like to add new features, please feel free to open an issue or submit a pull request on the GitHub repository.

# License

This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgements