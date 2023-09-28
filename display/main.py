import time
import board
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
from modules.config.config import Config



config =Config().conf
i2c = board.I2C()  # uses board.SCL and board.SDA
lcd = character_lcd.Character_LCD_RGB_I2C(i2c=i2c,columns=16, lines=2,address=int(config['I2C']['display'],16))


def boot():
    lcd.message = "Booting up\nChickenCTRL"

    # time.sleep(2)
    # lcd.message = ""
    # lcd.message = '\nPlease wait .  '
    # time.sleep(0.5)
    # lcd.message = '\nPlease wait .. '
    # time.sleep(0.5)
    # lcd.message = '\nPlease wait ...'
    # time.sleep(0.5)

boot()
