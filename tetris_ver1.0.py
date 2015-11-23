import random
import pygame
import sys
from pygame.locals import *
import copy
import threading

# control
LEFT = 0
RIGHT = 1
DOWN = 2
# mapping
DROP = 0
CLEAR = 1
FIX = 2
GHOST = 3
# state
TITLE = 0
PLAY = 1
GAMEOVER = 2
GAMECLEAR = 3
# draw
CELL = 24  # ブロック1つ(1マス)の大きさ

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

        self.clear_lines = []  # 消去するライン
        # 自由落下用変数
        self.fall_interval = 1000
        self.fall_time_sum = 0
        # 固定時間設定用変数
        self.fix_time_sum = 0
        self.time_to_fix = 1000
        self.fixing = False
        # 固定用フラグ
        self.fixed = False
        # hold用フラグ
        self.hold = False
        # T-Spin用
        self.t_spin_flag = False
        self.store_location = copy.deepcopy(block_instance.location)
        # スコア計算用変数
        self.score = 0
        # REN用変数,Flag
        self.ren = 0
        self.ren_flag = False
        # ラインクリア用フラグ
        self.line_clear_flag = False
        # 消したライン数
        self.cleared_lines = 0
        # LEVEL
        self.level = 1

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
                # 回転後のブロックの位置「location」を記憶
                self.store_location = copy.deepcopy(block_instance.location)
                return False
            collision_list = []
        return True

    def line_clear_check(self):
        self.clear_lines = []  # 消去可能ラインが何番目かを入れておく
        for y in range(self.field_height - 4, 2, -1):
            # フィールドの底から右方向に走査して，1行あたりの0の個数をカウント
            zero_count = self.field[y].count(0)
            if zero_count == 0: self.clear_lines.append(y)  # 消去可能
            if zero_count == 10: break  # これより上にブロックはないのでbreak
        if self.clear_lines: self.line_clear_flag = True  # 消去可能ラインがあったらフラグをTrueに
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
        # 消去済みライン数更新
        self.cleared_lines += len(self.clear_lines)
        # LEVEL UP 処理
        for i in range(1, 15):
            if self.level == i and self.cleared_lines >= i*10:
                self.level += 1
                self.fall_interval /= 2
                draw_instance.level_up_flag = True
                sound_instance.level_up.play()
        # ゲームクリア判定
        if self.cleared_lines >= 150:
            # ゲームクリア音再生
            sound_instance.game_clear.play()
            Player.game_state = GAMECLEAR

    def free_fall(self, time):
        if self.fall_time_sum >= self.fall_interval:
            if not self.bottom_hit(block_instance):
                self.mapping(block_instance, CLEAR)
                block_instance.control(DOWN)
                self.mapping(block_instance, DROP)
            else:
                self.fixing = True
            self.fall_time_sum = 0
        self.fall_time_sum += time

    def pre_fix(self, time):
        if self.fixing:
            if self.fix_time_sum >= self.time_to_fix:
                if not self.bottom_hit(block_instance):
                    self.fix_time_sum = 0
                else:
                    self.fix()
                    self.fix_time_sum = 0
                    return True
            self.fix_time_sum += time

    def fix(self):
        self.t_spin_flag = self.t_spin_check()  # Tスピン判定
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
        self.fixing = False
        self.game_over_check()

    def hard_drop(self):
