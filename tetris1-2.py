import random
import pygame
import sys
from pygame.locals import *
import copy


class Block:
    next1 = []  # ネクストブロック7種を入れる
    next2 = []  # ネクストブロック7種を入れる

    hold1 = []  # ホールド時にhold2の内容を移す
    hold2 = []  # 落下中のblockのパターンを入れておく

    drop_time = 0

    def __init__(self, process):
        self.create()
        if process == 'drop':
            self.pattern = Block.next1.pop(0)
            Block.next1.append(Block.next2.pop(0))  # next2からnext1へブロック１つを移す
        elif process == 'hold':
            self.pattern = Block.hold1
        self.loc = [6, 0]  # blockのfield配列内での位置を表す[x, y]
        self.state = [0, 0]  # [今の状態, 移行したい状態]

    def create(self):
        if len(Block.next1) == 0:
            # next1 next2ともに空なので両方にappend
            index_list = [1, 2, 3, 4, 5, 6, 7]
            random.shuffle(index_list)
            for i in index_list:
                pattern = self.pattern_create(i)
                Block.next1.append(pattern)
            index_list = [1, 2, 3, 4, 5, 6, 7]
            random.shuffle(index_list)
            for i in index_list:
                pattern = self.pattern_create(i)
                Block.next2.append(pattern)
        elif len(Block.next2) == 0:
            # next2が空なのでnext2にappend
            index_list = [1, 2, 3, 4, 5, 6, 7]
            for i in index_list:
                pattern = self.pattern_create(i)
                Block.next2.append(pattern)

    @staticmethod
    def pattern_create(index):
        if index == 1:  # I
            return ([[0, 0, 0, 0],
                     [1, 1, 1, 1],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0], ])
        if index == 2:  # O
            return ([[2, 2],
                     [2, 2], ])
        if index == 3:  # S
            return ([[0, 3, 3],
                     [3, 3, 0],
                     [0, 0, 0], ])
        if index == 4:  # Z
            return ([[4, 4, 0],
                     [0, 4, 4],
                     [0, 0, 0], ])
        if index == 5:  # J
            return ([[5, 0, 0],
                     [5, 5, 5],
                     [0, 0, 0], ])
        if index == 6:  # 2
            return ([[0, 0, 6],
                     [6, 6, 6],
                     [0, 0, 0], ])
        if index == 7:  # T
            return ([[0, 7, 0],
                     [7, 7, 7],
                     [0, 0, 0], ])

    def rotate(self, direction):
        pattern_len = len(self.pattern)
        pattern_copy = [[0 for col in range(pattern_len)] for row in range(pattern_len)]
        if direction == 'left':
            for y in range(pattern_len):
                for x in range(pattern_len):
                    pattern_copy[pattern_len - 1 - x][y] = self.pattern[y][x]
            self.state[1] -= 1
            self.state[1] %= 4
        if direction == 'right':
            for y in range(pattern_len):
                for x in range(pattern_len):
                    pattern_copy[x][pattern_len - 1 - y] = self.pattern[y][x]
            self.state[1] += 1
            self.state[1] %= 4
        for y in range(pattern_len):
            for x in range(pattern_len):
                self.pattern[y][x] = pattern_copy[y][x]

    def control(self, direction):
        if direction == 'left':
            self.loc[0] -= 1
        if direction == 'right':
            self.loc[0] += 1
        if direction == 'down':
            self.loc[1] += 1

    def held_already(self):
        block_index = 0
        for y in self.pattern:
            for x in y:
                if x != 0:
                    block_index = x
                    break
        if Block.hold2:
            Block.hold1 = Block.hold2
            pattern = self.pattern_create(block_index)
            Block.hold2 = pattern
            return True
        else:
            pattern = self.pattern_create(block_index)
            Block.hold2 = pattern
            return False


