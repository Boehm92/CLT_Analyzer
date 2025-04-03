import madcad as mdc
import numpy as np


class CltWall:
    def __init__(self):
        self.length = np.random.uniform(16000, 20000)
        self.height = np.random.uniform(2400, 3500)
        self.depth = np.random.uniform(600, 1600)
        self.wall_dimensions = mdc.vec3(self.length, self.depth, self.height)

    def transform(self):
        return mdc.brick(mdc.vec3(0, 0, 0), self.wall_dimensions)
