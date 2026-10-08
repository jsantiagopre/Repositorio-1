import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

# ── Pines del Motor Paso a Paso ──
pins = [35, 38, 37, 40]

# ── BUZZER ──
buzzer12 = 12

# ── SERVOMOTOR ──
pwmgpio33 = 33
frecuencia = 50

GPIO.setup(pwmgpio33, GPIO.OUT)
pwm = GPIO.PWM(pwmgpio33, frecuencia)
pwm.start(0)

GPIO.setup(buzzer12, GPIO.OUT)

def porcentaje(angulo):
    if angulo > 180 or angulo < 0:
        return 0
    comienzo = 4
    final = 12.5
    radio = (final - comienzo) / 180
    return comienzo + (angulo * radio)

# ── TOGGLES Y SALIDAS DC ──
TOGGLE_1 = 29
TOGGLE_2 = 31
SALIDA_1 = 7
SALIDA_2 = 11

# ── LCD ──
LCD_RS = 19
LCD_E  = 21
LCD_D4 = 15
LCD_D5 = 16
LCD_D6 = 18
LCD_D7 = 22

bits_datos = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]

LCD_CHR   = True
LCD_CMD   = False
LCD_CHARS = 16
LINE_1    = 0x80
LINE_2    = 0xC0

GPIO.setup(TOGGLE_1, GPIO.IN)
GPIO.setup(TOGGLE_2, GPIO.IN)
GPIO.setup(SALIDA_1, GPIO.OUT)
GPIO.setup(SALIDA_2, GPIO.OUT)

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
for salidas in bits_datos:
    GPIO.setup(salidas, GPIO.OUT)

# ── Funciones LCD ──
def lcd_toggle_enable():
    sleep(0.0005)
    GPIO.output(LCD_E, True)
    sleep(0.0005)
    GPIO.output(LCD_E, False)
    sleep(0.0005)

def lcd_write(bits, mode):
    GPIO.output(LCD_RS, mode)
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10: GPIO.output(LCD_D4, True)
    if bits & 0x20: GPIO.output(LCD_D5, True)
    if bits & 0x40: GPIO.output(LCD_D6, True)
    if bits & 0x80: GPIO.output(LCD_D7, True)
    lcd_toggle_enable()
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01: GPIO.output(LCD_D4, True)
    if bits & 0x02: GPIO.output(LCD_D5, True)
    if bits & 0x04: GPIO.output(LCD_D6, True)
    if bits & 0x08: GPIO.output(LCD_D7, True)
    lcd_toggle_enable()

def lcd_init():
    lcd_write(0x33, LCD_CMD)
    lcd_write(0x32, LCD_CMD)
    lcd_write(0x06, LCD_CMD)
    lcd_write(0x0C, LCD_CMD)
    lcd_write(0x28, LCD_CMD)
    lcd_write(0x01, LCD_CMD)
    sleep(0.0005)

def lcd_texto(message, line):
    message = message.ljust(LCD_CHARS, " ")
    lcd_write(line, LCD_CMD)
    for i in range(LCD_CHARS):
        lcd_write(ord(message[i]), LCD_CHR)

def sonar_zumbador():
    GPIO.output(buzzer12, True)
    sleep(1.0)
    GPIO.output(buzzer12, False)

# ── Secuencia paso a paso (medio paso, más torque) ──
#    IN1  IN2  IN3  IN4
SEQ = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
]

def stepper_girar(pasos, direccion=1, delay=0.005):
    """
    pasos:     número de pasos mecánicos
    direccion: 1 = adelante, -1 = atrás
    delay:     segundos entre fases (5 ms es un buen punto de partida)
    """
    total_fases = len(SEQ)
    for _ in range(pasos):
        for i in range(total_fases):
            # Elegir la fase según dirección
            idx = i if direccion == 1 else (total_fases - 1 - i)
            for pin, estado in zip(pins, SEQ[idx]):
                GPIO.output(pin, estado)
            sleep(delay)
    # Apagar bobinas al terminar para no calentar el driver
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)

# ── Inicialización ──
lcd_init()
ultimo_estado = None
servo_ejecutado = False      # ← bandera para ejecutar el servo UNA sola vez

try:
    while True:
        s1 = GPIO.input(TOGGLE_1)
        s2 = GPIO.input(TOGGLE_2)
        estado_actual = (s1, s2)

        # Zumbador solo al cambiar de estado
        if estado_actual != ultimo_estado:
            if s1 == s2:
                sonar_zumbador()
            ultimo_estado = estado_actual
            servo_ejecutado = False   # ← resetear bandera al cambiar estado

        # ── CASO 1: Giro Izquierda (Motor DC) ──
        if s1 == 1 and s2 == 0:
            lcd_texto('Giro Izquierda', LINE_1)
            GPIO.output(SALIDA_1, 1)
            GPIO.output(SALIDA_2, 0)
            sleep(0.1)

        # ── CASO 2: Giro Derecha (Motor DC) ──
        elif s1 == 0 and s2 == 1:
            lcd_texto('Giro Derecha', LINE_1)
            GPIO.output(SALIDA_1, 0)
            GPIO.output(SALIDA_2, 1)
            sleep(0.1)

        # ── CASO 3: Servomotor ──
        elif s1 == 0 and s2 == 0:
            GPIO.output(SALIDA_1, 0)
            GPIO.output(SALIDA_2, 0)

            if not servo_ejecutado:          # ← solo una vez
                servo_ejecutado = True

                lcd_texto('Servo: 135 deg', LINE_1)
                pwm.ChangeDutyCycle(porcentaje(135))
                sleep(2.0)

                lcd_texto('Servo: 0 deg  ', LINE_1)
                pwm.ChangeDutyCycle(porcentaje(0))
                sleep(2.0)

                # Detener señal PWM → elimina jitter, el servo se queda quieto
                pwm.ChangeDutyCycle(0)

            sleep(0.1)   # ← pausa corta para no saturar la CPU

        # ── CASO 4: Motor Paso a Paso ──
        elif s1 == 1 and s2 == 1:
            GPIO.output(SALIDA_1, 0)
            GPIO.output(SALIDA_2, 0)

            lcd_texto('Paso a Paso >>>', LINE_1)
            stepper_girar(pasos=100, direccion=1, delay=0.005)
            sleep(1.0)

            lcd_texto('Paso a Paso <<<', LINE_1)
            stepper_girar(pasos=100, direccion=-1, delay=0.005)
            sleep(1.0)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
