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
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_NONE
    )

    if len(contornos) == 0:
        print(f"No se encontraron contornos en {nombre}")
        return None

    contorno_exterior = max(contornos, key=cv2.contourArea)

    coordenadas_exterior = contorno_exterior.reshape(-1, 2)

    print("\n" + "=" * 40)
    print(nombre)
    print("=" * 40)

    print("\nCONTORNO EXTERIOR")
    print("Número de puntos:", len(coordenadas_exterior))
    print("Primeras coordenadas X,Y:")
    print(coordenadas_exterior[:20])

    archivo_exterior = nombre + "_exterior.csv"

    np.savetxt(
        archivo_exterior,
        coordenadas_exterior,
        delimiter=",",
        header="X,Y",
        comments="",
        fmt="%d"
    )

    print("Archivo guardado:", archivo_exterior)

    contornos_internos = []

    for i, contorno in enumerate(contornos):

        # Si tiene padre, es un contorno interno
        padre = jerarquia[0][i][3]

        if padre != -1:
            contornos_internos.append(contorno)

    print("\nCONTORNOS INTERNOS")
    print("Cantidad:", len(contornos_internos))

    coordenadas_internas = []

    for i, contorno in enumerate(contornos_internos):

        coordenadas = contorno.reshape(-1, 2)

        coordenadas_internas.append(coordenadas)

        print(f"\nContorno interno {i + 1}")
        print("Número de puntos:", len(coordenadas))
        print("Primeras coordenadas X,Y:")
        print(coordenadas[:20])

        archivo_interno = (
            nombre + f"_interior_{i + 1}.csv"
        )

        np.savetxt(
            archivo_interno,
            coordenadas,
            delimiter=",",
            header="X,Y",
            comments="",
            fmt="%d"
        )

        print("Archivo guardado:", archivo_interno)

    alto, ancho = gris.shape

    imagen_contorno = np.zeros(
        (alto, ancho),
        dtype=np.uint8
    )
    cv2.drawContours(
        imagen_contorno,
        [contorno_exterior],
        -1,
        255,
        2
    )

    cv2.drawContours(
        imagen_contorno,
        contornos_internos,
        -1,
        255,
        2
    )

    plt.figure(figsize=(8, 6))
    plt.imshow(imagen_contorno, cmap="gray")
    plt.title("Contornos - " + nombre)
    plt.axis("off")
    plt.show()

    return coordenadas_exterior, coordenadas_internas

chevrolet = obtener_contorno(
    "image.png",
    "Chevrolet"
)
renault = obtener_contorno(
    "image2.png",
    "Renault"
)