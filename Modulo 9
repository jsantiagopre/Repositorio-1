import board
import busio as io
from time import sleep
import time
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_GPIO.I2C as I2C
import subprocess
RST = None  # Raspberry Pi pin configured to reset the OLED
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_address=0x3C)
disp.begin()
disp.clear()
disp.display()
image = Image.new('1', (disp.width, disp.height))
draw = ImageDraw.Draw(image)
ecci_bitmap = [
    0b1111111111,
    0b1111111111,
    0b1110000000,
    0b1110000000,
    0b1111111111,
    0b1111111111,
    0b1110000000,
    0b1110000000,
    0b1111111111,
    0b1111111111
]
def draw_ecci(x, y):
    for i in range(10):
        for j in range(10):
            if (ecci_bitmap[i] >> (9 - j)) & 1:
                draw.point((x + j, y + i), fill=1)

draw_ecci(20, 10)
ecci_bitmap = [
    0b1111111111,
    0b1111111111,
    0b1110000000,
    0b1110000000,
    0b1110000000,
    0b1110000000,
    0b1110000000,
    0b1110000000,
    0b1111111111,
    0b1111111111
]
def draw_ecci(x, y):
    for i in range(10):
        for j in range(10):
            if (ecci_bitmap[i] >> (9 - j)) & 1:
                draw.point((x + j, y + i), fill=1)

draw_ecci(40, 10)
disp.image(image)
disp.display()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    disp.clear()
    disp.display()
