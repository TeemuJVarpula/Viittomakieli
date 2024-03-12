from RPLCD import CharLCD
import time

# Initialize the LCD display
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

def text_display_lcd(predicted_character):
    # Clear the display
    lcd.clear()

    # Print predicted character and accuracy on the display
    lcd.cursor_pos = (0, 0)
    lcd.write_string(f"Predicted: {predicted_character}")

# Loop keeps the display on as long as the program is running
try:
    while True:
        text_display_lcd()
         # Pause the program for 5 seconds before writing new data to the display
        time.sleep(5) 
except KeyboardInterrupt:
    # Close the display when the program is stopped
    lcd.close()  
