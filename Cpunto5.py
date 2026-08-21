import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 8))

def dibujar_letra(letra, x, y):

    if letra == "D":
        plt.plot(
            [x, x, x + 0.6, x + 0.9, x + 0.6, x],
            [y, y + 2, y + 2, y + 1, y, y]
        )
    elif letra == "A":
        plt.plot(
            [x, x + 0.5, x + 1],
            [y, y + 2, y]
        )

        # Barra central
        plt.plot(
            [x + 0.2, x + 0.8],
            [y + 0.8, y + 0.8]
        )
    elif letra == "N":
        plt.plot(
            [x, x, x + 1, x + 1],
            [y, y + 2, y, y + 2]
        )
    elif letra == "I":
        plt.plot(
            [x, x + 1],
            [y + 2, y + 2]
        )

        plt.plot(
            [x + 0.5, x + 0.5],
            [y + 2, y]
        )

        plt.plot(
            [x, x + 1],
            [y, y]
        )

    elif letra == "L":
        plt.plot(
            [x, x],
            [y + 2, y]
        )

        plt.plot(
            [x, x + 1],
            [y, y]
        )

    elif letra == "O":

        theta = np.linspace(0, 2 * np.pi, 100)

        x_o = x + 0.5 + 0.5 * np.cos(theta)
        y_o = y + 1 + 1 * np.sin(theta)

        plt.plot(x_o, y_o)

    elif letra == "E":

        # Línea vertical
        plt.plot(
            [x, x],
            [y, y + 2]
        )

        # Línea superior
        plt.plot(
            [x, x + 1],
            [y + 2, y + 2]
        )

        # Línea central
        plt.plot(
            [x, x + 0.8],
            [y + 1, y + 1]
        )

        # Línea inferior
        plt.plot(
            [x, x + 1],
            [y, y]
        )

    elif letra == "J":

        # Línea superior
        plt.plot(
            [x, x + 1],
            [y + 2, y + 2]
        )

        # Línea vertical
        plt.plot(
            [x + 0.5, x + 0.5],
            [y + 2, y + 0.4]
        )

        # Parte curva
        theta = np.linspace(np.pi, 2 * np.pi, 50)

        x_j = x + 0.2 + 0.3 * np.cos(theta)
        y_j = y + 0.4 + 0.4 * np.sin(theta)

        plt.plot(x_j, y_j)

    elif letra == "R":

        # Línea vertical
        plt.plot(
            [x, x],
            [y, y + 2]
        )

        # Parte superior
        plt.plot(
            [x, x + 0.6, x + 0.8, x + 0.6, x],
            [y + 2, y + 2, y + 1.5, y + 1, y + 1]
        )

        # Diagonal
        plt.plot(
            [x + 0.5, x + 1],
            [y + 1, y]
        )

    elif letra == "M":

        plt.plot(
            [x, x, x + 0.5, x + 1, x + 1],
            [y, y + 2, y + 1, y + 2, y]
        )

def dibujar_nombre(nombre, x_inicial, y_inicial):

    espacio = 1.4

    for i, letra in enumerate(nombre):

        x = x_inicial + i * espacio

        dibujar_letra(letra, x, y_inicial)

dibujar_nombre("DANILO", 0, 5.5)

dibujar_nombre("DANIELA", 0, 2)

dibujar_nombre("JORMAN", 0, -1.5)

plt.title("Nombres de los integrantes")

plt.xlabel("Eje X")
plt.ylabel("Eje Y")

plt.axis("equal")

plt.grid(True)

plt.xlim(-1, 11)
plt.ylim(-2.5, 8)

plt.show()