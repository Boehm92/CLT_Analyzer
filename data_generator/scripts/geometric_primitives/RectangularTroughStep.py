import numpy as np
import madcad as mdc


class RectangularTroughStep:
    def __init__(self):
        self.dir = np.random.choice(["direction_1", "direction_2", "direction_3", "direction_4", "direction_5",
                                     "direction_6", "direction_7", "direction_8"])
        self.positive_length = np.random.uniform(1, 4.5)
        self.positive_width = np.random.uniform(1, 4.5)
        self.negative_length = 9 - np.random.uniform(1, 4.5)
        self.negative_width = 9 - np.random.uniform(1, 4.5)
        self.depth = np.random.uniform(1, 9)
        self.negative_start_point = -0.0001
        self.positive_start_point = 10.0001

        self.max_volume = 810
        self.max_manufacturing_time = 1.25
        self.manufacturing_time_side_supplement = 0.16

        self.rectangular_vectors = {
            # left bottom
            "direction_1": [mdc.vec3(self.negative_start_point, self.negative_start_point, self.negative_start_point),
                            mdc.vec3(self.positive_width, self.positive_start_point, self.depth)],

            # left upper
            "direction_2": [mdc.vec3(self.positive_width, self.positive_start_point, self.depth),
                            mdc.vec3(self.negative_start_point, self.negative_start_point, self.positive_start_point)],

            # right bottom
            "direction_3": [mdc.vec3(self.negative_width, self.negative_start_point, self.negative_start_point),
                            mdc.vec3(self.positive_start_point, self.positive_start_point, self.depth)],

            # right upper
            "direction_4": [mdc.vec3(self.positive_start_point, self.negative_start_point, self.positive_start_point),
                            mdc.vec3(self.negative_width, self.positive_start_point, self.depth)],

            # back bottom
            "direction_5": [mdc.vec3(self.positive_start_point, self.negative_length, self.depth),
                            mdc.vec3(self.negative_start_point, self.positive_start_point, self.negative_start_point)],

            # back upper
            "direction_6": [mdc.vec3(self.negative_start_point, self.negative_width, self.depth),
                            mdc.vec3(self.positive_start_point, self.positive_start_point, self.positive_start_point)],

            # front upper
            "direction_7": [mdc.vec3(self.positive_start_point, self.positive_length, self.depth),
                            mdc.vec3(self.negative_start_point, self.negative_start_point, self.positive_start_point)],

            # front bottom
            "direction_8": [mdc.vec3(self.negative_start_point, self.negative_start_point, self.negative_start_point),
                            mdc.vec3(self.positive_start_point, self.positive_length, self.depth)],
        }

    def manufacturing_time_calculation(self, rectangular_passage):
        manufacturing_time = self.max_manufacturing_time * (rectangular_passage.volume() / self.max_volume)
        if self.dir in ["direction_1", "direction_3", "direction_5", "direction_8"]:
            manufacturing_time += self.manufacturing_time_side_supplement
        return manufacturing_time

    def transformation(self):
        _rectangular_through_step = mdc.brick(self.rectangular_vectors[self.dir][0],
                                              self.rectangular_vectors[self.dir][1])
        _manufacturing_time = round(self.manufacturing_time_calculation(_rectangular_through_step), 4)

        return _rectangular_through_step, _manufacturing_time
