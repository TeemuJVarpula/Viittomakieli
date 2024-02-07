# Sign Language
SignLanguage_project

Project members:
    Teemu Varpula
    Seppo Lipponen
    Jussi Viitala
    Sushila Kandel

Project description:

    Initial plan is to make program that reads sign language signs with camera and translates those to text.

    First version of the program can read one sign, if possible later more. 

    Product:
        button for picture capture (later start of video regognition? )
        input from video camera ( pictures first )
        output to led screen  ( few row screen )
        power button ( optional )
        program 
        
Specs:
    - Discussion is to be made from where the "learning material" is coming from (licenses etc.)
        - Are we using own data/pictures or from some other source

    - "product" should be in small package which is easily used and transported (rasberry pii).

    - Product programming language is chosen to be python. This can be changed later if needed.


++Possible 

        Both direction communication
            + screen for picture/video output
            + Chatgpt support
            + bluetooht support
            + Text to speech output?



Program functionality phases:

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




