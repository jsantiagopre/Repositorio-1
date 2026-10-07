import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

# Pines del Motor Paso a Paso
pins = [35, 38, 37, 40]    # Sentido 1
pins1 = [40, 37, 38, 35]   # Sentido 2

# BUZZER
buzzer12 = 12

# SERVOMOTOR
pwmgpio33 = 33  
frecuencia = 50 

GPIO.setup(pwmgpio33, GPIO.OUT)
pwm = GPIO.PWM(pwmgpio33, frecuencia)
pwm.start(0)  # Se inicia el PWM una sola vez fuera del bucle

GPIO.setup(buzzer12, GPIO.OUT)

def porcentaje(angulo):
    if angulo > 180 or angulo < 0:
        return 0
    comienzo = 4
    final = 12.5
    radio = (final - comienzo) / 180
    return comienzo + (angulo * radio)

TOGGLE_1 = 29
TOGGLE_2 = 31 
SALIDA_1 = 7
SALIDA_2 = 11

LCD_RS = 19
LCD_E = 21
LCD_D4 = 15 
LCD_D5 = 16
LCD_D6 = 18
LCD_D7 = 22 

bits_datos = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]

LCD_CHR = True
LCD_CMD = False
LCD_CHARS = 16
LINE_1 = 0x80
LINE_2 = 0xC0

GPIO.setup(TOGGLE_1, GPIO.IN)
GPIO.setup(TOGGLE_2, GPIO.IN)
GPIO.setup(SALIDA_1, GPIO.OUT)
GPIO.setup(SALIDA_2, GPIO.OUT)

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

for salidas in bits_datos:
    GPIO.setup(salidas, GPIO.OUT)
    
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
    
    if bits & 0x10 == 0x10: GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20: GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40: GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80: GPIO.output(LCD_D7, True)
     
    lcd_toggle_enable()
    
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    
    if bits & 0x01 == 0x01: GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02: GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04: GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08: GPIO.output(LCD_D7, True)
        
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

# Inicialización única del LCD antes de entrar al bucle
lcd_init()
ultimo_estado = None

try:
    while True:
        s1 = GPIO.input(TOGGLE_1)
        s2 = GPIO.input(TOGGLE_2)
        estado_actual = (s1, s2)

        if estado_actual != ultimo_estado:
            if s1 == s2:
                sonar_zumbador()
            ultimo_estado = estado_actual

        # --- CASO 1: Giro Izquierda (Motor DC) ---
        if s1 == 1 and s2 == 0:
            lcd_texto('Giro Izquierda', LINE_1)
            GPIO.output(SALIDA_1, 1)
            GPIO.output(SALIDA_2, 0)
            sleep(0.1)

        # --- CASO 2: Giro Derecha (Motor DC) ---
        elif s1 == 0 and s2 == 1:
            lcd_texto('Giro Derecha', LINE_1)
            GPIO.output(SALIDA_1, 0)
            GPIO.output(SALIDA_2, 1)
            sleep(0.1)

        # --- CASO 3: Servomotor ---
        elif s1 == 0 and s2 == 0:
            # Apagar Motor DC
            GPIO.output(SALIDA_1, 0)
            GPIO.output(SALIDA_2, 0)
            
            lcd_texto('Servo: 135 deg', LINE_1)
            pwm.ChangeDutyCycle(porcentaje(135))
            sleep(2.0)
            
            lcd_texto('Servo: 0 deg', LINE_1)
            pwm.ChangeDutyCycle(porcentaje(0))
            sleep(2.0)

        # --- CASO 4: Motor Paso a Paso ---
        elif s1 == 1 and s2 == 1:
            # Apagar Motor DC
            GPIO.output(SALIDA_1, 0)
            GPIO.output(SALIDA_2, 0)
            
            lcd_texto('Motor Paso a Paso', LINE_1)
            
            # Secuencia en un sentido (13 pasos)
            for paso in range(13):
                for i in range(4):
                    for pin in pins:
                        GPIO.output(pin, GPIO.LOW)
                    GPIO.output(pins[i], GPIO.HIGH)
                    sleep(0.01)
            sleep(1)  
            
            # Secuencia en sentido inverso (13 pasos)
            for paso in range(13):
                for i in range(4):
                    for pin1 in pins1:
                        GPIO.output(pin1, GPIO.LOW)
                    GPIO.output(pins1[i], GPIO.HIGH)
                    sleep(0.01)
            sleep(1)  

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
