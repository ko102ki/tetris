import random
import pygame
import sys
from pygame.locals import *
import copy

LEFT = 0
RIGHT = 1
DOWN = 2

DROP = 0
CLEAR = 1
FIX = 2
GHOST = 3

TITLE = 0
PLAY = 1

# ブロック1つ(1マス)の大きさ
CELL = 24

class Block:

    drop_time = 0

    def __init__(self):
        self.next = []  # ネクストブロック7種を入れる
        self.next_spare = []  # ネクストブロック7種を入れる
        self.hold_now = []  # ホールド時に落下中のblockのパターンを入れておく
        self.hold_temp = []  # ホールド時にhold_nowの内容を移す

    def pop_block(self):
        self.pattern = self.next.pop(0)
        self.next.append(self.next_spare.pop())
        self.create_next()
        self.location = [6, 0]  # blockのfield配列内での位置を表す[x, y]
        self.state = [0, 0]  # [今の状態, 移行したい状態]

    def hold(self):
        if not field_instance.hold:
            field_instance.mapping(self, CLEAR)
            field_instance.mapping(ghost_instance, CLEAR)
            if self.hold_now:
                self.hold_temp = self.hold_now
                self.hold_now = self.pattern_create(self.return_now_pattern())
                self.pattern = self.hold_temp
                self.location = [6, 0]  # blockのfield配列内での位置を表す[x, y]
                self.state = [0, 0]  # [今の状態, 移行したい状態]
            else:
                self.hold_now = self.pattern_create(self.return_now_pattern())
                self.pop_block()
            ghost_instance.update()
            field_instance.ghost_mapping()
            field_instance.hold = True
            sound_instance.hold_sound.play()

    def return_now_pattern(self):
        for y in self.pattern:
            for x in y:
                if x != 0: return x
        return 0

    def create_next(self):
        def append_next(list):
            index_list = [1, 2, 3, 4, 5, 6, 7]
            random.shuffle(index_list)
            for i in index_list:
                list.append(self.pattern_create(i))
        if len(self.next) == 0:
            append_next(self.next)
            append_next(self.next_spare)
        elif len(self.next_spare) == 0:
            append_next(self.next_spare)

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

    def control(self, direction):
        if direction == LEFT: self.location[0] -= 1
        if direction == RIGHT: self.location[0] += 1
        if direction == DOWN: self.location[1] += 1

    def rotate(self, direction):
        pattern_len = len(self.pattern)
        pattern_copy = [[0 for col in range(pattern_len)] for row in range(pattern_len)]
        if direction == LEFT:
            for y in range(pattern_len):
                for x in range(pattern_len):
                    pattern_copy[pattern_len - 1 - x][y] = self.pattern[y][x]
            self.state[1] -= 1
            self.state[1] %= 4
        if direction == RIGHT:
            for y in range(pattern_len):
                for x in range(pattern_len):
                    pattern_copy[x][pattern_len - 1 - y] = self.pattern[y][x]
            self.state[1] += 1
            self.state[1] %= 4
        for y in range(pattern_len):
            for x in range(pattern_len):
                self.pattern[y][x] = pattern_copy[y][x]
        # 回転時のブロックの位置「location」を記憶
        self.store_location = self.location


