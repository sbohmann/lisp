from grid_reader import GridReader
from itertools import count


def run():
    a()
    b()


def a():
    grid = GridReader().result
    step_through(grid)


def b():
    grid = GridReader().result
    grid.remove_colliding_vehicles()
    grid.err_on_single_vehicle()
    step_through(grid)


def step_through(grid):
    for step in count(1):
        try:
            grid.step()
        except ValueError as error:
            print('Error at step', step, '-', error)
            break


run()
