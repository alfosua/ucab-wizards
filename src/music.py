import pygame

# inicializar variables del estado de música
playing = False  # bandera que define si la musica está ejecutandose
volume = 1       # el volumen actual de la música

def play(filepath: str, loops: int = -1, volume_multiplier: float = 1):
    global playing
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play(loops, 0, 300)
    pygame.mixer.music.set_volume(volume * volume_multiplier)
    playing = True

def stop():
    global playing
    pygame.mixer.music.stop()
    playing = False

def fadeout(time: int):
    global playing
    pygame.mixer.music.fadeout(time)
    playing = False

def is_playing():
    return playing

def play_secret():
    play("assets/music/secret.mp3")

def play_parchment_0():
    play("assets/music/parchment_0a.mp3", loops=1, volume_multiplier=0.33)
    pygame.mixer.music.queue("assets/music/parchment_0b.mp3", loops=-1)

def play_parchment_1():
    play("assets/music/parchment_1a.mp3", volume_multiplier=0.33)

def play_parchment_2():
    play("assets/music/parchment_2a.mp3", volume_multiplier=0.33)

def play_parchment_3():
    play("assets/music/parchment_3a.mp3", volume_multiplier=0.33)

def play_parchment_4():
    play("assets/music/parchment_4a.mp3", volume_multiplier=0.33)

def play_unforgiven():
    play("assets/music/unforgiven.mp3")
# Si quieres agregar más música, define una función como play_secret
# apuntando al archivo correcto, como por ejemplo:
# def play_my_song():
#     play("assets/sounds/my_song.mp3")
