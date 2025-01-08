import math
import pygame
import game
import interface
import states
import fonts
import texts
import images
import sounds
import strings
import music
import map
import wip # eliminar esta línea al empezar a trabajar en esta pantalla


tile_size = 80

wall = pygame.image.load("assets/images/map/wall.png")
wall = pygame.transform.scale(wall, (tile_size, tile_size * wall.get_height() / wall.get_width()))
floor = pygame.image.load("assets/images/map/floor.png")
floor = pygame.transform.scale(floor, (tile_size, tile_size))
door_h = pygame.image.load("assets/images/map/door_h.png")
door_h = pygame.transform.scale(door_h, (tile_size, tile_size * door_h.get_height() / door_h.get_width()))
door_v = pygame.image.load("assets/images/map/door_v.png")
door_v = pygame.transform.scale(door_v, (tile_size, tile_size * door_v.get_height() / door_v.get_width()))
blademaster = pygame.image.load("assets/images/enemies/blademaster.png")
blademaster = pygame.transform.scale(blademaster, (tile_size, tile_size * blademaster.get_height() / blademaster.get_width()))

map_mat = map.generate_map()

player_left = pygame.image.load("assets/images/skins/samuel/left.png")
player_right = pygame.image.load("assets/images/skins/samuel/right.png")
player_back = pygame.image.load("assets/images/skins/samuel/back.png")
player_front = pygame.image.load("assets/images/skins/samuel/front.png")
player_front_walk = [ 
    pygame.image.load("assets/images/skins/samuel/walk/front_01.png"),     
    pygame.image.load("assets/images/skins/samuel/walk/front_02.png")     
]
player_back_walk =  [ 
    pygame.image.load("assets/images/skins/samuel/walk/back_01.png"),     
    pygame.image.load("assets/images/skins/samuel/walk/back_02.png")     
]
player_left_walk =  [ 
    pygame.image.load("assets/images/skins/samuel/walk/left_01.png"),     
    pygame.image.load("assets/images/skins/samuel/walk/left_02.png")     
]
player_right_walk =  [ 
    pygame.image.load("assets/images/skins/samuel/walk/right_01.png"),     
    pygame.image.load("assets/images/skins/samuel/walk/right_02.png")     
]
player = player_front
player_x = tile_size * 1
player_y = tile_size * 1
player_direction = "front"
player_walking = False
camera_x = 0
camera_y = 0
speed = 5

WALKING = 0
TALKING = 1
INTO_FIGHT = 2
state = WALKING
into_fight_started = 0

# Debugging
IGNORE_ENEMY_BLOCK = True

