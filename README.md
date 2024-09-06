# ADScopeControl: Python Project for Digilent Analog Devices USB Oscilloscope Control

PyADScopeControl (*A*nalog *D*iscovery Scopes) is a Python project developed to control Digilent's [Analog Discovery 
Essentials](https://digilent.com/reference/test-and-measurement/start) USB oscilloscopes.
The following models are fully supported, however only the *Analog Discovery 2* has been tested for use:
- [Analog Discovery 2](https://digilent.com/reference/test-and-measurement/analog-discovery-2/start) (**Tested**)
- [Analog Discovery 3](https://digilent.com/reference/test-and-measurement/analog-discovery-3/start) (**Not** Tested)
- [Analog Discovery Studio](https://digilent.com/reference/test-and-measurement/analog-discovery-studio/start) (**Not** Tested)
- [Digital Discovery](https://digilent.com/reference/test-and-measurement/digital-discovery/start) (**Not** Tested)	

# Installation and Usage
##  Installation
### Using pip and PyPI

```bash
pip install PyADScopeControl
```

### Using pip and the repository

```bash
pip install git+https://github.com/agentsmith29/PyADScopeControl.git
```
### Cloning from source

Clone the repository:
```bash
https://github.com/agentsmith29/PyADScopeControl.git
```
Install dependencies:

```bash
# Create a virtual environment
python -m venv .venv
# Activate the virtual environment on Windows and GitBash
. .venv/bin/activate

# Activate the virtual environment on Windows and cmd
# .venv\Scripts\activate

# Activate the virtual environment on Linux/MacOS
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage
Run the main script:

### Direct Usage
If you just want to run the script directly, you can use the following command:
```bash
python examples/main.py
```

### Using the package
If you want to use the package in your own code, you can import the package and use it as follows:
Package documentation for the config can be found [here (confPy6)](https://github.com/agentsmith29/confPy6).

```python
from PyADScopeControl import ADScopeControl

# The config class, that stores the configuration for the scope
# using the confPy6 package (https://github.com/agentsmith29/confPy6).
conf = CaptDevice.Config()
# Enable the log
conf.internal_log_enabled = False

# --- Create the model, controller, and view. ---

# Pass the config to the model.
model = CaptDevice.Model(conf) 

# Pass the model and None to the controller.
# The second argument start_capture_flag (here set to None) is a multiprocessing.Value that 
# triggers the scope. 
# This can be used to create a shared value between processes (e.g. a trigger by another process)
controller = CaptDevice.Controller(
    model, 
    None # start_capture_flag: multiprocessing.Value, triggers the scope
)

# Create the view
window = CaptDevice.View(model, controller)

# Show the window
window.show()
```

An example how to use this package in conjunction with another package can be found in 
the [PySacherECLControl](https://github.com/agentsmith29/PySacherECLControl) repository.

# GUI

Use the graphical interface to adjust laser parameters, monitor data, and control the laser.
Refer to the user manual or documentation for detailed instructions on specific operations and functionalities.



# Contributing

Contributions to Laser Control are welcome! If you have suggestions for improvements, encounter any issues, or would 
like to add new features, please feel free to open an issue or submit a pull request on the GitHub repository.


# Citing
This project is part of the Software [FlexSensor](https://github.com/agentsmith29/flexsensor), which has been published under DOI [10.2139/ssrn.4828876](https://doi.org/10.2139/ssrn.4828876).

Please cite it correctly.
```
Schmidt, Christoph and Hinum-Wagner, Jakob Wilhelm and Klambauer, Reinhard and Bergmann, Alexander, Flexsensor: Automated Measurement Software for Rapid Photonic Circuits Capturing. Available at SSRN: https://ssrn.com/abstract=4828876 or http://dx.doi.org/10.2139/ssrn.4828876 
```

# License

This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgements
