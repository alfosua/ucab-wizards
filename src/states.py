import game

# ESTADOS
# menúes
INTRO = 0
TITLESCREEN = 1
MAIN_MENU = 2
LOAD_GAME_MENU = 3
CREDITS = 4
# en juego
LOADING = 100
EXPLORATION = 101
BATTLE = 112
VICTORY = 103
GAMEOVER = 105
ENDGAME = 199
# para depuración
WIP = -100

# inicializar variables de estado
current_state = INTRO             # el estado inicial es la pantalla de introducción
current_state_started = 0         # tick del momento que empezó el actual estado
current_state_first_frame = True  # bandera que define si este es el primer tick del estado

def finish_frame():
    global current_state_first_frame
    if game.get_current_ticks() > current_state_started:
        current_state_first_frame = False

def get_state():
    return current_state

def get_started_at():
    return current_state_started

def is_current(state):
    return current_state == state

def is_first_frame():
    return current_state_first_frame

def change_state(new_state):
    global current_state
    global current_state_started
    global current_state_first_frame
    current_state = new_state
    current_state_started = game.get_current_ticks()
    current_state_first_frame = True
