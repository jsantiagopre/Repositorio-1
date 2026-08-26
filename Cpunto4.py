import matplotlib.pyplot as plt

print("VECTOR EN UN SISTEMA DE COORDENADAS 3D")

x = float(input("Ingrese X: "))
y = float(input("Ingrese Y: "))
z = float(input("Ingrese Z: "))

fig = plt.figure(figsize=(8, 7))
ax = fig.add_subplot(111, projection='3d')

# Dibujar vector
ax.quiver(0, 0, 0, x, y, z)

# Punto final
ax.scatter(x, y, z, s=60)

# Etiqueta
ax.text(x, y, z, f" ({x}, {y}, {z})")

# Ejes
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

ax.set_title("Vector en el espacio 3D")

# Límites
limite = max(abs(x), abs(y), abs(z)) + 1

ax.set_xlim([-limite, limite])
ax.set_ylim([-limite, limite])
ax.set_zlim([-limite, limite])

plt.show()