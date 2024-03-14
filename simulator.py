import sys
from time import sleep
import pygame
from pygame.locals import *
import numpy as np

from GravitationalField import GravitationalField

MAP_WIDTH = 50
MAP_HEIGHT = 50

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

arr = np.random.uniform(low=0.0, high=1.0, size=(MAP_WIDTH, MAP_HEIGHT))
# arr = np.zeros((MAP_WIDTH, MAP_HEIGHT))
# arr = np.random.vonmises(0, 1, (MAP_WIDTH, MAP_HEIGHT))
arr[0][0] = 1
# arr[0][1] = 1
# arr[0][2] = 1
# arr[1, 0] = 1
# arr[1, 1] = 1
# arr[1, 2] = 1
# arr[2, 0] = 1
# arr[2, 1] = 1
arr[2, 2] = 1

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
            # R is exchange rate
            # e1 is the old energy of this node
            # e2 is the new energy of this node
            # o is outflowing amount of energy
            # ne1 is the old energy of the neighbour
            # ne2 is the new energy of the neighbour
            # t is the transfer ratio

            R = 0.01
            G = 0.2

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

            vector = gf.get_vector_at_point(x, y)
            # get which neighbor this vector points to
            # and transfer energy to that neighbor

            neighbor = (x + int(vector[0]), y + int(vector[1]))
            if (
                neighbor[0] < 0
                or neighbor[0] >= MAP_WIDTH
                or neighbor[1] < 0
                or neighbor[1] >= MAP_HEIGHT
            ):
                continue

            differential = next_arr[x][y] - next_arr[neighbor[0]][neighbor[1]]
            if differential < 0:
                differential = next_arr[x][y]

            next_arr[x][y] -= differential * G
            next_arr[neighbor[0]][neighbor[1]] += differential * G

            # # distribution should be proportional to the difference in energy

            # total_transferred = 0
            # for dx, dy, diff in donees:
            #     t = diff / donee_diff_sum
            #     new_amount = next_arr[dx][dy] + (o * t)
            #     next_arr[dx][dy] = total_transferred = new_amount

            #     # check if we have overshoot
            #     if total_transferred > 1:
            #         surplus = total_transferred - 1
            #         next_arr[dx][dy] = 1
            #         next_arr[x][y] += surplus
            #         total_transferred -= surplus

            #     print("total transferred", total_transferred)

            # mean = neighbourhood_energy / neighbour_count

            # diff = cell_energy - mean
            # overshoot = (1 - mean) * (diff )

            # next_arr[x][y] = min(
            #     1.0, max(0.0, cell_energy + (diff + overshoot)))
    # always add energy in the center
    # next_arr[MAP_WIDTH // 2][MAP_HEIGHT // 2] = 1
    # next_arr[MAP_WIDTH // 3][MAP_HEIGHT // 3] = 1
    # next_arr[MAP_WIDTH // 4][MAP_HEIGHT // 4] = 1

    return next_arr


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # diffusion
    arr = generate_next_arr(arr)
    # print("GEN")

    # Paint
    count += 1
    if count % 10 == 0:
        count = 0
        screen.fill(color_bg)
        for x in range(0, MAP_WIDTH):
            for y in range(0, MAP_HEIGHT):
                val = arr[x][y]
                color_base = 20
                color = ((255 - color_base) * val) + color_base
                # print(val)

                try:
                    screen.fill((color, color, color), (x * CELL_WIDTH,
                                y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
                except Exception as e:
                    print(e)
                    print("Error occurred at", x, y, "and the value was", val)

    # stats
    total = np.sum(arr)
    pygame.display.set_caption(f"Total energy: {total}")

    pygame.display.update()
    clock.tick(60)
