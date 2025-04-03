import numpy as np
import madcad as mdc


class ElectricalCabinet:
    def __init__(self, base_primitive):
        self.dir = np.random.choice(["direction_1", "direction_2"])
        self.pos_x = np.random.uniform(100, base_primitive.length - 1000)
        self.width = self.pos_x + np.random.uniform(700, 900)
        self.negativ_pos_y = -0.1
        self.negative_depth = np.random.uniform(40, 50)
        self.positive_pos_y = base_primitive.depth + 0.1
        self.positive_depth = base_primitive.depth - np.random.uniform(40, 50)
        self.pos_z = np.random.uniform(1000, base_primitive.height - 1000)
        self.height = self.pos_z + np.random.uniform(700, 900)

        self.max_volume = 810
        self.max_manufacturing_time = 1.25
        self.manufacturing_time_side_supplement = 0.16

        self.transform = {
            "direction_1": [mdc.vec3(self.pos_x, self.negativ_pos_y, self.pos_z),
                            mdc.vec3(self.width, self.negative_depth, self.height)],
            "direction_2": [mdc.vec3(self.pos_x, self.positive_depth, self.pos_z),
                            mdc.vec3(self.width, self.positive_pos_y, self.height)],
        }

    def manufacturing_time_calculation(self, rectangular_passage):
        manufacturing_time = self.max_manufacturing_time * (rectangular_passage.volume() / self.max_volume)

        return manufacturing_time

    def transformation(self):
        _window = mdc.brick(self.transform[self.dir][0], self.transform[self.dir][1])
        _manufacturing_time = round(self.manufacturing_time_calculation(_window), 4)

        return _window, _manufacturing_time
