from RPLCD import CharLCD

# Initialize the LCD display
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

def send(predicted_character):

    lcd.write_string(predicted_character)
