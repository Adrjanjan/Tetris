import pygame
from pygame.locals import *
import os


class Scores:

    def __init__(self, screen, board_width, board_height):

        self._screen = screen
        self._width = board_width
        self._height = board_height
        self._scores_top_left = (110, 250)
        self._margin = 12

        if os.name == "nt":
            self._score_file = os.path.join(os.path.dirname(__file__), "scores.txt").replace("/", "\\")
            self._score_foto_dir = os.path.join(os.path.dirname(__file__), "graphics", "Scores.png").replace("/", "\\")
            self._font_path = os.path.join(os.path.dirname(__file__), "font", "Roboto-Bold.ttf").replace("/", "\\")
        elif os.name == "posix":
            self._score_file = os.path.join(os.path.dirname(__file__), "scores.txt").replace("\\", "/")
            self._score_foto_dir = os.path.join(os.path.dirname(__file__), "graphics", "Scores.png").replace("\\", "/")
            self._font_path = os.path.join(os.path.dirname(__file__), "font", "Roboto-Bold.ttf").replace("\\", "/")
        else:
            self._score_file = os.path.join(os.path.dirname(__file__), "scores.txt")
            self._score_foto_dir = os.path.join(os.path.dirname(__file__), "graphics", "Scores.png")
            self._font_path = os.path.join(os.path.dirname(__file__), "font", "Roboto-Bold.ttf")

        self._score_foto = pygame.image.load(self._score_foto_dir).convert()
        self._score_foto_rect = self._score_foto.get_rect()
        self._score_foto = pygame.transform.scale(self._score_foto, (self._width, self._height))

        pygame.font.init()
        self._roboto_bold_30 = pygame.font.Font(self._font_path, 30)
        self._roboto_bold_40 = pygame.font.Font(self._font_path, 40)

    def add_score(self, name, score):
        scores = []

        with open(self._score_file, "r") as scores_file:
            for line in scores_file:
                scores.append(line.split(" "))

        if len(scores) > 0:
            for i in range(len(scores), 0, -1):
                if score > int(scores[0][1]):
                    scores.insert(0, [name, str(score) + "\n"])
                    break
                if int(scores[i - 1][1]) > score:
                    scores.insert(i - 1, [name, str(score) + "\n"])
                    print(scores)
                    break
        else:
            scores.append([name, str(score) + "\n"])

        while len(scores) > 5:
            del scores[-1]

        with open(self._score_file, "w") as scores_file:
            for line in scores:
                scores_file.writelines(str(line[0]) + " " + str(line[1]))

    def show_scores(self):
        scores = []
        self._screen.blit(self._score_foto, self._score_foto_rect)

        with open(self._score_file, "r") as scores_file:
            for line in scores_file:
                scores.append(line.split(" "))

            if len(scores) > 0:
                for i in range(len(scores)):
                    self.write(scores[i][0], (221, 221, 221), self._scores_top_left[0],
                               self._scores_top_left[1] + i * (self._margin + 30))

                    self.write(scores[i][1][:-1], (221, 221, 221), self._scores_top_left[0] + 260,
                               self._scores_top_left[1] + i * (self._margin + 30))

                    self.write(scores[i][0], (153, 153, 153), self._scores_top_left[0] + 1,
                               self._scores_top_left[1] + i * (self._margin + 30) + 1)

                    self.write(scores[i][1][:-1], (153, 153, 153), self._scores_top_left[0] + 260 + 1,
                               self._scores_top_left[1] + i * (self._margin + 30) + 1)

        pygame.display.update()

    def write(self, string, col, top_left_x=0, top_left_y=0):
        text_surf = self._roboto_bold_30.render(string, True, col)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (top_left_x, top_left_y)
        self._screen.blit(text_surf, text_rect)

    def write_center(self, string, col, adj_ver=0, adj_hor=0):
        text_surf = self._roboto_bold_30.render(string, True, col)
        text_rect = text_surf.get_rect()
        text_rect.center = self._screen.get_rect().center
        text_rect.topleft = (text_rect.topleft[0] + adj_hor, text_rect.topleft[1] + adj_ver)
        self._screen.blit(text_surf, text_rect)

    def clear_scores(self):
        scores_file = open(self._score_file, "w")
        scores_file.close()

    def insert_name(self):
        name = ""

        while True:
            for evt in pygame.event.get():
                if evt.type == KEYDOWN:
                    if evt.unicode.isalpha():
                        name += evt.unicode
                    elif evt.key == K_BACKSPACE:
                        name = name[:-1]
                    elif evt.key == K_RETURN:
                        self._screen.fill((64, 65, 68))
                        pygame.display.flip()
                        return name
                elif evt.type == QUIT:
                    pygame.display.flip()
                    self._screen.fill((64, 65, 68))
                    return name
            self._screen.fill((64, 65, 68))

            self.write_center("Podaj nazwę - max. 6 znaków:", (221, 221, 221))

            self.write_center("Podaj nazwę - max. 6 znaków:", (153, 153, 153), 1, 1)

            self.write_center(name, (221, 221, 221), 40)

            self.write_center(name, (153, 153, 153), 41)

            pygame.display.flip()