class Window:
    _field = [
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99], ]

    _field_height = 25
    _field_width = 16

    def __init__(self):
        self.block_img = []
        self.load_image()
        self.shift_loc = [0, 0]  # 壁蹴り時のシフト幅[x, y]
        self.lines = []  # 消去するライン
        self.score = 0
        self.ren = 0
        self.ren_credit = None
        self.t_spin_credit = None

    def mapping(self, block, process):
        field_x = block.loc[0]
        field_y = block.loc[1]
        pattern_len = len(block.pattern)
        end_x = field_x + pattern_len
        end_y = field_y + pattern_len

        if process == 'line_clear':
            cl_flag = False
            for y in self.lines:
                del Window._field[y]
                cl_flag = True
            for y in range(len(self.lines)):
                Window._field.insert(2, [99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99])
            if cl_flag:
                clear_sound.play()

        if process == 'clear_effect':
            for y in self.lines:
                self._field[y] = [99, 99, 99, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 99, 99, 99]

        for y in range(field_y, end_y):
            for x in range(field_x, end_x):
                pattern_x = x - field_x
                pattern_y = y - field_y
                code = block.pattern[pattern_y][pattern_x]  # patternリストの中を左上から右に向かって走査
                if code:
                    if process == 'drop':
                        Window._field[y][x] = code
                    elif process == 'clear':
                        Window._field[y][x] = 0
                    elif process == 'fix':
                        Window._field[y][x] = code + 10
                    elif process == 'ghost':
                        Window._field[y][x] = -1*code

    def draw(self, screen):
        field_left_margin = cell * 4  # +3が実際の表示領域
        field_top_margin = cell * 1  # +2が実際の表示領域

        next_left_margin = cell * 19
        next_top_margin = cell * 5

        hold_left_margin = cell * 1
        hold_top_margin = cell * 5

        screen.fill((0, 0, 0))
        screen.blit(next_title, (next_left_margin, next_top_margin - cell * 2))
        screen.blit(hold, (hold_left_margin, hold_top_margin - cell * 2))
        screen.blit(score_title, (hold_left_margin, hold_top_margin + cell * 3))
        score_num = game_font.render(str(window_instance.score), True, (255, 255, 255))
        screen.blit(score_num, (hold_left_margin, hold_top_margin + cell * 4))

        # T-spin描画用
        if self.t_spin_credit:
            screen.blit(self.t_spin_credit, (hold_left_margin, hold_top_margin + cell * 7))
        else:
            pass

        # REN描画用
        if self.ren_credit:
            screen.blit(self.ren_credit, (hold_left_margin, hold_top_margin + cell * 6))
        else:
            pass

        # field描画用
        for y in range(2, Window._field_height - 2):
            for x in range(2, Window._field_width - 2):
                code = Window._field[y][x]
                self.blit_img(code, x, y, field_left_margin, field_top_margin)

        # next描画用
        next1_len = len(Block.next1) - 2
        for z in range(next1_len):
            block_len = len(Block.next1[z])
            for y in range(block_len):
                for x in range(block_len):
                    if Block.next1[z][y][x]:
                        code = Block.next1[z][y][x]
                        self.blit_img(code, x, y, next_left_margin, next_top_margin + 96 * z)

        # hold描画用
        for y in range(len(Block.hold2)):
            for x in range(len(Block.hold2)):
                if Block.hold2[y][x]:
                    code = Block.hold2[y][x]
                    self.blit_img(code, x, y, hold_left_margin, hold_top_margin)

    def blit_img(self, code, x, y, left_margin, bottom_margin):
        block_size = 24
        if code == 99:
            screen.blit(self.block_img[7], (left_margin + x * block_size, bottom_margin + y * block_size))
        elif code == 1 or code == 11 or code == -1:
            if code == -1:
                self.block_img[0].set_alpha(100)
                screen.blit(self.block_img[0], (left_margin + x * block_size, bottom_margin + y * block_size))
            else:
                self.block_img[0].set_alpha(255)
                screen.blit(self.block_img[0], (left_margin + x * block_size, bottom_margin + y * block_size))

        elif code == 2 or code == 12 or code == -2:
            if code == -2:
                self.block_img[1].set_alpha(100)
                screen.blit(self.block_img[1], (left_margin + x * block_size, bottom_margin + y * block_size))
            else:
                self.block_img[1].set_alpha(255)
                screen.blit(self.block_img[1], (left_margin + x * block_size, bottom_margin + y * block_size))

        elif code == 3 or code == 13 or code == -3:
            if code == -3:
                self.block_img[2].set_alpha(100)
                screen.blit(self.block_img[2], (left_margin + x * block_size, bottom_margin + y * block_size))
            else:
                self.block_img[2].set_alpha(255)
                screen.blit(self.block_img[2], (left_margin + x * block_size, bottom_margin + y * block_size))

        elif code == 4 or code == 14 or code == -4:
            if code == -4:
                self.block_img[3].set_alpha(100)
                screen.blit(self.block_img[3], (left_margin + x * block_size, bottom_margin + y * block_size))
            else:
                self.block_img[3].set_alpha(255)
                screen.blit(self.block_img[3], (left_margin + x * block_size, bottom_margin + y * block_size))

        elif code == 5 or code == 15 or code == -5:
            if code == -5:
                self.block_img[4].set_alpha(100)
                screen.blit(self.block_img[4], (left_margin + x * block_size, bottom_margin + y * block_size))
            else:
                self.block_img[4].set_alpha(255)
                screen.blit(self.block_img[4], (left_margin + x * block_size, bottom_margin + y * block_size))

        elif code == 6 or code == 16 or code == -6:
            if code == -6:
                self.block_img[5].set_alpha(100)
                screen.blit(self.block_img[5], (left_margin + x * block_size, bottom_margin + y * block_size))
            else:
                self.block_img[5].set_alpha(255)
                screen.blit(self.block_img[5], (left_margin + x * block_size, bottom_margin + y * block_size))

        elif code == 7 or code == 17 or code == -7:
            if code == -7:
                self.block_img[6].set_alpha(100)
                screen.blit(self.block_img[6], (left_margin + x * block_size, bottom_margin + y * block_size))
            else:
                self.block_img[6].set_alpha(255)
                screen.blit(self.block_img[6], (left_margin + x * block_size, bottom_margin + y * block_size))
        elif code == 100:
            screen.blit(self.block_img[8], (left_margin + x * block_size, bottom_margin + y * block_size))

    def load_image(self):
        self.block_img.append(pygame.image.load('data/i.bmp'))
        self.block_img.append(pygame.image.load('data/o.bmp'))
        self.block_img.append(pygame.image.load('data/s.bmp'))
        self.block_img.append(pygame.image.load('data/z.bmp'))
        self.block_img.append(pygame.image.load('data/j.bmp'))
        self.block_img.append(pygame.image.load('data/l.bmp'))
        self.block_img.append(pygame.image.load('data/t.bmp'))
        self.block_img.append(pygame.image.load('data/w.bmp'))
        self.block_img.append(pygame.image.load('data/c.bmp'))

    @staticmethod
    def left_hit(block):
        pattern_len = len(block.pattern)
        for x in range(pattern_len):
            for y in range(pattern_len):
                if block.pattern[y][x]:
                    field_x = block.loc[0] + x
                    field_y = block.loc[1] + y
                    if Window._field[field_y][field_x - 1] > 10:
                        return True
        return False

    @staticmethod
    def right_hit(block):
        pattern_len = len(block.pattern)
        for x in range(pattern_len - 1, -1, -1):
            for y in range(pattern_len):
                if block.pattern[y][x]:
                    field_x = block.loc[0] + x
                    field_y = block.loc[1] + y
                    if Window._field[field_y][field_x + 1] > 10:
                        return True
        return False

    @staticmethod
    def bottom_hit(block, process):
        pattern_len = len(block.pattern)

        if process == 'drop':
            for y in range(pattern_len - 1, -1, -1):
                for x in range(pattern_len):
                    if block.pattern[y][x]:
                        field_x = block.loc[0] + x
                        field_y = block.loc[1] + y
                        if Window._field[field_y + 1][field_x] > 10:
                            return True
            return False

    @staticmethod
    def rotate_hit(block):
        pattern_len = len(block.pattern)
        collision_list = []
        shift_list = []

        if pattern_len == 4:  # Iミノ用
            # 右回転
            if block.state == [0, 1]:
                shift_list = [[0, 0], [-2, 0], [1, 0], [-2, 1], [1, -2]]
            if block.state == [1, 2]:
                shift_list = [[0, 0], [-1, 0], [2, 1], [-1, -2], [2, -1]]
            if block.state == [2, 3]:
                shift_list = [[0, 0], [2, 0], [-1, 0], [2, -1], [-1, 2]]
            if block.state == [3, 0]:
                shift_list = [[0, 0], [1, 0], [-2, 0], [1, 2], [-2, -1]]
            # 左回転
            if block.state == [0, 3]:
                shift_list = [[0, 0], [-1, 0], [2, 0], [-1, -2], [2, 1]]
            if block.state == [3, 2]:
                shift_list = [[0, 0], [-2, 0], [1, 0], [-2, 1], [1, -2]]
            if block.state == [2, 1]:
                shift_list = [[0, 0], [1, 0], [-2, 0], [1, 2], [-2, -1]]
            if block.state == [1, 0]:
                shift_list = [[0, 0], [2, 0], [-1, 0], [2, -1], [-1, 2]]
        else:  # I，O以外のミノ用
            # 右回転
            if block.state == [0, 1]:
                shift_list = [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
            if block.state == [1, 2]:
                shift_list = [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]]
            if block.state == [2, 3]:
                shift_list = [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]]
            if block.state == [3, 0]:
                shift_list = [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]]
            # 左回転
            if block.state == [0, 3]:
                shift_list = [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]]
            if block.state == [3, 2]:
                shift_list = [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]]
            if block.state == [2, 1]:
                shift_list = [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
            if block.state == [1, 0]:
                shift_list = [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]]

        for shift_axis in shift_list:
            for y in range(pattern_len):
                for x in range(pattern_len):
                    if block.pattern[y][x]:
                        field_x = block.loc[0] + x + shift_axis[0]
                        field_y = block.loc[1] + y + shift_axis[1]
                        if Window._field[field_y][field_x] > 10:
                            collision_list.append(99)
                        else:
                            collision_list.append(0)
            if not 99 in collision_list:
                block.loc[0] += shift_axis[0]
                block.loc[1] += shift_axis[1]
                block.state[0] = block.state[1]
