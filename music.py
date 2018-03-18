import os
import random
import pygame


class Music:

    _BACKGROUND_MUSIC = ["BenZel_-_Wasted_Love_Spectrasoul_Remix_",
                         "Elliot_Moss_-_Slip_SpectraSoul_Bootleg_",
                         "Hybrid_Minds_-_Lost_",
                         "Hybrid_Minds_-_Meant_To_Be",
                         "Hybrid_Minds_-_Summer_Rain",
                         "Jakwob_-_Blinding_Hybrid_Minds_Remix_",
                         "SpectraSoul_-_How_We_Live",
                         "SpectraSoul_-_Second_Chance"]

    def __init__(self):
        self._NOW_PLAYED = random.choice(self._BACKGROUND_MUSIC)
        pygame.mixer.init()  # Music
        pygame.mixer.music.set_volume(0.3)

    def play_a_next_song(self):
        next_song = random.choice(self._BACKGROUND_MUSIC)

        while next_song == self._NOW_PLAYED:
            next_song = random.choice(self._BACKGROUND_MUSIC)
        self._NOW_PLAYED = next_song

        if os.name == "nt":
            _SONG = os.path.join(os.path.dirname(__file__), "music", next_song + ".wav").replace("/", "\\")
        elif os.name == "posix":
            _SONG = os.path.join(os.path.dirname(__file__), "music", next_song + ".wav").replace("\\", "/")
        else:
            _SONG = os.path.join(os.path.dirname(__file__), "music", next_song + ".wav")

        pygame.mixer.music.load(_SONG)
        pygame.mixer.music.play(0)

    @staticmethod
    def cleared_line_sound():
        if os.name == "nt":
            _effect = pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), "music", "Cleared_Line.wav").replace("\\", "/"))
        elif os.name == "posix":
            _effect = pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), "music", "Cleared_Line.wav").replace("\\", "/"))
        else:
            _effect = pygame.mixer.Sound(
                os.path.join(os.path.dirname(__file__), "music", "Cleared_Line.wav").replace("\\", "/"))
        _effect.play()
