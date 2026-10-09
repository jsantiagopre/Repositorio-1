import tkinter as tk
import RPi.GPIO as GPIO
import sys

# Configuración de los pines
led_pin_1 = 11
led_pin_2 = 13
 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin_1, GPIO.OUT)
GPIO.setup(led_pin_2, GPIO.OUT)


# Función para encender y apagar el LED
def toggle_led_1():
    current_state_1 = GPIO.input(led_pin_1)
    GPIO.output(led_pin_1, not current_state_1)  # Cambia el estado del LED

def toggle_led_2():
    current_state_2 = GPIO.input(led_pin_2)
    GPIO.output(led_pin_2, not current_state_2)  # Cambia el estado del LED
    sys.exit()  # Termina el programa


# Configuración de la ventana de Tkinter
root = tk.Tk()
root.title("Control de LED")

# Botón para encender/apagar el LED
led_button_1 = tk.Button(root, text="LED_1", command=toggle_led_1)
led_button_1.pack(pady=300)
led_button_1.place(x=50, y=50)

# Botón para encender/apagar el LED
led_button_2 = tk.Button(root, text="LED_2", command=toggle_led_2)
led_button_2.pack(pady=300)
led_button_2.place(x=100, y=150)


# Cierre adecuado de GPIO al salir
def on_closing():
    GPIO.cleanup()  # Limpia los pines GPIO
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar la aplicación
root.mainloop()

