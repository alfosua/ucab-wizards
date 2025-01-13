import pygame
import game
from pygame import Surface, Vector2, Color
from pygame.font import Font

# constantes de referencia
ALPHA_MAX = 255

# rellenos comunes
fill_white = pygame.Surface(game.get_screen_rect().size)
fill_white.fill("white")
fill_black = pygame.Surface(game.get_screen_rect().size)
fill_black.fill("black")
fill_red = pygame.Surface(game.get_screen_rect().size)
fill_red.fill("red")

# anclas comunes
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
def draw_surface(
        source: Surface,
        position: Vector2 = game.get_screen_rect().center,
        anchor: Vector2 = anchor_center,
        special_flags: int = 0,
        target: Surface = game.get_screen()):
    source_rect = source.get_rect()
    anchor_offset_x = source_rect.width * anchor.x
    anchor_offset_y = source_rect.height * anchor.y
    target.blit(source, (position[0] - anchor_offset_x, position[1] - anchor_offset_y), special_flags=special_flags)


# escala una imagen según una fracción del ancho de la pantalla
def scale_by_screen_width_fraction(source: Surface, fraction: float):
    source_rect = source.get_rect()
    screen_rect = game.get_screen_rect()
    target_width = screen_rect.width * fraction
    target_size = (target_width, target_width * source_rect.height / source_rect.width)
    result = pygame.transform.scale(source, target_size)
    return result


# renderiza un texto con borde
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

# dibuja una superficie con un efecto de aparación progresiva
def draw_fade_out(source: Surface,
                 position: Vector2 = game.get_screen_rect().center,
                 anchor: Vector2 = anchor_center,
                 ticks: int = None,
                 duration: int = 500,
                  special_flags: int = 0,
                 target: Surface = game.get_screen()):
    # establecer valores iniciales
    if ticks is None:
        ticks = game.get_current_ticks()

    # calcular transición y aplicarlo en la transparencia de la superficie
    alpha = interpolation(ALPHA_MAX, 0, ticks, duration)
    source.set_alpha(alpha)
    
    # dibujar en objetivo
    draw_surface(source, position, anchor, special_flags, target)

# dibuja una superficie con un efecto de desaparación progresiva
def draw_fade_in(source: Surface,
                  position: Vector2 = game.get_screen_rect().center,
                  anchor: Vector2 = anchor_center,
                  ticks: int = None,
                  duration: int = 500,
                  special_flags: int = 0,
                  target: Surface = game.get_screen()):
    # establecer valores iniciales
    if ticks is None:
        ticks = game.get_current_ticks()

    # calcular transición y aplicarlo en la transparencia de la superficie
    alpha = interpolation(0, ALPHA_MAX, ticks, duration)
    source.set_alpha(alpha)
    
    # dibujar en objetivo
    draw_surface(source, position, anchor, special_flags, target)

# calcula interpolación entre un inicio y fin dado los milisegundos
# transcurridos con respecto a una duración especifica
def interpolation(start: int, end: int, ticks: int, duration: int):
    if ticks > duration:
        return end
    return round(start + (end - start) * ticks / duration)
