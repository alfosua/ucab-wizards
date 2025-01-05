# Algoritmo de generación de mapa
import random

ancho = 21
alto = 21

def generate_map() -> str:
    # Crear un laberinto vacío
    mapa = [["X" for _ in range(ancho)] for _ in range(alto)]

    # Definir las posiciones de inicio y salida
    inicio = (1, 1)
    salida = (alto - 2, ancho - 2)

    # Crear una pila para el algoritmo DFS
    stack = [inicio]
    mapa[inicio[0]][inicio[1]] = " "

    # Definir las direcciones de movimiento
    direcciones = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        x, y = stack[-1]
        random.shuffle(direcciones)
        moved = False

        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 < nx < alto - 1 and 0 < ny < ancho - 1 and mapa[nx][ny] == "X":
                tipo = random.randint(0, 9)
                if tipo == 9:
                    mapa[nx][ny] = "E"
                else:
                    mapa[nx][ny] = " "
                mapa[x + dx // 2][y + dy // 2] = " "
                stack.append((nx, ny))
                moved = True
                break

        if not moved:
            stack.pop()

    # Asegurar que haya un inicio y una salida sin obstrucciones
    mapa[inicio[0]][inicio[1]] = "I"
    mapa[salida[0]][salida[1]] = "S"
    return mapa