def run():
    # obtener información general del juego para uso posterior
    global player_x
    global player_y
    global player
    global camera_x
    global camera_y
    global state
    global into_fight_started
    global player_walking
    global player_direction

    current_ticks = states.get_current_state_ticks()
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()
    keys_up = game.get_keys_up()
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    
    if states.is_entering_state():
        music.play_unforgiven()

    blocks_pos = calc_blocks_pos(map_mat)
    enemies_pos = calc_enemies_pos(map_mat)

    player_walking = False

    if state == WALKING:
        if keys_pressed[pygame.K_LEFT]:
            player_direction = "left"
            player_walking = True
            player_x = player_x - speed
        elif keys_pressed[pygame.K_RIGHT]:
            player_x = player_x + speed
            player_direction = "right"
            player_walking = True
        elif keys_pressed[pygame.K_UP]:
            player_y = player_y - speed
            player_direction = "back"
            player_walking = True
        elif keys_pressed[pygame.K_DOWN]:
            player_y = player_y + speed
            player_direction = "front"
            player_walking = True
                
        if player_walking:
            if player_direction == "front":
                walk = player_front_walk
            elif player_direction == "back":
                walk = player_back_walk
            elif player_direction == "left":
                walk = player_left_walk
            elif player_direction == "right":
                walk = player_right_walk
            player = walk[current_ticks // 400 % 2]
        else:
            if player_direction == "front":
                player = player_front
            elif player_direction == "back":
                player = player_back
            elif player_direction == "left":
                player = player_left
            elif player_direction == "right":
                player = player_right

            
        player_bounds = calc_bounds(player_x, player_y, tile_size/2, tile_size/2)

        for block_x, block_y in blocks_pos:
            block_bounds = calc_bounds(block_x, block_y, tile_size, tile_size)
            (traspaso, traspaso_x, traspaso_y) = aabb_collision(player_bounds, block_bounds)
            
            if traspaso:
                if abs(traspaso_x) < abs(traspaso_y):
                    player_x = player_x + traspaso_x
                else:
                    player_y = player_y + traspaso_y

        for enemy_x, enemy_y in enemies_pos:
            enemy_bounds = calc_bounds(enemy_x, enemy_y, tile_size + 40, tile_size + 40)          
            (traspaso, traspaso_x, traspaso_y) = aabb_collision(player_bounds, enemy_bounds)
            
            if traspaso and (keys_down[pygame.K_SPACE] or keys_down[pygame.K_RETURN]):
                state = TALKING
                
    elif state == TALKING:        
        if keys_down[pygame.K_SPACE] or keys_down[pygame.K_RETURN]:
            state = INTO_FIGHT
            into_fight_started = current_ticks
        if keys_down[pygame.K_ESCAPE]:
            state = WALKING
    
    camera_x = max(-tile_size, player_x - screen_rect.width / 2)
    camera_y = max(-tile_size, player_y - screen_rect.height / 2)
    
    player = pygame.transform.scale(player, (tile_size, tile_size))

    entities = [
        (player, (player_x, player_y))
    ]
    
    draw_map(map_mat, entities)

    if state == TALKING:
        enemy_dialogue = fonts.menu.render("TU PUTA MADRE", True, "white")
        screen.blit(enemy_dialogue, (0, 0))

    if state == INTO_FIGHT:
        if into_fight_started:
            interface.draw_fade_in(interface.fill_black, ticks=current_ticks - into_fight_started, duration=1000)
        if current_ticks - into_fight_started > 1000:
            states.change_state(states.BATTLE)

    if states.is_exiting_state():
        music.stop()

def calc_bounds(x, y, ancho, alto): 
    left = x + tile_size/2 - ancho/2
    right = x + tile_size/2 + ancho/2
    front = y + tile_size/2 + alto/2
    back = y + tile_size/2 - alto/2
    return(left, right, front, back)

# Detección de colisión usando el algoritmo de caja delimitadora alineada por eje
# (por su siglas en ingles, Aligned Axis Bounding Box)
def aabb_collision(a_bounds, b_bounds):
    (a_left, a_right, a_front, a_back) = a_bounds
    (b_left, b_right, b_front, b_back) = b_bounds
    traspaso_left = b_right - a_left
    traspaso_right = a_right - b_left
    traspaso_front = b_front - a_back
    traspaso_back = a_front - b_back
    traspaso = traspaso_left >= 0 and traspaso_right >= 0 and traspaso_front >= 0 and traspaso_back >= 0
    
    if traspaso_right < traspaso_left:
        traspaso_x = - traspaso_right
    else:
        traspaso_x = traspaso_left

    if traspaso_back < traspaso_front:
        traspaso_y = - traspaso_back
    else:
        traspaso_y = traspaso_front
    
    return (traspaso, traspaso_x, traspaso_y)


def calc_blocks_pos(matriz: list[list[str]]) -> list[tuple[int, int]]:
    pos_vec = []

    for i, rows in enumerate(matriz):
        for j, columna in enumerate(rows):
            if columna == "X" or (columna == "E" and not IGNORE_ENEMY_BLOCK):
                pos_vec.append((j * tile_size, i * tile_size))

    return pos_vec


def calc_enemies_pos(matriz: list[list[str]]) -> list[tuple[int, int]]:
    pos_vec = []

    for i, rows in enumerate(matriz):
        for j, columna in enumerate(rows):
            if columna == "E":
                pos_vec.append((j * tile_size, i * tile_size))

    return pos_vec


def draw_map(mat: str, entidades):
    lienzo = game.get_screen()

    # dibujar pisos
    for i, fila in enumerate(mat):
        for j, columna in enumerate(fila):
            if columna != "#":
                lienzo.blit(floor, posicion_por_camara(j * tile_size, i * tile_size))

    # dibujar paredes
    for i, fila in enumerate(mat):
        for entidad in entidades:
            (entidad_imagen, (entidad_x, entidad_y)) = entidad
            entidad_fila = math.floor((entidad_y + tile_size / 2) / tile_size) 
            if entidad_fila == i:
                lienzo.blit(entidad_imagen, posicion_por_camara(entidad_x, entidad_y))

        for j, columna in enumerate(fila):
            posicion_x = j * tile_size
            posicion_y = i * tile_size - tile_size / 4
            if columna == "X":
                lienzo.blit(wall, posicion_por_camara(posicion_x, posicion_y))
            if columna == "D":
                lienzo.blit(door_v, posicion_por_camara(posicion_x, posicion_y))
            if columna == "U":
                lienzo.blit(door_h, posicion_por_camara(posicion_x, posicion_y))
            if columna == "E":
                lienzo.blit(blademaster, posicion_por_camara(posicion_x, posicion_y))

def posicion_por_camara(posicion_x, posicion_y):
    return (posicion_x - camera_x, posicion_y - camera_y)