#                spin_type = Window.t_spin_check(shift_axis)
                return False
            collision_list = []
        return True

    def t_spin_check(self):
        surrounding_list = []  # Tミノの周囲の要素を入れる
        pattern_len = len(block_instance.pattern)
        for y in range(pattern_len):
            for x in range(pattern_len):
                field_x = block_instance.loc[0] + x
                field_y = block_instance.loc[1] + y
                # Tミノの周囲の要素を調べる
                # Tミノではない要素かつ0でない(空のマスの)要素
                if Window._field[field_y][field_x] != 7 and Window._field[field_y][field_x] != 0:
                    surrounding_list.append(99)
                else:
                    surrounding_list.append(0)
        if surrounding_list.count(99) == 3 or surrounding_list.count(99) == 5:
            return True

            """
        for y in range(3):
            for x in range(3):
                self._field[][]
        block_instance.loc[]

        block_index = 0
        for y in block_instance.pattern:
            for x in y:
                if x != 0:
                    block_index = x
                    break
            if block_index != 0:
                break
        if block_index == 7 and axis != [0, 0]:
            pass
        if Block.hold2:
            Block.hold1 = Block.hold2
            pattern = self.pattern_create(block_index)
            Block.hold2 = pattern
            return True
        else:
            pattern = self.pattern_create(block_index)
            Block.hold2 = pattern
            return False
        pass
            """

    def line_check(self):
        self.lines = []
        for y in range(Window._field_height - 4, 2, -1):
            zero_cnt = Window._field[y].count(0)
            if zero_cnt == 0:
                self.lines.append(y)
            if zero_cnt == 10:
                break

    def hard_drop(self):
        hard_flag = True
        while hard_flag:
            if not window_instance.bottom_hit(block_instance, 'drop'):
                window_instance.mapping(block_instance, 'clear')
                block_instance.control('down')
                # 自分が動かしたマス目分だけスコアに加算
                self.score += 1
            else:
                hard_flag = False
