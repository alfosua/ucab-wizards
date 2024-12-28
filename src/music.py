import pygame

# inicializar variables del estado de música
playing = False  # bandera que define si la musica está ejecutandose
volume = 1.0     # el volumen actual de la música

def play(filepath: str):
    global playing
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volume)
    playing = True

def stop():
    global playing
    pygame.mixer.music.stop()
    playing = False

def is_playing():
    return playing

def play_secret():
    play("assets/music/secret.mp3")

# Si quieres agregar más música, define una función como play_secret
# apuntando al archivo correcto, como por ejemplo:
# def play_my_song():
#     play("assets/sounds/my_song.mp3")
