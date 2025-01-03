import strings
import fonts
import interface

# colores
color_primary = "#fec203"
color_secondary = "#c33f95"
color_tertiary = "#16002e"

press_spacebar_anytime = fonts.body.render(strings.press_spacebar_anytime, False, "white")

# textos para el menú principal
menu_press_any_button = interface.render_text_with_outline(fonts.menu, strings.press_any_button, True, color_primary, 3, color_tertiary)
menu_new_game_primary = interface.render_text_with_outline(fonts.menu, strings.new_game, True, color_primary, 3, color_tertiary)
menu_new_game_secondary = interface.render_text_with_outline(fonts.menu, strings.new_game, True, color_secondary, 3, color_tertiary)
menu_load_game_primary = interface.render_text_with_outline(fonts.menu, strings.load_game, True, color_primary, 3, color_tertiary)
menu_load_game_secondary = interface.render_text_with_outline(fonts.menu, strings.load_game, True, color_secondary, 3, color_tertiary)
menu_quit_primary = interface.render_text_with_outline(fonts.menu, strings.quit, True, color_primary, 3, color_tertiary)
menu_quit_secondary = interface.render_text_with_outline(fonts.menu, strings.quit, True, color_secondary, 3, color_tertiary)
menu_select_your_tarnished_primary = interface.render_text_with_outline(fonts.menu, strings.select_your_tarnished, True, color_primary, 3, color_tertiary)
menu_select_your_tarnished_secondary = interface.render_text_with_outline(fonts.menu, strings.select_your_tarnished, True, color_secondary, 3, color_tertiary)
menu_set_your_tarnished_name_primary = interface.render_text_with_outline(fonts.menu, strings.set_your_tarnished_name, True, color_primary, 3, color_tertiary)
menu_set_your_tarnished_name_secondary = interface.render_text_with_outline(fonts.menu, strings.set_your_tarnished_name, True, color_secondary, 3, color_tertiary)
menu_start_doom_primary = interface.render_text_with_outline(fonts.menu, strings.start_doom, True, color_primary, 3, color_tertiary)
menu_start_doom_secondary = interface.render_text_with_outline(fonts.menu, strings.start_doom, True, color_secondary, 3, color_tertiary)

# textos para pantallas de carga
loading_ellipsis = [
    fonts.menu.render("Loading", True, "white"),
    fonts.menu.render("Loading.", True, "white"),
    fonts.menu.render("Loading..", True, "white"),
    fonts.menu.render("Loading...", True, "white"),
]
loading_quotes = []
for quote in strings.loading_quotes:
    quote_lines = []
    for line in quote:
        quote_lines.append(fonts.menu.render(line, True, "white"))
    loading_quotes.append(quote_lines)

# agregar cada renderización de texto estática aquí...
