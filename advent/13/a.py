from grid_reader import GridReader
from itertools import count


def run():
    grid = GridReader().result
    grid.remove_colliding_vehicles()
    grid.err_on_single_vehicle()
    for step in count(1):
        try:
            grid.step()
        except ValueError as error:
            print('Error at step', step, '-', error)
            break


run()
