import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

print("FUNCIÓN DE TRANSFERENCIA DE SEGUNDO ORDEN")

K = float(input("Ingrese K: "))
wn = float(input("Ingrese wn: "))
zita = float(input("Ingrese zita: "))

a1 = 2 * zita * wn
a0 = wn**2
numerador = [K* wn**2]
denominador = [1, a1, a0]

sistema = signal.TransferFunction(numerador, denominador)

# Polos
polos = np.roots(denominador)

print("\nPolos del sistema:")
print(polos)

# Determinar tipo de sistema
discriminante = a1**2 - 4*a0

if discriminante < 0:
    tipo = "SUBAMORTIGUADO"
elif discriminante == 0:
    tipo = "CRÍTICAMENTE AMORTIGUADO"
else:
    tipo = "SOBREAMORTIGUADO"

print("\nTipo de sistema:", tipo)

# Respuesta al escalón
tiempo, respuesta = signal.step(sistema)

plt.figure(figsize=(9, 5))
plt.plot(tiempo, respuesta)

plt.title("Respuesta al escalón - " + tipo)
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid(True)

plt.show()