import math
import numpy as np
import madcad as mdc


class XFitConnector:
    def __init__(self, base_primitive):
        self.dir = np.random.choice(["direction_1", "direction_2"])
        self.negative_pos_x = -0.0001
        self.positive_pos_x = base_primitive.length + 0.0001
        self.pos_z = np.random.uniform(400, base_primitive.height - 400)
        self.positive_start_point = base_primitive.depth + 0.001
        self.depth = 250

        self.max_volume = 27712812
        self.max_manufacturing_time = 2
        self.movement_time_supplement = 0.33

        self.vectors = {
            "direction_1": {
                "vector_D": mdc.vec3(self.negative_pos_x, self.positive_start_point, self.pos_z),
                "vector_C": mdc.vec3(self.negative_pos_x, self.positive_start_point, self.pos_z -200),
                "vector_B": mdc.vec3((self.negative_pos_x + 100), self.positive_start_point, self.pos_z - 220),
                "vector_A": mdc.vec3((self.negative_pos_x + 100), self.positive_start_point, self.pos_z + 20)
            },
            "direction_2": {
                "vector_A": mdc.vec3(self.positive_pos_x, self.positive_start_point, self.pos_z),
                "vector_B": mdc.vec3(self.positive_pos_x, self.positive_start_point, self.pos_z - 200),
                "vector_C": mdc.vec3((self.positive_pos_x - 100), self.positive_start_point, self.pos_z - 220),
                "vector_D": mdc.vec3((self.positive_pos_x - 100), self.positive_start_point, self.pos_z + 20),
            }
        }

        self.depth = {
            "direction_1": - self.depth * mdc.Y,
            "direction_2": - self.depth * mdc.Y,
        }

    def manufacturing_time_calculation(self, triangle):
        manufacturing_time = self.max_manufacturing_time
        manufacturing_time += self.movement_time_supplement

        return manufacturing_time

    def transformation(self):
        _x_fit_connector = mdc.web(
            mdc.Segment(self.vectors[self.dir]["vector_A"], self.vectors[self.dir]["vector_B"]),
            mdc.Segment(self.vectors[self.dir]["vector_B"], self.vectors[self.dir]["vector_C"]),
            mdc.Segment(self.vectors[self.dir]["vector_C"], self.vectors[self.dir]["vector_D"]),
            mdc.Segment(self.vectors[self.dir]["vector_D"], self.vectors[self.dir]["vector_A"])
        )


        solid = mdc.extrusion(self.depth[self.dir], mdc.flatsurface(_x_fit_connector))

        manufacturing_time = round(self.manufacturing_time_calculation(solid), 4)

        return solid, manufacturing_time
