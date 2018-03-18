import pygame
import os
import music


class Playground:

    def __init__(self, scr, boardWidth, boardHeight, ratio, margin):
        self._ratio = ratio
        self._screen = scr
        self._boardWidth = boardWidth
        self._boardHeight = boardHeight
        self._margin = margin
        self._size_x = self._ratio * self._boardWidth
        self._size_y = self._ratio * self._boardHeight
        self._board = [[0 for ii in range(self._boardWidth)] for jj in range(self._boardHeight)]
        self._background, self._background_rect = self.get_photo("Background.png", 300, 600)

    def on_intro(self):

        if os.name == "nt":
            image_dir = os.path.join(os.path.dirname(__file__), 'graphics', 'Intro.png').replace("/", "\\")
        elif os.name == "posix":
            image_dir = os.path.join(os.path.dirname(__file__), 'graphics', 'Intro.png').replace("\\", "/")
        else:
            image_dir = os.path.join(os.path.dirname(__file__), 'graphics', 'Intro.png')

        picture = pygame.image.load(image_dir).convert()
        picture_rect = picture.get_rect()
        picture = pygame.transform.scale(picture, (640, 640))

        self._screen.blit(picture, picture_rect)
        pygame.display.update()

    def draw_once(self):
        left_margin, left_margin_rect = self.get_photo("Left_margin.png", 20, 600)  # (0, 20)
        right_margin, right_margin_rect = self.get_photo("Right_margin.png", 20, 600)  # (640, 20)
        upper_margin, upper_margin_rect = self.get_photo("Upper_margin.png", 640, 20)  # (0, 0)
        lower_margin, lower_margin_rect = self.get_photo("Lower_margin.png", 640, 20)  # (0, 620)

        self._screen.blit(left_margin, (left_margin_rect[0], left_margin_rect[1] + 20))
        self._screen.blit(right_margin, (right_margin_rect[0] + 620, right_margin_rect[1] + 20))
        self._screen.blit(upper_margin, upper_margin_rect)
        self._screen.blit(lower_margin, (lower_margin_rect[0], lower_margin_rect[1] + 620))

    def draw_playground(self):
        self._screen.blit(self._background, (self._background_rect[0] + 20, self._background_rect[1] + 20))

        for i in range(self._boardHeight):
            for j in range(self._boardWidth):
                if self._board[i][j] != 0:
                    self.draw_box(i, j, self._board[i][j])

    def draw_box(self, y, x, bl_id):
        size_x = self._margin + self._ratio * x
        size_y = self._margin + self._ratio * y

        BLACK = (0, 0, 0)
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
            (size_x + 6, size_y + 6), (size_x + 9, size_y + 21), (size_x + 24, size_y + 24), (size_x + 6, size_y + 24)))

        pygame.draw.rect(self._screen, BLACK, (size_x, size_y, self._ratio, self._ratio), 2)

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

    def draw_falling(self, piece):
        if piece is not None:
            for ii in range(4):
                for jj in range(4):
                    if piece.rot[ii][jj] != 0 and piece.vertical + ii + 1 > 0:
                        self.draw_box(piece.vertical + ii, piece.horizontal + jj, piece.rot[ii][jj])

    def rotate_tetromino(self, piece):
        if self.is_in_valid_position(piece, adjRot=1):
            piece.rotate(1)

    def move_side_tetromino(self, piece, side):   # side is left = -1 or right = 1
        if piece.vertical + 4 < 0:
            return
        if self.is_in_valid_position(piece, adjHor=side):
            piece.move_sides(side)

    def move_down_tetromino(self, piece):
        if self.is_in_valid_position(piece, adjVert=1):
            piece.move_down()

    def dropdown(self, piece):
        while(self.is_in_valid_position(piece, adjVert=1)):
            piece.move_down()

    @staticmethod
    def refall(piece1):
        piece1.vertical = -5
        piece1.horizontal = 3

    def add_tetromino(self, piece):  # if cannot add to _board return False
        for x in range(len(piece.rot)):
            for y in range(len(piece.rot[x])):
                if piece.rot[x][y] != 0 and x + piece.vertical >= 0:
                    self._board[x + piece.vertical][y + piece.horizontal] = piece.rot[x][y]  # add when stopped

    def is_in_valid_position(self, piece, adjRot=0, adjVert=0, adjHor=0):
        # Return True if in valid, False if collides / is out of bounds
        piece.rotate(adjRot)

        for x in range(len(piece.rot)):
            for y in range(len(piece.rot[x])):
                is_above_playground = (x + piece.vertical + adjVert <= 0) and (0 <= (y + piece.horizontal + adjHor) < 10)
                if is_above_playground or piece.rot[x][y] == 0:  # blank spot in template
                    continue
                if not self.is_on_playground(piece, x, y, adjVert, adjHor):  # passes side or bottom
                    piece.rotate(-adjRot)  # back to initial position
                    return False
                if self._board[x + piece.vertical + adjVert] \
                             [y + piece.horizontal + adjHor] != 0:  # not blank in template and on _board

                    piece.rotate(-adjRot)
                    return False
        piece.rotate(-adjRot)
        return True

    @staticmethod
    def is_on_playground(piece, x, y, adjVert, adjHor):

        return((x + piece.vertical + adjVert) < 20 and
               0 <= (y + piece.horizontal + adjHor) < 10)

    def delete_full_lines(self, score, lvl):
        # Counting from top - we evade missing consecutive full lines

        combo = 0                  # overal number of deleted lines in this version - max 4, which is tetris move
        for row in range(len(self._board)):
            if self._board[row].count(0) == 0:
                combo += 1
                music.Music.cleared_line_sound()
                # droping down rest of _board
                for drop in range(row, -1, -1):
                    if drop - 1 < 0:
                        self._board[drop] = [0 for i in range(len(self._board[drop]))]
                    else:
                        self._board[drop] = self._board[drop - 1]

        if combo == 1:
            score = score + 40 + lvl
        elif combo == 2:
            score = score + 100 + lvl
        elif combo == 3:
            score = score + 160 + lvl
        elif combo == 4:
            score = score + 250 + lvl

        return score

    @staticmethod
    def calc_lvl_and_fall_speed(score):

        lvl = int(score / 100) + 1
        move_down_speed = 0.3 - (lvl * 0.001)
        return lvl, move_down_speed
