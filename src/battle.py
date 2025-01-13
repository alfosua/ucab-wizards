import math
import pygame
import game
import savedata
import interface
import states
import fonts
import texts
import images
import sounds
import strings
import music
import random
import exploration
import menu
from time import sleep
import wip # eliminar esta línea al empezar a trabajar en esta pantalla

#Lienzo
screen_rect = game.get_screen_rect()
BG = pygame.image.load("assets/images/battleresources/BattleBG.jpg")
BG = pygame.transform.scale(BG, screen_rect.size)
MC = pygame.image.load("assets/images/battleresources/Bichito.png")
MC = pygame.transform.scale(MC,(240,240))
Enemy = pygame.image.load("assets/images/battleresources/BattleEnemy.png")
Enemy = pygame.transform.scale (Enemy, (300,300))
MenuBG = pygame.image.load("assets/images/battleresources/BattleMenu.png")
MenuBG = pygame.transform.scale (MenuBG, (150, 150))
MagicBG = pygame.image.load ("assets/images/battleresources/MagicMenu.png")
MagicBG = pygame.transform.scale (MagicBG, (290, 150))
goscreen = pygame.image.load("assets/images/battleresources/GameOver.png")
goscreen = pygame.transform.scale(goscreen, (500, 300))

#Transición
entering = True
boss_battle = False

#Vida
Enemy_HP = 4
Player_HP = 4
Player_max_HP = 4
Health = pygame.image.load("assets/images/battleresources/heart.png")
Health = pygame.transform.scale (Health, (50,50))

#Turnos
Player_Turn = 0
Enemy_Turn = 1
CURRENT_TURN = Player_Turn
selected_option = 0
menu_options = ["Fight", "Magic", "Meditate", "Run"]

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
game_over_menu = 2
current_menu = battle_menu

#Tiempo
clock = pygame.time.Clock()
Turn_started = 0

font = pygame.font.SysFont(None, 36)

#Menu de Muerte
gameover_option = [ "Restart", "Main Menu" ]
choise = 0
selected_choise = 0

def draw_menu_death(screen):
    font = pygame.font.SysFont(None, 32)
    for z, choise in enumerate(gameover_option):
        color = (255, 0, 0) if z == selected_choise else (255, 255, 255)
        text = font.render(choise, True, color)
        screen.blit(text, (300, 500 + z * 50))

def death_options(choise):
    global current_menu
    global battle_menu
    global CURRENT_TURN
    global Player_HP
    if choise == 0:
        states.change_state(states.LOADING)
        exploration.state = exploration.WALKING
        savedata.load_game()
        current_menu = battle_menu
        CURRENT_TURN = Player_Turn
        
    elif choise == 1:
        states.change_state(states.MAIN_MENU)
        current_menu = battle_menu
        CURRENT_TURN = Player_Turn  
    Player_HP = 4


def run_gameover():
    global game_over_menu
    global spells_menu
    global battle_menu
    global game_over_menu
    global current_menu
    global selected_choise

    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = game.get_current_ticks()
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()
    current_menu = game_over_menu
    # TODO: implementar pantalla de game over
    # mostrar pantalla de trabajo en progreso (eliminar al empezar a trabajar en esta pantalla)
    screen.fill("black")
    screen.blit(goscreen, (160, 20))
    if current_menu == game_over_menu:
        draw_menu_death(screen)
        if keys_down[pygame.K_UP]:
            selected_choise = (selected_choise - 1) % len(gameover_option)
        if keys_down[pygame.K_DOWN]:
            selected_choise = (selected_choise + 1) % len(gameover_option)
        if keys_down[pygame.K_RETURN] or keys_down[pygame.K_SPACE]:
            death_options(selected_choise)

    # para cambiar de estado de juego usa la siguiente línea de código (descomentada)
    # states.change_state(states.WIP)

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
    global entering

    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = states.get_current_state_ticks()
    keys_pressed = game.get_keys_pressed()
    keys_down = game.get_keys_down()
    
    screen.blit(BG, (0,0))
    screen.blit(MC,(75,420))
    screen.blit(Enemy, (500,30))

    # Reproducir música solo cuando empieza este estado
    if states.is_entering_state():
        #Musica
        if boss_battle:
            music.play_boss_battle()
        else:
            music.play_battle()
        # activamos la transición
        entering = True

    #Vida del Enemigo y El personaje
    
    magic_text = fonts.talk.render(f"MANA= {Player_PP}", True, "Royalblue2")
    screen.blit(magic_text, (100, 380))

    for i in range(Player_HP):
        screen.blit(Health, (100 + 60 * i, 415))

    for i in range(Enemy_HP):
        screen.blit (Health, (500 + 60 * i, 50))
    
    if CURRENT_TURN == Player_Turn and not entering:
        if current_menu == battle_menu:
            screen.blit(MenuBG, (280, 485))
            draw_menu(screen)
            if keys_down[pygame.K_UP]:
                selected_option = (selected_option - 1) % len(menu_options)
            if keys_down[pygame.K_DOWN]:
                selected_option = (selected_option + 1) % len(menu_options)
            if keys_down[pygame.K_RETURN] or keys_down[pygame.K_SPACE]:
                handle_menu_selection(selected_option)

        elif current_menu == spells_menu:
            screen.blit(MagicBG, (290, 485))
            draw_menu_magic(screen)
            if keys_down[pygame.K_UP]:
                selected_spell = (selected_spell - 1) % len(Spells)
            if keys_down[pygame.K_DOWN]:
                selected_spell = (selected_spell + 1) % len(Spells)
            if keys_down[pygame.K_x] or keys_down[pygame.K_ESCAPE]:
                current_menu = battle_menu
            if keys_down[pygame.K_RETURN] or keys_down[pygame.K_SPACE]:
                handle_menu_selection_magic(selected_spell)    

    if CURRENT_TURN == Enemy_Turn:
        if Enemy_HP > 0:
            if current_ticks - Turn_started > 1000:
                Player_HP = Player_HP - 1
                sounds.play_hurt()
                CURRENT_TURN = Player_Turn
                current_menu = battle_menu
        if Enemy_HP <= 0:
            if boss_battle:
                states.change_state(states.VICTORY)
            else:
                change_to_exploration()
                exploration.kill_count = exploration.kill_count + 1
                savedata.save_game()

    if current_ticks < 2000:
        fill = interface.fill_black if not boss_battle else interface.fill_red
        interface.draw_fade_out(fill, ticks=current_ticks, duration=2000)
    else:
        entering = False
    
    if Player_HP <= 0:
        states.change_state(states.GAMEOVER)

    # Reproducir música solo cuando empieza este estado
    if states.is_exiting_state():
        music.stop()

