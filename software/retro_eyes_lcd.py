import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
import time

# LCD Configuration
lcd_columns = 8
lcd_rows = 2
lcd_rs = digitalio.DigitalInOut(board.D25)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D23)
lcd_d5 = digitalio.DigitalInOut(board.D17)
lcd_d6 = digitalio.DigitalInOut(board.D18)
lcd_d7 = digitalio.DigitalInOut(board.D22)

lcd = character_lcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
    lcd_columns, lcd_rows)

def define_custom_characters():
    # Define custom characters
    top_left = [
        0b11111,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b11111
    ]
    
    bottom_left = [
        0b11111,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b11111
    ]
    
    top_right = [
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111
    ]
    
    bottom_right = [
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111
    ]
    
    # Store custom characters
    lcd.create_char(0, top_left)  # Store top left
    lcd.create_char(1, bottom_left)  # Store bottom left
    lcd.create_char(2, top_right)  # Store top right
    lcd.create_char(3, bottom_right)  # Store bottom right

def display_custom_characters():
    lcd.clear()
    # Create a 2x2 block using the custom characters
    lcd.message = "\x00\x02\n\x01\x03"

if __name__ == "__main__":
    define_custom_characters()
    display_custom_characters()