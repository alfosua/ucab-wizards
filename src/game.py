# Este archivo define la información general de la ejecución de la partida

# importar modulos de
import pygame

# inicializar información general de la ejecución de la partida
running = True               # bandera para definir si el juego se encuentra ejecutando
paused = False               # bandera para definir si el juego se encuentra en pausa
pause_started = 0            # cuando la pause comenzó
elapsed_ticks = 0            # la cantidad de ticks pasados desde el último frame (respetando la pausa de juego)
current_ticks = 0            # la cantidad de ticks hasta ahora (respetando la pausa de juego)
unescaled_elapsed_ticks = 0  # la cantidad de ticks pasados desde el último frame (sin respetar la pausa de juego)
unscaled_current_ticks = 0   # la cantidad de ticks hasta ahora (sin respetar la pausa de juego)

# inicializar diccionarios de seguimientos de teclas
keys_to_track = [
    # Todas las letras
    pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f,
    pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l,
    pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r,
    pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x,
    pygame.K_y, pygame.K_z,
    # Todos los números
    pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
    pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
    # Teclas direccionales
    pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
    # Teclas recurrentes
    pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_TAB,
    # Teclas de función
    pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, pygame.K_F6,
    pygame.K_F7, pygame.K_F8, pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12,
    # Teclas modificadores
    pygame.K_LSHIFT, pygame.K_LCTRL, pygame.K_LALT, pygame.K_RSHIFT, pygame.K_RCTRL, pygame.K_RALT,
]
keys_down = {key: False for key in keys_to_track}

def init_frame():
    global running
    global paused
    global pause_started
    global elapsed_ticks
    global current_ticks
    global unescaled_elapsed_ticks
    global unscaled_current_ticks
    global keys_down

    # capturar información para temporizadores
    unescaled_elapsed_ticks = pygame.time.get_ticks() - unscaled_current_ticks
    unscaled_current_ticks = pygame.time.get_ticks()
    if not paused:
        elapsed_ticks = unescaled_elapsed_ticks
        current_ticks = current_ticks + elapsed_ticks
        pause_started = 0
    else:
        elapsed_ticks = 0
        if not pause_started:
            pause_started = unscaled_current_ticks

    # inicializar información para seguimiento de teclas
    keys_down = {key: False for key in keys_to_track}

    # inicialmente procesar los eventos para lógica básica y captura
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys_down[event.key] = True


def is_paused():
    return paused

def get_pause_started_at():
    return pause_started

def set_pause(value: bool):
    global paused
    paused = value

def get_screen():
    return pygame.display.get_surface()

def get_screen_rect():
    return get_screen().get_rect()

def get_current_ticks():
    return current_ticks

def get_unscaled_current_ticks():
    return unscaled_current_ticks

def get_elapsed_ticks():
    return elapsed_ticks

def get_keys_pressed():
    return pygame.key.get_pressed()

def get_keys_down():
    return keys_down