def change_to_exploration():
    global Player_HP
    global Player_max_HP
    global Enemy_HP
    global CURRENT_TURN
    states.change_state(states.EXPLORATION)
    exploration.state = exploration.WALKING
    exploration.enemies_killed.append(exploration.current_enemy_idx)
    Player_max_HP = 4 + math.floor(exploration.kill_count / 3)
    Player_HP = Player_max_HP
    Enemy_HP = random.randint(3, 5)
    CURRENT_TURN = Player_Turn

def handle_menu_selection(option):
    global Enemy_HP
    global CURRENT_TURN
    global current_menu
    global Turn_started
    global Player_PP
    
    current_ticks = states.get_current_state_ticks()

    if option == 0:
        sounds.play_damage()
        Enemy_HP = Enemy_HP - 1
        CURRENT_TURN = Enemy_Turn
        Turn_started = current_ticks
    elif option == 1:
        current_menu = spells_menu
    elif option == 2:
        Player_PP = Player_PP + 15
        if Player_PP > 20:
            Player_PP = 20
        CURRENT_TURN = Enemy_Turn
        Turn_started = current_ticks
    elif option == 3 and not boss_battle:
        change_to_exploration()

def handle_menu_selection_magic(chosen_spell):
    global Enemy_HP
    global CURRENT_TURN
    global Player_PP
    global Turn_started
    global Player_HP
    
    current_ticks = states.get_current_state_ticks()

    if chosen_spell == 0 and Player_PP >= 5:
        Enemy_HP = Enemy_HP - 2
        Player_PP = Player_PP - 5
        sounds.spell_fireball()

    elif chosen_spell == 1 and Player_PP >= 7:
        Player_HP = Player_HP + 2
        Player_PP = Player_PP - 7
        if Player_HP > Player_max_HP:
            Player_HP = Player_max_HP
        sounds.spell_heal()

    elif chosen_spell == 2 and Player_PP >= 10:
        if chosen_spell == 2 and Player_PP >= 10:
            sounds.spell_rude_buster()
            sleep(0.20)
            sounds.spell_rude_buster_hit()
        Enemy_HP = Enemy_HP - 3 
        Player_PP = Player_PP - 10

    elif chosen_spell == 3 and  Player_PP >= 4:
        Enemy_HP = Enemy_HP - 1
        Player_PP = Player_PP - 4
        sounds.spell_tumbleweed()
        
    CURRENT_TURN = Enemy_Turn
    Turn_started = current_ticks
    
def run_victory():
    # obtener información general del juego para uso posterior
    screen = game.get_screen()
    screen_rect = game.get_screen_rect()
    current_ticks = states.get_current_state_ticks()

    screen.fill("red")
    win_str = "Tu alma ha sido liberada.\n¡Has ganado el juego! :D"
    for i, line in enumerate(win_str.split("\n")):
        line_text = fonts.credit_body.render(line, True, "white")
        interface.draw_surface(line_text,  (screen_rect.centerx, screen_rect.centery + i * 50 - 30))

    if current_ticks > 5000 or game.is_any_key_down():
        states.change_state(states.CREDITS)
