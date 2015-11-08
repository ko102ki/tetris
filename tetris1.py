from random import randint
from pprint import pprint
import pygame
import sys
from pygame.locals import *


class Mino:
    # クラス変数（文頭のアンダースコアで外部から参照不可）
    _i = [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],]

    _o = [
        [2, 2],
        [2, 2],]

    _s = [
        [0, 3, 3],
        [3, 3, 0],
        [0, 0, 0],]

    _z = [
        [4, 4, 0],
        [0, 4, 4],
        [0, 0, 0],]

    _j = [
        [5, 0, 0],
        [5, 5, 5],
        [0, 0, 0],]

    _l = [
        [0, 0, 6],
        [6, 6, 6],
        [0, 0, 0],]

    _t = [
        [0, 7, 0],
        [7, 7, 7],
        [0, 0, 0],]

    def __init__(self):
        self.pattern = self.create()
        self.loc = [4, 0] #  [x, y]

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

    def rotate(self, direct):
        plen = len(self.pattern)
        pcopy = [[0 for col in range(plen)] for row in range(plen)]
        if direct == 'left':
            for y in range(plen):
                for x in range(plen):
                    pcopy[plen - 1 - x][y] = self.pattern[y][x]
        if direct == 'right':
            for y in range(plen):
                for x in range(plen):
                    pcopy[x][plen - 1 - y] = self.pattern[y][x]
        for y in range(plen):
            for x in range(plen):
                self.pattern[y][x] = pcopy[y][x]

    def control(self, direct):
        if direct == 'left':
            self.loc[0] -= 1
        if direct == 'right':
            self.loc[0] += 1
        if direct == 'down':
            self.loc[1] += 1


class Window:
    _field =[
            [99, 99, 99,  0,  0,  0,  0,  0,  0, 99, 99,  99],
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
            [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,  99],]

    def __init__(self):
        self.load_image()

    def mapping(self, pattern, loc, process):
        loc_x = loc[0]
        loc_y = loc[1]
        plen = len(pattern)
        end_x = loc_x + plen
        end_y = loc_y + plen

        if process == 'lclear':
            for y in self.lines:
                del self._field[y]
            for y in self.lines:
                self._field.insert(2, [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99])
            return 0

        for y in range(loc_y, end_y):
            for x in range(loc_x, end_x):
                px = x - loc_x
                py = y - loc_y
                code = pattern[py][px]
                if code:
                    if process == 'drop':
                        Window._field[y][x] = code
                    elif process == 'clear':
                        Window._field[y][x] = 0
                    elif process == 'fix':
                        Window._field[y][x] = code + 10

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for y in range(23):
            for x in range(12):
                code = Window._field[y][x]
                if code == 99:
                    screen.blit(self.block_img[7], (x * 24, y * 24))
                elif code == 1 or code == 11:
                    screen.blit(self.block_img[0], (x * 24, y * 24))
                elif code == 2 or code == 12:
                    screen.blit(self.block_img[1], (x * 24, y * 24))
                elif code == 3 or code == 13:
                    screen.blit(self.block_img[2], (x * 24, y * 24))
                elif code == 4 or code == 14:
                    screen.blit(self.block_img[3], (x * 24, y * 24))
                elif code == 5 or code == 15:
                    screen.blit(self.block_img[4], (x * 24, y * 24))
                elif code == 6 or code == 16:
                    screen.blit(self.block_img[5], (x * 24, y * 24))
                elif code == 7 or code == 17:
                    screen.blit(self.block_img[6], (x * 24, y * 24))

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

    def left_hit(self, pattern, loc):
        plen = len(pattern)
        for x in range(plen):
            for y in range(plen):
                if pattern[y][x]:
                    fx = loc[0] + x
                    fy = loc[1] + y
                    if self._field[fy][fx - 1] > 10:
                        return True
        return False

    def right_hit(self, pattern, loc):
        plen = len(pattern)
        for x in range(plen - 1, -1, -1):
            for y in range(plen):
                if pattern[y][x]:
                    fx = loc[0] + x
                    fy = loc[1] + y
                    if self._field[fy][fx + 1] > 10:
                        return True
        return False

    def bottom_hit(self, pattern, loc):
        plen = len(pattern)
        for y in range(plen - 1, -1, -1):
            for x in range(plen):
                if pattern[y][x]:
                    fx = loc[0] + x
                    fy = loc[1] + y
                    if self._field[fy + 1][fx] > 10:
                        return True
        return False

    def rotate_hit(self, pattern, loc):
        plen = len(pattern)
