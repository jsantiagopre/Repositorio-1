import math

print("Seleccione el solido al cual desea saber el volumen")
print("1. Prisma\n2. Piramida\n3 Cono truncado\n4.Cilindro\n")
Solido=int(input("Seleccione el solido:\n"))

if Solido == 1:
    print("PRISMA")
    area_base = float(input("Ingrese el area de la base: "))
    altura = float(input("Ingrese la altura: "))
    volumen = area_base * altura
    print(f"El volumen del prisma es: {volumen}")
elif Solido == 2:
    print("PIRAMIDE")
    area_base = float(input("Ingrese el area de la base: "))
    altura = float(input("Ingrese la altura: "))
    volumen = (area_base * altura) / 3
    print(f"El volumen de la piramide es: {volumen}")
elif Solido == 3:
    print("CONO TRUNCADO")
    radio_mayor = float(input("Ingrese el radio mayor: "))
    radio_menor = float(input("Ingrese el radio menor: "))
    altura = float(input("Ingrese la altura: "))
    volumen = (math.pi * altura / 3) * (radio_mayor**2+radio_mayor*radio_menor+radio_menor**2)
    print(f"El volumen del cono truncado es: {volumen}")
elif Solido == 4:
    print("CILINDRO")
    radio = float(input("Ingrese el radio: "))
    altura = float(input("Ingrese la altura: "))
    volumen = math.pi * radio**2 * altura
    print(f"El volumen del cilindro es: {volumen}")
else :
    print("Opcion invalida")