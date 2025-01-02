import pygame
import game
import states

def state_controls():
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()

    if keys_down[pygame.K_F1]:
        states.change_state(states.INTRO)
    if keys_down[pygame.K_F2]:
        states.change_state(states.TITLESCREEN)
    if keys_down[pygame.K_F3]:
        states.change_state(states.MAIN_MENU)
    
    if keys_pressed[pygame.K_LSHIFT] and keys_down[pygame.K_ESCAPE]:
        game.running = False
