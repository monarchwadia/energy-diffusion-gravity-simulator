import sys
from time import sleep
import pygame
from pygame.locals import *
import numpy as np

MAP_WIDTH = 30
MAP_HEIGHT = 30

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

CELL_WIDTH = SCREEN_WIDTH / MAP_WIDTH
CELL_HEIGHT = SCREEN_HEIGHT / MAP_HEIGHT

MAX_DIFFERENTIAL = 8

pygame.init()

color_fg = pygame.Color(190, 190, 190)
color_bg = pygame.Color(30, 30, 30)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(color_bg)

clock = pygame.time.Clock()
clock.tick(60)


# class Ball(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.rect = pygame.Rect(50, 50, 100, 100)

#     def update(self):
#         self.rect.x = self.rect.x + norm.rvs()
#         self.rect.y = self.rect.y + norm.rvs()

#     def draw(self):
#         pygame.draw.rect(screen, color_fg, self.rect)


# b = Ball()

arr = np.zeros((MAP_WIDTH, MAP_HEIGHT))
arr[MAP_WIDTH // 2][MAP_HEIGHT // 2] = 1

neighbors = [
    (-1, -1, 1.0),  (0, -1, 1.0),   (1, -1, 1.0),
    (-1, 0, 1.0),   (0, 0, 0),      (1, 0, 1.0),
    (-1, 1, 1.0),   (0, 1, 1.0),    (1, 1, 1.0)
]


def generate_next_arr(old_arr):
    next_arr = np.zeros((MAP_WIDTH, MAP_HEIGHT))
    for x in range(0, MAP_WIDTH):
        for y in range(0, MAP_HEIGHT):
            cell_energy = old_arr[x][y]

            neighbour_count = 0
            neighbourhood_energy = 0

            for dx, dy, weight in neighbors:
                if (
                    x + dx < 0
                    or x + dx >= MAP_WIDTH
                    or y + dy < 0
                    or y + dy >= MAP_HEIGHT
                ):
                    continue

                neighbour_count += 1
                neighbor_energy = old_arr[x + dx][y + dy]
                neighbourhood_energy += neighbor_energy

            old = cell_energy
            mean = neighbourhood_energy / neighbour_count
            new = mean - ((old - mean) * 0.5)

            next_arr[x][y] = min(max(new, 0), 1)

            # mean = neighbourhood_energy / neighbour_count

            # diff = cell_energy - mean
            # overshoot = (1 - mean) * (diff )

            # next_arr[x][y] = min(
            #     1.0, max(0.0, cell_energy + (diff + overshoot)))
    return next_arr


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # diffusion
    arr = generate_next_arr(arr)
    print("GEN")

    # Paint
    screen.fill(color_bg)
    for x in range(0, MAP_WIDTH):
        for y in range(0, MAP_HEIGHT):
            val = arr[x][y]
            color_base = 20
            color = ((255 - color_base) * val) + color_base
            print(val)
            screen.fill((color, color, color), (x * CELL_WIDTH,
                        y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

    # stats
    total = np.sum(arr)
    pygame.display.set_caption(f"Total: {total}")

    pygame.display.update()
    clock.tick(15)