#        self.mapping(block_instance, CLEAR)
        while not self.bottom_hit(block_instance):
            self.mapping(block_instance, CLEAR)
            block_instance.control(DOWN)
            field_instance.mapping(block_instance, DROP)
            self.score += 1
        sound_instance.hard_sound.play()
        # DROPしたことがわかるように1度だけ描画
        draw_instance.draw_play(time_passed)
        self.fix()

    def t_spin_check(self):
        if block_instance.return_now_pattern() == 7:
            if block_instance.location == self.store_location:
                surrounding_list = []  # Tミノの周囲の要素を入れる
                pattern_len = len(block_instance.pattern)
                top = []  # Tミノの上部の要素を入れる
                bottom = []  # Tミノの下部の要素を入れる
                # Tミノの周囲の要素を調べる
                for y in range(0, pattern_len, 2):
                    for x in range(0, pattern_len, 2):
                        field_x = block_instance.location[0] + x
                        field_y = block_instance.location[1] + y
                        code = self.field[field_y][field_x]
                        surrounding_list.append(code)
                # リストをイテレータに変換
                iter_list = iter(surrounding_list)
                # ブロックの回転状態によって上部，下部が異なるのでそれに応じてリストに追加していく（10を超える要素のみ）
                if block_instance.state[0] == 0:
                    for i in range(2):
                        code = next(iter_list)
                        if code > 10: top.append(code)
                    for i in range(2):
                        code = next(iter_list)
                        if code > 10: bottom.append(code)
                elif block_instance.state[0] == 1:
                    for i in range(2):
                        code = next(iter_list)
                        if code > 10: bottom.append(code)
                        code = next(iter_list)
                        if code > 10: top.append(code)
                elif block_instance.state[0] == 2:
                    for i in range(2):
                        code = next(iter_list)
                        if code > 10: bottom.append(code)
                    for i in range(2):
                        code = next(iter_list)
                        if code > 10: top.append(code)
                elif block_instance.state[0] == 3:
                    for i in range(2):
                        code = next(iter_list)
                        if code > 10: top.append(code)
                        code = next(iter_list)
                        if code > 10: bottom.append(code)
                # topとbottom内の要素数に応じてスピンの判定
                if len(top) == 2 and len(bottom) >= 1:
                    print('T-Spin')
                    return True
                elif len(top) == 1 and len(bottom) == 2:
                    print('Mini T-Spin')
                    return True
                return False
            return False
        return False

    def ghost_mapping(self):
        while not self.bottom_hit(ghost_instance):
            ghost_instance.control(DOWN)
        self.mapping(ghost_instance, GHOST)

    def score_count(self):
        cleared_lines = len(self.clear_lines)
        score = 0
        if cleared_lines == 1:
            if self.t_spin_flag:
                draw_instance.t_spin_type = 'Single !'
                sound_instance.t_spin_sound.play()
                print('t-spin1')
                score = 800
            else:
                score = 100
        elif cleared_lines == 2:
            if self.t_spin_flag:
                draw_instance.t_spin_type = 'Double !'
                sound_instance.t_spin_sound.play()
                print('t-spin2')
                score = 1200
            else:
                score = 300
        elif cleared_lines == 3:
            if self.t_spin_flag:
                draw_instance.t_spin_type = 'Triple !'
                sound_instance.t_spin_sound.play()
                print('t-spin3')
                score = 1600
            else:
                score = 500
        elif cleared_lines == 4:
            draw_instance.tetris_str_flag = True
            print('tetris')
            score = 800
        else:
            if self.t_spin_flag:
                draw_instance.t_spin_type = ' '
        if self.ren >= 1:
            # RENをスコアに加算
            score += self.ren * 50
            draw_instance.ren_number = str(self.ren)
#            if self.ren == 1: sound_instance.ren1.play()
#            if self.ren == 2: sound_instance.ren2.play()
#            if self.ren == 3: sound_instance.ren3.play()
#            if self.ren >= 4: sound_instance.ren4.play()
            if self.ren == 1: sound_instance.clear_sound2.play()
            if self.ren == 2: sound_instance.clear_sound3.play()
            if self.ren == 3: sound_instance.clear_sound4.play()
            if self.ren >= 4: sound_instance.clear_sound4.play()
        self.score += score

    def game_over_check(self):
        for y in range(0, 2):
            for x in range(self.field_width):
                if self.field[y][x] != 0:
                    if self.field[y][x] != 99:
                        # ゲームオーバー音再生
                        sound_instance.game_over.play()
                        # ゲーム状態をゲームオーバーに変更
                        Player.game_state = GAMEOVER
                        # スコアレコードに書き込み
                        score_file = open('data/score.txt', 'a')
                        score_file.write(str(self.score) + '\n')
                        score_file.close()
                        # スコアレコードの長さが3より小さい場合は'-'を3つ書き込み
                        score_file = open('data/score.txt', 'r')
                        score_list = score_file.read()
                        score_list = score_list.split('\n')
                        score_file.close()
                        score_file = open('data/score.txt', 'a')
                        if len(score_list) < 3:
                            for i in range(3):
                                score_file.write('-\n')
                        break
            if Player.game_state == GAMEOVER: break


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

class Draw():
    def __init__(self):
        self.block_img = []
        self.load_image()
        screen_size = (CELL * 27, CELL * 27)
        self.screen = pygame.display.set_mode(screen_size)

        # フォント準備
        self.title_font = pygame.font.Font('data/mplus-1m-bold.ttf', 80)
#        self.title_font.set_bold(True)
        self.game_font = pygame.font.Font('data/mplus-1m-bold.ttf', 30)
