import cv2
import numpy as np
import matplotlib.pyplot as plt


def obtener_contorno(ruta_imagen, nombre):

    img = cv2.imread(ruta_imagen)

    if img is None:
        print(f"No se pudo abrir la imagen: {ruta_imagen}")
        return None

    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gris = cv2.GaussianBlur(gris, (5, 5), 0)

    _, binaria = cv2.threshold(
        gris,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    contornos, jerarquia = cv2.findContours(
        binaria,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    if len(contornos) == 0:
        print(f"No se encontraron contornos en {nombre}")
        return None

    contorno = max(contornos, key=cv2.contourArea)

    coordenadas = contorno.reshape(-1, 2)

    print("\n" + nombre)
    print("Número de puntos:", len(coordenadas))
    print("Primeras coordenadas X,Y:")
    print(coordenadas[:20])

    archivo = nombre + "_coordenadas.csv"

    np.savetxt(
        archivo,
        coordenadas,
        delimiter=",",
        header="X,Y",
        comments="",
        fmt="%d"
    )

    print("Archivo guardado:", archivo)

    alto, ancho = gris.shape

    imagen_contorno = np.zeros(
        (alto, ancho),
        dtype=np.uint8
    )
    cv2.drawContours(
        imagen_contorno,
        [contorno],
        -1,
        255,
        2
    )

    plt.figure(figsize=(8, 6))
    plt.imshow(imagen_contorno, cmap="gray")
    plt.title("Contorno - " + nombre)
    plt.axis("off")
    plt.show()

    return coordenadas

chevrolet = obtener_contorno(
    "image.png",
    "Chevrolet"
)

renault = obtener_contorno(
    "image2.png",
    "Renault"
)