import numpy as np
import madcad as mdc


class Window:
    def __init__(self, base_primitive):
        self.dir = "direction_1"
        self.pos_x = np.random.uniform(300, base_primitive.length - 1200)
        self.width = self.pos_x + 900
        self.pos_y = -0.0001
        self.depth = base_primitive.depth + 0.0001
        self.pos_z = np.random.uniform(300, base_primitive.height - 1200)
        self.height = self.pos_z + 900

        self.max_volume = 243000000  # mm²
        self.max_manufacturing_time = 3
        self.manufacturing_time_side_supplement = 0.33

        self.transform = {
            "direction_1": [mdc.vec3(self.pos_x, self.pos_y, self.pos_z),
                            mdc.vec3(self.width, self.depth, self.height)],
        }

    def manufacturing_time_calculation(self, rectangular_passage):
        manufacturing_time = self.max_manufacturing_time

        return manufacturing_time

    def transformation(self):
        _window = mdc.brick(self.transform[self.dir][0], self.transform[self.dir][1])
        _manufacturing_time = round(self.manufacturing_time_calculation(_window), 4)

        return _window, _manufacturing_time