#                window.mapping(mino, 'fix')
#                window.line_check()
#                window.mapping(mino, 'line_clear')
        return True

    @staticmethod
    def g_hard_drop():
        hard_flag = True
        while hard_flag:
            if not window_instance.bottom_hit(ghost, 'drop'):
                window_instance.mapping(ghost, 'clear')
                ghost.control('down')
                window_instance.mapping(ghost, 'ghost')
            else:
                hard_flag = False
                window_instance.mapping(ghost, 'ghost')
        return True

    def score_count(self):
        cleared_lines = len(self.lines)
        score = 0
        if cleared_lines == 1:
            score = 100
        elif cleared_lines == 2:
            score = 300
        elif cleared_lines == 3:
            score = 500
        elif cleared_lines == 4:
            score = 800
        self.score += score

    def ren_count(self):
        if self.ren >= 1:
            self.score += self.ren * 50
            ren_char = str(self.ren) + 'REN'
            self.ren_credit = game_font.render(ren_char, True, (255, 255, 255))


class Ghost:
    def __init__(self):
        self.loc = copy.deepcopy(block_instance.loc)
        self.pattern = copy.deepcopy(block_instance.pattern)

    def update(self):
        self.loc = copy.deepcopy(block_instance.loc)
        self.pattern = copy.deepcopy(block_instance.pattern)

    def control(self, direction):
        if direction == 'left':
            self.loc[0] -= 1
        if direction == 'right':
            self.loc[0] += 1
        if direction == 'down':
            self.loc[1] += 1


