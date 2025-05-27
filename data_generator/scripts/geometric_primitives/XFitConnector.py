import math

import numpy as np
import madcad as mdc


class XFitConnector:
    def __init__(self, base_primitive):
        self.dir = np.random.choice(["direction_1", "direction_2", "direction_3", "direction_4"])
        self.negativ_pos_x = -100
        self.positive_pos_x = base_primitive.length - np.random.uniform(200, 300)
        self.length = np.random.uniform(300, 400)
        self.pos_z = np.random.uniform(400, base_primitive.height - 400)

        self.negative_start_point = -0.0001
        self.positive_start_point = base_primitive.depth + 0.0001
        self.depth = np.random.uniform(100, 200)
        self.angle = math.sin(math.radians(60))

        self.max_volume = 27712812
        self.max_manufacturing_time = 1.5
        self.movement_time_supplement = 0.33

        self.triangle_vectors = {
            "direction_1": [
                mdc.vec3(self.negativ_pos_x, self.positive_start_point, self.pos_z),
                mdc.vec3(self.negativ_pos_x + self.length, self.positive_start_point,
                         self.pos_z + (self.length * self.angle)),
                mdc.vec3(self.negativ_pos_x + self.length, self.positive_start_point,
                         self.pos_z - (self.length * self.angle))],

            "direction_2": [
                mdc.vec3(self.negativ_pos_x + self.length, self.negative_start_point, self.pos_z - (self.length * self.angle)),
                mdc.vec3(self.negativ_pos_x + self.length, self.negative_start_point,
                         self.pos_z + (self.length * self.angle)),
                mdc.vec3(self.negativ_pos_x, self.negative_start_point, self.pos_z)],

            "direction_3": [
                mdc.vec3(self.positive_pos_x, self.positive_start_point, self.pos_z - (self.length * self.angle)),
                mdc.vec3(self.positive_pos_x, self.positive_start_point, self.pos_z + (self.length * self.angle)),
                mdc.vec3(self.positive_pos_x + self.length, self.positive_start_point, self.pos_z)],

            "direction_4": [
                mdc.vec3(self.positive_pos_x + self.length, self.negative_start_point, self.pos_z),
                mdc.vec3(self.positive_pos_x, self.negative_start_point, self.pos_z + (self.length * self.angle)),
                mdc.vec3(self.positive_pos_x, self.negative_start_point, self.pos_z - (self.length * self.angle))]
        }

        self.dept = {
            "direction_1": - self.depth * mdc.Y,
            "direction_2": self.depth * mdc.Y,
            "direction_3": - self.depth * mdc.Y,
            "direction_4": self.depth * mdc.Y,
        }

    def manufacturing_time_calculation(self, triangle):
        manufacturing_time = self.max_manufacturing_time * (triangle.volume() / self.max_volume)
        manufacturing_time += self.movement_time_supplement

        return manufacturing_time

    def transformation(self):
        _x_fit_connector = [mdc.Segment(self.triangle_vectors[self.dir][0], self.triangle_vectors[self.dir][1]),
                            mdc.Segment(self.triangle_vectors[self.dir][1], self.triangle_vectors[self.dir][2]),
                            mdc.Segment(self.triangle_vectors[self.dir][2], self.triangle_vectors[self.dir][0])],

        _x_fit_connector = mdc.extrusion(self.dept[self.dir], mdc.flatsurface(_x_fit_connector))

        _manufacturing_time = round(self.manufacturing_time_calculation(_x_fit_connector), 4)

        return _x_fit_connector, _manufacturing_time
