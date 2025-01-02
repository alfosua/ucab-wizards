from pygame.mixer import Sound

# sonido easter egg de kojima
kojima = Sound("assets/sounds/kojima.mp3")

# sonidos de pantalla de introducción
konami_intro = Sound("assets/sounds/konami_intro.mp3")

# sonidos de los menúes
menu_possessed_laugh = Sound("assets/sounds/menu/possessed_laugh.mp3")
menu_start_game = Sound("assets/sounds/menu/start_game.mp3")
menu_button_switch = Sound("assets/sounds/menu/button_switch.mp3")
menu_button_tap = Sound("assets/sounds/menu/button_tap.mp3")

def play(sound: Sound, volume_multiplier: float = 1):
    sound.set_volume(volume_multiplier)
    sound.play()

def play_menu_start_game() -> None:
    play(menu_start_game)

def play_menu_possessed_laugh() -> None:
    play(menu_possessed_laugh, volume_multiplier=2)

def play_menu_button_switch() -> None:
    play(menu_button_switch)

def play_menu_button_tap() -> None:
    play(menu_button_tap)

# agregar cada sonido a utilizar aquí...
