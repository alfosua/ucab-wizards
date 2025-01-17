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

# sonidos para el modo batalla
being_hurt = Sound("assets/sounds/battle/hurt.wav")
hurt_enemy = Sound("assets/sounds/battle/damage.wav")
fireballsfx = Sound("assets/sounds/battle/spellfireballsfx.wav")
healsfx = Sound("assets/sounds/battle/spellhealsfx.wav")
rudebustersfx = Sound("assets/sounds/battle/spellrudebustersfx.wav")
rudebusterhit = Sound("assets/sounds/battle/spellrudebusterhitsfx.wav")
tumbleweedsfx = Sound("assets/sounds/battle/spelltumbleweedsfx.wav")

# sonidos para el endgame
endgame_ambience = Sound("assets/sounds/endgame/ambience.mp3")
endgame_evil_laugh = Sound("assets/sounds/endgame/evil_laugh.mp3")
endgame_heart_beat = Sound("assets/sounds/endgame/heart_beat.mp3")
endgame_people_screaming = Sound("assets/sounds/endgame/people_screaming.mp3")
endgame_people_screaming_hell = Sound("assets/sounds/endgame/people_screaming_hell.mp3")
endgame_tense = Sound("assets/sounds/endgame/tense.mp3")


def play(sound: Sound, loops: int = 0, volume_multiplier: float = 1):
    sound.set_volume(volume_multiplier)
    sound.play(loops=loops)

def play_menu_start_game() -> None:
    play(menu_start_game)

def play_menu_possessed_laugh() -> None:
    play(menu_possessed_laugh, volume_multiplier=2)

def play_menu_button_switch() -> None:
    play(menu_button_switch)

def play_menu_button_tap() -> None:
    play(menu_button_tap)

def play_hurt():
    play(being_hurt)

def play_damage():
    play(hurt_enemy)

def spell_fireball():
    play(fireballsfx)

def spell_heal():
    play(healsfx)

def spell_rude_buster():
    play(rudebustersfx)

def spell_tumbleweed():
    play(tumbleweedsfx)

def spell_rude_buster_hit():
    play(rudebusterhit)

# agregar cada sonido a utilizar aquí...
