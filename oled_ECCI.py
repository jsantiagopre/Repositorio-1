import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw

# ---------- Configuración de la pantalla ----------
ANCHO, ALTO = 128, 64
i2c = busio.I2C(board.SCL, board.SDA)
disp = adafruit_ssd1306.SSD1306_I2C(ANCHO, ALTO, i2c, addr=0x3C)

# Limpia la pantalla
disp.fill(0)
disp.show()

# Imagen en blanco y negro (modo '1') para dibujar
image = Image.new('1', (ANCHO, ALTO))
draw = ImageDraw.Draw(image)

# ---------- Bitmaps de las letras (10x10) ----------
LETRAS = {
    'E': [
        0b1111111111,
        0b1111111111,
        0b1110000000,
        0b1110000000,
        0b1111111111,
        0b1111111111,
        0b1110000000,
        0b1110000000,
        0b1111111111,
        0b1111111111,
    ],
    'C': [
        0b1111111111,
        0b1111111111,
        0b1110000000,
        0b1110000000,
        0b1110000000,
        0b1110000000,
        0b1110000000,
        0b1110000000,
        0b1111111111,
        0b1111111111,
    ],
    'I': [
        0b1111111111,
        0b1111111111,
        0b0000110000,
        0b0000110000,
        0b0000110000,
        0b0000110000,
        0b0000110000,
        0b0000110000,
        0b1111111111,
        0b1111111111,
    ],
}

# ---------- Función para dibujar una letra ----------
def dibujar_letra(bitmap, x, y, escala=1):
    """Dibuja un bitmap de 10x10. 'escala' agranda cada píxel."""
    for fila in range(10):
        for col in range(10):
            if (bitmap[fila] >> (9 - col)) & 1:
                draw.rectangle(
                    (x + col * escala, y + fila * escala,
                     x + col * escala + escala - 1, y + fila * escala + escala - 1),
                    fill=1)

# ---------- Dibuja "ECCI" ----------
texto = "ECCI"
escala = 2                      # cada letra queda de 20x20 px
separacion = 8
x = 10
y = (ALTO - 10 * escala) // 2   # centrado vertical

for letra in texto:
    dibujar_letra(LETRAS[letra], x, y, escala)
    x += 10 * escala + separacion

# Enviar la imagen a la pantalla
disp.image(image)
disp.show()

# ---------- Mantener el programa en ejecución ----------
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    disp.fill(0)
    disp.show()