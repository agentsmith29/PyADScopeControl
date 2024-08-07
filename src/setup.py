from distutils.core import setup

setup(
    name='captdevicecontrol',
    version='1.0.0',
    packages=['ADScopeControl', 'ADScopeControl.view', 'ADScopeControl.model',
              'ADScopeControl.model.submodels', 'ADScopeControl.controller',
              'ADScopeControl.controller.mp_AD2Capture', "ADScopeControl.resources",
              'ADScopeControl.constants'],
    package_dir={'': 'src'},
    url='https://gitlab.tugraz.at/flexsensor-public/captdevicecontrol',
    license=' GNU GENERAL PUBLIC LICENSE v3',
    author='Christoph Schmidt',
    author_email='cschmidt.fs@gmail.com',
    description='A UI for controlling the Analog Discovery Series'
)
