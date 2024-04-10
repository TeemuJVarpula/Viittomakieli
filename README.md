# Sign Language

Sign Language_project. 
    Project was part of course and was made within project time line. Project is now ended and archived.

## Project members:

    * Teemu Varpula
    * Seppo Lipponen
    * Jussi Viitala
    * Sushila Kandel

## Project description:

    Initial plan is to make program that reads sign language signs with camera and translates those to text.

    First version of the program can read one sign, if possible later more.

### Product:

        button for picture capture (later start of video recognition? )
        input from video camera ( pictures first )
        output to led screen  ( few row screen )
        power button ( optional )
        program

## Specs:

    - Discussion is to made from where the "learning material" is coming from (licenses etc.)
        - Are we using own data/pictures or from some other source

    - "product" should be in small package which is easily used and transported (raspberry pi).

    - Product programming language is chosen to be python. This can be changed later if needed.

#### Possible

        Both direction communication
            + screen for picture/video output
            + Chatgpt support
            + bluetooth support
            + Text to speech output?

### Program functionality phases:

    main program working
    video camera functioning with rasberry
    output screen functioning with rasberry
    sign language samples/database (one picture of letter first)
    take picture by pressing button
    compare picture to database (return keyword)
    check keyword against wordfile (return word)
    print word to screen (show green led) or show error (show red led)
    program ready for next word

    When starting print welcome text

    Main loop:
        wait for button press
            press button for picture capture
                picture from camera taken
                ?saved to folder?
            check if taken picture is in databse
                returning correct word for picture to output device
                if match does not happen YIELD ERROR!!!!!
            output text to "screen"
                print once

        if shutdown pressed
            say good bye





        input from video camera ( pictures first )
        output to led screen  ( few row screen )
        power button ( optional )
        program

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
