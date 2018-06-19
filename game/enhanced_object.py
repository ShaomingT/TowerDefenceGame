from enemy import AbstractEnemy, SimpleEnemy
from enhanced_enemy import ArmoredEnemy, SpawnEnemy
from level import AbstractLevel
from enemy import AbstractEnemy

__author__ = "Alex Teng"


# Could be moved to a separate file, perhaps levels/simple.py, and imported
class MyLevel(AbstractLevel):
    """A simple game level containing examples of how to generate a wave"""
    waves = 20

    def get_wave(self, wave):
        """Returns enemies in the 'wave_n'th wave

        Parameters:
            wave (int): The nth wave

        Return:
            list[tuple[int, AbstractEnemy]]: A list of (step, enemy) pairs in the
                                             wave, sorted by step in ascending order
        """
        enemies = []

        if wave == 1:
            # A hardcoded singleton list of (step, enemy) pairs

            enemies = [(10, SimpleEnemy())]
        elif wave == 2:
            # A hardcoded list of multiple (step, enemy) pairs

            enemies = [(30, SimpleEnemy()), (15, SimpleEnemy()), (15, SimpleEnemy())]
        elif 3 <= wave < 10:
            # List of (step, enemy) pairs spread across an interval of time (steps)

            steps = int(40 * (wave ** .5))  # The number of steps to spread the enemies across
            count = wave * 2  # The number of enemies to spread across the (time) steps

            for step in self.generate_intervals(steps, count):
                enemies.append((step, SimpleEnemy()))
                enemies.append((step, SpawnEnemy()))

        elif wave == 10:
            # Generate sub waves
            sub_waves = [
                # (steps, number of enemies, enemy constructor, args, kwargs)
                (50, 10, ArmoredEnemy, (), {}),  # 10 enemies over 50 steps
                (100, None, None, None, None),  # then nothing for 100 steps
                (100, 10, SimpleEnemy, (), {})  # then another 10 enemies over 50 steps
            ]

            enemies = self.generate_sub_waves(sub_waves)

        else:  # 11 <= wave <= 20
            # Now it's going to get hectic

            sub_waves = [
                (
                    int(13 * wave),  # total steps
                    int(25 * wave ** (wave / 50)),  # number of enemies
                    SimpleEnemy,  # enemy constructor
                    (),  # positional arguments to provide to enemy constructor
                    {},  # keyword arguments to provide to enemy constructor
                ),
                (120, None, None, None, None),
                (
                    int(25 * wave),  # total steps
                    int(22 * wave ** (wave / 50)),  # number of enemies
                    ArmoredEnemy,  # enemy constructor
                    (),  # positional arguments to provide to enemy constructor
                    {},  # keyword arguments to provide to enemy constructor
                ),
                (120, None, None, None, None),
                (
                    int(45 * wave * 1.5),  # total steps
                    int(20 * wave ** (wave / 50)),  # number of enemies
                    SpawnEnemy,  # enemy constructor
                    (),  # positional arguments to provide to enemy constructor
                    {},  # keyword arguments to provide to enemy constructor
                ),

            ]

            enemies = self.generate_sub_waves(sub_waves)

        return enemies
