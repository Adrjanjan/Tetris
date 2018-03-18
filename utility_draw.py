import pygame
import os


class UtilityWindow:
    next_piece = None

    def __init__(self, scr, board_width, board_height, ratio, margin):

        self._ratio = ratio
        self._screen = scr
        self._boardWidth = board_width
        self._boardHeight = board_height
        self._MARGIN = margin
        self._SIZE_X = self._ratio * self._boardWidth
        self._SIZE_Y = self._ratio * self._boardHeight
        self._board = [[0 for ii in range(self._boardWidth)] for jj in range(self._boardHeight)]

        self._font_front_col = (153, 153, 153)
        self._font_back_col = (221, 221, 221)
        self._background_col = (64, 65, 68)
        self._falling_background_col = (108, 109, 112)

        if os.name == "nt":
            self._font_path = os.path.join(os.path.dirname(__file__), "font", "Roboto-Bold.ttf").replace("/", "\\")
        elif os.name == "posix":
            self._font_path = os.path.join(os.path.dirname(__file__), "font", "Roboto-Bold.ttf").replace("\\", "/")
        else:
            self._font_path = os.path.join(os.path.dirname(__file__), "font", "Roboto-Bold.ttf")

        pygame.font.init()
        self._roboto_bold_30 = pygame.font.Font(self._font_path, 30)

    def draw_once(self):
        background = self.get_photo("Utility.png", 300, 600)
        # noinspection PyUnresolvedReferences
        self._screen.blit(background[0], (background[1][0] + self._MARGIN + self._SIZE_X,
                                          background[1][1] + self._MARGIN))

    def draw_background(self, score, level, refall):
        pygame.draw.rect(self._screen, self._falling_background_col, (self._MARGIN + self._SIZE_X + 40,
                                                                      self._MARGIN + 62, 220, 220))

        self.draw_next(self.next_piece)

        pygame.draw.rect(self._screen, self._background_col, (self._MARGIN + self._SIZE_X + 30,
                                                              self._MARGIN + 335, 250, 50))

        self.write(str(score), self._font_back_col, self._SIZE_X + self._MARGIN + 40, 355)

        self.write(str(score), self._font_front_col, self._SIZE_X + self._MARGIN + 41, 356)

        self.write(str(level), self._font_back_col, self._SIZE_X + self._MARGIN + 180, 355)

        self.write(str(level), self._font_front_col, self._SIZE_X + self._MARGIN + 181, 356)

        self.hide_refall(refall)

    @staticmethod
    def get_photo(name, size_x, size_y):
        if os.name == "nt":
            image_dir = os.path.join(os.path.dirname(__file__), 'graphics', name).replace("/", "\\")
        elif os.name == "posix":
            image_dir = os.path.join(os.path.dirname(__file__), 'graphics', name).replace("\\", "/")
        else:
            image_dir = os.path.join(os.path.dirname(__file__), 'graphics', name)

        picture = pygame.image.load(image_dir).convert()
        picture_rect = picture.get_rect()
        picture = pygame.transform.scale(picture, (size_x, size_y))

        return picture, picture_rect

    def write(self, string, color, top_left_x, top_left_y):
        text_surf = self._roboto_bold_30.render(string, True, color)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (top_left_x, top_left_y)
        self._screen.blit(text_surf, text_rect)

    def draw_next(self, piece):
        if piece is not None:
            for ii in range(len(piece.rot)):
                for jj in range(len(piece.rot[ii])):
                    if piece.rot[ii][jj] != 0:
                        self.draw_box(piece.vertical + ii+1, piece.horizontal + jj, piece.rot[ii][jj])

    def draw_box(self, y, x, bl_id):
        size_x = self._MARGIN + self._ratio * x
        size_y = self._MARGIN + self._ratio * y

        black = (0, 0, 0)
        colour = (((201, 115, 255), (235, 184, 255), (127, 63, 152), (210, 162, 221)),  # 1: Pink       - I
                  ((5, 32, 226), (64, 59, 244), (9, 9, 147), (73, 112, 219)),  # 2: Dark Blue  - T
                  ((255, 227, 87), (255, 255, 50), (255, 189, 0), (255, 235, 153)),  # 3: Yellow     - O
                  ((247, 148, 30), (251, 176, 64), (241, 90, 41), (243, 173, 92)),  # 4: Orange     - J
                  ((0, 165, 224), (0, 224, 255), (28, 117, 188), (70, 200, 190)),  # 5: Light Blue - L
                  ((84, 214, 0), (156, 255, 0), (57, 161, 74), (152, 221, 62)),  # 6: Green      - S
                  ((255, 36, 55), (255, 148, 150), (190, 30, 45), (255, 148, 150)))  # 7: Red        - Z

        pygame.draw.rect(self._screen, colour[bl_id - 1][0], (size_x, size_y, self._ratio, self._ratio))

        pygame.draw.polygon(self._screen, colour[bl_id - 1][1], (
            (size_x + 2, size_y + 2), (size_x + 28, size_y + 2), (size_x + 28, size_y + 28), (size_x + 24, size_y + 24),
            (size_x + 24, size_y + 6), (size_x + 6, size_y + 6)))

        pygame.draw.polygon(self._screen, colour[bl_id - 1][2], (
            (size_x + 2, size_y + 2), (size_x + 6, size_y + 6), (size_x + 6, size_y + 24), (size_x + 24, size_y + 24),
            (size_x + 28, size_y + 28), (size_x + 2, size_y + 28)))

        pygame.draw.polygon(self._screen, colour[bl_id - 1][3], (
            (size_x + 6, size_y + 6), (size_x + 8, size_y + 22), (size_x + 24, size_y + 24), (size_x + 6, size_y + 24)))

        pygame.draw.rect(self._screen, black, (size_x, size_y, self._ratio, self._ratio), 2)

    def draw_box2(self, y, x, bl_id):
        size_x = self._MARGIN + self._ratio * x
        size_y = self._MARGIN + self._ratio * y

        block_image = [self.get_photo("Empty.png", 30, 30), self.get_photo("1.png", 30, 30),
                       self.get_photo("2.png",     30, 30), self.get_photo("3.png", 30, 30),
                       self.get_photo("4.png",     30, 30), self.get_photo("5.png", 30, 30),
                       self.get_photo("6.png",     30, 30), self.get_photo("7.png", 30, 30)]

        # noinspection PyUnresolvedReferences
        self._screen.blit(block_image[bl_id][0], (block_image[bl_id][1][0] + size_x, block_image[bl_id][1][1] + size_y))

    def hide_refall(self, to_hide):

        if to_hide == 1:
            pygame.draw.polygon(self._screen, (64, 65, 68), (
                (self._SIZE_X + self._MARGIN + 70, 445),
                (self._SIZE_X + self._MARGIN + 155, 575),
                (self._SIZE_X + self._MARGIN + 230, 445),
                (self._SIZE_X + self._MARGIN + 155, 393)))

        elif to_hide == 2:
            pygame.draw.rect(self._screen, (64, 65, 68),
                             (self._MARGIN + self._SIZE_X + 20, self._MARGIN + 400, 160, 195))
            pygame.draw.rect(self._screen, (64, 65, 68),
                             (self._MARGIN + self._SIZE_X + 175, self._MARGIN + 400, 30, 100))
        elif to_hide == 3:
            pygame.draw.rect(self._screen, (64, 65, 68),
                             (self._MARGIN + self._SIZE_X + 20, self._MARGIN + 400, 270, 200))
