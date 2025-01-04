import datetime
import math
import random
import pygame
import game
import interface
import savedata
import states
import fonts
import texts
import images
import sounds
import strings
import music
import wip # eliminar esta línea al empezar a trabajar en esta pantalla

white_background = pygame.Surface(game.get_screen_rect().size)


def run_intro():
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = game.get_current_ticks()

    intro_ticks = current_ticks - states.get_started_at()

    if states.is_entering_state():
        sounds.konami_intro.play()

    ucab_logo_rect = images.ucab_logo.get_rect()
    ucab_logo_pos = (screen_rect.centerx - ucab_logo_rect.width / 2, screen_rect.centery - ucab_logo_rect.height / 2)
    pygame_logo_rect = images.pygame_logo.get_rect()
    pygame_logo_pos = (screen_rect.centerx - pygame_logo_rect.width / 2, screen_rect.centery - pygame_logo_rect.height / 2)
    
    if intro_ticks > 2900 and intro_ticks < 3400:
        alpha = (intro_ticks - 2900) % 500 * 255 / 500
        white_background.set_alpha(alpha)
        white_background.fill("white")
        screen.blit(white_background, (0, 0))
        images.ucab_logo.set_alpha(alpha)
        screen.blit(images.ucab_logo, ucab_logo_pos)

    if intro_ticks > 3400 and intro_ticks < 7100:
        white_background.set_alpha(255)
        white_background.fill("white")
        screen.blit(white_background, (0, 0))
        images.ucab_logo.set_alpha(255)
        screen.blit(images.ucab_logo, ucab_logo_pos)

    if intro_ticks > 7100 and intro_ticks < 7600:
        alpha = 255 - (intro_ticks - 7100) % 500 * 255 / 500
        white_background.set_alpha(alpha)
        white_background.fill("white")
        screen.blit(white_background, (0, 0))
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
    
    if intro_ticks > 14000 or game.is_any_key_down():
        states.change_state(states.TITLESCREEN)
    
    if states.is_exiting_state():
        sounds.konami_intro.stop()


def run_titlescreen():
    # obtener información general del juego para uso posterior
    screen_rect = game.get_screen_rect()
    current_ticks = states.get_current_state_ticks()
    
    if states.is_entering_state():
        music.play_parchment_0()
        
    draw_titlescreen_background()
    
    game_logo_wave_y = math.sin(current_ticks / 360) * 20

    interface.draw_surface(images.titlescreen_game_logo, (screen_rect.centerx, screen_rect.centery - game_logo_wave_y - 50))

    if current_ticks // 750 % 2 == 0:
        interface.draw_surface(texts.menu_press_any_button, (screen_rect.centerx, screen_rect.bottom - 100))

    if current_ticks < 5000:
        interface.draw_fade_in(interface.fill_black, ticks=current_ticks, duration=5000)

    if current_ticks >= 500 and game.is_any_key_down():
        states.change_state(states.MAIN_MENU)
        
    if states.is_exiting_state():
        music.stop()

