import math
from tower import AbstractTower, SimpleTower, AbstractObstacle
from enemy import AbstractEnemy, SimpleEnemy
from level import AbstractLevel
from range_ import AbstractRange, CircularRange, PlusRange, DonutRange

from utilities import Countdown, euclidean_distance, angular_difference, normalise_vector, rotate_point, rotate_toward, \
    angle_between, rectangles_intersect, get_delta_through_centre
import math
from typing import Union

from core import Unit, Point2D, UnitManager
from enemy import AbstractEnemy
from range_ import AbstractRange, CircularRange, PlusRange, DonutRange
from utilities import Countdown, euclidean_distance, rotate_toward, angle_between, polar_to_rectangular, \
    rectangles_intersect

__author__ = "Alex Teng"


class ArmoredEnemy(AbstractEnemy):
    """Armored Enemies that immune to projectile and explosive attacks"""
    name = "Armored Enemy"
    colour = '#678A0C'  # Amaranth

    points = 80

    def __init__(self, grid_size=(.3, .3), grid_speed=6 / 60, health=200):
        super().__init__(grid_size, grid_speed, health)

    def damage(self, damage, type_):
        """Inflict damage on the enemy

        Parameters:
            damage (int): The amount of damage to inflict
            type_ (str): The type of damage to do i.e. projectile, explosive
        """
        ##  Why cannot I use type_ == 'pro' or 'exp'?
        if type_ == 'projectile':
            pass
        elif type_ == 'explosive':
            pass
        else:
            self.health -= damage
            print(self.health)

        if self.health < 0:
            self.health = 0

    def step(self, data):
        """Move the enemy forward a single time-step

        Parameters:
            grid (GridCoordinateTranslator): Grid the enemy is currently on
            path (Path): The path the enemy is following

        Returns:
            bool: True iff the new location of the enemy is within the grid
        """
        grid = data.grid
        path = data.path

        # Repeatedly move toward next cell centre as much as possible
        movement = self.grid_speed
        while movement > 0:
            cell_offset = grid.pixel_to_cell_offset(self.position)

            # Assuming cell_offset is along an axis!
            offset_length = abs(cell_offset[0] + cell_offset[1])

            if offset_length == 0:
                partial_movement = movement
            else:
                partial_movement = min(offset_length, movement)

            cell_position = grid.pixel_to_cell(self.position)
            delta = path.get_best_delta(cell_position)

            # Ensures enemy will move to the centre before moving toward delta
            dx, dy = get_delta_through_centre(cell_offset, delta)

            speed = partial_movement * self.cell_size
            self.move_by((speed * dx, speed * dy))
            self.position = tuple(int(i) for i in self.position)

            movement -= partial_movement

        intersects = rectangles_intersect(*self.get_bounding_box(), (0, 0), grid.pixels)
        return intersects or grid.pixel_to_cell(self.position) in path.deltas


class SpawnEnemy(AbstractEnemy):
    """An enemy that can spawn enemy."""
    name = "Spawn Enemy"
    colour = '#666633'  # Amaranth
    _type = None
    points = 120

    def __init__(self, grid_size=(.3, .3), grid_speed=6 / 60, health=400):
        super().__init__(grid_size, grid_speed, health)

    def damage(self, damage, type_):
        """Inflict damage on the enemy

        Parameters:
            damage (int): The amount of damage to inflict
            type_ (str): The type of damage to do i.e. projectile, explosive
        """
        self._type = type_
        self.health -= damage
        # print(self.health)

        if self.health < 0:
            self.health = 0

    def is_dead(self):
        """(bool) True iff the enemy is dead i.e. health below zero"""
        return self.health <= 0

    def step(self, data):
        """Move the enemy forward a single time-step

        Parameters:
            grid (GridCoordinateTranslator): Grid the enemy is currently on
            path (Path): The path the enemy is following

        Returns:
            bool: True iff the new location of the enemy is within the grid
        """
        grid = data.grid
        path = data.path

        # Repeatedly move toward next cell centre as much as possible
        movement = self.grid_speed
        while movement > 0:
            cell_offset = grid.pixel_to_cell_offset(self.position)

            # Assuming cell_offset is along an axis!
            offset_length = abs(cell_offset[0] + cell_offset[1])

            if offset_length == 0:
                partial_movement = movement
            else:
                partial_movement = min(offset_length, movement)

            cell_position = grid.pixel_to_cell(self.position)
            delta = path.get_best_delta(cell_position)

            # Ensures enemy will move to the centre before moving toward delta
            dx, dy = get_delta_through_centre(cell_offset, delta)

            speed = partial_movement * self.cell_size
            self.move_by((speed * dx, speed * dy))
            self.position = tuple(int(i) for i in self.position)

            movement -= partial_movement

        intersects = rectangles_intersect(*self.get_bounding_box(), (0, 0), grid.pixels)
        return intersects or grid.pixel_to_cell(self.position) in path.deltas