class Field:

    field_height = 25
    field_width = 16

    def __init__(self):
        self.field = [
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

        self.shift_loc = [0, 0]  # 壁蹴り時のシフト幅[x, y]
        self.clear_lines = []  # 消去するライン
        # 自由落下用変数
        self.fall_interval = 1000
        self.fall_time_sum = 0

        # 固定時間設定用変数
        self.fix_time_sum = 0
        self.time_to_fix = 1000

        # 固定用フラグ
        self.fixed = False

        # hold用フラグ
        self.hold = False

        # T-Spin用フラグ
        self.t_spin_flag = False

        # スコア計算用変数
        self.score = 0

        # REN用変数,Flag
        self.ren = 0
        self.ren_flag = False

        # ラインクリア用フラグ
        self.line_clear_flag = False

        self.ren_credit = None
        self.t_spin_credit = None

    def mapping(self, block, process):
        field_x = block.location[0]
        field_y = block.location[1]
        pattern_len = len(block.pattern)
        end_x = field_x + pattern_len
        end_y = field_y + pattern_len
        for y in range(field_y, end_y):
            for x in range(field_x, end_x):
                pattern_x = x - field_x
                pattern_y = y - field_y
                code = block.pattern[pattern_y][pattern_x]  # patternリストの中を左上から右に向かって走査
                if code:
                    if process == DROP: self.field[y][x] = code
                    elif process == CLEAR: self.field[y][x] = 0
                    elif process == FIX: self.field[y][x] = code + 10
                    elif process == GHOST: self.field[y][x] = -1 * code

    def left_hit(self, block):
        pattern_len = len(block.pattern)
        for x in range(pattern_len):
            for y in range(pattern_len):
                if block.pattern[y][x]:
                    field_x = block.location[0] + x
                    field_y = block.location[1] + y
                    if self.field[field_y][field_x - 1] > 10: return True
        return False

    def right_hit(self, block):
        pattern_len = len(block.pattern)
        for x in range(pattern_len - 1, -1, -1):
            for y in range(pattern_len):
                if block.pattern[y][x]:
                    field_x = block.location[0] + x
                    field_y = block.location[1] + y
                    if self.field[field_y][field_x + 1] > 10: return True
        return False

    def bottom_hit(self, block):
        pattern_len = len(block.pattern)
        for y in range(pattern_len - 1, -1, -1):
            for x in range(pattern_len):
                if block.pattern[y][x]:
                    field_x = block.location[0] + x
                    field_y = block.location[1] + y
                    if self.field[field_y + 1][field_x] > 10: return True
        return False

    def rotate_hit(self, block):
        pattern_len = len(block.pattern)
        collision_list = []
        shift_list = []
        if pattern_len == 4:  # Iミノ用
            # 右回転
            if block.state == [0, 1]: shift_list = [[0, 0], [-2, 0], [1, 0], [-2, 1], [1, -2]]
            if block.state == [1, 2]: shift_list = [[0, 0], [-1, 0], [2, 1], [-1, -2], [2, -1]]
            if block.state == [2, 3]: shift_list = [[0, 0], [2, 0], [-1, 0], [2, -1], [-1, 2]]
            if block.state == [3, 0]: shift_list = [[0, 0], [1, 0], [-2, 0], [1, 2], [-2, -1]]
            # 左回転
            if block.state == [0, 3]: shift_list = [[0, 0], [-1, 0], [2, 0], [-1, -2], [2, 1]]
            if block.state == [3, 2]: shift_list = [[0, 0], [-2, 0], [1, 0], [-2, 1], [1, -2]]
            if block.state == [2, 1]: shift_list = [[0, 0], [1, 0], [-2, 0], [1, 2], [-2, -1]]
            if block.state == [1, 0]: shift_list = [[0, 0], [2, 0], [-1, 0], [2, -1], [-1, 2]]
        else:  # I，O以外のミノ用
            # 右回転
            if block.state == [0, 1]: shift_list = [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
            if block.state == [1, 2]: shift_list = [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]]
            if block.state == [2, 3]: shift_list = [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]]
            if block.state == [3, 0]: shift_list = [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]]
            # 左回転
            if block.state == [0, 3]: shift_list = [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]]
            if block.state == [3, 2]: shift_list = [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]]
            if block.state == [2, 1]: shift_list = [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
            if block.state == [1, 0]: shift_list = [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]]
        for shift_axis in shift_list:
            for y in range(pattern_len):
                for x in range(pattern_len):
                    if block.pattern[y][x]:
                        field_x = block.location[0] + x + shift_axis[0]
                        field_y = block.location[1] + y + shift_axis[1]
                        if self.field[field_y][field_x] > 10: collision_list.append(99)
                        else: collision_list.append(0)
            if not 99 in collision_list:
                block.location[0] += shift_axis[0]
                block.location[1] += shift_axis[1]
                block.state[0] = block.state[1]
