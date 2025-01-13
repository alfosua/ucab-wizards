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
    if keys_down[pygame.K_F4]:
        states.change_state(states.NEW_GAME_MENU)
    if keys_pressed[pygame.K_LSHIFT] and keys_down[pygame.K_F4]:
        states.change_state(states.LOAD_GAME_MENU)
    if keys_down[pygame.K_F5]:
        states.change_state(states.EXPLORATION)
    if keys_down[pygame.K_F6]:
        states.change_state(states.BATTLE)
    if keys_down[pygame.K_F7]:
        states.change_state(states.VICTORY)
    if keys_down[pygame.K_F8]:
        states.change_state(states.GAMEOVER)
    if keys_down[pygame.K_F9]:
        states.change_state(states.ENDGAME)
    if keys_down[pygame.K_F10]:
        states.change_state(states.CREDITS)
    if keys_down[pygame.K_F11]:
        states.change_state(states.LOADING)
    if keys_down[pygame.K_F12]:
        states.change_state(states.WIP)
    
    if keys_pressed[pygame.K_LSHIFT] and keys_down[pygame.K_ESCAPE]:
        game.running = False