#        pcopy = [[0 for col in range(plen)] for row in range(plen)]
        revise = 0
#        for y in range(plen):
#            for x in range(plen):
#                pcopy[y][x] = pattern[y][x]

#        mino.rotate(direct, pattern)

        for y in range(plen):
            for x in range(plen):
                if pattern[y][x]:
                    fx = loc[0] + x + revise
                    fy = loc[1] + y
                    if self._field[fy][fx] > 10:
                        return True
        return False

    def line_check(self):
        self.lines = []
        for y in range(21, 2, -1):
            zero_cnt = self._field[y].count(0)
            if zero_cnt == 0:
                self.lines.append(y)
            if zero_cnt == 10:
                break
#        print(lines)



class Player:

    def mino_control(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_z:
                    loc[1] += 1

#loc = Block().rtn_loc()
pygame.init()
screen_size = (288, 552)
screen = pygame.display.set_mode(screen_size)

#インスタンス生成
mino = Mino()
window = Window()
window.mapping(mino.pattern, mino.loc, 'drop')

fixed = False

lcnt = 0
rcnt = 0
dcnt = 0

while True:
#    if fixed:
#        mino = Mino()
#        fixed = False

    window.draw(screen)
    pygame.display.update()

    pygame.event.pump()

    pressed = pygame.key.get_pressed()

    if pressed[K_LEFT]:
        lcnt += 1
        if lcnt == 100:
            if window.left_hit(mino.pattern, mino.loc):
                pass
            else:
                window.mapping(mino.pattern, mino.loc, 'clear')
                mino.control('left')
                window.mapping(mino.pattern, mino.loc, 'drop')
            lcnt = 0

    if pressed[K_RIGHT]:
        rcnt += 1
        if rcnt == 100:
            if window.right_hit(mino.pattern, mino.loc):
                pass
            else:
                window.mapping(mino.pattern, mino.loc, 'clear')
                mino.control('right')
                window.mapping(mino.pattern, mino.loc, 'drop')
            rcnt = 0

    if pressed[K_DOWN]:
        dcnt += 1
        if dcnt == 95:
            if window.bottom_hit(mino.pattern, mino.loc):
                window.mapping(mino.pattern, mino.loc, 'fix')
                window.line_check()
                window.mapping(mino.pattern, mino.loc, 'lclear')
                fixed = True
                mino = Mino()
            else:
                window.mapping(mino.pattern, mino.loc, 'clear')
                mino.control('down')
                window.mapping(mino.pattern, mino.loc, 'drop')
            dcnt = 0

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.quit()

#            if event.key == K_LEFT:
#                if window.left_hit(mino.pattern, mino.loc):
#                    break
#                else:
#                    window.mapping(mino.pattern, mino.loc, 'clear')
#                    mino.control('left')
#                    window.mapping(mino.pattern, mino.loc, 'drop')
#
#            if event.key == K_RIGHT:
#                if window.right_hit(mino.pattern, mino.loc):
#                    break
#                else:
#                    window.mapping(mino.pattern, mino.loc, 'clear')
#                    mino.control('right')
#                    window.mapping(mino.pattern, mino.loc, 'drop')

#            if event.key == K_DOWN:
#                if window.bottom_hit(mino.pattern, mino.loc):
#                    window.mapping(mino.pattern, mino.loc, 'fix')
#                    window.line_check()
#                    window.mapping(mino.pattern, mino.loc, 'lclear')
#                    fixed = True
#                    break
#                else:
#                    window.mapping(mino.pattern, mino.loc, 'clear')
#                    mino.control('down')
#                    window.mapping(mino.pattern, mino.loc, 'drop')

            if event.key == K_z:
                window.mapping(mino.pattern, mino.loc, 'clear')
                mino.rotate('left')
                if window.rotate_hit(mino.pattern, mino.loc):
                    mino.rotate('right')
                    window.mapping(mino.pattern, mino.loc, 'drop')
                    break
                else:
                    window.mapping(mino.pattern, mino.loc, 'drop')

            if event.key == K_x:
                window.mapping(mino.pattern, mino.loc, 'clear')
                mino.rotate('right')
                if window.rotate_hit(mino.pattern, mino.loc):
                    mino.rotate('left')
                    window.mapping(mino.pattern, mino.loc, 'drop')
                    break
                else:
                    window.mapping(mino.pattern, mino.loc, 'drop')

    pygame.display.update()
#mino = Mino().create()
#window = Window()
#window.mapping(mino, loc)
#
#print(loc)
#print(mino)
#print(window.self.block_img)