# mainループ

# ブロック1つ(1マス)の大きさ
cell = 24

# pygame初期化
pygame.init()
screen_size = (cell * 27, cell * 27)
screen = pygame.display.set_mode(screen_size)

# インスタンス生成
block_instance = Block('drop')
window_instance = Window()
ghost = Ghost()
window_instance.g_hard_drop()
window_instance.mapping(block_instance, 'drop')

# フォント準備
sys_font = pygame.font.SysFont(None, 100)
game_font = pygame.font.SysFont(None, 40)
title1 = sys_font.render('Space to', True, (255, 255, 255))
title2 = sys_font.render('Start!', True, (255, 255, 255))
score_title = game_font.render('SCORE', True, (255, 255, 255))
hold = game_font.render('HOLD', True, (255, 255, 255))
next_title = game_font.render('NEXT', True, (255, 255, 255))

# キー入力用カウンタ
left_count = 0
right_count = 0
down_count = 0
down_threshold = 4
side_threshold = 5
# pygame.key.set_repeat(70, 10)

# Timer
clock = pygame.time.Clock()

# BGM
pygame.mixer.music.load('data/bgm01_intro.ogg')
# pygame.mixer.music.set_volume(1)

# サウンドの読み込み
fix_sound = pygame.mixer.Sound('data/fix.wav')
hard_sound = pygame.mixer.Sound('data/hard.wav')
rotate_sound = pygame.mixer.Sound('data/rotate.wav')
hold_sound = pygame.mixer.Sound('data/hold.wav')
clear_sound = pygame.mixer.Sound('data/clear.wav')
# control_sound = pygame.mixer.Sound('data/control.wav')

# Flag
start = False
fixed = False
holdable = True
fixing = False
ren_flag = False
t_spin_flag = False
drop_time = 0
fix_time = 0

#  ゲームループ
while True:

    time_passed = clock.tick_busy_loop(60)

    while not start:
        screen.blit(title1, (120, 150))
        screen.blit(title2, (120, 250))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    start = True
#                    pygame.mixer.music.play(1)

