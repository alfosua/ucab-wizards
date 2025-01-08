import pygame
import interface

screen_rect = pygame.display.get_surface().get_rect()

# aviso de trabajo en progreso
wip = pygame.image.load("assets/images/wip.png")
wip = pygame.transform.scale(wip, (screen_rect.width, screen_rect.width * wip.get_rect().height / wip.get_rect().width))

# imagenes para intro
ucab_logo = pygame.image.load("assets/images/titlescreen/ucab_logo.jpg")
ucab_logo = interface.scale_by_screen_width_fraction(ucab_logo, 1)
pygame_logo = pygame.image.load("assets/images/titlescreen/pygame_logo.png")
pygame_logo = interface.scale_by_screen_width_fraction(pygame_logo, 2 / 3)

# imagenes para pantalla de título
titlescreen_background = pygame.image.load("assets/images/titlescreen/background.png")
titlescreen_background = pygame.transform.scale(titlescreen_background, screen_rect.size)
titlescreen_game_logo = pygame.image.load("assets/images/titlescreen/game_logo.png")
titlescreen_game_logo = interface.scale_by_screen_width_fraction(titlescreen_game_logo, 2 / 3)
torch_fire_flame_anim = [
    pygame.image.load("assets/images/titlescreen/torch_fire_flame/0.png"),
    pygame.image.load("assets/images/titlescreen/torch_fire_flame/1.png"),
    pygame.image.load("assets/images/titlescreen/torch_fire_flame/2.png"),
    pygame.image.load("assets/images/titlescreen/torch_fire_flame/3.png"),
    pygame.image.load("assets/images/titlescreen/torch_fire_flame/4.png"),
    pygame.image.load("assets/images/titlescreen/torch_fire_flame/5.png"),
    pygame.image.load("assets/images/titlescreen/torch_fire_flame/6.png"),
    pygame.image.load("assets/images/titlescreen/torch_fire_flame/7.png"),
]

# imagenes para menúes
menu_background = pygame.image.load("assets/images/menu/background.png")
menu_background = pygame.transform.scale(menu_background, screen_rect.size)

# imagenes para el selector de skins
skins_white_front = pygame.image.load("assets/images/skins/samuel/front.png")
skins_white_right = pygame.image.load("assets/images/skins/samuel/right.png")
skins_white_back = pygame.image.load("assets/images/skins/samuel/back.png")
skins_white_left = pygame.image.load("assets/images/skins/samuel/left.png")
skins_white_front_walk = [ 
    pygame.image.load("assets/images/skins/samuel/walk/front_01.png"),     
    pygame.image.load("assets/images/skins/samuel/walk/front_02.png")     
]
skins_white_back_walk =  [ 
    pygame.image.load("assets/images/skins/samuel/walk/back_01.png"),     
    pygame.image.load("assets/images/skins/samuel/walk/back_02.png")     
]
skins_white_left_walk =  [ 
    pygame.image.load("assets/images/skins/samuel/walk/left_01.png"),     
    pygame.image.load("assets/images/skins/samuel/walk/left_02.png")     
]
skins_white_right_walk =  [ 
    pygame.image.load("assets/images/skins/samuel/walk/right_01.png"),     
    pygame.image.load("assets/images/skins/samuel/walk/right_02.png")     
]
skins_white_all = [
    skins_white_front,
    skins_white_back,
    skins_white_left,
    skins_white_right,
    skins_white_front_walk,
    skins_white_back_walk,
    skins_white_left_walk,
    skins_white_right_walk,
]
skins_white_showcase = [
    skins_white_front,
    skins_white_right,
    skins_white_back,
    skins_white_left,
]


skins_red_all = [
    skins_white_front,
    skins_white_back,
    skins_white_left,
    skins_white_right,
    skins_white_front_walk,
    skins_white_back_walk,
    skins_white_left_walk,
    skins_white_right_walk,
]
skins_red_showcase = [
    skins_white_showcase[0].copy(),
    skins_white_showcase[1].copy(),
    skins_white_showcase[2].copy(),
    skins_white_showcase[3].copy(),
]
for img in skins_red_all:
    if isinstance(img, pygame.Surface):
        img.fill("red", special_flags=pygame.BLEND_MIN)
    elif isinstance(img, list):
        for img2 in img:
            img2.fill("red", special_flags=pygame.BLEND_MIN)
for img in skins_red_showcase:
    img.fill("red", special_flags=pygame.BLEND_MIN)


skins_gold_all = [
    skins_white_front,
    skins_white_back,
    skins_white_left,
    skins_white_right,
    skins_white_front_walk,
    skins_white_back_walk,
    skins_white_left_walk,
    skins_white_right_walk,
]
skins_gold_showcase = [
    skins_white_showcase[0].copy(),
    skins_white_showcase[1].copy(),
    skins_white_showcase[2].copy(),
    skins_white_showcase[3].copy(),
]
for img in skins_gold_all:
    if isinstance(img, pygame.Surface):
        img.fill("red", special_flags=pygame.BLEND_MIN)
    elif isinstance(img, list):
        for img2 in img:
            img2.fill("red", special_flags=pygame.BLEND_MIN)
for img in skins_gold_showcase:
    img.fill("gold", special_flags=pygame.BLEND_MIN)

# agregar cada imagen a utilizar aquí...
