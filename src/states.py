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
next_state = None                 # el estado el cual el juego estará transicionando
previous_state = None             # el estado anterior del juego
entering_state = True             # bandera que define si está entrando en el estado (es el primer frame)
exiting_state = False             # bandera que define si este saliendo en el estado (es el último frame)

def init_frame():
    global previous_state
    global current_state
    global next_state
    global current_state_started
    global entering_state
    if next_state != None:
        previous_state = current_state
        current_state = next_state
        next_state = None
        current_state_started = game.get_current_ticks()
        entering_state = True

def finish_frame():
    global entering_state
    global exiting_state
    entering_state = False
    exiting_state = False

def change_state(new_state):
    global next_state
    global exiting_state
    next_state = new_state
    exiting_state = True

def get_state():
    return current_state

def get_started_at():
    return current_state_started

def is_current(state):
    return current_state == state

def is_entering_state():
    return entering_state

def is_exiting_state():
    return exiting_state