#    if not pygame.mixer.music.get_busy():
#        pygame.mixer.music.load('data/bgm01.ogg')
#        pygame.mixer.music.play(-1)
    if fixed:
        block_instance = Block('drop')
        ghost = Ghost()
        window_instance.g_hard_drop()
        window_instance.mapping(block_instance, 'drop')
        fixed = False

    window_instance.draw(screen)
    pygame.display.update()

    # 自由落下
    if drop_time >= 1000:
        if not window_instance.bottom_hit(block_instance, 'drop'):
            window_instance.mapping(block_instance, 'clear')
            block_instance.control('down')
            ghost.update()
            window_instance.g_hard_drop()
            window_instance.mapping(block_instance, 'drop')
        else:
            fixing = True
        drop_time = 0
    drop_time += time_passed
    # 自由落下ここまで

    pressed = pygame.key.get_pressed()
    if pressed[K_DOWN]:
        down_count += 1
        if down_count >= down_threshold:
            if not window_instance.bottom_hit(block_instance, 'drop'):
                window_instance.mapping(block_instance, 'clear')
                block_instance.control('down')
                # 自分が動かしたマス目分だけスコアに加算
                window_instance.score += 1
                ghost.update()
                window_instance.g_hard_drop()
                window_instance.mapping(block_instance, 'drop')
            else:
                fixing = True
            down_count = 0

    if pressed[K_LEFT]:
        left_count += 1
        if left_count >= side_threshold:
            if not window_instance.left_hit(block_instance):
                window_instance.mapping(block_instance, 'clear')
                block_instance.control('left')
                window_instance.mapping(ghost, 'clear')
                ghost.update()
                window_instance.g_hard_drop()
                window_instance.mapping(block_instance, 'drop')
            left_count = 0

    if pressed[K_RIGHT]:
        right_count += 1
        if right_count >= side_threshold:
            if not window_instance.right_hit(block_instance):
                window_instance.mapping(block_instance, 'clear')
                block_instance.control('right')
                window_instance.mapping(ghost, 'clear')
                ghost.update()
                window_instance.g_hard_drop()
                window_instance.mapping(block_instance, 'drop')
            right_count = 0

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()

            if event.key == K_z:
                rotate_sound.play()
                window_instance.mapping(block_instance, 'clear')
                window_instance.mapping(ghost, 'clear')
                block_instance.rotate('left')
                if window_instance.rotate_hit(block_instance):
                    block_instance.rotate('right')
                else:
                    fix_time = 0
                ghost.update()
                window_instance.g_hard_drop()
                window_instance.mapping(block_instance, 'drop')

            if event.key == K_x:
                rotate_sound.play()
                window_instance.mapping(block_instance, 'clear')
                window_instance.mapping(ghost, 'clear')
                block_instance.rotate('right')
                if window_instance.rotate_hit(block_instance):
                    block_instance.rotate('left')
                else:
                    fix_time = 0
                ghost.update()
                window_instance.g_hard_drop()
                window_instance.mapping(block_instance, 'drop')

            if event.key == K_LSHIFT:
                if holdable:
                    hold_sound.play()
                    window_instance.mapping(block_instance, 'clear')
                    window_instance.mapping(ghost, 'clear')
                    if block_instance.held_already():
                        block_instance = Block('hold')
                    else:
                        block_instance = Block('drop')
                    holdable = False
                    ghost.update()
                    window_instance.g_hard_drop()
                    window_instance.mapping(block_instance, 'drop')

            if event.key == K_UP:
                hard_sound.play()
                if window_instance.hard_drop():
                    fixing = True
                    fix_time = 500

    # 固定処理 フラグがTrueのときだけ行う．0.5秒経ったら固定
    if fixing:
        if fix_time >= 500:
            if not window_instance.bottom_hit(block_instance, 'drop'):
                fix_time = 0
            else:
                # T-spin判定
                block_index = 0
                for y in block_instance.pattern:
                    for x in y:
                        if x != 0:
                            block_index = x
                            break
                    if block_index != 0:
                        break
                if block_index == 7:
                    t_spin_flag = window_instance.t_spin_check()


                window_instance.mapping(block_instance, 'fix')
                window_instance.line_check()

                # 固定音処理
                fix_sound.play()

                # 固定描画処理
                if window_instance.lines:
                    if t_spin_flag:
                        t_spin_str = 'T-Spin' + str(len(window_instance.lines))
                        window_instance.t_spin_credit = game_font.render(t_spin_str, True, (255, 255, 255))
                        t_spin_flag = False

                    window_instance.score_count()
                    window_instance.mapping(block_instance, 'clear_effect')
                    window_instance.draw(screen)
                    pygame.display.update()
                    pygame.time.wait(500)
                    window_instance.mapping(block_instance, 'line_clear')
                    if not ren_flag:
                        ren_flag = True
                    elif ren_flag:
                        window_instance.ren += 1
                elif not window_instance.lines and ren_flag:
                    ren_flag = False
                    window_instance.ren = 0
                    window_instance.ren_credit = None
                else:
                    window_instance.t_spin_credit = None
                window_instance.ren_count()
                fixed = True
                holdable = True
                fixing = False
                fix_time = 0
        fix_time += time_passed
    # 固定処理ここまで