def draw_titlescreen_torch_flame(position: pygame.Vector2 = pygame.Vector2(0, 0), target: pygame.Surface = game.get_screen()):
    ticks = states.get_current_state_ticks()
    current_sprite_idx = (ticks // 160) % 8
    current_sprite = images.torch_fire_flame_anim[current_sprite_idx]
    (pos_x, pos_y) = position
    interface.draw_surface(current_sprite, (pos_x, pos_y), interface.anchor_bottom, target=target)

def draw_titlescreen_background(zoom: float = 1):
    # crear superficie intermediaria primero
    screen_rect = game.get_screen_rect()
    result = pygame.Surface(screen_rect.size)
    # dibujar elementos sobre dicha superficie intermediaria
    interface.draw_surface(images.titlescreen_background, screen_rect.center, target=result)
    draw_titlescreen_torch_flame((screen_rect.centerx - 148, screen_rect.centery - 76), result)
    draw_titlescreen_torch_flame((screen_rect.centerx + 158, screen_rect.centery - 76), result)
    # aplicar efecto de zoom en la superficie intermediaria
    result = pygame.transform.scale(result, (screen_rect.width * zoom, screen_rect.height * zoom))
    # finalmente dibujar en pantalla
    interface.draw_surface(result, screen_rect.center)


menu_button_cursor = 0
menu_transitioning_started = 0
menu_transition_duration = 1000

main_menu_buttons = [
    (texts.menu_new_game_primary, texts.menu_new_game_secondary),
    (texts.menu_load_game_primary, texts.menu_load_game_secondary),
    (texts.menu_quit_primary, texts.menu_quit_secondary),
]

def run_main_menu():
    # importamos variables globales a cambiar
    global menu_go_back
    global menu_button_cursor
    global menu_transitioning_started

    # obtener información general del juego para uso posterior
    keys_down = game.get_keys_down()
    current_ticks = states.get_current_state_ticks()
    
    if states.is_entering_state():
        music.play_parchment_1()
        sounds.play_menu_possessed_laugh()
        menu_go_back = False
        menu_button_cursor = 0
        menu_transitioning_started = 0

    if not menu_transitioning_started:
        if keys_down[pygame.K_UP] or keys_down[pygame.K_w]:
            sounds.play_menu_button_switch()
            menu_button_cursor = menu_button_cursor - 1
        if keys_down[pygame.K_DOWN] or keys_down[pygame.K_s]:
            sounds.play_menu_button_switch()
            menu_button_cursor = menu_button_cursor + 1
        menu_button_cursor = menu_button_cursor % len(main_menu_buttons)

        if keys_down[pygame.K_RETURN] or keys_down[pygame.K_SPACE]:
            sounds.play_menu_button_tap()
            menu_transitioning_started = current_ticks

    background_zoom = 1
    if menu_transitioning_started:
        background_zoom = 1 + (current_ticks - menu_transitioning_started) / menu_transition_duration * 5
    draw_titlescreen_background(background_zoom)

    menu_content = render_menu_content()
    menu_content.set_alpha(255)
    if menu_transitioning_started:
        alpha = 255 - (current_ticks - menu_transitioning_started) * 255 / menu_transition_duration * 3
        menu_content.set_alpha(alpha)
    interface.draw_surface(menu_content)

    if menu_transitioning_started:
        interface.draw_fade_out(interface.fill_black, ticks=current_ticks - menu_transitioning_started, duration=menu_transition_duration)

    if menu_transitioning_started and current_ticks - menu_transitioning_started >= menu_transition_duration:
        if menu_button_cursor == 0:
            states.change_state(states.NEW_GAME_MENU)
        elif menu_button_cursor == 1:
            states.change_state(states.LOAD_GAME_MENU)
        elif menu_button_cursor == 2:
            game.running = False
    
    if states.is_exiting_state():
        music.stop()


def render_menu_content():
    # obtener información general del juego para uso posterior
    main_menu_ticks = states.get_current_state_ticks()
    screen_rect = game.get_screen_rect()
    result = pygame.Surface(screen_rect.size, pygame.SRCALPHA)

    # dibujar logo de juego
    game_logo_wave_y = math.sin(main_menu_ticks / 250) * 20
    game_logo_wave_x = math.cos(main_menu_ticks / 500) * 50
    game_logo_fraction = 1 / 3
    game_logo_pos_y = screen_rect.height / 4

    if main_menu_ticks < 250:
        game_logo_fraction = (2 / 3) - main_menu_ticks % 250 * (1 / 3) / 250
        game_logo_pos_y = screen_rect.centery - main_menu_ticks % 250 * (screen_rect.height / 4) / 250

    game_logo_fraction + (main_menu_ticks - menu_transitioning_started) / menu_transition_duration * 5
    game_logo_scaled = interface.scale_by_screen_width_fraction(images.titlescreen_game_logo, game_logo_fraction)
    game_logo_draw_pos = (screen_rect.centerx - game_logo_wave_x, game_logo_pos_y - game_logo_wave_y)

    interface.draw_surface(game_logo_scaled, game_logo_draw_pos, target=result)

    # dibujar botones
    buttons_offset_y = 100
    buttons_wave_y_highlight = math.sin(main_menu_ticks / 150) * 3
    buttons_wave_y = math.sin(main_menu_ticks / 250) * 5
    buttons_pos_x = screen_rect.centerx

    if main_menu_ticks < 350:
        buttons_pos_x = main_menu_ticks % 350 * screen_rect.centerx / 350

    for i, (highlight, base) in enumerate(main_menu_buttons):
        target = highlight if menu_button_cursor == i else base

        wave_multiplier = 1.75 if menu_button_cursor == i else 1 / (i + 0.5)
        wave_y = buttons_wave_y_highlight if menu_button_cursor == i else buttons_wave_y
        wave_offset_y = wave_y * wave_multiplier
        row_offset_y = buttons_offset_y + i * 50
        button_draw_pos = (buttons_pos_x, screen_rect.centery + row_offset_y + wave_offset_y)

        interface.draw_surface(target, button_draw_pos, target=result)
    
    return result


menu_go_back = False
player_name_text_input = ""
player_name_text_input_render = None
skin_cursor = 0

skin_options = [
    # nombre, imagenes, ...
    ("White", images.skins_white),
    ("Red", images.skins_red),
    ("Gold", images.skins_gold),
]

def run_new_game():
    global menu_go_back
    global menu_button_cursor
    global menu_transitioning_started
    global player_name_text_input
    global player_name_text_input_render
    global skin_cursor

    # obtener información general del juego para uso posterior
    screen_rect = game.get_screen_rect()
    keys_down = game.get_keys_down()
    current_ticks = states.get_current_state_ticks()

    if states.is_entering_state():
        music.play_parchment_2()
        menu_go_back = False
        menu_button_cursor = 0
        menu_transitioning_started = 0
        player_name_text_input = ""
        player_name_text_input_render = None
        skin_cursor = 0

    ignore_text_input = False
    ignore_start_tap = False
    if not menu_transitioning_started:
        if keys_down[pygame.K_ESCAPE]:
            sounds.play_menu_button_tap()
            menu_go_back = True
            menu_transitioning_started = current_ticks

        if keys_down[pygame.K_UP] or (keys_down[pygame.K_w] and menu_button_cursor != 1):
            sounds.play_menu_button_switch()
            menu_button_cursor = menu_button_cursor - 1
            ignore_text_input = True
        if keys_down[pygame.K_DOWN] or (keys_down[pygame.K_s] and menu_button_cursor != 1):
            sounds.play_menu_button_switch()
            menu_button_cursor = menu_button_cursor + 1
            ignore_text_input = True
        menu_button_cursor = menu_button_cursor % 3

        if menu_button_cursor == 0:
            if keys_down[pygame.K_LEFT] or keys_down[pygame.K_a]:
                sounds.play_menu_button_switch()
                skin_cursor = skin_cursor - 1
            if keys_down[pygame.K_RIGHT] or keys_down[pygame.K_d]:
                sounds.play_menu_button_switch()
                skin_cursor = skin_cursor + 1
            skin_cursor = skin_cursor % len(skin_options)
    
        if menu_button_cursor == 1 and not ignore_text_input:
            for event in game.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        sounds.play_menu_button_switch()
                        menu_button_cursor = 2
                        ignore_start_tap = True
                    elif event.key == pygame.K_BACKSPACE:
                        sounds.play_menu_button_switch()
                        player_name_text_input = player_name_text_input[:-1]
                        player_name_text_input_render = fonts.player_name_input.render(player_name_text_input, True, "white")
                    elif len(player_name_text_input) < 18 and event.unicode.isalpha() or event.unicode.isnumeric() or event.unicode == " ":
                        sounds.play_menu_button_switch()
                        player_name_text_input = player_name_text_input + event.unicode
                        player_name_text_input_render = fonts.player_name_input.render(player_name_text_input, True, "white")
        
        if menu_button_cursor == 2 and not ignore_start_tap and (keys_down[pygame.K_SPACE] or keys_down[pygame.K_RETURN]):
            if len(player_name_text_input) > 0:
                sounds.play_menu_button_tap()
                sounds.play_menu_start_game()
                menu_transitioning_started = current_ticks
            else:
                sounds.play_menu_button_switch()
                menu_button_cursor = 1
                ignore_text_input = True

    interface.draw_surface(images.menu_background)

    # dibujar selector de skin de personaje
    interface.draw_surface(texts.menu_select_your_tarnished_primary if menu_button_cursor == 0 else texts.menu_select_your_tarnished_secondary, (screen_rect.centerx, screen_rect.top + 100))
    (skin_name, skin_images) = skin_options[skin_cursor]
    skin_name_render = fonts.menu.render(skin_name, True, "white")
    skin_image = skin_images[current_ticks // 500 % 4] if menu_button_cursor == 0 else skin_images[0]
    skin_image_offset_y = 150
    interface.draw_surface(skin_image, (screen_rect.centerx, screen_rect.top + skin_image_offset_y), interface.anchor_top)
    interface.draw_surface(skin_name_render, (screen_rect.centerx, screen_rect.top + skin_image_offset_y + 110), interface.anchor_top)

    # dibujar entrada de texto para nombre de personaje
    interface.draw_surface(texts.menu_set_your_tarnished_name_primary if menu_button_cursor == 1 else texts.menu_set_your_tarnished_name_secondary, (screen_rect.centerx, screen_rect.centery))
    text_input_offset_y = 100
    if player_name_text_input_render:
        interface.draw_surface(player_name_text_input_render, (screen_rect.centerx, screen_rect.centery + text_input_offset_y))
        underline = pygame.Surface((player_name_text_input_render.get_width(), 4))
        underline.fill("white")
        interface.draw_surface(underline, (screen_rect.centerx, screen_rect.centery + text_input_offset_y + player_name_text_input_render.get_height() / 2 + 5), interface.anchor_top)
    if menu_button_cursor == 1 and current_ticks // 500 % 2 == 0:
        text_cursor = pygame.Surface((6, 55))
        text_cursor.fill("white")
        text_cursor_offset_x = 0 if not player_name_text_input_render else player_name_text_input_render.get_width() / 2
        interface.draw_surface(text_cursor, (screen_rect.centerx + text_cursor_offset_x + 10, screen_rect.centery + text_input_offset_y), interface.anchor_left)

    # dibujar botón de empezar
    interface.draw_surface(texts.menu_start_doom_primary if menu_button_cursor == 2 else texts.menu_start_doom_secondary, (screen_rect.centerx, screen_rect.bottom - 100))

    if current_ticks < 500:
        interface.draw_fade_in(interface.fill_black, ticks=current_ticks, duration=500)

    if menu_transitioning_started:
        interface.draw_fade_out(interface.fill_black, ticks=current_ticks - menu_transitioning_started, duration=menu_transition_duration)

    if menu_transitioning_started and current_ticks - menu_transitioning_started > menu_transition_duration:
        if menu_go_back:
            states.change_state(states.MAIN_MENU)
        else:
            # inicializar nueva partida en el sistema de guardas
            saves = savedata.get_saves()
            savedata.init_save(player_name_text_input, str(skin_cursor), str(datetime.datetime.today()), f"{player_name_text_input}_{len(saves) + 1}.txt")

            # pasar pantalla de carga
            states.change_state(states.LOADING)

    if states.is_exiting_state():
        music.stop()


loaded_saves = []

def run_load_game():
    global menu_go_back
    global menu_button_cursor
    global menu_transitioning_started
    global loaded_saves

    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    keys_down = game.get_keys_down()
    current_ticks = states.get_current_state_ticks()

    if states.is_entering_state():
        music.play_parchment_3()
        menu_button_cursor = 0
        menu_transitioning_started = 0
        loaded_saves = savedata.get_saves()

    if not menu_transitioning_started:
        if keys_down[pygame.K_ESCAPE]:
            sounds.play_menu_button_tap()
            menu_go_back = True
            menu_transitioning_started = current_ticks

        if keys_down[pygame.K_UP] or keys_down[pygame.K_w]:
            sounds.play_menu_button_switch()
            menu_button_cursor = menu_button_cursor - 1
        if keys_down[pygame.K_DOWN] or keys_down[pygame.K_s]:
            sounds.play_menu_button_switch()
            menu_button_cursor = menu_button_cursor + 1
        menu_button_cursor = menu_button_cursor % len(loaded_saves)
        
        if keys_down[pygame.K_SPACE] or keys_down[pygame.K_RETURN]:
            sounds.play_menu_button_tap()
            sounds.play_menu_start_game()
            menu_transitioning_started = current_ticks

    # dibujar la página de guardas
    page_size = 3
    page_count = math.ceil(len(loaded_saves) / page_size)
    current_page = math.floor(menu_button_cursor / page_size)
    start_index = current_page * page_size
    end_index = start_index + page_size
    box_gap = 30
    box_padding = 20
    for i, save in enumerate(loaded_saves[start_index:end_index]):
        idx = i + current_page * page_size
        box_size = (screen_rect.width - 100*2, 200)
        skin_size_sqr = box_size[1] - box_padding * 2
        box_pos = (screen_rect.centerx - box_size[0] / 2, screen_rect.top + box_gap + (box_size[1] + box_gap) * i)
        box_rect = (box_pos, box_size)
        pygame.draw.rect(screen, texts.color_primary if menu_button_cursor == idx else texts.color_secondary, box_rect, 4)

        (player_name, skin_idx, date_str, _) = save
        skin = pygame.transform.scale(skin_options[int(skin_idx)][1][0], (skin_size_sqr, skin_size_sqr))
        interface.draw_surface(skin, (box_pos[0] + box_padding, box_pos[1] + box_padding), interface.anchor_topleft)

        text_offset = box_pos[0] + box_padding + skin_size_sqr + box_padding
        text_padding = box_padding * 1.5

        player_name_text = fonts.menu.render(player_name, True, "white")
        interface.draw_surface(player_name_text, (text_offset, box_pos[1] + text_padding), interface.anchor_topleft)

        skin_text = fonts.menu.render(skin_options[int(skin_idx)][0], True, "white")
        interface.draw_surface(skin_text, (text_offset, box_pos[1] + box_size[1] / 2), interface.anchor_left)

        date_dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
        date_text = fonts.menu.render(date_dt.strftime("%Y-%m-%d %H:%M:%S"), True, "white")
        interface.draw_surface(date_text, (text_offset, box_pos[1] + box_size[1] - text_padding), interface.anchor_bottomleft)
    
    # dibujar contador de páginas
    if page_count > 1:
        current_page_text = fonts.menu.render(f"{current_page + 1}-{page_count}", True, "white")
        interface.draw_surface(current_page_text, (screen_rect.right - box_gap, screen_rect.bottom - box_gap), interface.anchor_bottomright)

    if current_ticks < 500:
        interface.draw_fade_in(interface.fill_black, ticks=current_ticks, duration=500)

    if menu_transitioning_started:
        interface.draw_fade_out(interface.fill_black, ticks=current_ticks - menu_transitioning_started, duration=menu_transition_duration)

    if menu_transitioning_started and current_ticks - menu_transitioning_started > menu_transition_duration:
        if menu_go_back:
            states.change_state(states.MAIN_MENU)
        else:
            # pasar pantalla de carga
            states.change_state(states.LOADING)

    if states.is_exiting_state():
        music.stop()


loading_duration = 10000
quote_idx = 0

def run_loading():
    global quote_idx

    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = states.get_current_state_ticks()

    if states.is_entering_state():
        quote_idx = random.randint(0, len(texts.loading_quotes) - 1)

    loading_text = texts.loading_ellipsis[current_ticks // 500 % len(texts.loading_ellipsis)]
    interface.draw_surface(loading_text, (screen_rect.right - 100, screen_rect.bottom - 30), interface.anchor_bottom)

    quote = texts.loading_quotes[quote_idx]
    for i, quote_line in enumerate(quote):
        interface.draw_surface(quote_line, (screen_rect.centerx, screen_rect.centery - 40 * len(quote) / 2 + 40 * i))

    if current_ticks < 500:
        interface.draw_fade_in(interface.fill_black, ticks=current_ticks, duration=500)

    if current_ticks > loading_duration:
        interface.draw_fade_out(interface.fill_black, ticks=current_ticks - loading_duration, duration=500)
    
    # después de 5 minutos y medio, pasar a pantalla de exploración
    if current_ticks > loading_duration + 500:
        states.change_state(states.EXPLORATION)


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

credits_offset = 0

def run_credits():
    global credits_offset

    # obtener información general del juego para uso posterior
    screen_rect = game.get_screen_rect()
    current_ticks = states.get_current_state_ticks()

    credits_render = render_credits()

    if current_ticks > 2000:
        if game.is_any_key_down():
            speed = 2
        else:
            speed = 1
        credits_offset = credits_offset + speed

    
    interface.draw_surface(images.menu_background)
    interface.draw_surface(credits_render, (screen_rect.centerx, screen_rect.top - credits_offset), interface.anchor_top)


def render_credits() -> pygame.Surface:
    screen_rect = game.get_screen_rect()
    result = pygame.Surface((screen_rect.width, 5000), pygame.SRCALPHA)

    offset = 100
    two_column_values_offset = 50

    interface.draw_surface(images.titlescreen_game_logo, (screen_rect.centerx, offset), interface.anchor_top, target=result)
    offset = offset + images.titlescreen_game_logo.get_height() + 200

    for section in strings.credits:
        title = section[0]
        title_render = fonts.credit_title.render(title, True, "white")
        interface.draw_surface(title_render, (screen_rect.centerx, offset), interface.anchor_top, target=result)
        offset = offset + title_render.get_height() + 100

        for item in section[1:]:
            key = item[0]
            value = item[1]

            key_render = fonts.credit_body.render(key, True, "white")
            if isinstance(value, list):
                interface.draw_surface(key_render, (screen_rect.centerx - 20 - two_column_values_offset, offset), interface.anchor_right, target=result)
            if isinstance(value, str):
                interface.draw_surface(key_render, (screen_rect.centerx, offset), target=result)

            if isinstance(value, list):
                for sub_value in value:
                    sub_value_render = fonts.credit_body.render(sub_value, True, "white")
                    interface.draw_surface(sub_value_render, (screen_rect.centerx + 20 - two_column_values_offset, offset), interface.anchor_left, target=result)
                    offset = offset + sub_value_render.get_height() + 10
            if isinstance(value, str):
                offset = offset + sub_value_render.get_height() + 10
                for line in value.split("\n"):
                    line_render = fonts.credit_body.render(line, True, "white")
                    interface.draw_surface(line_render, (screen_rect.centerx, offset), target=result)
                    offset = offset + line_render.get_height() + 10
            
            offset = offset + 25
        offset = offset + 100
    
    interface.draw_surface(images.ucab_logo, (screen_rect.centerx, offset), interface.anchor_top, target=result)
    offset = offset + images.ucab_logo.get_height() + 200

    interface.draw_surface(images.pygame_logo, (screen_rect.centerx, offset), interface.anchor_top, target=result)
    offset = offset + images.ucab_logo.get_height() + 200
    
    return result
