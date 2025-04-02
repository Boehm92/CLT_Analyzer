import numpy as np
import madcad as mdc


class RectangularPocket:
    def __init__(self):
        self.dir = np.random.choice(["direction_1", "direction_2", "direction_3", "direction_4", "direction_5",
                                    "direction_6"])
        self.pos_x = np.random.uniform(0.5, 8.5)
        self.pos_y = np.random.uniform(0.5, 8.5)
        self.width = np.random.uniform(self.pos_x + 0.5, 9.5)
        self.length = np.random.uniform(self.pos_y + 0.5, 9.5)
        self.start_point_positive_direction = -0.0001
        self.end_point_negative_direction = 10.0001
        self.end_point = np.random.uniform(1, 9)

        self.max_volume = 810
        self.max_manufacturing_time = 1.25
        self.manufacturing_time_side_supplement = 0.16
        self.manufacturing_time_bottom_supplement = 1

        self.transform = {
            "direction_1": [mdc.vec3(self.pos_x, self.pos_y, self.start_point_positive_direction),
                            mdc.vec3(self.width, self.length,self.end_point)],
            "direction_2": [mdc.vec3(self.pos_x, self.pos_y, self.end_point),
                            mdc.vec3(self.width, self.length, self.end_point_negative_direction)],
            "direction_3": [mdc.vec3(self.pos_x, self.start_point_positive_direction, self.pos_y),
                            mdc.vec3(self.width, self.end_point, self.length)],
            "direction_4": [mdc.vec3(self.pos_x, self.end_point, self.pos_y),
                            mdc.vec3(self.width, self.end_point_negative_direction, self.length)],
            "direction_5": [mdc.vec3(self.start_point_positive_direction, self.pos_x, self.pos_y),
                            mdc.vec3(self.end_point, self.width, self.length)],
            "direction_6": [mdc.vec3(self.end_point, self.pos_x, self.pos_y),
                            mdc.vec3(self.end_point_negative_direction, self.width, self.length)]
        }

    def manufacturing_time_calculation(self, rectangular_passage):
        manufacturing_time = self.max_manufacturing_time * (rectangular_passage.volume() / self.max_volume)
        if self.dir in ["direction_3", "direction_4", "direction_5", "direction_6"]:
            manufacturing_time += self.manufacturing_time_side_supplement
        if self.dir == "direction_1":
            manufacturing_time += self.manufacturing_time_bottom_supplement
        return manufacturing_time


    def transformation(self):
        _rectangular_passage = mdc.brick(self.transform[self.dir][0], self.transform[self.dir][1])
        _manufacturing_time = round(self.manufacturing_time_calculation(_rectangular_passage), 4)

        return _rectangular_passage, _manufacturing_time
