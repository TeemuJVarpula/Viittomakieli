from RPLCD import CharLCD
import time

# Initialize the LCD display
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

def text_display_lcd(predicted_character):
    # Clear the display
    lcd.clear()
    # Print the predicted character on the display
    lcd.cursor_pos = (0, 0)
    lcd.write_string(f"Predicted: {predicted_character}")

# Loop keeps the display on as long as the program is running
try:
    # Initialize an empty string to store the predicted characters
    predicted_string = ""
    while True:
        # Prompt the user to enter a predicted character
        predicted_character = input("Enter a predicted character: ")
        # Add the predicted character to the string
        predicted_string += predicted_character
        # Display the current string on the LCD
        text_display_lcd(predicted_string)
except KeyboardInterrupt:
    # Close the display when the program is stopped
    lcd.close()