#        self.game_font.set_bold(True)
        # TITLE
        self.title_str = self.title_font.render('テ', True, (255, 255, 255))
        self.press_str = self.game_font.render('スペースキーを押してスタート!', True, (255, 255, 255))
        # GAMEOVER
        self.gameover_str = self.title_font.render('GAME OVER', True, (255, 255, 255))
        self.gameclear_str = self.title_font.render('GAME CLEAR!!', True, (255, 255, 255))
        self.record_str = self.game_font.render('ランキング', True, (255, 255, 255))
        self.retry_str = self.game_font.render('スペースキーでもう一度プレイ', True, (255, 255, 255))
        # PLAY
        self.score_str = self.game_font.render('SCORE', True, (255, 255, 255))
        self.hold_str = self.game_font.render('HOLD', True, (255, 255, 255))
        self.next_str = self.game_font.render('NEXT', True, (255, 255, 255))
        self.lines_str = self.game_font.render('LINES', True, (255, 255, 255))
        self.level_str = self.game_font.render('LEVEL', True, (255, 255, 255))

        # PLAY用変数
        self.field_left_margin = CELL * 4  # +3が実際の表示領域
        self.field_top_margin = CELL * 1  # +2が実際の表示領域
        self.next_left_margin = CELL * 19
        self.next_top_margin = CELL * 5
        self.hold_left_margin = CELL * 1
        self.hold_top_margin = CELL * 5

        # TETRIS表示用
        self.tetris_str_flag = False
        self.tetris_time = 0

        # REN表示用
        self.ren_number = 0
        self.ren_time = 0

        # T-spin表示用
        self.t_spin_type = None
        self.t_spin_time = 0

        # LEVEL UP用
        self.level_up_str = self.game_font.render('LEVEL UP!', True, (255, 255, 255))
        self.level_up_flag = False
        self.level_up_time = 0

        # クリアエフェクト表示時間
        self.clear_display_time = 2000
        self.clear_display_time_sum = 0

    def draw_title(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.title_str, (50, 50))
        self.screen.blit(self.press_str, (50, 200))

    def draw_game_over(self, clear):
        # 画面を黒で塗りつぶし
        self.screen.fill((0, 0, 0))
        # ゲームオーバーの文字を表示
        if clear: self.screen.blit(self.gameclear_str, (50, 50))
        else: self.screen.blit(self.gameover_str, (50, 50))
        # リトライの文字を表示
        self.screen.blit(self.retry_str, (150, 550))
        # 自分のスコアを表示
        score_num = self.game_font.render('あなたのスコア : ' + str(field_instance.score), True, (255, 255, 255))
        self.screen.blit(score_num, (50, 200))
        # ランキングを読み込んでトップ3を表示
        self.screen.blit(self.record_str, (50, 300))
        score_data = open('data/score.txt', 'r')
        score_list = score_data.read()
        score_list = score_list.split('\n')
        score_list.sort(reverse=True)
        for i in range(3):
            top3 = self.game_font.render(str(i + 1) + ' : ' + str(score_list[i]), True, (255, 255, 255))
            self.screen.blit(top3, (100, 350 + 50 * i))
        # キャラクター表示
        if clear: self.screen.blit(self.game_clear, (300, 230))
        else: self.screen.blit(self.game_over, (300, 230))


    def draw_play(self, time):
        self.screen.fill((0, 0, 0))
        # 各種文字表示
        self.screen.blit(self.next_str, (self.next_left_margin, self.next_top_margin - CELL * 2))
        self.screen.blit(self.hold_str, (self.hold_left_margin, self.hold_top_margin - CELL * 2))
        self.screen.blit(self.score_str, (self.hold_left_margin, self.hold_top_margin + CELL * 3))
        self.screen.blit(self.lines_str, (self.hold_left_margin, self.hold_top_margin + CELL * 6))
        self.screen.blit(self.level_str, (self.hold_left_margin, self.hold_top_margin + CELL * 9))
        # SCORE表示
        score_num = self.game_font.render(str(field_instance.score), True, (255, 255, 255))
        self.screen.blit(score_num, (self.hold_left_margin, self.hold_top_margin + CELL * 4))
        # LINES表示
        lines_num = self.game_font.render(str(field_instance.cleared_lines), True, (255, 255, 255))
        self.screen.blit(lines_num, (self.hold_left_margin, self.hold_top_margin + CELL * 7))
        # LEVEL表示
        level_num = self.game_font.render(str(field_instance.level), True, (255, 255, 255))
        self.screen.blit(level_num, (self.hold_left_margin, self.hold_top_margin + CELL * 10))

        # TETRIS描画用
        if self.tetris_str_flag:
            if self.tetris_time <= 2000:
                self.tetris_str = self.game_font.render('TETRIS!', True, (255, 255, 255))
                self.screen.blit(self.tetris_str, (self.hold_left_margin, self.hold_top_margin + CELL * 12))
            else:
                self.tetris_time = 0
                self.tetris_str_flag = False
            self.tetris_time += time

        # REN描画用
        if self.ren_number:
            if self.ren_time <= 2000:
                self.ren_str = self.game_font.render(self.ren_number + 'REN', True, (255, 255, 255))
                self.screen.blit(self.ren_str, (self.hold_left_margin, self.hold_top_margin + CELL * 14))
            else:
                self.ren_time = 0
                self.ren_number = 0
            self.ren_time += time

        # T-spin描画用
        if self.t_spin_type:
            if self.t_spin_time <= 2000:
                self.t_spin_str1 = self.game_font.render('T-Spin', True, (255, 255, 255))
                self.t_spin_str2 = self.game_font.render(self.t_spin_type, True, (255, 255, 255))
                self.screen.blit(self.t_spin_str1, (self.hold_left_margin, self.hold_top_margin + CELL * 15))
                self.screen.blit(self.t_spin_str2, (self.hold_left_margin, self.hold_top_margin + CELL * 16))
            else:
                self.t_spin_time = 0
                self.t_spin_type = None
            self.t_spin_time += time

        # LEVEL UP表示
        if self.level_up_flag:
            if self.level_up_time <= 2000:
                self.screen.blit(self.level_up_str, (self.hold_left_margin + CELL * 8, self.hold_top_margin + CELL * 20 - 10))
            else:
                self.level_up_time = 0
                self.level_up_flag = False
            self.level_up_time += time


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
                        self.blit_img(code, x, y, self.next_left_margin, self.next_top_margin + 96 * z)
        # hold描画用
        for y in range(len(block_instance.hold_now)):
            for x in range(len(block_instance.hold_now)):
                if block_instance.hold_now[y][x]:
                    code = block_instance.hold_now[y][x]
                    self.blit_img(code, x, y, self.hold_left_margin, self.hold_top_margin)

    def clear_effect(self):
        block_size = 24
        if len(field_instance.clear_lines) == 1: sound_instance.clear_sound1.play()
        if len(field_instance.clear_lines) == 2: sound_instance.clear_sound2.play()
        if len(field_instance.clear_lines) == 3: sound_instance.clear_sound3.play()
        if len(field_instance.clear_lines) == 4: sound_instance.clear_sound4.play()
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
        self.game_over = pygame.image.load('data/denx_chan_over.png')
        self.game_clear = pygame.image.load('data/denx_chan_clear.png')