#                spin_type = Window.t_spin_check(shift_axis)
                return False
            collision_list = []
        return True

    def line_clear_check(self):
        self.clear_lines = []
        for y in range(self.field_height - 4, 2, -1):
            zero_count = self.field[y].count(0)
            if zero_count == 0:
                self.clear_lines.append(y)
            if zero_count == 10:
                break
        if self.clear_lines: self.line_clear_flag = True
        # RENの判定
        if self.clear_lines:
            if self.ren_flag: self.ren += 1
            else: self.ren_flag = True
        else:
            self.ren = 0
            self.ren_flag = False

    def line_clear(self):
        for y in self.clear_lines: del self.field[y]
        for y in range(len(self.clear_lines)):
            self.field.insert(2, [99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99])

    def free_fall(self, time):
        self.fall_time_sum += time
        if self.fall_time_sum >= self.fall_interval:
            if not self.bottom_hit(block_instance):
                self.mapping(block_instance, CLEAR)
                block_instance.control(DOWN)
                self.mapping(block_instance, DROP)
                self.fall_time_sum = 0
            self.fall_time_sum = 0

    def soft_drop_fix(self, time):
        if self.bottom_hit(block_instance):
            self.fix_time_sum += time
            if self.fix_time_sum >= self.time_to_fix:
                if self.bottom_hit(block_instance):
                    self.t_spin_flag = self.t_spin_check()  # Tスピン判定
                    self.fix()
                    self.fix_time_sum = 0
                else: self.fix_time_sum = 0

    def fix(self):
        self.mapping(block_instance, FIX)
        sound_instance.fix_sound.play()
        # 消去可能ライン数確認
        self.line_clear_check()
        # スコア計算
        self.score_count()
        # ライン消去
        self.line_clear()
#        # 固定されたらT−SpinのフラグをFalseに
#        self.t_spin_flag = False
        self.fixed = True
        self.game_over_check()

    def hard_drop(self):
        self.mapping(block_instance, CLEAR)
        while not self.bottom_hit(block_instance):
            block_instance.control(DOWN)
            self.score += 1
        sound_instance.hard_sound.play()
        self.fix()

    def ghost_mapping(self):
        while not self.bottom_hit(ghost_instance):
            ghost_instance.control(DOWN)
        self.mapping(ghost_instance, GHOST)

    def t_spin_check(self):
        if block_instance.return_now_pattern() == 7:
            surrounding_list = []  # Tミノの周囲の要素を入れる
            pattern_len = len(block_instance.pattern)
            # Tミノの周囲の要素を調べる
            for y in range(0, pattern_len, 2):
                for x in range(0, pattern_len, 2):
                    field_x = block_instance.location[0] + x
                    field_y = block_instance.location[1] + y
                    code = self.field[field_y][field_x]
                    if code > 10: surrounding_list.append(99)
            if surrounding_list.count(99) >= 3 and block_instance.location == block_instance.store_location:
                return True
            return False
        return False

    def score_count(self):
        cleared_lines = len(self.clear_lines)
        score = 0
        if cleared_lines == 1:
            if self.t_spin_flag:
                print('t-spin1')
                score = 800
            else:
                score = 100
        elif cleared_lines == 2:
            if self.t_spin_flag:
                print('t-spin2')
                score = 1200
            else:
                score = 300
        elif cleared_lines == 3:
            if self.t_spin_flag:
                print('t-spin3')
                score = 1600
            else:
                score = 500
        elif cleared_lines == 4:
            score = 800
        if self.ren >= 1:
            score += self.ren * 50
            print('ren', self.ren)
        self.score += score

    def game_over_check(self):
        for y in range(0, 2):
            for x in range(self.field_width):
                if self.field[y][x] != 0:
                    if self.field[y][x] != 99:
                        Player.game_state = TITLE


class Ghost:
    def __init__(self):
        self.location = copy.deepcopy(block_instance.location)
        self.pattern = copy.deepcopy(block_instance.pattern)

    def update(self):
        self.location = copy.deepcopy(block_instance.location)
        self.pattern = copy.deepcopy(block_instance.pattern)

    def control(self, direction):
        if direction == DOWN: self.location[1] += 1
#        if direction == LEFT: self.location[0] -= 1
#        if direction == RIGHT: self.location[0] += 1

