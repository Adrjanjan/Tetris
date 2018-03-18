import pygame
import sys
from time import time
import blocks as bl
import playground as pg
import utility_draw as ud
import music as ms
import scores as sc


class Game:

    def __init__(self):
        # Consts
        self._PLAYGROUND_WIDTH = 10  # PLGR - short for playground
        self._PLAYGROUND_HEIGHT = 20
        self._MARGIN = 20
        self._SCALE = 30  # px
        self._WIDTH = self._SCALE * self._PLAYGROUND_WIDTH * 2 + 2 * self._MARGIN  # *2, bo pole na wynik, menu
        self._HEIGHT = self._SCALE * self._PLAYGROUND_HEIGHT + 2 * self._MARGIN
        self._FPS = 30

        self._RUNNING = True
        self._PAUSED = False
        self._SWAPPED = False
        self._SCORES = False

        self._MOVE_SIDE_TIME = time()
        self._MOVE_DOWN_TIME = time()
        self._MOVE_SIDE_SPEED = 0
        self._MOVE_DOWN_SPEED = 0.4
        self._HIDE_REFALL = 0

        self._SCORE = 0
        self._LEVEL = 1

        # initialization
        pygame.init()                                                       # Pygame
        self.musicplayer = ms.Music()                                       # Music
        self.screen = pygame.display.set_mode((self._WIDTH, self._HEIGHT))  # Screen
        self.clock = pygame.time.Clock()                                    # clock
        pygame.display.set_caption(
            "Tetris - Adrian Janakiewicz (C) 2017 _FPS: {:.2f}".format(self.clock.get_fps()))  # Window caption

        self.playground = pg.Playground(self.screen, self._PLAYGROUND_WIDTH,
                                        self._PLAYGROUND_HEIGHT, self._SCALE, self._MARGIN)

        self.utility_window = ud.UtilityWindow(self.screen, self._PLAYGROUND_WIDTH,
                                               self._PLAYGROUND_HEIGHT, self._SCALE, self._MARGIN)

        self.scores_screen = sc.Scores(self.screen, self._WIDTH, self._HEIGHT)

        self.falling = bl.Tetromino(-5, 3)
        self.next_piece = bl.Tetromino(2, 13)
        self.utility_window.next_piece = self.next_piece

    def intro(self):
        self.playground.on_intro()
        intro = True

        while intro:
            if not pygame.mixer.music.get_busy():
                self.musicplayer.play_a_next_song()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    intro = False
                    self._RUNNING = False

                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()

                if (201 <= mouse_x <= 441 and 216 <= mouse_y <= 276) or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):  # run game
                    pygame.draw.rect(self.screen, (255, 255, 255, 10), (216, 201, 240, 60))
                    if mouse_click[0] == 1:
                        if not self._PAUSED:
                            self.__init__()
                        self._RUNNING = True
                        self._PAUSED = False
                        self.run()
                        self.playground.on_intro()

                if 201 <= mouse_x <= 441 and 366 <= mouse_y <= 426:  # show scores
                    pygame.draw.rect(self.screen, (255, 255, 255, 10), (216, 501, 240, 60))
                    if mouse_click[0] == 1:
                        self.show_scores()

                if 201 <= mouse_x <= 441 and 516 <= mouse_y <= 576:  # exit game
                    pygame.draw.rect(self.screen, (255, 255, 255, 10), (216, 501, 240, 60))
                    if mouse_click[0] == 1:
                        self._RUNNING = False
                        sys.exit()

    def run(self):  # game loop
        self.playground.draw_once()
        self.utility_window.draw_once()

        while self._RUNNING:
            if not pygame.mixer.music.get_busy():
                self.musicplayer.play_a_next_song()
            pygame.display.set_caption(
                "Tetris - Adrian Janakiewicz (C) 2017 FPS: {:.2f}".format(self.clock.get_fps()))  # Window caption + FPS

            self.events()

            self.loop()

            self.render()

            self.ticking()

    def show_scores(self):
        show_scores = True

        self.scores_screen.show_scores()

        while show_scores:
            if not pygame.mixer.music.get_busy():
                self.musicplayer.play_a_next_song()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    show_scores = False

                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()

                if 275 <= mouse_x <= 365 and 576 <= mouse_y <= 616:
                    if mouse_click[0] == 1:
                        show_scores = False

                elif 288 <= mouse_x <= 349 and 15 <= mouse_y <= 35:
                    if mouse_click[0] == 1:
                        self.scores_screen.clear_scores()
                        show_scores = False

        self.playground.on_intro()

    def events(self):

        for events in pygame.event.get():
            if events.type == pygame.QUIT or (events.type == pygame.KEYDOWN and events.key == pygame.K_ESCAPE):
                self._RUNNING = False

            elif events.type == pygame.KEYDOWN and self.falling is not None:
                if events.key in (pygame.K_UP,  pygame.K_w):
                    self.playground.rotate_tetromino(self.falling)

                elif events.key in (pygame.K_LEFT, pygame.K_a)and time() - self._MOVE_SIDE_TIME > self._MOVE_SIDE_SPEED:
                    self.playground.move_side_tetromino(self.falling, -1)
                    self._MOVE_SIDE_TIME = time()

                elif events.key in (pygame.K_RIGHT, pygame.K_d) and\
                        time() - self._MOVE_SIDE_TIME > self._MOVE_SIDE_SPEED:

                    self.playground.move_side_tetromino(self.falling, 1)
                    self._MOVE_SIDE_TIME = time()

                elif events.key in (pygame.K_DOWN, pygame.K_s):
                    self.playground.move_down_tetromino(self.falling)

                elif events.key == pygame.K_p:
                    self._PAUSED = True
                    self._RUNNING = False

                elif events.key == pygame.K_SPACE:
                    self.playground.dropdown(self.falling)
                    self.playground.add_tetromino(self.falling)
                    self.falling = None

                elif events.key == pygame.K_z:
                    if self._HIDE_REFALL < 3:
                        self._HIDE_REFALL += 1
                        self.playground.refall(self.falling)

                elif events.key == pygame.K_x:
                    if not self._SWAPPED:
                        self._SWAPPED = True
                        self.falling, self.next_piece = self.next_piece, self.falling
                        self.falling.vertical = -5
                        self.falling.horizontal = 3
                        self.next_piece.vertical = 2
                        self.next_piece.horizontal = 13
                        self.utility_window.next_piece = self.next_piece
                        self.playground.refall(self.falling)

    def loop(self):

        if self.falling is None:
            self._SWAPPED = False
            self.falling = self.next_piece
            self.falling.vertical = -5
            self.falling.horizontal = 3
            self.next_piece = bl.Tetromino(2, 13)
            self.utility_window.next_piece = self.next_piece
            if not self.playground.is_in_valid_position(self.falling):
                return

        can_fall = time() - self._MOVE_DOWN_TIME > self._MOVE_DOWN_SPEED
        if can_fall:
            if self.playground.is_in_valid_position(self.falling, adjVert=1):
                self.playground.move_down_tetromino(self.falling)
                self._MOVE_DOWN_TIME = time()

            else:
                if self.falling.vertical < 0:
                    self._RUNNING = False  # GAME OVER
                    if self._SCORE != 0:
                        self.scores_screen.add_score(self.scores_screen.insert_name(), self._SCORE)

                self.playground.add_tetromino(self.falling)
                self.falling = None

        self._SCORE = self.playground.delete_full_lines(self._SCORE, self._LEVEL)
        self._LEVEL, self._MOVE_DOWN_SPEED = self.playground.calc_lvl_and_fall_speed(self._SCORE)

    def render(self):

        self.playground.draw_playground()
        self.playground.draw_falling(self.falling)
        self.utility_window.draw_background(self._SCORE, self._LEVEL, self._HIDE_REFALL)
        pygame.display.update()

    def ticking(self):
        self.clock.tick(self._FPS)
