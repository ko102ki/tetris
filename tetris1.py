from random import randint
from pprint import pprint
import pygame

class Block:
    def __init__(self):
        self.loc = [[], []]
        self.loc[0] = 4  # X座標
        self.loc[1] = 0  # Y座標
    def rtn_loc(self):
        return self.loc


class Mino:
    # クラス変数（文頭のアンダースコアで外部から参照不可）
    _i = \
    [[0, 0, 0, 0],
     [1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0],]

    _o = \
    [[2, 2],
     [2, 2],]

    _s = \
    [[0, 3, 3],
     [3, 3, 0],
     [0, 0, 0],]

    _z = \
    [[4, 4, 0],
     [0, 4, 4],
     [0, 0, 0],]

    _j = \
    [[5, 0, 0],
     [5, 5, 5],
     [0, 0, 0],]

    _l = \
    [[0, 0, 6],
     [6, 6, 6],
     [0, 0, 0],]

    _t = \
    [[0, 7, 0],
     [7, 7, 7],
     [0, 0, 0],]

    def create(self):
        self.index = randint(0, 6)
        if self.index == 0:
            return Mino._i
        if self.index == 1:
            return Mino._o
        if self.index == 2:
            return Mino._s
        if self.index == 3:
            return Mino._z
        if self.index == 4:
            return Mino._j
        if self.index == 5:
            return Mino._l
        if self.index == 6:
            return Mino._t

    def rotate(self, mino):
        for y in range(len(mino)):
            for x in range(len(mino)):
                self.mino_copy[y][x] = mino[y][x]
        return self.mino_copy

class Window:
    field =[[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0],
            [99, 99, 99,  0,  0,  0,  0,  0,  0, 99, 99,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99],
            [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,  99],
            ]

    def __init__(self):
        pygame.init()
        screen_size = (288, 552)
        screen = pygame.display.set_mode(screen_size)
        block_img = Window.load_image(self)
#        Window.mapping(self)
        Window.draw(self, screen, block_img)


    def mapping(self, mino, loc):
        self.loc_x = loc[0]
        self.loc_y = loc[1]
        self.mino_len = len(mino)
        self.end_x = self.loc_x + self.mino_len
        self.end_y = self.loc_y + self.mino_len

        for y in range(self.loc_y, self.end_y):
            for x in range(self.loc_x, self.end_x):
                self.mino_x = x - self.loc_x
                self.mino_y = y - self.loc_y
                Window.field[y][x] = mino[self.mino_y][self.mino_x]
        return Window.field

    def draw(self, screen, block_img):
        screen.fill((0, 0, 0))
        for y in range(23):
            for x in range(12):
                code = Window.field[y][x]
                if code == 99:
                    screen.blit(block_img[7], (x * 24, y * 24))
                elif code == 1 or code == 11:
                    screen.blit(block_img[0], (x * 24, y * 24))
                elif code == 2 or code == 12:
                    screen.blit(block_img[1], (x * 24, y * 24))
                elif code == 3 or code == 13:
                    screen.blit(block_img[2], (x * 24, y * 24))
                elif code == 4 or code == 14:
                    screen.blit(block_img[3], (x * 24, y * 24))
                elif code == 5 or code == 15:
                    screen.blit(block_img[4], (x * 24, y * 24))
                elif code == 6 or code == 16:
                    screen.blit(block_img[5], (x * 24, y * 24))
                elif code == 7 or code == 17:
                    screen.blit(block_img[6], (x * 24, y * 24))
        pygame.display.update()

    def load_image(self):
        self.block_img = [[], [], [], [], [], [], [], []]
        self.block_img[0] = pygame.image.load('data/i.bmp')
        self.block_img[1] = pygame.image.load('data/o.bmp')
        self.block_img[2] = pygame.image.load('data/s.bmp')
        self.block_img[3] = pygame.image.load('data/z.bmp')
        self.block_img[4] = pygame.image.load('data/j.bmp')
        self.block_img[5] = pygame.image.load('data/l.bmp')
        self.block_img[6] = pygame.image.load('data/t.bmp')
        self.block_img[7] = pygame.image.load('data/w.bmp')
        return self.block_img

class Player:

    def mino_control(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_z:
                    Mino.rotate(self, mino)

loc = Block().rtn_loc()
mino = Mino().create()
window = Window()
window.mapping(mino, loc)
print(loc)
print(mino)
print(window.block_img)
