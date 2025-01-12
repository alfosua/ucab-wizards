import pygame
import game
import states
import fonts
import texts
import images
import sounds
import strings
import music
import random
from time import sleep
import wip # eliminar esta línea al empezar a trabajar en esta pantalla
current_ticks = game.get_current_ticks()
#Lienzo
screen_rect = game.get_screen_rect()
BG = pygame.image.load("assets/images/battleresources/BattleBG.jpg")
BG = pygame.transform.scale(BG, screen_rect.size)
MC = pygame.image.load("assets/images/battleresources/Bichito.png")
MC = pygame.transform.scale(MC,(240,240))
Enemy = pygame.image.load("assets/images/battleresources/BattleEnemy.png")
Enemy = pygame.transform.scale (Enemy, (300,300))
MenuBG = pygame.image.load("assets/images/battleresources/BattleMenu.png")
MenuBG = pygame.transform.scale (MenuBG, (105, 150))
MagicBG = pygame.image.load ("assets/images/battleresources/MagicMenu.png")
MagicBG = pygame.transform.scale (MagicBG, (290, 150))

#Vida
Enemy_HP = 3
Player_HP = 3
Health = pygame.image.load("assets/images/battleresources/heart.png")
Health = pygame.transform.scale (Health, (50,50))

#Turnos
Player_Turn = 0
Enemy_Turn = 1
CURRENT_TURN = Player_Turn
selected_option = 0
menu_options = ["Fight", "Magic", "Items", "Run"]

#Menu de magia
Spells = [ "Fireball (5 Mana)", "Heal (7 Mana)", "Rude Buster (10 Mana)", "Tumbleweed (4 Mana)" ]
Chosing_Spell = 1
chosen_spell = 4
selected_spell = 0
Player_PP = 20

#Estados del menu
items_menu = 2
spells_menu = 1
battle_menu = 0
current_menu = battle_menu

#Tiempo
clock = pygame.time.Clock()
Turn_started = 0

font = pygame.font.SysFont(None, 36)

def draw_menu(screen):
    font = pygame.font.SysFont(None, 36)
    for i, option in enumerate(menu_options):
        color = (255, 0, 0) if i == selected_option else (255, 255, 255)
        text = font.render(option, True, color)
        screen.blit(text, (300, 500 + i * 30))

def draw_menu_magic(screen):
    font = pygame.font.SysFont(None, 36)
    for f, chosen_spell in enumerate(Spells):
        color = (255, 0, 0) if f == selected_spell else (255, 255, 255)
        text = font.render(chosen_spell, True, color)
        screen.blit(text, (300, 500 + f * 30))


def run_battle():
    global selected_option 
    global Player_HP
    global CURRENT_TURN
    global chosen_spell
    global current_menu
    global selected_spell
    global Enemy_HP
    global Turn_started

    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = game.get_current_ticks()
    pygame.display.set_caption(str(current_ticks))
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()
    # TODO: implementar pantalla de batalla
    screen.blit(BG, (0,0))
    screen.blit(MC,(75,420))
    screen.blit(Enemy, (500,30))

    # Reproducir música solo cuando empieza este estado
    if states.is_entering_state():
        #Musica
        music.play_battle()

    #Vida del Enemigo y El personaje
    
    magic_text = fonts.talk.render(f"MANA= {Player_PP}", True, "Royalblue2")
    screen.blit(magic_text, (100, 465))

    for i in range(Player_HP):
        screen.blit(Health, (100 + 60 * i, 415))

    for i in range(Enemy_HP):
        screen.blit (Health, (500 + 60 * i, 50))
    
    if CURRENT_TURN == Player_Turn:

        if current_menu == battle_menu:
            screen.blit(MenuBG, (280, 485))
            draw_menu(screen)
            if keys_down[pygame.K_UP]:
                selected_option = (selected_option - 1) % len(menu_options)
            if keys_down[pygame.K_DOWN]:
                selected_option = (selected_option + 1) % len(menu_options)
            if keys_down[pygame.K_RETURN]:
                handle_menu_selection(selected_option)

        elif current_menu == spells_menu:
            screen.blit(MagicBG, (290, 485))
            draw_menu_magic(screen)
            if keys_down[pygame.K_UP]:
                selected_spell = (selected_spell - 1) % len(Spells)
            if keys_down[pygame.K_DOWN]:
                selected_spell = (selected_spell + 1) % len(Spells)
            if keys_down[pygame.K_x]:
                current_menu = battle_menu
            if keys_down[pygame.K_RETURN]:
                handle_menu_selection_magic(selected_spell)
    #Limite de la vida        
    
    if CURRENT_TURN == Enemy_Turn:
        if current_ticks - Turn_started > 1000:
            Player_HP = Player_HP - 1
            sounds.play_hurt()
            CURRENT_TURN = Player_Turn
            current_menu = battle_menu

    # Reproducir música solo cuando empieza este estado
    if states.is_exiting_state():
        music.stop()

def handle_menu_selection(option):
    pygame.display.set_caption(str(current_ticks))
    global Enemy_HP
    global CURRENT_TURN
    global current_menu
    global Turn_started

    if option == 0:
        sounds.play_damage()
        Enemy_HP = Enemy_HP - 1
        print("Option 1 selected")  
        CURRENT_TURN = Enemy_Turn
        Turn_started = game.current_ticks

    elif option == 1:
        current_menu = spells_menu            
        print("Option 2 selected")
            
    elif option == 2:
        print("Option 3 selected")

    elif option == 3:
        print("Option 4 selected")


def handle_menu_selection_magic(chosen_spell):
    current_ticks = game.get_current_ticks()
    global Enemy_HP
    global CURRENT_TURN
    global Player_PP
    global Turn_started
    global Player_HP

    if chosen_spell == 0 and Player_PP > 5:
        Enemy_HP = Enemy_HP - 2
        Player_PP = Player_PP - 5
        Turn_started = game.current_ticks
        sounds.spell_fireball()

    elif chosen_spell == 1 and Player_PP > 7:
        Player_HP = Player_HP + 2
        Player_PP = Player_PP - 7
        if Player_HP > 3:
            Player_HP = 3
        Turn_started = game.current_ticks
        sounds.spell_heal()
    elif chosen_spell == 2 and Player_PP > 10:
        if chosen_spell == 2 and Player_PP > 10:
            sounds.spell_rude_buster()
            sleep(0.20)
            sounds.spell_rude_buster_hit()
        Enemy_HP = Enemy_HP - 3 
        Player_PP = Player_PP - 10
        Turn_started = game.current_ticks

    elif chosen_spell == 3 and  Player_PP > 4:
        Enemy_HP = Enemy_HP - 1
        Player_PP = Player_PP - 4
        Turn_started = game.current_ticks
        sounds.spell_tumbleweed()
        
    CURRENT_TURN = Enemy_Turn

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
