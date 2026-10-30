
import board
import adafruit_ssd1306
import time

i2c = board.I2C()

disp = adafruit_ssd1306.SSD1306_I2C(
    128, 32, i2c, addr=0x3C
)

# Limpiar pantalla
disp.fill(0)
disp.show()


ecci_bitmap = [
    0b111111111111,
    0b111111111111,
    0b111100000000,
    0b111100000000,
    0b111111111111,
    0b111111111111,
    0b111100000000,
    0b111100000000,
    0b111111111111,
    0b111111111111
]

ecci_bitmap2 = [
    0b111111111111,
    0b111111111111,
    0b111100000000,
    0b111100000000,
    0b111100000000,
    0b111100000000,
    0b111100000000,
    0b111100000000,
    0b111111111111,
    0b111111111111
]


def draw_ecci(x, y, bitmap):

    for i in range(10):
        for j in range(12):

            if (bitmap[i] >> (11 - j)) & 1:
                disp.pixel(x + j, y + i, 1)


disp.fill(0)

draw_ecci(20, 10, ecci_bitmap)
draw_ecci(40, 10, ecci_bitmap2)

# Actualizar pantalla
disp.show()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:

    disp.fill(0)
    disp.show()
    print("Programa finalizado")
