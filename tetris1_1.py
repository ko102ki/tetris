import random
import pygame
import sys
from pygame.locals import *
import copy


class Block:
    next1 = []  # ネクストブロック7種を入れる
    next2 = []  # ネクストブロック7種を入れる

    hold1 = []  # ホールド時にhold2の内容を移す
    hold2 = []  # 落下中のblock_instanceのパターンを入れておく

    drop_time = 0

    def __init__(self, process):
        self.create_next_block()
        if process == 'drop':
            self.pattern = Block.next1.pop(0)
            Block.next1.append(Block.next2.pop(0))  # next2からnext1へブロック１つを移す
        elif process == 'hold':
            self.pattern = Block.hold1
        self.loc = [6, 0]  # block_instanceのfield配列内での位置を表す[x, y]
        self.state = [0, 0]  # [今の状態, 移行したい状態]
        # キー入力用カウンタ
        self.left_count = 0
        self.right_count = 0
        self.down_count = 0
        self.down_threshold = 4
        self.side_threshold = 5

    def create_next_block(self):
        if len(Block.next1) == 0:
            # next1 next2ともに空なので両方にブロックのパターンを入れる
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
            # next2が空なのでnext2にブロックのパターンを入れる
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
        if index == 6:  # L
            return ([[0, 0, 6],
                     [6, 6, 6],
                     [0, 0, 0], ])
        if index == 7:  # T
            return ([[0, 7, 0],
                     [7, 7, 7],
                     [0, 0, 0], ])

    def rotate(self, direction):
        pattern_len = len(self.pattern)
        # インスタンスのパターンデータと同じ長さのリストをつくる
        # 回転させるためには1度コピーを作ってそれを回転させたデータをもとのインスタンスに反映
        pattern_copy = [[0 for col in range(pattern_len)] for row in range(pattern_len)]
        if direction == 'left':
            for y in range(pattern_len):
                for x in range(pattern_len):
                    pattern_copy[pattern_len - 1 - x][y] = self.pattern[y][x]
            self.state[1] -= 1  # 左に90度回転を-1とし，それを4で割ったあまりをstate[1]に代入
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
        # 上下左右の移動を担当
        if direction == 'left':
            self.loc[0] -= 1
        if direction == 'right':
            self.loc[0] += 1
        if direction == 'down':
            self.loc[1] += 1

    def held_already(self):
        # すでにホールドされているか調べる関数．されていればTrue，そうでなければFalse
        block_index = 0  # ブロックのパターンが何かをまず調べ，わかったらそれを代入
        for y in self.pattern:
            for x in y:
                if x != 0:
                    block_index = x
                    break
            if block_index == 0:
                break
        if Block.hold2:
            Block.hold1 = Block.hold2
            pattern = self.pattern_create(block_index) #  今のブロックの種類に合わせてpatternを再生成
            Block.hold2 = pattern #  再生成したpatternはhold2に入れる
            return True
        else:
            # すでにホールドされているものはないのでhold1に移すものはない
            pattern = self.pattern_create(block_index)
            Block.hold2 = pattern
            return False

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_DOWN]:
            self.down_count += 1
            if self.down_count >= self.down_threshold:
                if not window.bottom_hit(self, 'drop'):
                    window.mapping(self, 'clear')
                    self.control('down')
                    # 自分が動かしたマス目分だけスコアに加算
                    window.score += 1
                    ghost.update()
                    window.ghost_hard_drop()
                    window.mapping(self, 'drop')
                else:
                    fixing = True
                self.down_count = 0

        if pressed[K_LEFT]:
            self.left_count += 1
            if self.left_count >= self.side_threshold:
                if not window.left_hit(self):
                    window.mapping(self, 'clear')
                    self.control('left')
                    window.mapping(ghost, 'clear')
                    ghost.update()
                    window.ghost_hard_drop()
                    window.mapping(self, 'drop')
                self.left_count = 0

        if pressed[K_RIGHT]:
            self.right_count += 1
            if self.right_count >= self.side_threshold:
                if not window.right_hit(self):
                    window.mapping(self, 'clear')
                    self.control('right')
                    window.mapping(ghost, 'clear')
                    ghost.update()
                    window.ghost_hard_drop()
                    window.mapping(self, 'drop')
                self.right_count = 0

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()

                if event.key == K_z:
                    rotate_sound.play()
                    window.mapping(block_instance, 'clear')
                    window.mapping(ghost, 'clear')
                    block_instance.rotate('left')
                    if window.rotate_hit(block_instance):
                        block_instance.rotate('right')
                    else:
                        fix_time = 0
                    ghost.update()
                    window.ghost_hard_drop()
                    window.mapping(block_instance, 'drop')

                if event.key == K_x:
                    rotate_sound.play()
                    window.mapping(block_instance, 'clear')
                    window.mapping(ghost, 'clear')
                    block_instance.rotate('right')
                    if window.rotate_hit(block_instance):
                        block_instance.rotate('left')
                    else:
                        fix_time = 0
                    ghost.update()
                    window.ghost_hard_drop()
                    window.mapping(block_instance, 'drop')

                if event.key == K_LSHIFT:
                    if holdable:
                        hold_sound.play()
                        window.mapping(block_instance, 'clear')
                        window.mapping(ghost, 'clear')
                        if block_instance.held_already():
                            block_instance = Block('hold')
                        else:
                            block_instance = Block('drop')
                        holdable = False
                        ghost.update()
                        window.ghost_hard_drop()
                        window.mapping(block_instance, 'drop')

                if event.key == K_UP:
                    hard_sound.play()
                    if window.hard_drop():
                        fixing = True
                        fix_time = 500

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

    def mapping(self, block, process):
        # ブロックインスタンスのパターンデータをフィールドに反映する関数
        field_x = block.loc[0] #  ブロックのパターン配列の一番左上のx座標．フィールド内で位置を表す
        field_y = block.loc[1] #  ブロックのパターン配列の一番左上のy座標．フィールド内で位置を表す
        pattern_len = len(block.pattern)
        end_x = field_x + pattern_len #  走査の終了位置のx座標
        end_y = field_y + pattern_len #  走査の終了位置のy座標

        if process == 'line_clear':
            cl_flag = False
            for y in self.lines:
                del Window._field[y]
                cl_flag = True
                Window._field.insert(2, [99, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 99])
            if cl_flag:
                clear_sound.play()

        if process == 'clear_effect':
            for y in self.lines:
                self._field[y] = [99, 99, 99, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 99, 99, 99]

        for y in range(field_y, end_y):
            for x in range(field_x, end_x):
                pattern_x = x - field_x #  パターン配列内でのx座標
                pattern_y = y - field_y #  パターン配列内でのy座標
                pattern_data = block.pattern[pattern_y][pattern_x]  # パターン配列の中を左上から右に向かって走査
                if pattern_data: #  0でない要素を見つけたら
                    #  各プロセスに応じてフィールドに代入するデータを決める
                    if process == 'drop':
                        Window._field[y][x] = pattern_data
                    elif process == 'clear':
                        Window._field[y][x] = 0
                    elif process == 'fix':
                        Window._field[y][x] = pattern_data + 10
                    elif process == 'ghost':
                        Window._field[y][x] = -1 * pattern_data

    # ブロック操作系メソッド
    @staticmethod
    def left_hit(block):
        # パターン配列内を左上から下方向に向かって走査し，
        # 0でない要素を見つけたらそのひとつ左隣に10を超える要素(障害物)があるかを調べる
        # 10を超える要素があったら(ぶつかっていたら)Trueを返し，なければFalseを返す
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
        # パターン配列内を右上から下方向に向かって走査し，
        # 0でない要素を見つけたらそのひとつ右隣に10を超える要素(障害物)があるかを調べる
        # 10を超える要素があったら(ぶつかっていたら)Trueを返し，なければFalseを返す
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
        # パターン配列内を左下から右方向に向かって走査し，
        # 0でない要素を見つけたらそのひとつ下に10を超える要素(障害物)があるかを調べる
        # 10を超える要素があったら(ぶつかっていたら)Trueを返し，なければFalseを返す
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
        shift_list = [] #  壁蹴り時に軸をどれだけシフトさせるかのリスト
        collision_list = [] #  各軸で衝突判定をした結果，障害物があれば99を要素として入れる

        # ブロックの状態に応じてどのシフトリストを使うかを決める
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

        # 上で決めたシフトリストの要素を1つずつ取り出して衝突判定をしていく
        # ぶつかっていればcollision_listに99を追加し，そうでなければ0を追加する
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
            # その軸について衝突判定が終わったら衝突リスト内に99があるかを調べる
            # なければその軸の位置で回転が可能なので軸のx，y座標をブロックの座標に足す
            # ブロックの状態を書き換えたらFalseを返しておわり
            if not 99 in collision_list:
                block.loc[0] += shift_axis[0]
                block.loc[1] += shift_axis[1]
                block.state[0] = block.state[1]
                return False
            # 99があった場合(ぶつかってしまう)場合はcollision_listを空にして次の軸で再度チェック
            collision_list = []
        #すべての軸で判定して衝突してしまう場合はreturnを返して終わり
        return True

    def hard_drop(self):
        # hd_flagがTrueの間だけbottom_hitと下移動を繰り返す
        # hitしたところでFalseにしてストップ
        hd_flag = True
        while hd_flag:
            if self.bottom_hit(block_instance, 'drop'):
                hd_flag = False
            else:
                self.mapping(block_instance, 'clear')
                block_instance.control('down')
                # 自分が動かしたマス目分だけスコアに加算
                self.score += 1
            #                window.mapping(mino, 'fix')
            #                window.line_check()
            #                window.mapping(mino, 'line_clear')
        return hd_flag

    @staticmethod
    def ghost_hard_drop():
        hd_flag = True
        while hd_flag:
            if window.bottom_hit(ghost_instance, 'drop'):
                hd_flag = False
                window.mapping(ghost, 'ghost')
            else:
                window.mapping(ghost_instance, 'clear')
                ghost.control('down')
                window.mapping(ghost, 'ghost')
        return True

    def line_check(self):
        self.lines = []
        for y in range(Window._field_height - 4, 2, -1):
            zero_count = Window._field[y].count(0)
            if zero_count == 0:
                self.lines.append(y)
            if zero_count == 10:
                break

    # スコア系メソッド
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

    # 描画系メソッド
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
        score_num = game_font.render(str(window.score), True, (255, 255, 255))
        screen.blit(score_num, (hold_left_margin, hold_top_margin + cell * 4))

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
        nexts_len = len(Block.next1) - 2
        for z in range(nexts_len):
            next_len = len(Block.next1[z])
            for y in range(next_len):
                for x in range(next_len):
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


