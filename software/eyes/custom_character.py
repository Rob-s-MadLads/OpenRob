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
    clear = [
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
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
    
    fill = [
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111
    ]
    
    lcd.create_char(0, fill )
    lcd.create_char(1, clear)
#     lcd.create_char(2, fill )
#     lcd.create_char(3, clear)
#     circle = [
#         0b11111,
#         0b10001,
#         0b10001,
#         0b10001,
#         0b10001,
#         0b10001,
#         0b10001,
#         0b11111
#     ]
def display_custom_characters():
    lcd.clear()
    # Create a 2x2 block using the custom characters
    lcd.message = "\x00\n\x01"

if __name__ == "__main__":
    define_custom_characters()
    display_custom_characters()