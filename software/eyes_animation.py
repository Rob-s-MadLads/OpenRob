import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
import time

class LCDAnimator:
    def __init__(self, lcd_columns=8, lcd_rows=2):
        # LCD Configuration
        self.lcd_columns = lcd_columns
        self.lcd_rows = lcd_rows
        self.lcd_rs = digitalio.DigitalInOut(board.D25)
        self.lcd_en = digitalio.DigitalInOut(board.D24)
        self.lcd_d4 = digitalio.DigitalInOut(board.D23)
        self.lcd_d5 = digitalio.DigitalInOut(board.D17)
        self.lcd_d6 = digitalio.DigitalInOut(board.D18)
        self.lcd_d7 = digitalio.DigitalInOut(board.D22)
        
        self.lcd = character_lcd.Character_LCD_Mono(
            self.lcd_rs, self.lcd_en, self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7,
            self.lcd_columns, self.lcd_rows
        )
        
        self.define_custom_characters()

    def define_custom_characters(self):
        # Define custom characters
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
        test = [
            0b11111,
            0b10001,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
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
        
        # Store custom characters
        self.lcd.create_char(0, fill)  # Store filled character
        self.lcd.create_char(1, clear)  # Store clear character
        self.lcd.create_char(2, test)
    def display_character(self, char_code, col, row):
        # Move cursor to the specified position
        self.lcd.cursor_position(col, row)
        # Display the character
        self.lcd.message = chr(char_code)
    
    def clear_screen(self):
        self.lcd.clear()
    
    def animate_character(self):
        self.clear_screen()
        for row in range(self.lcd_rows):
            for col in range(self.lcd_columns):
                self.display_character(0, col, row)
                time.sleep(0.1)
                self.clear_screen()
                
# if __name__ == "__main__":
animator = LCDAnimator()
#     animator.animate_character()