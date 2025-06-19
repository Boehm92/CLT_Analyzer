import numpy as np
import madcad as mdc


class ElectricalWire:
    def __init__(self, base_primitive):
        self.dir = np.random.choice(["direction_2", "direction_4"])
        self.pos_x = np.random.uniform(100, base_primitive.length - 100)
        self.pos_z = np.random.uniform(100, base_primitive.height - 100)
        self.positive_pos_y = base_primitive.depth + 0.0001

        self.length = np.random.uniform(500, 5000)
        self.width = 80
        self.positive_depth = base_primitive.depth - 50

        # self.negativ_pos_y = -0.0001
        # self.negative_depth = 80

        self.max_volume = 20000000 # mm²
        self.max_manufacturing_time = 1
        self.movement_time_supplement = 0.17

        self.transform = {
            # "direction_1": [mdc.vec3(self.pos_x, self.negativ_pos_y, self.pos_z),
            #                 mdc.vec3(self.width, self.negative_depth, self.height)],
            # "direction_3": [mdc.vec3(self.pos_z, self.negativ_pos_y, self.pos_x),
            #                 mdc.vec3(self.height, self.negative_depth, self.width)],
            "direction_2": [mdc.vec3(self.pos_x, self.positive_depth, self.pos_z),
                            mdc.vec3(self.pos_x + self.length, self.positive_pos_y, self.pos_z + self.width)],
            "direction_4": [mdc.vec3(self.pos_x, self.positive_depth, self.pos_z ),
                            mdc.vec3(self.pos_x + self.width, self.positive_pos_y, self.pos_z + self.length)],
        }

    def manufacturing_time_calculation(self, rectangular_passage):
        manufacturing_time = self.max_manufacturing_time

        return manufacturing_time

    def transformation(self):
        _window = mdc.brick(self.transform[self.dir][0], self.transform[self.dir][1])
        _manufacturing_time = round(self.manufacturing_time_calculation(_window), 4)

        return _window, _manufacturing_time
