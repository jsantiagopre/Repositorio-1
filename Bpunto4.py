print("Escoger entre robot Cilíndrico, Cartesiano y esférico:")
print("1. Robot Cilindrico\n2. Robot Cartesiano\n3. Robot Esferico")

Robot = int(input("Seleccione el tipo de robot: "))

if Robot == 1:
    print("\nRobot seleccionado: Cilindrico")
    print("Numero de articulaciones: 3")
    print("2 articulaciones prismaticas y 1 rotacional.")
elif Robot == 2:
    print("\nRobot seleccionado: Cartesiano")
    print("Numero de articulaciones: 3")
    print("3 articulaciones prismaticas.")
elif Robot == 3:
    print("\nRobot seleccionado: Esferico")
    print("Numero de articulaciones: 3")
    print("2 articulaciones rotacionales y 1 prismatica.")
else:
    print("Opcion invalida.")
    