class Draw:
    def __init__(self):
        self.block_img = []
        self.load_image()
        screen_size = (CELL * 27, CELL * 27)
        self.screen = pygame.display.set_mode(screen_size)
        # フォント準備
        sys_font = pygame.font.SysFont(None, 80)
        self.game_font = pygame.font.SysFont(None, 40)
        self.title = sys_font.render('Press Space to Start', True, (255, 255, 255))
        self.score_title = self.game_font.render('SCORE', True, (255, 255, 255))
        self.hold_title = self.game_font.render('HOLD', True, (255, 255, 255))
        self.next_title = self.game_font.render('NEXT', True, (255, 255, 255))
        # T-spinの文字表示時間
        self.display_time = 2000
        self.display_time_sum = 0
        self.display_t_spin = False
        # クリアエフェクト表示時間
        self.clear_display_time = 2000
        self.clear_display_time_sum = 0

    def draw_title(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.title, (20, 150))

    def draw_play(self, time):
        self.screen.fill((0, 0, 0))

        self.field_left_margin = CELL * 4  # +3が実際の表示領域
        self.field_top_margin = CELL * 1  # +2が実際の表示領域

        next_left_margin = CELL * 19
        next_top_margin = CELL * 5

        hold_left_margin = CELL * 1
        hold_top_margin = CELL * 5

        self.screen.blit(self.next_title, (next_left_margin, next_top_margin - CELL * 2))
        self.screen.blit(self.hold_title, (hold_left_margin, hold_top_margin - CELL * 2))
        self.screen.blit(self.score_title, (hold_left_margin, hold_top_margin + CELL * 3))
        score_num = self.game_font.render(str(field_instance.score), True, (255, 255, 255))
        self.screen.blit(score_num, (hold_left_margin, hold_top_margin + CELL * 4))

        # REN描画用
        if field_instance.ren > 0:
            self.ren_title = self.game_font.render(str(field_instance.ren) + 'REN', True, (255, 255, 255))
            self.screen.blit(self.ren_title, (hold_left_margin, hold_top_margin + CELL * 6))

        # T-spin描画用
        if field_instance.t_spin_flag:
            self.display_t_spin = True
        if self.display_t_spin:
            self.display_time_sum += time
            if self.display_time_sum < self.display_time:
                self.t_spin_title = self.game_font.render('T-Spin', True, (255, 255, 255))
                self.screen.blit(self.t_spin_title, (hold_left_margin, hold_top_margin + CELL * 7))
            else:
                self.display_t_spin = False
                self.display_time_sum = 0

        # field描画用
        for y in range(2, Field.field_height - 2):
            for x in range(2, Field.field_width - 2):
                code = field_instance.field[y][x]
                self.blit_img(code, x, y, self.field_left_margin, self.field_top_margin)

        # next描画用
        next_len = len(block_instance.next) - 2
        for z in range(next_len):
            block_len = len(block_instance.next[z])
            for y in range(block_len):
                for x in range(block_len):
                    if block_instance.next[z][y][x]:
                        code = block_instance.next[z][y][x]
                        self.blit_img(code, x, y, next_left_margin, next_top_margin + 96 * z)

        # hold描画用
        for y in range(len(block_instance.hold_now)):
            for x in range(len(block_instance.hold_now)):
                if block_instance.hold_now[y][x]:
                    code = block_instance.hold_now[y][x]
                    self.blit_img(code, x, y, hold_left_margin, hold_top_margin)

    def line_clear(self):
        block_size = 24
        sound_instance.clear_sound.play()
        for y in reversed(field_instance.clear_lines):
            for x in range(3, Field.field_width - 3):
                self.screen.blit(self.block_img[8], (self.field_left_margin + x * block_size, self.field_top_margin + y * block_size))
            pygame.display.update()
        field_instance.line_clear_flag = False

    def blit_img(self, code, x, y, left_margin, bottom_margin):
        block_size = 24
        if code == 99:
            self.screen.blit(self.block_img[7], (left_margin + x * block_size, bottom_margin + y * block_size))
        elif code == 1 or code == 11 or code == -1:
            if code == -1:
                self.block_img[0].set_alpha(100)
                self.screen.blit(self.block_img[0], (left_margin + x * block_size, bottom_margin + y * block_size))
            else:
                self.block_img[0].set_alpha(255)
                self.screen.blit(self.block_img[0], (left_margin + x * block_size, bottom_margin + y * block_size))

        elif code == 2 or code == 12 or code == -2:
            if code == -2:
                self.block_img[1].set_alpha(100)
                self.screen.blit(self.block_img[1], (left_margin + x * block_size, bottom_margin + y * block_size))
            else:
                self.block_img[1].set_alpha(255)
                self.screen.blit(self.block_img[1], (left_margin + x * block_size, bottom_margin + y * block_size))

        elif code == 3 or code == 13 or code == -3:
            if code == -3:
                self.block_img[2].set_alpha(100)
                self.screen.blit(self.block_img[2], (left_margin + x * block_size, bottom_margin + y * block_size))
            else:
                self.block_img[2].set_alpha(255)
                self.screen.blit(self.block_img[2], (left_margin + x * block_size, bottom_margin + y * block_size))

        elif code == 4 or code == 14 or code == -4:
            if code == -4:
                self.block_img[3].set_alpha(100)
                self.screen.blit(self.block_img[3], (left_margin + x * block_size, bottom_margin + y * block_size))
            else:
                self.block_img[3].set_alpha(255)
                self.screen.blit(self.block_img[3], (left_margin + x * block_size, bottom_margin + y * block_size))

        elif code == 5 or code == 15 or code == -5:
            if code == -5:
                self.block_img[4].set_alpha(100)
                self.screen.blit(self.block_img[4], (left_margin + x * block_size, bottom_margin + y * block_size))
            else:
                self.block_img[4].set_alpha(255)
                self.screen.blit(self.block_img[4], (left_margin + x * block_size, bottom_margin + y * block_size))

        elif code == 6 or code == 16 or code == -6:
            if code == -6:
                self.block_img[5].set_alpha(100)
                self.screen.blit(self.block_img[5], (left_margin + x * block_size, bottom_margin + y * block_size))
            else:
                self.block_img[5].set_alpha(255)
                self.screen.blit(self.block_img[5], (left_margin + x * block_size, bottom_margin + y * block_size))

        elif code == 7 or code == 17 or code == -7:
            if code == -7:
                self.block_img[6].set_alpha(100)
                self.screen.blit(self.block_img[6], (left_margin + x * block_size, bottom_margin + y * block_size))
            else:
                self.block_img[6].set_alpha(255)
                self.screen.blit(self.block_img[6], (left_margin + x * block_size, bottom_margin + y * block_size))
        elif code == 100:
            self.screen.blit(self.block_img[8], (left_margin + x * block_size, bottom_margin + y * block_size))

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

