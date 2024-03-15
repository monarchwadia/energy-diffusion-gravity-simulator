from GravitationalField import GravitationalField
from constants import G, MAP_HEIGHT, MAP_WIDTH, R

neighbors: list[tuple[int, int]] = [
    (-1, -1),  (0, -1),   (1, -1),
    (-1, 0),              (1, 0),
    (-1, 1),   (0, 1),    (1, 1)
]


def update_cell(gf: GravitationalField, next_arr: list[list[float]], x: int, y: int):
    # e1 is the old energy of this node
    # e2 is the new energy of this node
    # o is outflowing amount of energy
    # ne1 is the old energy of the neighbour
    # ne2 is the new energy of the neighbour
    # t is the transfer ratio

    for dx, dy in neighbors:
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
        return

    differential = next_arr[x][y] - \
        next_arr[grav_neighbor[0]][grav_neighbor[1]]
    if differential < 0:
        differential = next_arr[x][y]

    next_arr[x][y] -= differential * G
    next_arr[grav_neighbor[0]][grav_neighbor[1]] += differential * G
