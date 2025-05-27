import numpy as np
import madcad as mdc
from data_generator.scripts.geometric_primitives.base_primitive import CltWall


class PowerOutlet:
    def __init__(self, _base_primitive):
        self.dir = np.random.choice(["direction_1", "direction_2"])

        self.radius = 34
        self.pos_x = np.random.uniform(self.radius + 0.5, _base_primitive.length - self.radius)
        self.pos_z = np.random.uniform(self.radius + 0.5, _base_primitive.height - self.radius)
        self.positive_start_point = _base_primitive.depth + 0.0001
        self.negative_start_point = - 0.0001
        self.end_point = np.random.uniform(50, 60)

        self.max_volume = 217790  # mm²
        self.max_manufacturing_time = 0.07
        self.movement_time_supplement = 0.17

        self.transform = {
            "direction_1": [mdc.vec3(self.pos_x, (self.positive_start_point - self.end_point), self.pos_z),
                            mdc.vec3(self.pos_x, self.positive_start_point, self.pos_z)],

            "direction_2": [mdc.vec3(self.pos_x, self.negative_start_point, self.pos_z),
                            mdc.vec3(self.pos_x, (self.negative_start_point + self.end_point), self.pos_z)],
        }

    def manufacturing_time_calculation(self, _through_hole):
        manufacturing_time = self.max_manufacturing_time * (_through_hole.volume() / self.max_volume)
        manufacturing_time += self.movement_time_supplement

        return manufacturing_time

    def transformation(self):
        _power_outlet = mdc.cylinder(self.transform[self.dir][0], self.transform[self.dir][1], self.radius)
        _power_outlet.mergeclose()
        _power_outlet = mdc.segmentation(_power_outlet)
        _manufacturing_time = round(self.manufacturing_time_calculation(_power_outlet), 4)

        return _power_outlet, _manufacturing_time
