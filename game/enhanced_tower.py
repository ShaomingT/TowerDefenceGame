from tower import AbstractTower, SimpleTower, AbstractObstacle
import math
from typing import Union
from enemy import AbstractEnemy
from range_ import DonutRange
from utilities import euclidean_distance, rotate_toward, angle_between, polar_to_rectangular

__author__ = "Alex Teng"


class Energy(AbstractObstacle):
    """A simple projectile fired from a MissileTower"""
    name = "Energy"
    colour = '#6699ff'  # blue

    rotation_threshold = (1 / 3) * math.pi

    def __init__(self, position, cell_size, target: AbstractEnemy, size=.1,
                 rotation: Union[int, float] = 0, grid_speed=.5, damage=15):
        super().__init__(position, (size, 0), cell_size, grid_speed=grid_speed, rotation=rotation, damage=damage)
        self.target = target

    def step(self, units):
        """Performs a time step for this missile

        Moves towards target and damages if collision occurs
        If target is dead, this missile expires

        Parameters:
            units.enemies (UnitManager): The unit manager to select targets from

        Return:
            (persist, new_obstacles) pair, where:
                - persist (bool): True if the obstacle should persist in the game (else will be removed)
                - new_obstacles (list[AbstractObstacle]): A list of new obstacles to add to the game, or None
        """
        if self.target.is_dead():
            return False, None

        # move toward the target
        radius = euclidean_distance(self.position, self.target.position)

        if radius <= self.speed:
            self.target.damage(self.damage, 'energy')
            return False, None

        # Rotate toward target and move
        angle = angle_between(self.position, self.target.position)
        self.rotation = rotate_toward(self.rotation, angle, self.rotation_threshold)

        dx, dy = polar_to_rectangular(self.speed, self.rotation)
        x, y = self.position
        self.position = x + dx, y + dy

        return True, None


class EnergyTower(SimpleTower):
    """A tower that fires energy that track a target"""
    name = 'Energy Tower'
    colour = '#1073A1'

    cool_down_steps = 8

    base_cost = 200
    level_cost = 180

    range = DonutRange(1.5, 4.5)
    rotation_threshold = (1 / 3) * math.pi

    def __init__(self, cell_size: int, grid_size=(.9, .9), rotation=math.pi * .25, base_damage=150, level: int = 1):
        super().__init__(cell_size, grid_size=grid_size, rotation=rotation, base_damage=base_damage, level=level)

        self._target: AbstractEnemy = None

    def _get_target(self, units) -> Union[AbstractEnemy, None]:
        """Returns previous target, else selects new one if previous is invalid

        Invalid target is one of:
            - dead
            - out-of-range

        Return:
            AbstractEnemy: Returns previous target, unless it is non-existent or invalid (see above),
                           Otherwise, selects & returns new target if a valid one can be found,
                           Otherwise, returns None
        """
        if self._target is None \
                or self._target.is_dead() \
                or not self.is_position_in_range(self._target.position):
            self._target = self.get_unit_in_range(units)

        return self._target

    def step(self, units):
        """Rotates toward 'target' and fires missile if possible"""
        self.cool_down.step()

        target = self._get_target(units.enemies)

        if target is None:
            return None

        # Rotate toward target
        angle = angle_between(self.position, target.position)
        partial_angle = rotate_toward(self.rotation, angle, self.rotation_threshold)

        self.rotation = partial_angle

        if angle != partial_angle or not self.cool_down.is_done():
            return None

        self.cool_down.start()

        # Spawn energy on tower

        energy = Energy(self.position, self.cell_size, target, rotation=self.rotation,
                        damage=self.get_damage(), grid_speed=.3)

        # Move missile to outer edge of tower
        radius = self.grid_size[0] / 2
        delta = polar_to_rectangular(self.cell_size * radius, partial_angle)
        energy.move_by(delta)

        return [energy]


class Gravity(AbstractObstacle):
    """A simple projectile fired from a MissileTower"""
    name = "Gravity"
    colour = ['black', 'white']  # blue
    layer = 0
    rotation_threshold = (1 / 3) * math.pi

    def __init__(self, position, cell_size, targets, size=.1,
                 rotation: Union[int, float] = 0, grid_speed=.5, damage=15):
        super().__init__(position, (size, 0), cell_size, grid_speed=grid_speed, rotation=rotation, damage=damage)
        self.targets = targets

    def step(self, units):
        """Performs a time step for this gravity
            Wipe out all the targets in blazae towers' range
        Parameters:
            units.enemies (UnitManager): The unit manager to select targets from

        Return:
            (persist, new_obstacles) pair, where:
                - persist (bool): True if the obstacle should persist in the game (else will be removed)
                - new_obstacles (list[AbstractObstacle]): A list of new obstacles to add to the game, or None
        """

        for t in self.targets:
            t.damage(self.damage, 'gravity')

        if self.layer >= 20:
            return False, None

        self.layer += 1

        # print(self.layer)

        return True, None


class BlazarTower(AbstractTower):
    """A tower that cause a gravity filed the wipe out all the enemies in range."""
    name = 'Blazar Tower'
    colour = '#000099'
    # Blazar tower is a disposable tower.
    cool_down_steps = 99999999999999

    base_cost = 5000
    level_cost = 999999999999999

    range = DonutRange(1, 3.5)

    rotation_threshold = (1 / 3) * math.pi
    num = 1

    def __init__(self, cell_size: int, grid_size=(.9, .9), rotation=math.pi * .25, base_damage=999, level: int = 1):
        super().__init__(cell_size, grid_size=grid_size, rotation=rotation, base_damage=base_damage, level=level)

        self._target: AbstractEnemy = None

    def step(self, units):
        """Wipe out all the enemies in range"""
        targets = self.get_units_in_range(units.enemies)

        if targets is None:
            return None

        if not self.cool_down.is_done():
            return None

        self.cool_down.start()
        # Spawn gravity on tower
        gravity = Gravity(self.position, self.cell_size, targets, rotation=self.rotation,
                          damage=self.get_damage(), grid_speed=.3)

        self.cool_down.step()

        return [gravity]
