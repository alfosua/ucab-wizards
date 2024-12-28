import pygame

screen_rect = pygame.display.get_surface().get_rect()

# aviso de trabajo en progreso
wip = pygame.image.load("assets/images/wip.png")
wip = pygame.transform.scale(wip, (screen_rect.width, screen_rect.width * wip.get_rect().height / wip.get_rect().width))

# agregar cada imagen a utilizar aquí...
