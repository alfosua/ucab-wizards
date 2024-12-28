import pygame

screen_rect = pygame.display.get_surface().get_rect()

# aviso de trabajo en progreso
wip = pygame.image.load("assets/images/wip.png")
wip = pygame.transform.scale(wip, (screen_rect.width, screen_rect.width * wip.get_rect().height / wip.get_rect().width))

# imagenes para intro
ucab_logo = pygame.image.load("assets/images/titlescreen/ucab_logo.png")
ucab_logo = pygame.transform.scale(ucab_logo, (500, 500))
pygame_logo = pygame.image.load("assets/images/titlescreen/pygame_logo.png")
pygame_logo_width = screen_rect.width / 3 * 2
pygame_logo_size = (pygame_logo_width, pygame_logo_width * pygame_logo.get_rect().height / pygame_logo.get_rect().width)
pygame_logo = pygame.transform.scale(pygame_logo, pygame_logo_size)

# agregar cada imagen a utilizar aquí...
