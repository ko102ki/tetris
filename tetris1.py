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
        self.loc = [4, 0] #  ミノの配列の[0][0]の座標 [x, y]
        self.state = [0, 0] # [今の状態, 移行したい状態]

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
        pattern_len = len(self.pattern)
        pattern_copy = [[0 for col in range(pattern_len)] for row in range(pattern_len)]
        if direct == 'left':
            for y in range(pattern_len):
                for x in range(pattern_len):
                    pattern_copy[pattern_len - 1 - x][y] = self.pattern[y][x]
            self.state[1] -= 1
            self.state[1] %= 4
        if direct == 'right':
            for y in range(pattern_len):
                for x in range(pattern_len):
                    pattern_copy[x][pattern_len - 1 - y] = self.pattern[y][x]
            self.state[1] += 1
            self.state[1] %= 4
        for y in range(pattern_len):
            for x in range(pattern_len):
                self.pattern[y][x] = pattern_copy[y][x]

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
        self.shift_loc = [0, 0]

    def mapping(self, pattern, loc, process):
#        loc[0] = loc[0] + self.shift_loc[0]
#        loc[1] = loc[1] + self.shift_loc[1]
        field_x = loc[0]
        field_y = loc[1]
#        field_x = loc[0] + self.shift_loc[0]
#        field_y = loc[1] + self.shift_loc[1]
        pattern_len = len(pattern)
        end_x = field_x + pattern_len
        end_y = field_y + pattern_len

        if process == 'line_clear':
            for y in self.lines:
                del self._field[y]
            for y in self.lines:
                self._field.insert(2, [99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  99])
            return 0

        for y in range(field_y, end_y):
            for x in range(field_x, end_x):
                pattern_x = x - field_x
                pattern_y = y - field_y
                code = pattern[pattern_y][pattern_x] #  patternリストの中を左上から横方向に走査
#                if code:
#                    if process == 'drop':
#                        Window._field[y + self.shift_loc[1]][x + self.shift_loc[0]] = code
#                    elif process == 'clear':
#                        Window._field[y + self.shift_loc[1]][x + self.shift_loc[0]] = 0
##                        Window._field[y][x] = 0
#                    elif process == 'fix':
#                        Window._field[y + self.shift_loc[1]][x + self.shift_loc[0]] = code + 10
##                        Window._field[y][x] = code + 10
                if code:
                    if process == 'drop':
                        Window._field[y][x] = code
                    elif process == 'clear':
                        Window._field[y][x] = 0
                    #                        Window._field[y][x] = 0
                    elif process == 'fix':
                        Window._field[y][x] = code + 10
                    #                        Window._field[y][x] = code + 10

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
        pattern_len = len(pattern)
        for x in range(pattern_len):
            for y in range(pattern_len):
                if pattern[y][x]:
                    field_x = loc[0] + x
                    field_y = loc[1] + y
                    if self._field[field_y][field_x - 1] > 10:
                        return True
        return False

    def right_hit(self, pattern, loc):
        pattern_len = len(pattern)
        for x in range(pattern_len - 1, -1, -1):
            for y in range(pattern_len):
                if pattern[y][x]:
                    field_x = loc[0] + x
                    field_y = loc[1] + y
                    if self._field[field_y][field_x + 1] > 10:
                        return True
        return False

    def bottom_hit(self, pattern, loc):
        pattern_len = len(pattern)
        for y in range(pattern_len - 1, -1, -1):
            for x in range(pattern_len):
                if pattern[y][x]:
                    field_x = loc[0] + x
                    field_y = loc[1] + y
                    if self._field[field_y + 1][field_x] > 10:
                        return True
        return False

#    def rotate_hit(self, pattern, loc, state):
    def rotate_hit(self, mino):
        if mino.state == [0, 1]:
            shift_list = [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
        if mino.state == [1, 2]:
            shift_list = [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]]
        if mino.state == [2, 3]:
            shift_list = [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]]
        if mino.state == [3, 0]:
            shift_list = [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]]
        if mino.state == [0, 3]:
            shift_list = [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]]
        if mino.state == [3, 2]:
            shift_list = [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]]
        if mino.state == [2, 1]:
            shift_list = [[0, 0], [-1, -1], [-1, -1], [0, 2], [-1, 2]]
        if mino.state == [1, 0]:
            shift_list = [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]]

        pattern_len = len(mino.pattern)
        collision_list = []

        for shift_axis in shift_list:
            for y in range(pattern_len):
                for x in range(pattern_len):
                    if mino.pattern[y][x]:
                        field_x = mino.loc[0] + x + shift_axis[0]
                        field_y = mino.loc[1] + y + shift_axis[1]
                        if self._field[field_y][field_x] > 10:
                            collision_list.append(99)
                        else:
                            collision_list.append(0)
            if not 99 in collision_list:
                self.shift_loc = shift_axis
                mino.loc[0] += shift_axis[0]
                mino.loc[1] += shift_axis[1]
                mino.state[0] = mino.state[1]
                return False
            collision_list = []
        return True

