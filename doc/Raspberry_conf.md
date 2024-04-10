# opencv
	sudo apt install python3-opencv

# Camera
	sudo apt install libcap-dev libcamera-dev python3-picamera2

# Python virtual environment. Mainly for mediapipe
	mkdir PythonEnv
	cd PythonEnv

    # Creates environment and inherit system-site-packages. https://www.raspberrypi.com/documentation/computers/os.html#using-a-separate-environment-for-each-project
	python -m venv --system-site-packages env		

    # Enter into virtual environment (in PythonEnv). "deactivate" to exit.
	source env/bin/activate							

	python -m pip install mediapipe
	python -m pip install scikit-learn

# For possible custom build of mediapipe
	Could replace the need for the virtual environment.

	https://github.com/superuser789/MediaPipe-on-RaspberryPi
	https://github.com/koenvervloesem/bazel-on-arm