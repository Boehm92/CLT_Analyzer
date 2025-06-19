import numpy as np
import madcad as mdc


class ElectricalCabinet:
    def __init__(self, base_primitive):
        self.dir = "direction_2"
        self.pos_x = np.random.uniform(300, base_primitive.length - 1000)
        self.width = self.pos_x + 300
        self.negative_pos_y = -0.0001
        self.negative_depth = 200
        self.positive_pos_y = base_primitive.depth + 0.0001
        self.positive_depth = base_primitive.depth - 100
        self.pos_z = np.random.uniform(300, base_primitive.height - 1000)
        self.height = self.pos_z + 500

        self.max_volume = 40500000  # mm²
        self.max_manufacturing_time = 1.5
        self.movement_time_supplement = 0.17

        self.transform = {
            "direction_1": [mdc.vec3(self.pos_x, self.negative_pos_y, self.pos_z),
                            mdc.vec3(self.width, self.negative_depth, self.height)],
            "direction_2": [mdc.vec3(self.pos_x, self.positive_depth, self.pos_z),
                            mdc.vec3(self.width, self.positive_pos_y, self.height)],
        }

    def manufacturing_time_calculation(self, rectangular_passage):
        manufacturing_time = self.max_manufacturing_time

        return manufacturing_time

    def transformation(self):
        _window = mdc.brick(self.transform[self.dir][0], self.transform[self.dir][1])
        _manufacturing_time = round(self.manufacturing_time_calculation(_window), 4)

        return _window, _manufacturing_time