class Ghost:
    def __init__(self):
        self.loc = copy.deepcopy(block_instance.loc)
        self.pattern = copy.deepcopy(block_instance.pattern)

    def update(self):
        self.loc = copy.deepcopy(block_instance.loc)
        self.pattern = copy.deepcopy(block_instance.pattern)

    def control(self, direct):
        if direct == 'left':
            self.loc[0] -= 1
        if direct == 'right':
            self.loc[0] += 1
        if direct == 'down':
            self.loc[1] += 1

class Player:
    def __init__(self):
# mainループ

# ブロック1つ(1マス)の大きさ
cell = 24

# PyGame初期化
pygame.init()
screen_size = (cell * 27, cell * 27)
screen = pygame.display.set_mode(screen_size)

# インスタンス生成
block_instance = Block('drop')
window = Window()
ghost = Ghost()
window.g_hard_drop()
window.mapping(block_instance, 'drop')

# フォント準備
sys_font = pygame.font.SysFont(None, 100)
game_font = pygame.font.SysFont(None, 40)
title1 = sys_font.render('Space to', True, (255, 255, 255))
title2 = sys_font.render('Start!', True, (255, 255, 255))
score_title = game_font.render('SCORE', True, (255, 255, 255))
hold = game_font.render('HOLD', True, (255, 255, 255))
next_title = game_font.render('NEXT', True, (255, 255, 255))

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
        window.g_hard_drop()
        window.mapping(block_instance, 'drop')
        fixed = False

    window.draw(screen)
    pygame.display.update()

    # 自由落下
    if drop_time >= 1000:
        if not window.bottom_hit(block_instance, 'drop'):
            window.mapping(block_instance, 'clear')
            block_instance.control('down')
            ghost.update()
            window.g_hard_drop()
            window.mapping(block_instance, 'drop')
        else:
            fixing = True
        drop_time = 0
    drop_time += time_passed
    # 自由落下ここまで


    # 固定処理 フラグがTrueのときだけ行う．0.5秒経ったら固定
    if fixing:
        if fix_time >= 500:
            if not window.bottom_hit(block_instance, 'drop'):
                fix_time = 0
            else:
                window.mapping(block_instance, 'fix')
                window.line_check()

                # 固定音処理
                fix_sound.play()

                # 固定描画処理
                if window.lines:
                    window.score_count()
                    window.mapping(block_instance, 'clear_effect')
                    window.draw(screen)
                    pygame.display.update()
                    pygame.time.wait(500)
                    window.mapping(block_instance, 'line_clear')
                    if not ren_flag:
                        ren_flag = True
                    elif ren_flag:
                        window.ren += 1
                elif not window.lines and ren_flag:
                    ren_flag = False
                    window.ren = 0
                    window.ren_credit = None
                window.ren_count()
                fixed = True
                holdable = True
                fixing = False
                fix_time = 0
        fix_time += time_passed
    # 固定処理ここまで



