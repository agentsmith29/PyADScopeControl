rm -r ../pyinstaller

pyinstaller \
--paths=/c/Users/myjustice/Documents/workspace/fs.captdevicecontrol/src \
--specpath ../pyinstaller/spec \
--distpath ../pyinstaller/spec/dist \
--workpath ../pyinstaller/spec/build \
main.py