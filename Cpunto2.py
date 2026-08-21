import numpy as np
import matplotlib.pyplot as plt

K = float(input("Ingrese K: "))
wn = float(input("Ingrese wn: "))
zita = float(input("Ingrese zita: "))

numerador = K * wn**2

a1 = 2 * zita * wn
a0 = wn**2

if zita > 0 and zita < 1:

    tipo = "SUBAMORTIGUADO"

elif zita == 1:

    tipo = "CRITICAMENTE AMORTIGUADO"

elif zita > 1:

    tipo = "SOBREAMORTIGUADO"

else:

    tipo = "INESTABLE"

print("\nFactor de amortiguamiento:", zita)
print("Tipo de sistema:", tipo)

t = np.linspace(0, 10 / wn, 1000)

if zita > 0 and zita < 1:

    wd = wn * np.sqrt(1 - zita**2)

    y = K * (
        1
        - np.exp(-zita * wn * t)
        * (
            np.cos(wd * t)
            + (zita / np.sqrt(1 - zita**2))
            * np.sin(wd * t)
        )
    )

elif zita == 1:

    y = K * (
        1 - np.exp(-wn * t) * (1 + wn * t)
    )

elif zita > 1:

    p1 = -wn * (zita - np.sqrt(zita**2 - 1))
    p2 = -wn * (zita + np.sqrt(zita**2 - 1))

    y = K * (
        1
        + (p2 * np.exp(p1 * t) - p1 * np.exp(p2 * t))
        / (p1 - p2)
    )

else:

    y = np.zeros(len(t))

plt.plot(t, y)

plt.axhline(K, linestyle="--", label="Valor final")

plt.title("Respuesta al escalón")
plt.xlabel("Tiempo [s]")
plt.ylabel("Salida")

plt.grid()
plt.legend()

plt.show()