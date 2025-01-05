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
player = player_front
player_x = tile_size * 1
player_y = tile_size * 1
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

    current_ticks = states.get_current_state_ticks()
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()
    keys_up = game.get_keys_up()
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()

    blocks_pos = calc_blocks_pos(map_mat)

    if state == WALKING:
        if keys_pressed[pygame.K_LEFT]:
            player = player_left
            player_x = player_x - speed
        elif keys_pressed[pygame.K_RIGHT]:
            player_x = player_x + speed
            player = player_right
        elif keys_pressed[pygame.K_UP]:
            player_y = player_y - speed
            player = player_back
        elif keys_pressed[pygame.K_DOWN]:
            player_y = player_y + speed
            player = player_front

        for block_x, block_y in blocks_pos:
            player_limit_left = player_x
            player_limit_right = player_x + tile_size
            player_limit_back = player_y
            player_limit_front = player_y + tile_size
            block_limit_left = block_x
            block_limit_right = block_x + tile_size
            block_limit_back = block_y
            block_limit_front = block_y + tile_size

            (overlap, overlap_x, overlap_y) = aabb_collision(player_limit_left,
                                                            player_limit_right,
                                                            player_limit_front,
                                                            player_limit_back,
                                                            block_limit_left,
                                                            block_limit_right,
                                                            block_limit_front,
                                                            block_limit_back)
            
            if overlap:
                if abs(overlap_x) < abs(overlap_y):
                    player_x = player_x + overlap_x
                else:
                    player_y = player_y + overlap_y

        for enemy_x, enemy_y in blocks_pos:
            player_limit_left = player_x
            player_limit_right = player_x + tile_size
            player_limit_back = player_y
            player_limit_front = player_y + tile_size
            block_limit_left = enemy_x - 40
            block_limit_right = enemy_y + tile_size + 40
            block_limit_back = enemy_y + 40
            block_limit_front = enemy_y + tile_size - 40

            (overlap, overlap_x, overlap_y) = aabb_collision(player_limit_left,
                                            player_limit_right,
                                            player_limit_front,
                                            player_limit_back,
                                            block_limit_left,
                                            block_limit_right,
                                            block_limit_front,
                                            block_limit_back)
            
            pygame.display.set_caption(str(overlap))
            if overlap and (keys_down[pygame.K_SPACE] or keys_down[pygame.K_RETURN]):
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


def aabb_collision(a_left, a_right, a_front, a_back, b_left, b_right, b_front, b_back):
    overlap_left = b_right - a_left
    overlap_right = a_right - b_left
    overlap_front = b_front - a_back
    overlap_back = a_front - b_back
    overlap = overlap_left >= 0 and overlap_right >= 0 and overlap_front >= 0 and overlap_back >= 0
    
    if overlap_right < overlap_left:
        overlap_x = - overlap_right
    else:
        overlap_x = overlap_left

    if overlap_back < overlap_front:
        overlap_y = - overlap_back
    else:
        overlap_y = overlap_front
    
    return (overlap, overlap_x, overlap_y)


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
            entidad_fila = math.floor(entidad_y / tile_size)
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
