import time
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
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

# Matriz de ejemplo (tu función 'ecci_bitmap')
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
                # Corregido: se usa draw.point en lugar de draw.pixel
                draw.point((x + j, y + i), fill=1)

# Dibujar las formas
draw_ecci(20, 10)
draw_ecci(40, 10)

# Mostrar la imagen en la pantalla OLED
disp.image(image)
disp.show()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    disp.fill(0)
    disp.show()
