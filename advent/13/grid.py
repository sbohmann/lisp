from functools import cmp_to_key


class Grid:
    def __init__(self, rail_map, vehicles, vehicle_map):
        self._initialize_configuration()
        self._setup_state(rail_map, vehicle_map, vehicles)

    def _setup_state(self, rail_map, vehicle_map, vehicles):
        self._rail_map = rail_map
        self._vehicles = vehicles
        self._vehicle_map = vehicle_map
        self._removed_vehicles = set()

    def _initialize_configuration(self):
        self._remove_colliding_vehicles = False
        self._err_on_single_vehicle = False

    def remove_colliding_vehicles(self):
        self._remove_colliding_vehicles = True

    def err_on_single_vehicle(self):
        self._err_on_single_vehicle = True

    def step(self):
        self._check_against_no_vehicles_left()
        self._sort_vehicles_by_position()
        self._move_vehicles()
        self._report_single_vehicle()

    def _check_against_no_vehicles_left(self):
        if len(self._vehicles) == 0:
            raise ValueError('No vehicles left')

    def _sort_vehicles_by_position(self):
        self._vehicles.sort(key=cmp_to_key(compare_vehicle_positions))

    def _move_vehicles(self):
        for vehicle in self._vehicles.copy():
            if vehicle not in self._removed_vehicles:
                self._move_vehicle(vehicle)
                self._change_vehicle_direction(vehicle)

    def _report_single_vehicle(self):
        if self._err_on_single_vehicle and len(self._vehicles) == 1:
            last_vehicle = self._vehicles[0]
            raise ValueError('Single Vehicle at x:' + str(last_vehicle.x) + ', y: ' + str(last_vehicle.y))

    def _move_vehicle(self, vehicle):
        self._remove_vehicle_from_map(vehicle)
        vehicle.move()
        self._add_vehicle_to_map(vehicle)

    def _change_vehicle_direction(self, vehicle):
        self._rail_map[vehicle.y][vehicle.x].change_vehicle_direction(vehicle)

    def _remove_vehicle_from_map(self, vehicle):
        self._vehicle_map[vehicle.y][vehicle.x] = None

    def _add_vehicle_to_map(self, vehicle):
        if not self._detect_collision(vehicle):
            self._vehicle_map[vehicle.y][vehicle.x] = vehicle

    def _detect_collision(self, vehicle):
        vehicle_in_position = self._vehicle_map[vehicle.y][vehicle.x]
        removed = False
        if vehicle_in_position is not None:
            if self._remove_colliding_vehicles:
                self._remove_vehicle(vehicle)
                self._remove_vehicle(vehicle_in_position)
                removed = True
            else:
                raise ValueError('Collision at x: ' + str(vehicle.x) + ', y: ' + str(vehicle.y))
        return removed

    def _remove_vehicle(self, vehicle):
        self._vehicles.remove(vehicle)
        self._removed_vehicles.add(vehicle)
        self._vehicle_map[vehicle.y][vehicle.x] = None


def compare_vehicle_positions(a, b):
    if a.y < b.y:
        return -1
    elif a.y > b.y:
        return 1
    elif a.x < b.x:
        return -1
    elif a.x > b.x:
        return 1
    else:
        return 0
