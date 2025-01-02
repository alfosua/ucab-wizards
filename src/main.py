# importar modulos de pygame
import pygame

# inicializar modulos de pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# inicializar ventana
screen = pygame.display.set_mode((800, 720))

# inicializar reloj de juego
clock = pygame.time.Clock()

# importar modulos de juego
import game
import debug
import states
import savedata
import music

# importar y cargar recursos estáticos de juego
import strings
import fonts
import texts
import images
import sounds

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
    states.init_frame() # información del estado de juego

    # limpiar contenido dibujado anteriormente
    screen.fill("black")

    debug.state_controls()

    # ejecutar lógica de juego según el estado actual
    # para los estados de menués
    if states.is_current(states.INTRO):
        menu.run_intro()

    elif states.is_current(states.TITLESCREEN):
        menu.run_titlescreen()

    elif states.is_current(states.MAIN_MENU):
        menu.run_main_menu()

    elif states.is_current(states.NEW_GAME_MENU):
        menu.run_new_game()

    elif states.is_current(states.LOAD_GAME_MENU):
        menu.run_load_game()

    elif states.is_current(states.CREDITS):
        menu.run_credits()

    elif states.is_current(states.LOADING):
        menu.run_loading()
    
    # para los estados en juego
    elif states.is_current(states.EXPLORATION):
        exploration.run()

    elif states.is_current(states.BATTLE):
        battle.run_battle()

    elif states.is_current(states.VICTORY):
        battle.run_victory()

    elif states.is_current(states.GAMEOVER):
        battle.run_gameover()

    elif states.is_current(states.ENDGAME):
        menu.run_endgame()

    # para los estados de depuración
    elif states.is_current(states.WIP):
        wip.run()

    # mostrar cambios realizados en pantalla
    pygame.display.flip()

    # finalizar frame
    states.finish_frame() # información del estado de juego
    game.finish_frame() # información general del juego

    clock.tick(60)  # limitar frames por segundo a 60

pygame.quit()
