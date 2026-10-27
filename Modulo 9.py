import time
import board
from PIL import Image, ImageDraw
import adafruit_ssd1306

# Configurar el bus I2C usando la librería moderna 'board'
i2c = board.I2C()

# Configuración de la pantalla OLED (128x32 píxeles, dirección I2C 0x3C)
oled_width = 128
oled_height = 32
disp = adafruit_ssd1306.SSD1306_I2C(oled_width, oled_height, i2c, addr=0x3C)

# Limpiar la pantalla al iniciar
disp.fill(0)
disp.show()

# Crear una imagen en blanco para dibujar
image = Image.new('1', (disp.width, disp.height))
draw = ImageDraw.Draw(image)

def draw_bitmap(x, y, bitmap):
    for i in range(10):
        for j in range(10):
            if (bitmap[i] >> (9 - j)) & 1:
                draw.point((x + j, y + i), fill=1)  # <- Usando point en lugar de pixel

# 1. Primer mapa de bits (Letra 'E')
ecci_bitmap_1 = [
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

# 2. Segundo mapa de bits (Letra 'C')
ecci_bitmap_2 = [
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

# Dibujar las dos letras en diferentes posiciones (X, Y)
draw_bitmap(20, 10, ecci_bitmap_1)  # Dibuja la 'E'
draw_bitmap(40, 10, ecci_bitmap_2)  # Dibuja la 'C'

# Mostrar la imagen en la pantalla OLED
disp.image(image)
disp.show()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    disp.fill(0)
    disp.show()