class Player:
    # キー入力用カウンタ
    down_threshold = 2
    side_threshold = 3
    game_state = TITLE

    def __init__(self):
        self.left_count = 0
        self.right_count = 0
        self.down_count = 0

    def title_key_handler(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                if event.key == K_SPACE:
                    Player.game_state = PLAY

    def key_handler(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_DOWN]:
            self.down_count += 1
            if self.down_count >= Player.down_threshold:
                if not field_instance.bottom_hit(block_instance):
                    field_instance.mapping(block_instance, CLEAR)
                    block_instance.control(DOWN)
                    # 自分が動かしたマス目分だけスコアに加算
                    field_instance.score += 1
                    field_instance.mapping(block_instance, DROP)
                self.down_count = 0

        if pressed[K_LEFT]:
            self.left_count += 1
            if self.left_count >= Player.side_threshold:
                if not field_instance.left_hit(block_instance):
                    field_instance.mapping(block_instance, CLEAR)
                    field_instance.mapping(block_instance, CLEAR)  # フィールドからブロックを削除
                    field_instance.mapping(ghost_instance, CLEAR)  # フィールドからゴーストブロックを削除
                    block_instance.control(LEFT)
                    ghost_instance.update()  # ゴーストブロックの座標をブロックのものに更新
                    field_instance.ghost_mapping() # ゴーストブロックをマッピング
                    field_instance.mapping(block_instance, DROP)
                self.left_count = 0

        if pressed[K_RIGHT]:
            self.right_count += 1
            if self.right_count >= Player.side_threshold:
                if not field_instance.right_hit(block_instance):
                    field_instance.mapping(block_instance, CLEAR)  # フィールドからブロックを削除
                    field_instance.mapping(ghost_instance, CLEAR)  # フィールドからゴーストブロックを削除
                    block_instance.control(RIGHT)
                    ghost_instance.update()  # ゴーストブロックの座標をブロックのものに更新
                    field_instance.ghost_mapping() # ゴーストブロックをマッピング
                    field_instance.mapping(block_instance, DROP)
                self.right_count = 0

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()

                if event.key == K_z:
                    sound_instance.rotate_sound.play()
                    field_instance.mapping(block_instance, CLEAR)  # フィールドからブロックを削除
                    field_instance.mapping(ghost_instance, CLEAR)  # フィールドからゴーストブロックを削除
                    block_instance.rotate(LEFT)
                    if field_instance.rotate_hit(block_instance):
                        block_instance.rotate(RIGHT)
                    else:
                        ghost_instance.update()  # ゴーストブロックの座標をブロックのものに更新
                        field_instance.ghost_mapping() # ゴーストブロックをマッピング
#                        fix_time = 0
                    field_instance.mapping(block_instance, DROP)

                if event.key == K_x:
                    sound_instance.rotate_sound.play()
                    field_instance.mapping(block_instance, CLEAR)  # フィールドからブロックを削除
                    field_instance.mapping(ghost_instance, CLEAR)  # フィールドからゴーストブロックを削除
                    block_instance.rotate(RIGHT)
                    if field_instance.rotate_hit(block_instance):
                        block_instance.rotate(LEFT)
                    else:
                        ghost_instance.update()  # ゴーストブロックの座標をブロックのものに更新
                        field_instance.ghost_mapping() # ゴーストブロックをマッピング
#                        fix_time = 0
                    field_instance.mapping(block_instance, DROP)  #ブロックをマッピング
                if event.key == K_LSHIFT:
                    block_instance.hold()

                if event.key == K_UP:
#                    hard_sound.play()
                    field_instance.hard_drop()

class Sound:
    def __init__(self):
        self.fix_sound = pygame.mixer.Sound('data/fix.wav')
        self.hard_sound = pygame.mixer.Sound('data/hard.wav')
        self.rotate_sound = pygame.mixer.Sound('data/rotate.wav')
        self.hold_sound = pygame.mixer.Sound('data/hold.wav')
        self.clear_sound = pygame.mixer.Sound('data/clear.wav')
        # control_sound = pygame.mixer.Sound('data/control.wav')

#        self.bgm = pygame.mixer.music.load('data/bgm01_intro.ogg')
        self.bgm = pygame.mixer.music.load('data/bgm.ogg')
        pygame.mixer.music.play(1)

#    if not pygame.mixer.music.get_busy():
#        pygame.mixer.music.load('data/bgm01.ogg')
#        pygame.mixer.music.play(-1)

# ゲーム開始前の初期化処理が必要か
play_init = True

pygame.init()
clock = pygame.time.Clock()

player_instance = Player()
draw_instance = Draw()
sound_instance = Sound()

while True:

    if Player.game_state == TITLE:
        draw_instance.draw_title()
        player_instance.title_key_handler()
        pygame.display.update()
        play_init = True

    if Player.game_state == PLAY:
        if play_init:
            block_instance = Block()
            block_instance.create_next()  # ツモ作成
            block_instance.pop_block()  # ブロック生成
            field_instance = Field()
            ghost_instance = Ghost()
            ghost_instance.update()  # ゴーストブロックの座標をブロックのものに更新
            field_instance.ghost_mapping() # ゴーストブロックをマッピング
            field_instance.mapping(block_instance, DROP)  # フィールドにマッピング
            # ゲーム開始前の初期化処理が完了
            play_init = False

        if field_instance.fixed:
            block_instance.pop_block()  # ブロックを生成
            ghost_instance = Ghost()  # ゴーストブロックを生成
            ghost_instance.update()  # ゴーストブロックの座標をブロックのものに更新
            field_instance.ghost_mapping() # ゴーストブロックをマッピング
            field_instance.fixed = False
            field_instance.t_spin_flag = False
            field_instance.hold = False

        time_passed = clock.tick(60)
        player_instance.key_handler()
        field_instance.free_fall(time_passed)
        field_instance.soft_drop_fix(time_passed)
        if field_instance.line_clear_flag:
            draw_instance.line_clear()
            pygame.time.wait(500)
        draw_instance.draw_play(time_passed)
        pygame.display.update()