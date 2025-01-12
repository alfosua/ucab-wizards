import math
import pygame
import battle
import game
import interface
import states
import fonts
import texts
import images
import random
import sounds
import strings
import music
import map
import wip # eliminar esta línea al empezar a trabajar en esta pantalla

#Dialog Box
TalkingBG = pygame.image.load("assets/images/battleresources/MagicMenu.png")
TalkingBG = pygame.transform.scale(TalkingBG, (700,200))

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
kill_count = 0

WALKING = 0
TALKING = 1
INTO_FIGHT = 2
INTO_ENDGAME = 3
state = WALKING
state_started = 0
state_is_starting = False
endgame = False
endgame_start_distance_to_portal = 0
player_distance_to_portal = 0
endgame_started = 0
endgame_is_starting = False
endgame_evil_laugh_has_played = False
endgame_snd_evil_laugh_has_played = False
endgame_evil_laughes_fade_out = False
Dialogue_IDX = 0

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
    global state_started
    global player_walking
    global player_direction
    global state_is_starting
    global Dialogue_IDX
    global kill_count
    global endgame
    global endgame_is_starting
    global endgame_started
    global endgame_start_distance_to_portal
    global player_distance_to_portal
    global endgame_evil_laugh_has_played
    global endgame_snd_evil_laugh_has_played
    global endgame_evil_laughes_fade_out

    current_ticks = states.get_current_state_ticks()
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()
    keys_up = game.get_keys_up()
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    
    # empezar a reproducir la música del modo exploración al principio de este estado
    if states.is_entering_state():
        music.play_unforgiven()

    # realizar calculos para saber cuales son las posiciones de las paredes
    blocks_pos = calc_blocks_pos(map_mat)

    # realizar calculos para saber cuales son las posiciones de los enemigos
    enemies_pos = calc_enemies_pos(map_mat)

    # definir bandera por cada frame que advierte si el jugador está caminando actualmente
    player_walking = False

    # si el jugador se encuentra en estado libre para caminar
    if state == WALKING:
        # dependiendo de cual tecla direccional el jugador toca,
        # el personaje efectuara un desplazamiento hacia dicha dirección  
        if keys_pressed[pygame.K_LEFT]:
            player_x = player_x - speed
            player_direction = "left"
            player_walking = True
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
                
        # si el personaje esta caminando,
        if player_walking:
            # definir la animación de caminar según su dirección
            if player_direction == "front":
                walk = player_front_walk
            elif player_direction == "back":
                walk = player_back_walk
            elif player_direction == "left":
                walk = player_left_walk
            elif player_direction == "right":
                walk = player_right_walk
            # y establecerla como imagen del personaje jugador
            # realizando una animación de 2 frames por cada 2 quintos de segundo
            player = walk[current_ticks // 400 % 2]
        else:
            # sino, establecer dibujo del personaje parado según su dirección
            if player_direction == "front":
                player = player_front
            elif player_direction == "back":
                player = player_back
            elif player_direction == "left":
                player = player_left
            elif player_direction == "right":
                player = player_right

        # calcular limites del hit box del jugador
        player_bounds = calc_bounds(player_x, player_y, tile_size/2, tile_size/2)

        # por cada posición de pared que exista
        for block_x, block_y in blocks_pos:
            # calcular limites del hit box de la pared
            block_bounds = calc_bounds(block_x, block_y, tile_size, tile_size)
            # calcular si el jugador está chocando contra la pared
            (traspaso, traspaso_x, traspaso_y) = aabb_collision(player_bounds, block_bounds)
            # en caso que haya un traspaso, pues evitar que el personaje repase la pared
            if traspaso:
                if abs(traspaso_x) < abs(traspaso_y):
                    player_x = player_x + traspaso_x
                else:
                    player_y = player_y + traspaso_y

        # si no estamos en el endgame
        if not endgame:
            # verificar si podemos interactuar con los enemigos
            # por cada posición de enemigo que exista
            for enemy_x, enemy_y in enemies_pos:
                # calcular limites del hit box (mas grande de lo normal) del enemigo
                enemy_bounds = calc_bounds(enemy_x, enemy_y, tile_size + 40, tile_size + 40)
                # calcular si el jugador esta tocando al rango del enemigo
                (traspaso, traspaso_x, traspaso_y) = aabb_collision(player_bounds, enemy_bounds)
                # en caso que haya un traspaso y se toque la tecla para interactuar
                # entonces pasar al modo de conversar 
                if traspaso and (keys_down[pygame.K_SPACE] or keys_down[pygame.K_RETURN]):
                    state = TALKING
        
        if endgame:
            # calcular posición del portal
            (portal_x, portal_y) = calc_portal_pos(map_mat)

            # administración de sonidos ambientales en el endgame
            if endgame_is_starting:
                # Detener música de fondo
                music.fadeout(2500)
                # empezar a reproducir todos los sonidos ambientales
                # cuando recien empiece el endgame
                sounds.play(sounds.endgame_ambience, loops=-1)
                sounds.play(sounds.endgame_heart_beat, loops=-1)
                sounds.play(sounds.endgame_people_screaming, loops=-1)
                sounds.play(sounds.endgame_people_screaming_hell, loops=-1)
                sounds.play(sounds.endgame_tense, loops=-1)
                # calcular distancia del punto de inicio de endgame (según la posición actual del jugador) contra el portal
                endgame_start_distance_to_portal = math.sqrt((portal_x - player_x)**2 + (portal_y - player_y)**2)
                # no repetir estas acciones
                endgame_is_starting = False

            # calcular distancia del jugador contra el portal
            player_distance_to_portal = math.sqrt((portal_x - player_x)**2 + (portal_y - player_y)**2)

            # calcular volumen de sonidos ambientales según la distancia con el jugador
            volume_offset = player_distance_to_portal / endgame_start_distance_to_portal * 3 / 2 if player_distance_to_portal < endgame_start_distance_to_portal * 2 / 3 else 1
            volume_offset_hell = player_distance_to_portal / endgame_start_distance_to_portal * 3 if player_distance_to_portal < endgame_start_distance_to_portal / 3 else 1

            # establecer volumen según la distancia en cada sonido ambiental
            sounds.endgame_heart_beat.set_volume(clamp_volume(volume_offset))
            sounds.endgame_people_screaming.set_volume(clamp_volume(1 - calc_shrinking_as_closer(volume_offset)))
            sounds.endgame_people_screaming_hell.set_volume(clamp_volume(1 - calc_shrinking_as_closer(volume_offset_hell)))
            sounds.endgame_tense.set_volume(clamp_volume(1 - calc_shrinking_as_closer(volume_offset)))

            # calcular limites del portal (mas grande de lo normal) del enemigo
            portal_bounds = calc_bounds(portal_x, portal_y, tile_size, tile_size)
            # calcular si el jugador esta tocando al rango del protal
            (traspaso, traspaso_x, traspaso_y) = aabb_collision(player_bounds, portal_bounds)
            # en caso que haya un traspaso al portal, entrar dentro de la batalla del boss
            if traspaso:
                state = INTO_ENDGAME
                state_started = current_ticks
                sounds.endgame_ambience.fadeout(2500)
                sounds.endgame_heart_beat.fadeout(2500)
                sounds.endgame_people_screaming.fadeout(2500)
                sounds.endgame_people_screaming_hell.fadeout(2500)
                sounds.endgame_tense.fadeout(2500)
    
    # si el jugador se encuentra en estado de conversación
    elif state == TALKING:
        # si toca el boton de aceptar pelea, pasa a estado empezar batalla 
        if keys_down[pygame.K_SPACE] or keys_down[pygame.K_RETURN]:
            state = INTO_FIGHT
            state_started = current_ticks
        # si toca el boton para rechazar, regresa al estado libre para caminar
        if keys_down[pygame.K_ESCAPE]:
            state = WALKING
    
    # calcular camara para mostrar la posición del jugador según su desplazamiento
    calc_camera_position()
    
    # escalar la imagen del jugador al tamaño de la baldosa
    player = pygame.transform.scale(player, (tile_size, tile_size))

    # dibujar el mapa
    draw_map()

    # mostrar la cantidad de almas consumidas
    kill_count_text = fonts.body.render(f"{kill_count} - {len(enemies_pos)}", True, "white")
    interface.draw_surface(kill_count_text, (screen_rect.right - 20, screen_rect.top + 20), interface.anchor_topright)

    # mostrar dialogo de conversación cuando este en estado de conversación
    if state == TALKING:
        if state_is_starting == True:
            Dialogue_IDX = random.randint(0, len(strings.Dialogues)-1)
            state_is_starting = False
        screen.blit(TalkingBG, (45, 500))
        Dialoguestn = strings.Dialogues[Dialogue_IDX]
        for i, line in enumerate(Dialoguestn.split("\n")):
            enemy_dialogue = fonts.talk.render(line, True, "white")
            screen.blit(enemy_dialogue, (65, 525+50*i))

    # dentro del estado de empezar batalla
    if state == INTO_FIGHT:
        # mostrar transición de claro a oscuro en la pantalla (durante un segundo)
        if state_started:
            interface.draw_fade_in(interface.fill_black, ticks=current_ticks - state_started, duration=1000)
        # después de un segundo, pasar al modo batalla
        if current_ticks - state_started > 1000:
            states.change_state(states.BATTLE)

    # dentro del estado de empezar endgame
    if state == INTO_ENDGAME:
        endgame_ticks = current_ticks - state_started

        # mostrar transición de claro a oscuro en la pantalla (durante un segundo)
        if state_started:
            interface.draw_fade_in(interface.fill_red, ticks=endgame_ticks, duration=2500)
        
        if endgame_ticks > 2500:
            interface.draw_surface(interface.fill_red)
        
        if endgame_ticks > 5000 and endgame_ticks < 8000:
            draw_endgame_dialogue(strings.endgame_start_dialogue[0], endgame_ticks - 5000)
        
        if endgame_ticks > 8000 and endgame_ticks < 12000:
            draw_endgame_dialogue(strings.endgame_start_dialogue[1], endgame_ticks - 8000)
        
        if endgame_ticks > 12000 and endgame_ticks < 15000:
            draw_endgame_dialogue(strings.endgame_start_dialogue[2], endgame_ticks - 12000)
        
        if endgame_ticks > 15000 and endgame_ticks < 20000:
            draw_endgame_dialogue(strings.endgame_start_dialogue[3], endgame_ticks - 15000)
        
        if endgame_ticks > 20000 and endgame_ticks < 22000:
            draw_endgame_dialogue(strings.endgame_start_dialogue[4], endgame_ticks - 20000)
        
        if endgame_ticks > 22000 and endgame_ticks < 24000:
            dialogue_text = fonts.talk.render(strings.endgame_start_dialogue[4], True, "black")
            interface.draw_fade_out(dialogue_text, ticks=endgame_ticks - 22000, duration=2000)

        if endgame_ticks > 22000:
            if not endgame_evil_laugh_has_played:
                sounds.endgame_evil_laugh.play(loops=-1)
                endgame_evil_laugh_has_played = True
        
        if endgame_ticks > 25000:
            if not endgame_snd_evil_laugh_has_played:
                sounds.menu_possessed_laugh.play(loops=-1)
                sounds.menu_start_game.play(loops=-1)
                endgame_snd_evil_laugh_has_played = True
        
        if endgame_ticks > 27500 and not endgame_evil_laughes_fade_out:
            sounds.endgame_evil_laugh.fadeout(2500)
            sounds.menu_possessed_laugh.fadeout(2500)
            sounds.menu_start_game.fadeout(2500)
            endgame_evil_laughes_fade_out = False

        if current_ticks - state_started > 3000:
            states.change_state(states.BATTLE)
            battle.boss_battle = True
            battle.BG = images.boss_background
            battle.Enemy = images.boss
            battle.Enemy_HP = 20

    if state != INTO_ENDGAME and endgame:
        if current_ticks // 750 % 2 == 0:
            for i, line in enumerate(strings.endgame_false_win.split("\n")):
                dialogue_text = fonts.talk.render(line, True, "white")
                interface.draw_surface(dialogue_text, (screen_rect.centerx, screen_rect.bottom - 120 + 35 * i), interface.anchor_bottom)

        red_freq = player_distance_to_portal / endgame_start_distance_to_portal * 2 * 10000
        if red_freq > 0 and current_ticks // red_freq % 2 == 1:
            interface.draw_surface(interface.fill_red, special_flags=pygame.BLEND_RGBA_MULT, target=screen)

    # reglas para activar el comienzo del endgame
    if not endgame and kill_count == len(enemies_pos):
        endgame = True
        endgame_started = current_ticks
        endgame_is_starting = True

    # opciones de depuración
    # forzar activar endgame si presionas la tecla secreta
    if keys_pressed[pygame.K_LSHIFT] and keys_down[pygame.K_e]:
        kill_count = len(enemies_pos)
        endgame = True
        endgame_started = current_ticks
        endgame_is_starting = True
    # teletransportar al jugador al portal si presionas la tecla secreta
    if keys_pressed[pygame.K_LSHIFT] and keys_down[pygame.K_t]:
        (portal_x, portal_y) = calc_portal_pos(map_mat)
        player_x = portal_x
        player_y = portal_y

    # al salir de este estado de juego, pausar la música actual
    if states.is_exiting_state():
        music.stop()

# dibuja un dialogo para el inicio del endgame con una animación
def draw_endgame_dialogue(dialogue: str, ticks: int = 0):
    dialogue_duration = len(dialogue) * 100
    dialogue_slice = min(math.ceil(ticks * len(dialogue) / dialogue_duration), len(dialogue))
    dialogue_text = fonts.talk.render(dialogue[:dialogue_slice], True, "black")
    interface.draw_surface(dialogue_text)

# calcula el volument ambiental sin salir de los limites
def clamp_volume(x):
    return max(0, min(x, 1))

def calc_shrinking_as_closer(x):
    if x >= 1:
        return 1
    return -x * math.log(1 - x) * 0.5

# calcular posición de camará y establecer su variable global para su uso posterior
def calc_camera_position():
    # variables globales que actualizaremos
    global camera_x
    global camera_y

    # obtener instancias principales de juego
    screen_rect = game.get_screen_rect()

    # calcular limites de la camara
    # el limite izquierdo es una baldosa antes (mostrará hasta un borde negro)
    limit_left = -tile_size
    # el limite derecho es la cantidad entera de baldosas horizontalmente en el mapa mas una baldosa adicional
    limit_right = len(map_mat[0]) * tile_size - screen_rect.width + tile_size
    # el limite superior es una baldosa antes (mostrará hasta un borde negro)
    limit_top = -tile_size
    # el limite inferior es la cantidad entera de baldosas verticalmente en el mapa mas una baldosa adicional
    limit_bottom = len(map_mat) * tile_size - screen_rect.height + tile_size

    # calcular posicionamiento de la camará según la posición del jugador
    player_follow_x = player_x + tile_size / 2 - screen_rect.width / 2
    player_follow_y = player_y + tile_size / 2 - screen_rect.height / 2

    # si el desplazamiento de seguimiento horizontal del jugador es menor al limite izquierda
    if player_follow_x < limit_left:
        # la posición horizontal de la camara es el limite izquierdo
        camera_x = limit_left
    # si no, si el limite derecho es menor que el desplazamiento de seguimiento horizontal del jugador
    elif limit_right < player_follow_x:
        # la posición horizontal de la camara es el limite derecho
        camera_x = limit_right
    else:
        # de otra forma, la posición de la camara es el desplazamiento de seguimiento
        camera_x = player_follow_x

    # si el desplazamiento de seguimiento vertical del jugador es menor al limite superior
    if player_follow_y < limit_top:
        # la posición vertical de la camara es el limite superior
        camera_y = limit_top
    # si no, si el limite inferior es menor que el desplazamiento de seguimiento vertical del jugador
    elif limit_bottom < player_follow_y:
        # la posición vertical de la camara es el limite inferior
        camera_y = limit_bottom
    else:
        # de otra forma, la posición de la camara es el desplazamiento de seguimiento
        camera_y = player_follow_y


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


def calc_portal_pos(matriz: list[list[str]]) -> tuple[int, int]:
    for i, rows in enumerate(matriz):
        for j, columna in enumerate(rows):
            if columna == "S":
                return (j * tile_size, i * tile_size)


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

# funcion para dibujar mapa de mundo
def draw_map():
    screen=game.get_screen()
    # dibujamos el piso entero
    for i, fila in enumerate(map_mat):
        for j, columna in enumerate(fila):
            # si la columna es diferente de pared, dibujamos un piso
            if columna != "X":
                screen.blit(floor, posencam(tile_size*j, tile_size*i))
    # dibujamos al jugador, paredes y enemigos
    for i, fila in enumerate(map_mat):
        # calculamos en que fila se encuentra el jugador
        player_fila=math.floor((player_y+tile_size/2)/tile_size)
        # si el jugador se encuentra en la fila actual que estamos dibujando
        # dibujamos al jugador
        if i == player_fila:
            screen.blit(player, posencam(player_x, player_y))
        # por cada columna dibujamos una pared, o un enemigo
        for j, columna in enumerate(fila):
            # si la columna es pared, la dibujamos
            if columna == "X":
                screen.blit(wall, posencam(tile_size*j, tile_size*i-tile_size/4))
            # si la columna es enemigo, la dibujamos
            if columna == "E" and not endgame:
                screen.blit(blademaster, posencam(tile_size*j, tile_size*i))

# la funcion posencam (posicion en camara) sirve para establecer la camara
def posencam(x, y):
    return (x-camera_x, y-camera_y)
