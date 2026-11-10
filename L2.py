
import time
import board
import busio
import requests

import adafruit_ssd1306
import adafruit_ahtx0

from PIL import Image, ImageDraw, ImageFont


# ==================================================
# CONFIGURACION DE THINGSPEAK
# ==================================================

WRITE_API_KEY = "TU_WRITE_API_KEY"

URL = "https://api.thingspeak.com/update"


# ==================================================
# CONFIGURACION DEL BUS I2C
# ==================================================

i2c = board.I2C()


# ==================================================
# CONFIGURACION DE LA PANTALLA OLED SSD1306
# ==================================================

ANCHO = 128
ALTO = 64

oled = adafruit_ssd1306.SSD1306_I2C(
    ANCHO,
    ALTO,
    i2c,
    addr=0x3C
)

# Limpiar pantalla
oled.fill(0)
oled.show()


# ==================================================
# CONFIGURACION DEL SENSOR AHT20
# ==================================================

sensor = adafruit_ahtx0.AHTx0(i2c)


# ==================================================
# CONFIGURACION DE FUENTES
# ==================================================

try:
    fuente = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        12
    )
except:
    fuente = ImageFont.load_default()


# ==================================================
# FUNCION PARA MOSTRAR DATOS EN LA OLED
# ==================================================

def mostrar_datos(temperatura, humedad):

    imagen = Image.new("1", (ANCHO, ALTO))
    dibujo = ImageDraw.Draw(imagen)

    dibujo.text(
        (0, 0),
        "SISTEMA AHT20",
        font=fuente,
        fill=255
    )

    dibujo.line(
        (0, 17, 128, 17),
        fill=255
    )

    dibujo.text(
        (0, 23),
        "Temperatura:",
        font=fuente,
        fill=255
    )

    dibujo.text(
        (0, 38),
        "{:.1f} C".format(temperatura),
        font=fuente,
        fill=255
    )

    dibujo.text(
        (75, 23),
        "Humedad:",
        font=fuente,
        fill=255
    )

    dibujo.text(
        (75, 38),
        "{:.1f}%".format(humedad),
        font=fuente,
        fill=255
    )

    oled.image(imagen)
    oled.show()


# ==================================================
# FUNCION PARA ENVIAR DATOS A THINGSPEAK
# ==================================================

def enviar_thingspeak(temperatura, humedad):

    datos = {
        "api_key": WRITE_API_KEY,
        "field1": temperatura,
        "field2": humedad
    }

    try:

        respuesta = requests.get(
            URL,
            params=datos,
            timeout=10
        )

        if respuesta.status_code == 200:

            if respuesta.text != "0":
                print("Datos enviados correctamente")
                print("Registro:", respuesta.text)

            else:
                print("No se pudo registrar la informacion")

        else:
            print("Error HTTP:", respuesta.status_code)

    except requests.exceptions.RequestException as error:

        print("Error de conexion:", error)


# ==================================================
# PROGRAMA PRINCIPAL
# ==================================================

print("Iniciando sistema de monitoreo...")
print("Sensor AHT20 + OLED + ThingSpeak")

try:

    while True:

        # Leer temperatura y humedad
        temperatura = sensor.temperature
        humedad = sensor.relative_humidity

        # Mostrar datos por consola
        print("------------------------------")
        print("Temperatura: {:.2f} °C".format(temperatura))
        print("Humedad: {:.2f} %".format(humedad))

        # Mostrar datos en pantalla OLED
        mostrar_datos(temperatura, humedad)

        # Enviar informacion a ThingSpeak
        enviar_thingspeak(temperatura, humedad)

        # Esperar 20 segundos antes de actualizar
        time.sleep(20)


except KeyboardInterrupt:

    print("\nPrograma detenido por el usuario")

    oled.fill(0)
    oled.show()

