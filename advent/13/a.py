from grid import Grid
from itertools import count


def run():
    grid = Grid()
    grid.remove_colliding_vehicles()
    grid.err_on_single_vehicle()
    for step in count(1):
        try:
            grid.step()
        except ValueError as error:
            print('Error at step', step, '-', error)
            raise error


run()
