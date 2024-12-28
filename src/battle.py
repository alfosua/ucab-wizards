import pygame
import game
import states
import fonts
import texts
import images
import sounds
import strings
import music
import wip # eliminar esta línea al empezar a trabajar en esta pantalla

def run_battle():
    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = game.get_current_ticks()
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()

    # TODO: implementar pantalla de batalla
    # mostrar pantalla de trabajo en progreso (eliminar al empezar a trabajar en esta pantalla)
    wip.run()

    # para cambiar de estado de juego usa la siguiente línea de código (descomentada)
    # states.change_state(states.WIP)

def run_gameover():
    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = game.get_current_ticks()
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()

    # TODO: implementar pantalla de game over
    # mostrar pantalla de trabajo en progreso (eliminar al empezar a trabajar en esta pantalla)
    wip.run()

    # para cambiar de estado de juego usa la siguiente línea de código (descomentada)
    # states.change_state(states.WIP)

def run_victory():
    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = game.get_current_ticks()
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()

    # TODO: implementar pantalla de victoria
    # mostrar pantalla de trabajo en progreso (eliminar al empezar a trabajar en esta pantalla)
    wip.run()

    # para cambiar de estado de juego usa la siguiente línea de código (descomentada)
    # states.change_state(states.WIP)
