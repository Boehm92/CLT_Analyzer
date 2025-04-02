import numpy as np
import madcad as mdc


class Chamfer:
    def __init__(self):
        self.dir = np.random.choice(["direction_1", "direction_2", "direction_3", "direction_4", "direction_5",
                                     "direction_6", "direction_7", "direction_8", "direction_9", "direction_10",
                                     "direction_11", "direction_12"])
        self.depth = 10.0004
        self.X = np.random.uniform(0.5, 4.5)
        self.Y = self.X
        self.negative_start_point = -0.0001
        self.positive_start_point = 10.0001

        self.max_volume = 405
        self.max_manufacturing_time = 1.33
        self.manufacturing_time_side_supplement = 0.16
        self.manufacturing_time_bottom_supplement = 1

        self.chamfer_vectors = {
            # front side left edge
            "direction_1": {
                "vector_A": mdc.vec3(self.negative_start_point, self.Y, self.negative_start_point),
                "vector_B": mdc.vec3(self.X, self.negative_start_point, self.negative_start_point),
                "vector_C": mdc.vec3(self.negative_start_point, self.negative_start_point, self.negative_start_point)
            },
            # front side bottom edge
            "direction_2": {
                "vector_A": mdc.vec3(self.negative_start_point, self.negative_start_point, self.Y, ),
                "vector_B": mdc.vec3(self.negative_start_point, self.X, self.negative_start_point),
                "vector_C": mdc.vec3(self.negative_start_point, self.negative_start_point, self.negative_start_point)
            },

            # front side right edge
            "direction_3": {
                "vector_A": mdc.vec3(self.X, self.negative_start_point, self.negative_start_point),
                "vector_C": mdc.vec3(self.positive_start_point, self.negative_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.positive_start_point, self.Y, self.negative_start_point)
            },
            # front side right edge
            "direction_4": {
                "vector_A": mdc.vec3(self.negative_start_point, self.X, self.positive_start_point),
                "vector_C": mdc.vec3(self.negative_start_point, self.negative_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.negative_start_point, self.negative_start_point, self.Y)
            },
            # right side bottom edge
            "direction_5": {
                "vector_A": mdc.vec3(self.positive_start_point, self.negative_start_point, self.X, ),
                "vector_C": mdc.vec3(self.positive_start_point, self.negative_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.Y, self.negative_start_point, self.negative_start_point)
            },

            # right side top edge
            "direction_6": {
                "vector_A": mdc.vec3(self.Y, self.negative_start_point, self.positive_start_point),
                "vector_C": mdc.vec3(self.positive_start_point, self.negative_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.positive_start_point, self.negative_start_point, self.X)
            },
            # left side top edge
            "direction_7": {
                "vector_A": mdc.vec3(self.negative_start_point, self.negative_start_point, self.X),
                "vector_C": mdc.vec3(self.negative_start_point, self.negative_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.Y, self.negative_start_point, self.positive_start_point)
            },
            # left side bottom edge
            "direction_8": {
                "vector_A": mdc.vec3(self.negative_start_point, self.positive_start_point, self.X),
                "vector_C": mdc.vec3(self.negative_start_point, self.positive_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.Y, self.positive_start_point, self.negative_start_point),
            },
            # back left edge
            "direction_9": {
                "vector_A": mdc.vec3(self.X, self.positive_start_point, self.negative_start_point),
                "vector_C": mdc.vec3(self.negative_start_point, self.positive_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.negative_start_point, self.Y, self.negative_start_point),
            },
            # back bottom edge
            "direction_10": {
                "vector_A": mdc.vec3(self.negative_start_point, self.X, self.negative_start_point),
                "vector_C": mdc.vec3(self.negative_start_point, self.positive_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.negative_start_point, self.positive_start_point, self.Y),
            },
            # back bottom edge
            "direction_11": {
                "vector_A": mdc.vec3(self.positive_start_point, self.Y, self.negative_start_point),
                "vector_C": mdc.vec3(self.positive_start_point, self.positive_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.X, self.positive_start_point, self.negative_start_point),
            },
            # back top edge
            "direction_12": {
                "vector_A": mdc.vec3(self.negative_start_point, self.positive_start_point, self.Y),
                "vector_C": mdc.vec3(self.negative_start_point, self.positive_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.negative_start_point, self.X, self.positive_start_point),
            },
        }

        self.depth = {
            "direction_1": self.depth * mdc.Z,
            "direction_2": self.depth * mdc.X,
            "direction_3": self.depth * mdc.Z,
            "direction_4": self.depth * mdc.X,
            "direction_5": self.depth * mdc.Y,
            "direction_6": self.depth * mdc.Y,
            "direction_7": self.depth * mdc.Y,
            "direction_8": self.depth * -mdc.Y,
            "direction_9": self.depth * mdc.Z,
            "direction_10": self.depth * mdc.X,
            "direction_11": self.depth * mdc.Z,
            "direction_12": self.depth * mdc.X,
        }

    def manufacturing_time_calculation(self, chamfer):
        manufacturing_time = self.max_manufacturing_time * (chamfer.volume() / self.max_volume)
        if self.dir in ["direction_1", "direction_3", "direction_9", "direction_11"]:
            manufacturing_time += self.manufacturing_time_side_supplement
        if self.dir in ["direction_2", "direction_5", "direction_8", "direction_10"]:
            manufacturing_time += self.manufacturing_time_bottom_supplement
        return manufacturing_time

    def transformation(self):
        _chamfer = [mdc.Segment(self.chamfer_vectors[self.dir]["vector_A"], self.chamfer_vectors[self.dir]["vector_B"]),
                    mdc.Segment(self.chamfer_vectors[self.dir]["vector_B"], self.chamfer_vectors[self.dir]["vector_C"]),
                    mdc.Segment(self.chamfer_vectors[self.dir]["vector_C"], self.chamfer_vectors[self.dir]["vector_A"])]
        _chamfer = mdc.extrusion(self.depth[self.dir], mdc.flatsurface(_chamfer))
        _manufacturing_time = round(self.manufacturing_time_calculation(_chamfer), 4)

        return _chamfer, _manufacturing_time
