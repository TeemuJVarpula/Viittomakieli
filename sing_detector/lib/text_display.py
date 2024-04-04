from RPLCD.gpio import CharLCD as CharLCD_1
import RPi.GPIO as GPIO 
from RPLCD.i2c import CharLCD as CharLCD_ic2

GPIO.setmode(GPIO.BOARD) 
# Initialize the LCD display
lcd = CharLCD_1(cols=16, rows=2, pin_rs=37, pin_e=35, pin_rw=23, pins_data=[33, 31, 29, 23],numbering_mode=GPIO.BOARD)
lcd.clear()


# https://medium.com/@thedyslexiccoder/how-to-set-up-a-raspberry-pi-4-with-lcd-display-using-i2c-backpack-189a0760ae15
lcd_i2c = CharLCD_ic2(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
lcd_i2c.clear()


def send(text,accuracies):
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(text)
    
    lcd.cursor_pos = (1, 0)
    lcd.write_string(accuracies)
    
    lcd_i2c.clear()
    lcd_i2c.cursor_pos = (0, 0)
    lcd_i2c.write_string(text)
    
    lcd_i2c.cursor_pos = (1, 0)
    lcd_i2c.write_string(accuracies)