import numpy as np
import madcad as mdc


class ThroughHole:
    def __init__(self):
        self.dir = np.random.choice(["direction_1", "direction_2", "direction_3"])
        self.dir = np.random.choice(["direction_1"])
        self.radius = np.random.uniform(0.5, 2.25)
        self.pos_x = np.random.uniform(self.radius + 0.5, 9.5 - self.radius)
        self.pos_y = np.random.uniform(self.radius + 0.5, 9.5 - self.radius)
        self.start_point = -0.0001
        self.end_point = 10.0001

        self.max_volume = 632  # value determined by printing the volume of 3D object with max dimensions
        self.max_manufacturing_time = 0.25
        self.manufacturing_time_side_supplement = 0.16
        self.manufacturing_time_bottom_supplement = 1

        self.transform = {
            "direction_1": [mdc.vec3(self.pos_x, self.pos_y, self.start_point),
                            mdc.vec3(self.pos_x, self.pos_y, self.end_point)],
            "direction_2": [mdc.vec3(self.pos_x, self.start_point, self.pos_y),
                            mdc.vec3(self.pos_x, self.end_point, self.pos_y)],
            "direction_3": [mdc.vec3(self.start_point, self.pos_x, self.pos_y),
                            mdc.vec3(self.end_point, self.pos_x, self.pos_y)],
        }

    def manufacturing_time_calculation(self, _through_hole):
        manufacturing_time = self.max_manufacturing_time * (_through_hole.volume() / self.max_volume)

        if self.dir in ["direction_2", "direction_3"]:
            manufacturing_time += self.manufacturing_time_side_supplement

        return manufacturing_time

    def transformation(self):
        _through_hole = mdc.cylinder(self.transform[self.dir][0], self.transform[self.dir][1], self.radius)
        _manufacturing_time = round(self.manufacturing_time_calculation(_through_hole), 4)

        return _through_hole, _manufacturing_time
