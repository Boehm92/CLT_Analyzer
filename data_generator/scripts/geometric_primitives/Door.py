import numpy as np
import madcad as mdc


class Door:
    def __init__(self, _base_primitive):
        self.dir = "direction_1"
        self.pos_x = np.random.uniform(100, _base_primitive.length - 1000)
        self.pos_y = -0.1
        self.depth = 2000
        self.width = self.pos_x + 900
        self.start_point = -0.1
        self.height = 2010

        self.max_volume = 810
        self.max_manufacturing_time = 1.25
        self.manufacturing_time_side_supplement = 0.16

        self.transform = {
            "direction_1": [mdc.vec3(self.pos_x, self.pos_y, self.start_point),
                            mdc.vec3(self.width, self.depth, self.height)],
        }

    def manufacturing_time_calculation(self, rectangular_passage):
        manufacturing_time = self.max_manufacturing_time * (rectangular_passage.volume() / self.max_volume)

        return manufacturing_time

    def transformation(self):
        _rectangular_passage = mdc.brick(self.transform[self.dir][0], self.transform[self.dir][1])
        _manufacturing_time = round(self.manufacturing_time_calculation(_rectangular_passage), 4)

        return _rectangular_passage, _manufacturing_time