#            collision_list = []
#                            break
#                if collision_flag:
#                    break
        if 99 in collision_list:
            return True
        else:
            self.shift_loc = shift_axis
            state[0] = state[1]
            return False


#        self.axis = axis
#        state[0] = state[1]
#            return False
#            self.mapping(pattern, loc, 'drop', axis)
#            break


    def line_check(self):
        self.lines = []
        for y in range(21, 2, -1):
            zero_cnt = self._field[y].count(0)
            if zero_cnt == 0:
                self.lines.append(y)
            if zero_cnt == 10:
                break


pygame.init()
screen_size = (288, 552)
screen = pygame.display.set_mode(screen_size)

# インスタンス生成
mino = Mino()
window = Window()
window.mapping(mino.pattern, mino.loc, 'drop')
fixed = False
# キー入力用カウンタ
l_cnt = 0
r_cnt = 0
d_cnt = 0

TIMEREVENT = pygame.USEREVENT
#pygame.time.set_timer(TIMEREVENT, 100)

while True:
    if fixed:
        mino = Mino()
        fixed = False
    window.draw(screen)
    pygame.display.update()

    pygame.event.pump()

    pressed = pygame.key.get_pressed()

    if pressed[K_LEFT]:
        l_cnt += 1
        if l_cnt == 3:
            if not window.left_hit(mino.pattern, mino.loc):
                window.mapping(mino.pattern, mino.loc, 'clear')
                mino.control('left')
                window.mapping(mino.pattern, mino.loc, 'drop')
            l_cnt = 0

    if pressed[K_RIGHT]:
        r_cnt += 1
        if r_cnt == 3:
            if not window.right_hit(mino.pattern, mino.loc):
                window.mapping(mino.pattern, mino.loc, 'clear')
                mino.control('right')
                window.mapping(mino.pattern, mino.loc, 'drop')
            r_cnt = 0

    if pressed[K_DOWN]:
        d_cnt += 1
        if d_cnt == 3:
            if not window.bottom_hit(mino.pattern, mino.loc):
                window.mapping(mino.pattern, mino.loc, 'clear')
                mino.control('down')
                window.mapping(mino.pattern, mino.loc, 'drop')
            else:
                window.mapping(mino.pattern, mino.loc, 'fix')
                window.line_check()
                window.mapping(mino.pattern, mino.loc, 'line_clear')
                fixed = True
            d_cnt = 0

    for event in pygame.event.get():
        if event.type == TIMEREVENT:
            if window.bottom_hit(mino.pattern, mino.loc):
                window.mapping(mino.pattern, mino.loc, 'fix')
                window.line_check()
                window.mapping(mino.pattern, mino.loc, 'line_clear')
                fixed = True
                mino = Mino()
            else:
                window.mapping(mino.pattern, mino.loc, 'clear')
                mino.control('down')
                window.mapping(mino.pattern, mino.loc, 'drop')
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.quit()

            if event.key == K_z:
                window.mapping(mino.pattern, mino.loc, 'clear')
                mino.rotate('left')
#                if window.rotate_hit(mino.pattern, mino.loc, mino.state):
                if window.rotate_hit(mino):
                    mino.rotate('right')
                    window.mapping(mino.pattern, mino.loc, 'drop')
                else:
                    window.mapping(mino.pattern, mino.loc, 'drop')

            if event.key == K_x:
                window.mapping(mino.pattern, mino.loc, 'clear')
                mino.rotate('right')
#                if window.rotate_hit(mino.pattern, mino.loc, mino.state):
                if window.rotate_hit(mino):
                    mino.rotate('left')
                    window.mapping(mino.pattern, mino.loc, 'drop')
                else:
                    window.mapping(mino.pattern, mino.loc, 'drop')

    window.draw(screen)
    pygame.display.update()

