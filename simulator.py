import sys
import pygame
from pygame.locals import *
import numpy as np
from GravitationalField import GravitationalField

# Constants --------------------------------------------------------------------------

# R is the diffusion exchange rate between cells of different energy levels
# G is the gravitational constant
R = 0.01
G = 0.2  # TODO: Make sure this is the same as in GravitationalField.py

MAP_WIDTH = 250
MAP_HEIGHT = 250

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

CELL_WIDTH = SCREEN_WIDTH / MAP_WIDTH
CELL_HEIGHT = SCREEN_HEIGHT / MAP_HEIGHT

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

neighbors = [
    (-1, -1, 1.0),  (0, -1, 1.0),   (1, -1, 1.0),
    (-1, 0, 1.0),   (0, 0, 0),      (1, 0, 1.0),
    (-1, 1, 1.0),   (0, 1, 1.0),    (1, 1, 1.0)
]

count = 0


def generate_next_arr(old_arr):
    next_arr = np.copy(old_arr)
    gf = GravitationalField(old_arr)
    for x in range(0, MAP_WIDTH):
        for y in range(0, MAP_HEIGHT):
            # e1 is the old energy of this node
            # e2 is the new energy of this node
            # o is outflowing amount of energy
            # ne1 is the old energy of the neighbour
            # ne2 is the new energy of the neighbour
            # t is the transfer ratio

            for dx, dy, weight in neighbors:
                if (
                    x + dx < 0
                    or x + dx >= MAP_WIDTH
                    or y + dy < 0
                    or y + dy >= MAP_HEIGHT
                ):
                    continue

                e = next_arr[x][y]
                n = next_arr[x + dx][y + dy]

                if abs(e-n) < R:
                    continue

                if e > n:
                    next_arr[x][y] -= R
                    next_arr[x + dx][y + dy] += R
                else:
                    next_arr[x][y] += R
                    next_arr[x + dx][y + dy] -= R

            # get which neighbor this gravity_vector points to
            # and transfer energy to that grav_neighbor
            gravity_vector = gf.get_vector_at_point(x, y)
            grav_neighbor = (
                x + int(gravity_vector[0]), y + int(gravity_vector[1]))
            if (
                grav_neighbor[0] < 0
                or grav_neighbor[0] >= MAP_WIDTH
                or grav_neighbor[1] < 0
                or grav_neighbor[1] >= MAP_HEIGHT
            ):
                continue

            differential = next_arr[x][y] - \
                next_arr[grav_neighbor[0]][grav_neighbor[1]]
            if differential < 0:
                differential = next_arr[x][y]

            next_arr[x][y] -= differential * G
            next_arr[grav_neighbor[0]][grav_neighbor[1]] += differential * G

    return next_arr


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update
    arr = generate_next_arr(arr)

    # Paint
    # count += 1
    # if count % 10 == 0:
    #     count = 0
    if True:
        screen.fill(color_bg)
        for x in range(0, MAP_WIDTH):
            for y in range(0, MAP_HEIGHT):
                val = arr[x][y]
                color_base = 20
                color = ((255 - color_base) * val) + color_base

                hsva_color = pygame.color.Color(0, 0, 0, 0)
                try:
                    hsva_color.hsva = (val * 360, val * 50, val * 100, 100)
                except Exception as e:
                    pass
                # print(val)

                try:
                    screen.fill(hsva_color, (x * CELL_WIDTH,
                                y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
                except Exception as e:
                    print(e)
                    print("Error occurred at", x, y, "and the value was", val)

    # stats
    total = np.sum(arr)
    pygame.display.set_caption(f"Total energy: {total}")

    pygame.display.update()
    clock.tick(60)
