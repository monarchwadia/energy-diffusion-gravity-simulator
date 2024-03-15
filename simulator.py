import sys
import pygame
from pygame.locals import *
import numpy as np
from GravitationalField import GravitationalField
from constants import CELL_HEIGHT, CELL_WIDTH, G, MAP_HEIGHT, MAP_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
from update_cell import update_cell

# Pygame setup --------------------------------------------------------------------------

pygame.init()

color_fg = pygame.Color(190, 190, 190)
color_bg = pygame.Color(30, 30, 30)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(color_bg)

clock = pygame.time.Clock()
clock.tick(60)

# 2D Array --------------------------------------------------------------------------

arr = np.random.uniform(low=0.0, high=1.0, size=(MAP_WIDTH, MAP_HEIGHT))
# arr = np.zeros((MAP_WIDTH, MAP_HEIGHT))
# arr = np.random.vonmises(0, 1, (MAP_WIDTH, MAP_HEIGHT))


count = 0


def generate_next_arr(old_arr):
    next_arr = np.copy(old_arr)
    gf = GravitationalField(old_arr, G)
    for x in range(0, MAP_WIDTH):
        for y in range(0, MAP_HEIGHT):
            update_cell(gf, next_arr, x, y)

    return next_arr


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update
    arr = generate_next_arr(arr)

    if True:
        screen.fill(color_bg)
        for x in range(0, MAP_WIDTH):
            for y in range(0, MAP_HEIGHT):
                val = arr[x][y]

                hsva_color = pygame.color.Color(0, 0, 0, 0)
                try:
                    hsva_color.hsva = (val * 360, val * 50, val * 100, 100)
                except Exception as e:
                    if val >= 1:
                        hsva_color.hsva = (275, 100, 100, 100)
                    else:
                        hsva_color.hsva = (0, 0, 0, 0,)
                    # print(val)
                    pass

                try:
                    screen.fill(hsva_color, (x * CELL_WIDTH,
                                y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
                except Exception as e:
                    # print(e)
                    # print("Error occurred at", x, y, "and the value was", val)
                    pass

    # stats
    total = np.sum(arr)
    pygame.display.set_caption(f"Total energy: {total}")

    pygame.display.update()
    clock.tick(60)
