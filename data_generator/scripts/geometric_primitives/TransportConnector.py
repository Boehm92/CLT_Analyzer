import numpy as np
import madcad as mdc

class TransportConnector:
    def __init__(self, _base_primitive):
        self.dir = "direction_1"

        self.radius = 20
        self.pos_x = np.random.uniform(self.radius + 0.5, _base_primitive.length - self.radius)
        self.pos_y = _base_primitive.depth/2
        self.pos_z = _base_primitive.height - np.random.uniform(160, 180)
        self.height = _base_primitive.height + 0.0001

        self.max_volume = 226080
        self.max_manufacturing_time = 0.5

        self.transform = {
            "direction_1": [mdc.vec3(self.pos_x, self.pos_y, self.pos_z),
                            mdc.vec3(self.pos_x, self.pos_y, self.height)]
        }

    def manufacturing_time_calculation(self, _through_hole):
        manufacturing_time = self.max_manufacturing_time

        return manufacturing_time

    def transformation(self):
        _power_outlet = mdc.cylinder(self.transform[self.dir][0], self.transform[self.dir][1], self.radius)
        _power_outlet.mergeclose()
        _power_outlet = mdc.segmentation(_power_outlet)
        _manufacturing_time = round(self.manufacturing_time_calculation(_power_outlet), 4)

        return _power_outlet, _manufacturing_time
