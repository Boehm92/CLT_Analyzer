import math
import numpy as np
import madcad as mdc


class TriangularPassage:
    def __init__(self):
        self.dir = np.random.choice(["direction_1", "direction_2", "direction_3"])

        self.length = np.random.uniform(1, 4.5)
        self.pos_x = np.random.uniform(0.5, 9.5 - self.length)
        self.pos_y = np.random.uniform(0.5, 9.5 - self.length)
        self.negative_start_point = -0.0001
        self.depth = 10.0002
        self.angle = math.sin(math.radians(60))

        self.max_volume = 316
        self.max_manufacturing_time = 1
        self.manufacturing_time_side_supplement = 0.16

        self.triangle_vectors = {
            "direction_1": [mdc.vec3(self.pos_x + self.length, self.pos_y, self.negative_start_point),
                            mdc.vec3(self.pos_x, self.pos_y, self.negative_start_point),
                            mdc.vec3(self.pos_x + (self.length / 2),
                                     self.pos_y + (self.length * self.angle), self.negative_start_point)],
            "direction_2": [mdc.vec3(self.pos_x, self.negative_start_point, self.pos_y),
                            mdc.vec3(self.pos_x + self.length, self.negative_start_point, self.pos_y),
                            mdc.vec3(self.pos_x + (self.length / 2),
                                     self.negative_start_point, self.pos_y + (self.length * self.angle))],
            "direction_3": [mdc.vec3(self.negative_start_point, self.pos_x + self.length, self.pos_y),
                            mdc.vec3(self.negative_start_point, self.pos_x, self.pos_y),
                            mdc.vec3(self.negative_start_point, self.pos_x + (self.length / 2),
                                     self.pos_y + (self.length * self.angle))],
        }

        self.dept = {
            "direction_1": self.depth * mdc.Z,
            "direction_2": self.depth * mdc.Y,
            "direction_3": self.depth * mdc.X,
        }

    def manufacturing_time_calculation(self, triangle):
        manufacturing_time = self.max_manufacturing_time * (triangle.volume() / self.max_volume)
        if self.dir in ["direction_2", "direction_3"]:
            manufacturing_time += self.manufacturing_time_side_supplement
        return manufacturing_time

    def transformation(self):
        _triangular_primitive = [mdc.Segment(self.triangle_vectors[self.dir][0], self.triangle_vectors[self.dir][1]),
                                 mdc.Segment(self.triangle_vectors[self.dir][1], self.triangle_vectors[self.dir][2]),
                                 mdc.Segment(self.triangle_vectors[self.dir][2], self.triangle_vectors[self.dir][0])],

        _triangular_passage = mdc.extrusion(self.dept[self.dir], mdc.flatsurface(_triangular_primitive))
        _manufacturing_time = round(self.manufacturing_time_calculation(_triangular_passage), 4)

        return _triangular_passage, _manufacturing_time
