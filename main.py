import pygame
import random

from constants import *

pygame.init()


matrix = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

block = [[0 for _ in range(4)] for _ in range(4)]
block_row = 0
block_col = 3
block_type = 0
block_rotation = 0
block_tick = 0
new_block = True

block_time = 10

key_up = False
key_down = False
key_left = False
key_right = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()


def render_square(row, col, color):
    x = GRID_X + col * (GRID_WIDTH + 1)
    y = GRID_Y + row * (GRID_WIDTH + 1)
    pygame.draw.rect(screen, color,
                     (x, y, GRID_WIDTH, GRID_WIDTH))


def render_grid():
    for i in range(ROWS):
        for j in range(COLUMNS):
            render_square(i, j, BLOCK_COLORS[matrix[i][j]])


def render_block():
    for i in range(4):
        for j in range(4):
            if block[i][j]:
                render_square(block_row + i, block_col +
                              j, BLOCK_COLORS[block_type + 1])


def render():
    screen.fill(BACKGROUND_COLOR)
    render_grid()
    render_block()
    pygame.display.update()


def create_new_block():
    global block, block_row, block_col, block_type, block_rotation, new_block, block_tick

    block_type = random.randint(0, BLOCK_TYPES - 1)
    block_rotation = 0
    block_row = -2
    if block_type == 0:
        block_row += 1
    block_col = 3
    block_tick = 0
    block = ROTATIONS[block_type][block_rotation].copy()
    new_block = False


def move_allowed():
    for i in range(4):
        for j in range(4):
            if not block[i][j]:
                continue
            row = block_row + i
            col = block_col + j
            if row >= ROWS or col >= COLUMNS or col < 0:
                return False
            if matrix[row][col]:
                return False
    return True


def clear_lines():
    cleared = 0
    for i in range(ROWS - 1, -1, -1):
        filled = True
        for j in range(COLUMNS):
            if matrix[i][j] == 0:
                filled = False
                break
        if filled:
            matrix[i] = [0 for _ in range(COLUMNS)]
            cleared += 1
        elif cleared > 0:
            matrix[i+cleared] = matrix[i].copy()
            matrix[i] = [0 for _ in range(COLUMNS)]


def settle_block():
    for i in range(4):
        for j in range(4):
            if not block[i][j]:
                continue
            row = block_row + i
            col = block_col + j
            matrix[row][col] = block_type + 1
    clear_lines()


def block_fall():
    global block_row, new_block
    block_row += 1
    if not move_allowed():
        block_row -= 1
        settle_block()
        new_block = True


def rotate_block():
    global block, block_rotation

    max_rotate = len(ROTATIONS[block_type])
    block_rotation += 1
    if block_rotation >= max_rotate:
        block_rotation = 0

    block = ROTATIONS[block_type][block_rotation].copy()

    if not move_allowed():
        block_rotation -= 1
        if block_rotation < 0:
            block_rotation = max_rotate - 1

    block = ROTATIONS[block_type][block_rotation].copy()


def move_block():
    global block_col, block_row

    if key_left:
        block_col -= 1
    if key_right:
        block_col += 1
    if key_down:
        block_row += 1

    if not move_allowed():
        if key_left:
            block_col += 1
        if key_right:
            block_col -= 1
        if key_down:
            block_row -= 1


def update():
    global block_tick

    if new_block:
        create_new_block()
    else:
        block_tick += 1
        if block_tick >= block_time:
            block_tick = 0
            block_fall()

        if key_up:
            rotate_block()

        if key_left or key_right or key_down:
            move_block()


run = True

while run:
    clock.tick(FPS)

    key_up = False
    key_down = False
    key_left = False
    key_right = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                key_up = True
            elif event.key == pygame.K_DOWN:
                key_down = True
            elif event.key == pygame.K_LEFT:
                key_left = True
            elif event.key == pygame.K_RIGHT:
                key_right = True
    render()
    update()

pygame.quit()
