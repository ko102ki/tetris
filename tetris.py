import sys
#  import os
#  import time
import pygame
from pygame.locals import *
from pprint import pprint
from random import randint
from math import sqrt


#  初期化処理 メインループもここ
def init():
    field_data = field_init()
    block_index = randint(0, 6)
    drop_block = block_init(block_index)
    drop_location = [4, 0]
    field_mapping(field_data, drop_block, drop_location)

    pygame.init()
    screen_size = (288, 552)
    screen = pygame.display.set_mode(screen_size)

    block_img = [[], [], [], [], [], [], [], []]
    block_img[0] = pygame.image.load('data/i.bmp')
    block_img[1] = pygame.image.load('data/o.bmp')
    block_img[2] = pygame.image.load('data/s.bmp')
    block_img[3] = pygame.image.load('data/z.bmp')
    block_img[4] = pygame.image.load('data/j.bmp')
    block_img[5] = pygame.image.load('data/l.bmp')
    block_img[6] = pygame.image.load('data/t.bmp')
    block_img[7] = pygame.image.load('data/w.bmp')

    draw_field(field_data, screen, block_img)

    while True:
        on_key_down_handler(field_data, drop_block, drop_location, screen, block_img)
        pygame.display.update()


# 壁を含むフィールド配列を作成
def field_init():
    return [[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0],
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


#  引数に応じてブロック配列を生成
def block_init(code):
    if code == 0:  # I
        return [[0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                ]
    elif code == 1:  # O
        return [[2, 2],
                [2, 2],
                ]
    elif code == 2:  # S
        return [[0, 3, 3],
                [3, 3, 0],
                [0, 0, 0],
                ]
    elif code == 3:  # Z
        return [[4, 4, 0],
                [0, 4, 4],
                [0, 0, 0],
                ]
    elif code == 4:  # J
        return [[5, 0, 0],
                [5, 5, 5],
                [0, 0, 0],
                ]
    elif code == 5:  # L
        return [[0, 0, 6],
                [6, 6, 6],
                [0, 0, 0],
                ]
    elif code == 6:  # T
        return [[0, 7, 0],
                [7, 7, 7],
                [0, 0, 0],
                ]


def set_block(data, block, loc, first=False):
    block_index = randint(0, 6)
    data = block_init(block_index)
    loc = [4, 0]
    field_mapping(data, block, loc)


# pygameでキーハンドラを設定
def on_key_down_handler(data, block, loc, screen, block_img):
    left = 'left'
    right = 'right'
    down = 'down'
    left_turn = 'left_turn'
    right_turn = 'right_turn'

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key == K_LEFT:
                block_control(left, data, block, loc, screen, block_img)
            if event.key == K_RIGHT:
                block_control(right, data, block, loc, screen, block_img)
            if event.key == K_DOWN:
                block_control(down, data, block, loc, screen, block_img)
            if event.key == K_z:
                block_control(left_turn, data, block, loc, screen, block_img)
            if event.key == K_x:
                block_control(right_turn, data, block, loc, screen, block_img)


# ブロックを動かす
# 移動後、回転後のブロックをシミュレートして何かにぶつかるかを判定
# 判定がFalseならfield_mapping()に引数clearで現在のブロックがあるフィールド上の箇所をすべて0に書き換え
# 移動or回転をさせてから再度field_mapping()をする。引数にclearはつけない
def block_control(direct, data, block, loc, screen, block_img):
    # 移動
    if direct == 'left':
        if get_left_hit(data, block, loc):
            return True
        field_mapping(data, block, loc, 'clear')
        loc[0] -= 1
        #  Iミノ用の処理
        if loc[0] < 0:
            size_reduction(block, loc)

    if direct == 'right':
        if get_right_hit(data, block, loc):
            return True
        field_mapping(data, block, loc, 'clear')
        loc[0] += 1

    if direct == 'down':
        if get_bottom_hit(data, block, loc):
            field_mapping(data, block, loc, 'fixed')
            set_block(data, block, loc)
        field_mapping(data, block, loc, 'clear')
        loc[1] += 1

    # 回転
    if direct == 'left_turn':
        if get_rotate_hit(direct, data, block, loc):
            return True
        field_mapping(data, block, loc, 'clear')  # block内の要素をすべて0にする
        # 左の壁際用
        if loc[0] == 0:
            loc[0] += 1
        # 右の壁際用
        if loc[0] + len(block[0]) == 12:
            loc[0] -= 1
        if loc[0] + len(block[0]) > 12:
            loc[0] -= 2
        block_rotate(direct, block)

    if direct == 'right_turn':
        if get_rotate_hit(direct, data, block, loc):
            return True
        field_mapping(data, block, loc, 'clear')  # block内の要素をすべて0にする
        # 左の壁際用
        if loc[0] == 0:
            loc[0] += 1
        # 右の壁際用
        if loc[0] + len(block[0]) == 12:
            loc[0] -= 1
        if loc[0] + len(block[0]) > 12:
            loc[0] -= 2
        block_rotate(direct, block)

    # フィールドに反映後、画面描画
    field_mapping(data, block, loc)
    draw_field(data, screen, block_img)

    return False


# ブロックを回転させる
# 回転方向directに応じてblockを回転させてpattern_buffに代入
# pattern_buffを再度blockに代入して返す
def block_rotate(direct, block):
    block_size = len(block)
    pattern_buff = [[0 for col in range(block_size)] for row in range(block_size)]

    if direct == 'left_turn':
        # 左回転
        for y in range(block_size):
            for x in range(block_size):
                pattern_buff[block_size - 1 - x][y] = block[y][x]

    if direct == 'right_turn':
        # 右回転
        for y in range(block_size):
            for x in range(block_size):
                pattern_buff[x][block_size - 1 - y] = block[y][x]

    for y in range(block_size):
        for x in range(block_size):
            block[y][x] = pattern_buff[y][x]


def size_reduction(block, loc):
    for x in range(4):
        block[x].reverse()
    loc[0] = 0


# 各方向に移動、回転した場合に何かに接触するかを確認
# 接触する場合はTrueを返す
def get_left_hit(data, block, loc):
    block_len = len(block)
    for x in range(block_len):
        for y in range(block_len):
            if block[y][x]:
                fx = loc[0] + x
                fy = loc[1] + y
                if data[fy][fx - 1] > 10:
                    return True
    return False


def get_right_hit(data, block, loc):
    block_len = len(block)
    for x in range(block_len - 1, -1, -1):
        for y in range(block_len):
            if block[y][x]:
                fx = loc[0] + x
                fy = loc[1] + y
                if data[fy][fx + 1] > 10:
                    return True
    return False


def get_bottom_hit(data, block, loc):
    block_len = len(block)
    for y in range(block_len - 1, -1, -1):
        for x in range(block_len):
            if block[y][x]:
                fx = loc[0] + x
                fy = loc[1] + y
                if data[fy + 1][fx] > 10:
                    return True
    return False


# 現在のblockのコピーpattern_buffを作成
# 壁際で回転させようとすると壁より1マス内側に入ってから回転できるかを判定する
# その際に変数reviseを使用
def get_rotate_hit(direct, data, block, loc):
    block_len = len(block)
    pattern_buff = [[0 for col in range(block_len)] for row in range(block_len)]
    revise = 0

    for y in range(block_len):
        for x in range(block_len):
            pattern_buff[y][x] = 0

    for y in range(block_len):
        for x in range(block_len):
            pattern_buff[y][x] = block[y][x]

    # 壁蹴り用の処理
    # 左の壁際
    if loc[0] == 0:
        revise = 1
    # 右の壁際
    if loc[0] + block_len == 12:
        revise = -1
    # 右の壁際(Iミノ)
    if loc[0] + block_len > 12:
        revise = -2

    block_rotate(direct, pattern_buff)

    for y in range(block_len):
        for x in range(block_len):
            if pattern_buff[y][x]:
                fx = loc[0] + x + revise
                fy = loc[1] + y
                if data[fy][fx] > 10:
                    return True
    return False


# block配列をdata配列に反映する
# 引数clearがTrueならblock配列内の要素をすべて0にする
def field_mapping(data, block, loc, process='drop'):
    block_size = len(block)
    loc_x = loc[0]
    loc_y = loc[1]
    end_x = loc_x + block_size  # y軸走査の終了位置
    end_y = loc_y + block_size  # x軸走査の終了位置

    for y in range(loc_y, end_y):
        for x in range(loc_x, end_x):
            px = x - loc_x
            py = y - loc_y
            code = block[py][px]
            if code:
                if process == 'clear':
                    data[y][x] = 0
                elif process == 'fixed':
                    data[y][x] = code + 10
                else:
                    data[y][x] = code


# 画面描画
# data配列の要素を順番に描画していく
def draw_field(data, screen, block_img):
    screen.fill((0, 0, 0))
    for y in range(23):
        for x in range(12):
            code = data[y][x]
            if code == 0:
                sys.stdout.write('0')
            elif code == 99:
                screen.blit(block_img[7], (x * 24, y * 24))
                sys.stdout.write('9')
            elif code == 1 or code == 11:
                screen.blit(block_img[0], (x * 24, y * 24))
                sys.stdout.write('1')
            elif code == 2 or code == 12:
                screen.blit(block_img[1], (x * 24, y * 24))
                sys.stdout.write('1')
            elif code == 3 or code == 13:
                screen.blit(block_img[2], (x * 24, y * 24))
                sys.stdout.write('1')
            elif code == 4 or code == 14:
                screen.blit(block_img[3], (x * 24, y * 24))
                sys.stdout.write('1')
            elif code == 5 or code == 15:
                screen.blit(block_img[4], (x * 24, y * 24))
                sys.stdout.write('1')
            elif code == 6 or code == 16:
                screen.blit(block_img[5], (x * 24, y * 24))
                sys.stdout.write('1')
            elif code == 7 or code == 17:
                screen.blit(block_img[6], (x * 24, y * 24))
                sys.stdout.write('1')
        print('')


init()
