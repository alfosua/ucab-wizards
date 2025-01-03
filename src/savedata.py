import os

# inicializar sistema de guardas
def init():
    # crear directorio si no existe
    if not os.path.exists("saves"):
        os.mkdir("saves")

    # crear archivo indice si no existe
    if not os.path.exists("saves/index.txt"):
        with open("saves/index.txt", "w") as f:
            f.write("")

# inicializar guarda
def init_save(nombre: str, skin: str, fecha: str, archivo: str):
    with open("saves/index.txt", "a") as f:
        f.write(nombre + "," + skin + "," + fecha + "," + archivo + "\n")
    with open("saves/" + archivo, "w") as f:
        f.write("")

# dar todos los guardas
def get_saves():
    # se el especifica utf8 porque si no, no funciona
    with open("saves/index.txt", 'r', encoding='utf-8') as f:
        lista = []
        for linea in f:
            guarda = linea.split(",")
            lista.append(guarda)
        return lista

# dar con un guarda en especifico segun el indice
def get_save(indice: int):
    # se el especifica utf8 porque si no, no funciona
    with open("saves/index.txt", 'r', encoding='utf-8') as f:
        for i in range(indice):
            next(f)
        linea = next(f)
        guarda = linea.split(",")
        return guarda

def load_game() -> dict:
    # TODO: cargar estado de partida desde juego desde un archivo
    return {}

def save_game(data: dict):
    # TODO: guardar estado de partida en juego en un archivo
    pass