class Player:
    # キー入力用カウンタ
    # Windows
    down_threshold = 2
    side_threshold = 5
    # Mac
#    down_threshold = 1
#    side_threshold = 2
    # ゲーム状態を保持
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
        # ソフトドロップ
        if pressed[K_DOWN]:
            self.down_count += 1
            if self.down_count >= Player.down_threshold:
                if not field_instance.bottom_hit(block_instance):
                    field_instance.mapping(block_instance, CLEAR)
                    block_instance.control(DOWN)
                    sound_instance.control_sound.play()
                    # 自分が動かしたマス目分だけスコアに加算
                    field_instance.score += 1
                    field_instance.mapping(block_instance, DROP)
                else: field_instance.fixing = True
                self.down_count = 0

        # 左移動
        if pressed[K_LEFT]:
            self.left_count += 1
            if self.left_count >= Player.side_threshold:
                if not field_instance.left_hit(block_instance):
                    field_instance.mapping(block_instance, CLEAR)
                    field_instance.mapping(block_instance, CLEAR)  # フィールドからブロックを削除
                    field_instance.mapping(ghost_instance, CLEAR)  # フィールドからゴーストブロックを削除
                    sound_instance.control_sound.play()  # 移動音再生
                    block_instance.control(LEFT)
                    ghost_instance.update()  # ゴーストブロックの座標をブロックのものに更新
                    field_instance.ghost_mapping() # ゴーストブロックをマッピング
                    field_instance.mapping(block_instance, DROP)
                self.left_count = 0

        # 右移動
        if pressed[K_RIGHT]:
            self.right_count += 1
            if self.right_count >= Player.side_threshold:
                if not field_instance.right_hit(block_instance):
                    field_instance.mapping(block_instance, CLEAR)  # フィールドからブロックを削除
                    field_instance.mapping(ghost_instance, CLEAR)  # フィールドからゴーストブロックを削除
                    sound_instance.control_sound.play()  # 移動音再生
                    block_instance.control(RIGHT)
                    ghost_instance.update()  # ゴーストブロックの座標をブロックのものに更新
                    field_instance.ghost_mapping() # ゴーストブロックをマッピング
                    field_instance.mapping(block_instance, DROP)
                self.right_count = 0

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                # 左回転
                if event.key == K_z:
                    sound_instance.rotate_sound.play()
                    field_instance.mapping(block_instance, CLEAR)  # フィールドからブロックを削除
                    field_instance.mapping(ghost_instance, CLEAR)  # フィールドからゴーストブロックを削除
                    block_instance.rotate(LEFT)
                    if field_instance.rotate_hit(block_instance):
                        block_instance.rotate(RIGHT)
                    else:
                        field_instance.fix_time_sum = 0
                    ghost_instance.update()  # ゴーストブロックの座標をブロックのものに更新
                    field_instance.ghost_mapping() # ゴーストブロックをマッピング
                    field_instance.mapping(block_instance, DROP)
                # 右回転
                if event.key == K_x:
                    sound_instance.rotate_sound.play()
                    field_instance.mapping(block_instance, CLEAR)  # フィールドからブロックを削除
                    field_instance.mapping(ghost_instance, CLEAR)  # フィールドからゴーストブロックを削除
                    block_instance.rotate(RIGHT)
                    if field_instance.rotate_hit(block_instance):
                        block_instance.rotate(LEFT)
                    else:
                        field_instance.fix_time_sum = 0
                    ghost_instance.update()  # ゴーストブロックの座標をブロックのものに更新
                    field_instance.ghost_mapping() # ゴーストブロックをマッピング
                    field_instance.mapping(block_instance, DROP)  #ブロックをマッピング
                # ホールド
                if event.key == K_LSHIFT:
                    block_instance.hold()
                # ハードドロップ
                if event.key == K_UP:
                    field_instance.hard_drop()

