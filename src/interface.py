import pygame
import game
from pygame import Surface, Vector2, Color
from pygame.font import Font

anchor_center = Vector2(0.5, 0.5)
anchor_top = Vector2(0.5, 0)
anchor_bottom = Vector2(0.5, 1)
anchor_left = Vector2(0, 0.5)
anchor_right = Vector2(1, 0.5)
anchor_topleft = Vector2(0, 0)
anchor_topright = Vector2(1, 0)
anchor_bottomleft = Vector2(0, 1)
anchor_bottomright = Vector2(1, 1)

# dibuja una superficie usando el sistema de anclas
def draw_surface(source: Surface, position: Vector2 = game.get_screen_rect().center, anchor: Vector2 = anchor_center, target: Surface = game.get_screen()):
    source_rect = source.get_rect()
    anchor_offset_x = source_rect.width * anchor.x
    anchor_offset_y = source_rect.height * anchor.y
    target.blit(source, (position[0] - anchor_offset_x, position[1] - anchor_offset_y))


# Escala una imagen según una fracción del ancho de la pantalla
def scale_by_screen_width_fraction(source: Surface, fraction: float):
    source_rect = source.get_rect()
    screen_rect = game.get_screen_rect()
    target_width = screen_rect.width * fraction
    target_size = (target_width, target_width * source_rect.height / source_rect.width)
    result = pygame.transform.scale(source, target_size)
    return result


# Renderiza un texto con borde
def render_text_with_outline(font: Font, text: str, antialising: bool, fill_color: Color, border_width: int, border_color: Color):
    fill = font.render(text, antialising, fill_color)
    border = font.render(text, antialising, border_color)
    base_size = (fill.get_width() + border_width * 2, fill.get_height() + border_width * 2)
    result = Surface(base_size, pygame.SRCALPHA)
    result.blit(border, (0, 0))
    result.blit(border, (border_width, 0))
    result.blit(border, (border_width*2, 0))
    result.blit(border, (0, border_width))
    result.blit(border, (0, border_width*2))
    result.blit(border, (border_width, border_width))
    result.blit(border, (border_width*2, border_width*2))
    result.blit(fill, (border_width, border_width))
    return result
