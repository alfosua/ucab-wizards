import pygame
import game
import states
import fonts
import texts
import images
import sounds
import strings
import music

def run():
    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = game.get_current_ticks()
    unscaled_current_ticks = game.get_unscaled_current_ticks()
    paused_ticks = game.get_pause_started_at()
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()

    # realizar ciertos calculos de temporizadores
    wip_ticks = current_ticks - states.get_started_at()
    elapsed_seconds_in_wip = wip_ticks // 1000

    paused_wip_ticks = unscaled_current_ticks - paused_ticks
    elapsed_seconds_in_paused_wip = paused_wip_ticks // 1000

    # empezar a reproducir música (solo en el primer frame)
    if states.is_first_frame():
        music.play_secret()

    # procesamiento de interacciones por el usuario
    if keys_down[pygame.K_SPACE]:
        sounds.kojima.play()
    if keys_pressed[pygame.K_ESCAPE]:
        game.set_pause(True)
    else:
        game.set_pause(False)

    # controles para cambiar de estado
    current_state = states.get_state()
    if keys_down[pygame.K_1]:
        states.change_state(states.INTRO)
    if keys_down[pygame.K_2]:
        states.change_state(states.TITLESCREEN)
    if keys_down[pygame.K_3]:
        states.change_state(states.MAIN_MENU)
    if keys_down[pygame.K_4]:
        states.change_state(states.LOAD_GAME_MENU)
    if keys_down[pygame.K_5]:
        states.change_state(states.CREDITS)
    if states.get_state() != current_state:
        music.stop()

    # renderización de elementos en la pantalla

    # aviso de trabajo en progreso
    screen.blit(images.wip, (0, screen_rect.centery - images.wip.get_height() // 2))
    screen.blit(texts.press_spacebar_anytime, (screen_rect.centerx - texts.press_spacebar_anytime.get_width() // 2, screen_rect.bottom - texts.press_spacebar_anytime.get_height() - 20))
    
    # contador de segundos
    seconds_text = fonts.body.render(strings.wip_seconds_message.format(elapsed_seconds_in_wip), False, "white")
    screen.blit(seconds_text, (screen_rect.centerx - seconds_text.get_width() // 2, screen_rect.bottom - seconds_text.get_height() - 50))
    
    # contador de segundos cuando está pausado el juego
    if game.is_paused():
        paused_seconds_text = fonts.body.render(strings.wip_seconds_paused_message.format(elapsed_seconds_in_paused_wip), False, "white")
        screen.blit(paused_seconds_text, (screen_rect.centerx - seconds_text.get_width() // 2, screen_rect.bottom - seconds_text.get_height() - 80))
