
import board
import busio
import time

import adafruit_ssd1306
import adafruit_ahtx0

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# ==========================================
# CONFIGURACION DEL BUS I2C
# ==========================================

i2c = board.I2C()


# ==========================================
# CONFIGURACION DE LA PANTALLA OLED
# ==========================================

disp = adafruit_ssd1306.SSD1306_I2C(
    128, 32, i2c, addr=0x3C
)

disp.fill(0)
disp.show()


# ==========================================
# CONFIGURACION DEL SENSOR AHT20
# ==========================================

sensor = adafruit_ahtx0.AHTx0(i2c)


# ==========================================
# CONFIGURACION DE IMAGEN Y TEXTO
# ==========================================

width = disp.width
height = disp.height

image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()


# ==========================================
# LECTURA DE TEMPERATURA Y HUMEDAD
# ==========================================

try:

    while True:

        # Leer temperatura
        temperatura = sensor.temperature

        # Leer humedad relativa
        humedad = sensor.relative_humidity

        # Limpiar imagen
        draw.rectangle(
            (0, 0, width, height),
            outline=0,
            fill=0
        )

        # Mostrar temperatura
        draw.text(
            (0, 2),
            "Temperatura:",
            font=font,
            fill=255
        )

        draw.text(
            (82, 2),
            "{:.1f} C".format(temperatura),
            font=font,
            fill=255
        )

        # Mostrar humedad
        draw.text(
            (0, 18),
            "Humedad:",
            font=font,
            fill=255
        )

        draw.text(
            (82, 18),
            "{:.1f} %".format(humedad),
            font=font,
            fill=255
        )

        # Enviar imagen a la OLED
        disp.image(image)
        disp.show()

        # Mostrar datos en consola
        print("Temperatura: {:.1f} C".format(temperatura))
        print("Humedad: {:.1f} %".format(humedad))

        time.sleep(1)


except KeyboardInterrupt:

    disp.fill(0)
    disp.show()

    print("Programa finalizado")
