import numpy as np
import madcad as mdc


class RectangularPassage:
    def __init__(self):
        self.dir = np.random.choice(["direction_1", "direction_2", "direction_3"])
        self.pos_x = np.random.uniform(0.5, 8.5)
        self.pos_y = np.random.uniform(0.5, 8.5)
        self.width = np.random.uniform(self.pos_x + 0.5, 9.5)
        self.length = np.random.uniform(self.pos_y + 0.5, 9.5)
        self.start_point = -0.0001
        self.end_point = 10.0001

        self.max_volume = 810
        self.max_manufacturing_time = 1.25
        self.manufacturing_time_side_supplement = 0.16

        self.transform = {
            "direction_1": [mdc.vec3(self.pos_x, self.pos_y, self.start_point),
                            mdc.vec3(self.width, self.length, self.end_point)],
            "direction_2": [mdc.vec3(self.pos_x, self.start_point, self.pos_y),
                            mdc.vec3(self.width, self.end_point, self.length)],
            "direction_3": [mdc.vec3(self.start_point, self.pos_x, self.pos_y),
                            mdc.vec3(self.end_point, self.width, self.length)],
        }

    def manufacturing_time_calculation(self, rectangular_passage):
        manufacturing_time = self.max_manufacturing_time * (rectangular_passage.volume() / self.max_volume)
        if self.dir in ["direction_1", "direction_2"]:
            manufacturing_time += self.manufacturing_time_side_supplement

        return manufacturing_time

    def transformation(self):
        _rectangular_passage = mdc.brick(self.transform[self.dir][0], self.transform[self.dir][1])
        _manufacturing_time = round(self.manufacturing_time_calculation(_rectangular_passage), 4)

        return _rectangular_passage, _manufacturing_time
