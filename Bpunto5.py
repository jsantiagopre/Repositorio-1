while True:
    res = input("¿Desea continuar Si/No? ")
    res = res.lower()
    if res == "si":
        print("El programa continua\n")
    elif res == "no":
        print("Programa finalizado")
        break
    else:
        print("Respuesta no valida. Escriba Si o No.\n")