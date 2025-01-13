import os

import exploration

current_save = 0

# inicializar sistema de guardas
def init():
    # crear directorio si no existe
    if not os.path.exists("saves"):
        os.mkdir("saves")

    # crear archivo indice si no existe
    if not os.path.exists("saves/index.txt"):
        with open("saves/index.txt", "w", encoding='utf-8') as f:
            f.write("")

# inicializar guarda
def init_save(nombre: str, skin: str, fecha: str):
    idx = len(get_saves()) + 1
    archivo = str(idx) + "_" + nombre + ".txt"
    with open("saves/index.txt", "a", encoding='utf-8') as f:
        f.write(nombre + "," + skin + "," + fecha + "," + archivo + "\n")

    with open("saves/" + archivo, "w") as f:
        f.write(str(exploration.tile_size * 1) + "\n")
        f.write(str(exploration.tile_size * 1) + "\n")
        f.write(str(0) + "\n")
        f.write(str(0) + "\n")

        # TODO: inicializar la info de batalla

        for fila in exploration.map_mat:
            for columna in fila:
                f.write(columna)
                f.write(",")
            f.write("\n")
    
    load_skin(skin)
    set_current_save(idx-1)

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
        guarda = linea.replace("\n", "").split(",")
        return guarda
    
def set_current_save(indice: int):
    global current_save
    current_save = indice

# carga estado de partida en juego desde el archivo del guarda actual
def load_game():
    # obtener información básica
    save = get_save(current_save)
    (player_name, skin, date, archivo) = save

    # leer archivo de datos
    data = None
    with open("saves/" + archivo, "r") as f:
        data = f.read().splitlines(keepends=False)

    # establecer estado de juegos

    # información de skin
    load_skin(skin)

    # información del estado de juego (según )
    exploration.player_x = int(data[0])
    exploration.player_y = int(data[1])
    exploration.camera_x = int(data[2])
    exploration.camera_y = int(data[3])

    # TODO: cargar la info de batalla

    exploration.map_mat = []
    for fila in data[4:]:
        columnas = fila.split(",")
        fila_mat = []
        for columna in columnas:
            fila_mat.append(columna)
        exploration.map_mat.append(fila_mat)

# carga la skin según la seleccionada
def load_skin(skin: str):
    import images

    if skin == "0":
        selected_skin = images.skins_white_all
    elif skin == "1":
        selected_skin = images.skins_red_all
    elif skin == "2":
        selected_skin = images.skins_gold_all

    exploration.player = selected_skin[0]
    exploration.player_front = selected_skin[0]
    exploration.player_back = selected_skin[1]
    exploration.player_left = selected_skin[2]
    exploration.player_right = selected_skin[3]
    exploration.player_front_walk = selected_skin[4]
    exploration.player_back_walk = selected_skin[5]
    exploration.player_left_walk = selected_skin[6]
    exploration.player_right_walk = selected_skin[7]

# guarda estado de partida en juego el archivo del guarda actual
def save_game():
    # obtener información básica
    save = get_save(current_save)
    (player_name, skin, date, archivo) = save

    with open("saves/" + archivo, "w") as f:
        f.write(str(exploration.player_x) + "\n")
        f.write(str(exploration.player_y) + "\n")
        f.write(str(exploration.camera_x) + "\n")
        f.write(str(exploration.camera_y) + "\n")

        # TODO: guardar la info de batalla

        for fila in exploration.map_mat:
            f.write(fila.join(","))
            f.write("\n")
