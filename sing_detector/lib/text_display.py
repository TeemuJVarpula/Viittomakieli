from RPLCD import CharLCD
import RPi.GPIO as GPIO 

# Initialize the LCD display
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

def send(text):
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(text)
