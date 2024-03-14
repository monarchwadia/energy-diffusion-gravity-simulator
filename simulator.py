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

# arr = np.random.uniform(low=0.0, high=1.0, size=(MAP_WIDTH, MAP_HEIGHT))
arr = np.zeros((MAP_WIDTH, MAP_HEIGHT))
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
    for x in range(0, MAP_WIDTH):
        for y in range(0, MAP_HEIGHT):
            # R is exchange rate
            # e1 is the old energy of this node
            # e2 is the new energy of this node
            # o is outflowing amount of energy
            # ne1 is the old energy of the neighbour
            # ne2 is the new energy of the neighbour
            # t is the transfer ratio

            R = 0.1
            e1 = next_arr[x][y]

            o = R * e1
            next_arr[x][y] = e1 - o

            donee_diff_sum = 0
            donees = []
            for dx, dy, weight in neighbors:
                if (
                    x + dx < 0
                    or x + dx >= MAP_WIDTH
                    or y + dy < 0
                    or y + dy >= MAP_HEIGHT
                ):
                    continue

                ne1 = next_arr[x + dx][y + dy]

                if ne1 < e1:
                    diff = e1 - ne1
                    donees.append((x + dx, y + dy, diff))
                    donee_diff_sum += diff

            # distribution should be proportional to the difference in energy

            total_transferred = 0
            for dx, dy, diff in donees:
                t = diff / donee_diff_sum
                new_amount = next_arr[dx][dy] + (o * t)
                next_arr[dx][dy] = total_transferred = new_amount

                # check if we have overshoot
                if total_transferred > 1:
                    surplus = total_transferred - 1
                    next_arr[dx][dy] = 1
                    next_arr[x][y] += surplus
                    total_transferred -= surplus

                print("total transferred", total_transferred)

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
                screen.fill((color, color, color), (x * CELL_WIDTH,
                            y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

    # stats
    total = np.sum(arr)
    pygame.display.set_caption(f"Total: {total}")

    pygame.display.update()
    clock.tick(60)
