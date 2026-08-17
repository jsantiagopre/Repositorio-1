import random
print("Generador numeros aleatorios")
cantidad = int(input("¿Cuantos numeros desea generar?: "))
minimo = int(input("Ingrese el valor minimo del rango: "))
maximo = int(input("Ingrese el valor maximo del rango: "))
numeros=[]
for i in range(cantidad):
    numero=random.randint(minimo,maximo)
    numeros.append(numero)

print("Los numero generados en los rangos dados son:\n")
print(numeros)