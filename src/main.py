# importar modulos de pygame
import pygame

# inicializar modulos de pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# inicializar ventana
screen = pygame.display.set_mode((800, 720))
screen_rect = screen.get_rect()

# inicializar reloj de juego
clock = pygame.time.Clock()

# importar y cargar recursos estáticos de juego
import strings
import fonts
import texts
import images
import sounds

# importar modulos de juego
import game
import states
import savedata
import music

# inicializar modulos de juego
savedata.init()

# establecer nombre de ventana
pygame.display.set_caption(strings.game_name)

# importar modulos de lógica de estados de juego
import menu
import exploration
import battle
import wip

# ciclo de juego
while game.running:
    # inicializar frame
    game.init_frame() # información general del juego

    # limpiar contenido dibujado anteriormente
    screen.fill("black")

    # ejecutar lógica de juego según el estado actual
    # para los estados de menués
    if states.is_current(states.INTRO):
        # TODO: implementar pantalla de introducción
        # mostrar pantalla de trabajo en progreso (eliminar al empezar a trabajar en esta pantalla)
        menu.run_intro()

    if states.is_current(states.TITLESCREEN):
        # TODO: implementar pantalla de título de juego
        # mostrar pantalla de trabajo en progreso (eliminar al empezar a trabajar en esta pantalla)
        menu.run_titlescreen()

    if states.is_current(states.MAIN_MENU):
        # TODO: implementar pantalla de menú de juego
        # mostrar pantalla de trabajo en progreso (eliminar al empezar a trabajar en esta pantalla)
        menu.run_main_menu()

    if states.is_current(states.LOAD_GAME_MENU):
        # TODO: implementar pantalla de cargar partida de juego
        # mostrar pantalla de trabajo en progreso (eliminar al empezar a trabajar en esta pantalla)
        menu.run_load_game()

    if states.is_current(states.CREDITS):
        menu.run_credits()
    
    # para los estados en juego
    if states.is_current(states.EXPLORATION):
        exploration.run()

    if states.is_current(states.BATTLE):
        battle.run_battle()

    if states.is_current(states.VICTORY):
        battle.run_victory()

    if states.is_current(states.GAMEOVER):
        battle.run_gameover()

    if states.is_current(states.ENDGAME):
        menu.run_endgame()

    # para los estados de depuración
    if states.is_current(states.WIP):
        wip.run()

    # mostrar cambios realizados en pantalla
    pygame.display.flip()

    # finalizar frame
    states.finish_frame() # información del estado de juego

    clock.tick(60)  # limitar frames por segundo a 60

pygame.quit()
