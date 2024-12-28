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

background = pygame.Surface(game.get_screen_rect().size)

def run_intro():
    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = game.get_current_ticks()
    keys_down = game.get_keys_down()

    intro_ticks = current_ticks - states.get_started_at()

    if states.is_first_frame():
        sounds.konami_intro.play()

    ucab_logo_rect = images.ucab_logo.get_rect()
    ucab_logo_pos = (screen_rect.centerx - ucab_logo_rect.width / 2, screen_rect.centery - ucab_logo_rect.height / 2)
    pygame_logo_rect = images.pygame_logo.get_rect()
    pygame_logo_pos = (screen_rect.centerx - pygame_logo_rect.width / 2, screen_rect.centery - pygame_logo_rect.height / 2)
    
    if intro_ticks > 2900 and intro_ticks < 3400:
        alpha = (intro_ticks - 2900) % 500 * 255 / 500
        background.set_alpha(alpha)
        background.fill("white")
        screen.blit(background, (0, 0))
        images.ucab_logo.set_alpha(alpha)
        screen.blit(images.ucab_logo, ucab_logo_pos)

    if intro_ticks > 3400 and intro_ticks < 7100:
        background.set_alpha(255)
        background.fill("white")
        screen.blit(background, (0, 0))
        images.ucab_logo.set_alpha(255)
        screen.blit(images.ucab_logo, ucab_logo_pos)

    if intro_ticks > 7100 and intro_ticks < 7600:
        alpha = 255 - (intro_ticks - 7100) % 500 * 255 / 500
        background.set_alpha(alpha)
        background.fill("white")
        screen.blit(background, (0, 0))
        images.ucab_logo.set_alpha(alpha)
        screen.blit(images.ucab_logo, ucab_logo_pos)

    if intro_ticks > 8400 and intro_ticks < 8900:
        alpha = (intro_ticks - 8400) % 500 * 255 / 500
        images.pygame_logo.set_alpha(alpha)
        screen.blit(images.pygame_logo, pygame_logo_pos)

    if intro_ticks > 8900 and intro_ticks < 12600:
        images.pygame_logo.set_alpha(255)
        screen.blit(images.pygame_logo, pygame_logo_pos)

    if intro_ticks > 12600 and intro_ticks < 13100:
        alpha = 255 - (intro_ticks - 12600) % 500 * 255 / 500
        images.pygame_logo.set_alpha(alpha)
        screen.blit(images.pygame_logo, pygame_logo_pos)
    
    if intro_ticks > 14000:
        states.change_state(states.TITLESCREEN)
        sounds.konami_intro.stop()


def run_titlescreen():
    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = game.get_current_ticks()
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()

    # TODO: implementar pantalla de título de juego
    # mostrar pantalla de trabajo en progreso (eliminar al empezar a trabajar en esta pantalla)
    wip.run()

    # para cambiar de estado de juego usa la siguiente línea de código (descomentada)
    # states.change_state(states.WIP)

def run_main_menu():
    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = game.get_current_ticks()
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()

    # TODO: implementar pantalla de menu principal de juego
    # mostrar pantalla de trabajo en progreso (eliminar al empezar a trabajar en esta pantalla)
    wip.run()

    # para cambiar de estado de juego usa la siguiente línea de código (descomentada)
    # states.change_state(states.WIP)

def run_load_game():
    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = game.get_current_ticks()
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()

    # TODO: implementar pantalla de cargar partida
    # mostrar pantalla de trabajo en progreso (eliminar al empezar a trabajar en esta pantalla)
    wip.run()

    # para cambiar de estado de juego usa la siguiente línea de código (descomentada)
    # states.change_state(states.WIP)

def run_endgame():
    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = game.get_current_ticks()
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()

    # TODO: implementar pantalla de fin de juego
    # mostrar pantalla de trabajo en progreso (eliminar al empezar a trabajar en esta pantalla)
    wip.run()

    # para cambiar de estado de juego usa la siguiente línea de código (descomentada)
    # states.change_state(states.WIP)

def run_credits():
    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = game.get_current_ticks()
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()

    # TODO: implementar pantalla de créditos
    # mostrar pantalla de trabajo en progreso (eliminar al empezar a trabajar en esta pantalla)
    wip.run()

    # para cambiar de estado de juego usa la siguiente línea de código (descomentada)
    # states.change_state(states.WIP)