class Sound:
    def __init__(self):
        self.fix_sound = pygame.mixer.Sound('data/fix.wav')
        self.hard_sound = pygame.mixer.Sound('data/hard.wav')
        self.rotate_sound = pygame.mixer.Sound('data/rotate.wav')
        self.control_sound = pygame.mixer.Sound('data/control.wav')
        self.hold_sound = pygame.mixer.Sound('data/hold.wav')
        self.clear_sound1 = pygame.mixer.Sound('data/clear1.wav')
        self.clear_sound2 = pygame.mixer.Sound('data/clear2.wav')
        self.clear_sound3 = pygame.mixer.Sound('data/clear3.wav')
        self.clear_sound4 = pygame.mixer.Sound('data/clear4.wav')
        self.t_spin_sound = pygame.mixer.Sound('data/t_spin.wav')
        self.ren1 = pygame.mixer.Sound('data/ren1.wav')
        self.ren2 = pygame.mixer.Sound('data/ren2.wav')
        self.ren3 = pygame.mixer.Sound('data/ren3.wav')
        self.ren4 = pygame.mixer.Sound('data/ren4.wav')
        self.level_up = pygame.mixer.Sound('data/level_up.wav')
        self.game_clear = pygame.mixer.Sound('data/game_clear.wav')
        self.game_over = pygame.mixer.Sound('data/game_over.wav')

        pygame.mixer.music.load('data/bgm01_intro.ogg')
        pygame.mixer.music.set_volume(0.3)


# main
play_init = True  # ゲーム開始前の初期化処理が必要か
pygame.mixer.pre_init(44100, -16, 2, 1024)  # 音ズレ防止用
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

    if Player.game_state == GAMEOVER or Player.game_state == GAMECLEAR:
        pygame.mixer.music.stop()
        if Player.game_state == GAMEOVER:
            draw_instance.draw_game_over(clear=False)
        if Player.game_state == GAMECLEAR:
            draw_instance.draw_game_over(clear=True)
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
            pygame.mixer.music.play(1)
            # ゲーム開始前の初期化処理が完了
            play_init = False

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('data/bgm01_loop.ogg')
            pygame.mixer.music.play(-1)

        if field_instance.fixed:
            block_instance.pop_block()  # ブロックを生成
            ghost_instance = Ghost()  # ゴーストブロックを生成
            ghost_instance.update()  # ゴーストブロックの座標をブロックのものに更新
            field_instance.ghost_mapping() # ゴーストブロックをマッピング
            field_instance.fixed = False
            field_instance.t_spin_flag = False
            field_instance.hold = False

        time_passed = clock.tick(60)
        field_instance.free_fall(time_passed)  # 自由落下処理
        player_instance.key_handler()  # キー入力受付
        field_instance.pre_fix(time_passed)  # 固定処理
        if field_instance.line_clear_flag:
            draw_instance.clear_effect()
            pygame.time.wait(500)
        draw_instance.draw_play(time_passed)
        pygame.display.update()
