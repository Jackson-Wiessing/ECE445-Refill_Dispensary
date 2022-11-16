from machine import Pin, I2C

from ssd1306 import SSD1306_I2C

from oled import Write, GFX, SSD1306_I2C

from oled.fonts import ubuntu_mono_15, ubuntu_mono_20

import utime


WIDTH =128

HEIGHT= 64

i2c=I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)

print("i2c initialization done")

oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

print("post line 22")

write15 = Write(oled, ubuntu_mono_15)

write20 = Write(oled, ubuntu_mono_20)

write20.text("OLED", 0, 0)

write15.text("Display", 0, 10)

oled.text("ElectroniClinic", 0, 20)

oled.show()
