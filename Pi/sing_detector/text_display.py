from RPLCD import CharLCD

# Initialize the LCD display
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

# Initialize an empty string to store the predicted characters
predicted_string = ""

def text_display_lcd(predicted_character):
    global predicted_string  # Declare the variable as global to modify it inside the function
    # Append the predicted character to the string
    predicted_string += predicted_character
    # If the string is longer than 16 characters, truncate it to keep only the last 16 characters
    if len(predicted_string) > 16:
        predicted_string = predicted_string[-16:]
    # Clear the display
    lcd.clear()
    # Print the predicted string on the display
    lcd.cursor_pos = (0, 0)
    lcd.write_string(predicted_string)
