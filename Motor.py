import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

pins = [35, 38, 37, 40]    # CREACIÓN DE LA LISTA PARA LA SECUENCIA DEL MOTOR PASA-PASO lista pins
pins1 = [40, 37, 38, 35]   # CREACIÓN DE LA LISTA PARA LA SECUENCIA DEL MOTOR PASA-PASO lista pins1

# BUZZER
buzzer12 = 12

# SERVOMOTOR
pwmgpio33 = 33  # Use el GPIO13 en PWM1 para la señal de PWM
frecuencia = 50 # Esta frecuencia la da el fabricante del servomotor SG90 (T=20ms)

GPIO.setup(33, GPIO.OUT)  # Configuro el GPIO33 como salida
pwm = GPIO.PWM(pwmgpio33, frecuencia)

GPIO.setup(buzzer12, GPIO.OUT) # Buzzer como salida

def porcentaje(angulo): # Función que calcula el duty cycle desde el ángulo (0 a 180)
    if angulo > 180 or angulo < 0:
        return False
    comienzo = 4
    final = 12.5
    radio = (final - comienzo) / 180
    angulocomoporcentaje = angulo * radio
    return comienzo + angulocomoporcentaje

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

GPIO.setup(35, GPIO.OUT)  # BOBINA A DEL MOTOR_PASO_PASO
GPIO.setup(38, GPIO.OUT)  # BOBINA B DEL MOTOR_PASO_PASO
GPIO.setup(37, GPIO.OUT)  # BOBINA C DEL MOTOR_PASO_PASO
GPIO.setup(40, GPIO.OUT)  # BOBINA D DEL MOTOR_PASO_PASO

for salidas in bits_datos:
    GPIO.setup(salidas, GPIO.OUT)
    
def lcd_init():
    lcd_write(0x33, LCD_CMD)
    lcd_write(0x32, LCD_CMD)
    lcd_write(0x06, LCD_CMD)
    lcd_write(0x0C, LCD_CMD)
    lcd_write(0x28, LCD_CMD)
    lcd_write(0x01, LCD_CMD)
    sleep(0.0005)
    
def lcd_write(bits, mode):
    GPIO.output(LCD_RS, mode)
    
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)
     
    lcd_toggle_enable()
    
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)
        
    lcd_toggle_enable()
    
def lcd_toggle_enable():
    sleep(0.0005)
    GPIO.output(LCD_E, True)
    sleep(0.0005)
    GPIO.output(LCD_E, False)
    sleep(0.0005)
    
def lcd_texto(message, line):
    message = message.ljust(LCD_CHARS, " ")
    lcd_write(line, LCD_CMD)
    for i in range(LCD_CHARS):
        lcd_write(ord(message[i]), LCD_CHR)
        
def LCD(hora):
    lcd_init()
    lcd_texto(hora, LINE_1)
    sleep(0.01)

def sonar_zumbador():
    """Hace sonar el buzzer durante 1 segundo."""
    GPIO.output(buzzer12, True)
    sleep(1.0)
    GPIO.output(buzzer12, False)

# Variables para rastrear el último estado de los CNY70
ultimo_estado = None

try:
    while True:
        s1 = GPIO.input(TOGGLE_1)
        s2 = GPIO.input(TOGGLE_2)
        estado_actual = (s1, s2)

        # Si hubo un cambio en el estado de los CNY70
        if estado_actual != ultimo_estado:
            # Si ambos sensores son iguales (0,0) o (1,1)
            if s1 == s2:
                sonar_zumbador()
            ultimo_estado = estado_actual

        # --- CASO 1: Giro Izquierda ---
        if s1 == 1 and s2 == 0:
            LCD('Giro Izquierda')
            GPIO.output(SALIDA_1, 1)
            GPIO.output(SALIDA_2, 0)
            
        # --- CASO 2: Giro Derecha ---
        elif s1 == 0 and s2 == 1:
            LCD('Giro Derecha')
            GPIO.output(SALIDA_1, 0)
            GPIO.output(SALIDA_2, 1)

        # --- CASO 3: Servomotor 135° y -135° ---
        elif s1 == 0 and s2 == 0:
            LCD('Servo: 135 deg')
            pwm.start(porcentaje(0))       # Posición inicial 0°
            sleep(0.5)
            
            # Giro a 135°
            pwm.ChangeDutyCycle(porcentaje(135))
            sleep(2.0)                     # Espera 2 segundos
            
            # Giro a -135° (retorno a 0°)
            LCD('Servo: -135 deg')
            pwm.ChangeDutyCycle(porcentaje(0))
            sleep(2.0)
            
            pwm.stop()

        # --- CASO 4: Motor Paso a Paso ---
        elif s1 == 1 and s2 == 1:
            j = 1
            while j <= 13:
                for i in range(4):
                    LCD(f"Motor_Step: {j}")
                    for pin in pins:
                        GPIO.output(pin, GPIO.LOW)
                    GPIO.output(pins[i], GPIO.HIGH)
                    sleep(0.3)
                    j += 1
            sleep(1)  
            
            k = 1
            while k <= 13: 
                for i in range(4):
                    LCD(f"Motor_Step: {k}")
                    for pin1 in pins1:
                        GPIO.output(pin1, GPIO.LOW)
                    GPIO.output(pins1[i], GPIO.HIGH)
                    sleep(0.3)
                    k += 1
            sleep(1)  

except KeyboardInterrupt:
    GPIO.cleanup()
