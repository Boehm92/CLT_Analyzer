import numpy as np
import madcad as mdc


class TriangularBlindStep:
    def __init__(self):
        self.dir = np.random.choice(["direction_1", "direction_2", "direction_3", "direction_4", "direction_5",
                                     "direction_6", "direction_7", "direction_8", "direction_9", "direction_10",
                                     "direction_11", "direction_12", "direction_13", "direction_14", "direction_15",
                                     "direction_16", "direction_17", "direction_18", "direction_19", "direction_20",
                                     "direction_21", "direction_22", "direction_23", "direction_24"])
        self.depth = np.random.uniform(1, 9)
        self.X = np.random.uniform(4, 6)
        self.Y = np.random.uniform(4, 6)
        self.negative_start_point = -0.0001
        self.positive_start_point = 10.0001

        self.max_volume = 316
        self.max_manufacturing_time = 1
        self.manufacturing_time_side_supplement = 0.16
        self.manufacturing_time_bottom_supplement = 1

        self.triangular_vectors = {
            # front bottom left corner
            "direction_1": {
                "vector_A": mdc.vec3(self.negative_start_point, self.Y, self.negative_start_point),
                "vector_B": mdc.vec3(self.X, self.negative_start_point, self.negative_start_point),
                "vector_C": mdc.vec3(self.negative_start_point, self.negative_start_point, self.negative_start_point)
            },
            "direction_2": {
                "vector_A": mdc.vec3(self.negative_start_point, self.negative_start_point, self.Y, ),
                "vector_B": mdc.vec3(self.negative_start_point, self.X, self.negative_start_point),
                "vector_C": mdc.vec3(self.negative_start_point, self.negative_start_point, self.negative_start_point)
            },
            "direction_3": {
                "vector_A": mdc.vec3(self.Y, self.negative_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.negative_start_point, self.negative_start_point, self.X),
                "vector_C": mdc.vec3(self.negative_start_point, self.negative_start_point, self.negative_start_point)
            },

            # front bottom right corner
            "direction_4": {
                "vector_A": mdc.vec3(self.X, self.negative_start_point, self.negative_start_point),
                "vector_C": mdc.vec3(self.positive_start_point, self.negative_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.positive_start_point, self.Y, self.negative_start_point)
            },

            "direction_5": {
                "vector_A": mdc.vec3(self.positive_start_point, self.X, self.negative_start_point),
                "vector_C": mdc.vec3(self.positive_start_point, self.negative_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.positive_start_point, self.negative_start_point, self.Y)
            },

            "direction_6": {
                "vector_A": mdc.vec3(self.positive_start_point, self.negative_start_point, self.X, ),
                "vector_C": mdc.vec3(self.positive_start_point, self.negative_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.Y, self.negative_start_point, self.negative_start_point)
            },

            # front upper left corner
            "direction_7": {
                "vector_A": mdc.vec3(self.X, self.negative_start_point, self.positive_start_point),
                "vector_C": mdc.vec3(self.negative_start_point, self.negative_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.negative_start_point, self.Y, self.positive_start_point)
            },

            "direction_8": {
                "vector_A": mdc.vec3(self.negative_start_point, self.X, self.positive_start_point),
                "vector_C": mdc.vec3(self.negative_start_point, self.negative_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.negative_start_point, self.negative_start_point, self.Y)
            },

            "direction_9": {
                "vector_A": mdc.vec3(self.negative_start_point, self.negative_start_point, self.X),
                "vector_C": mdc.vec3(self.negative_start_point, self.negative_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.Y, self.negative_start_point, self.positive_start_point)
            },

            # front upper right corner
            "direction_10": {
                "vector_A": mdc.vec3(self.positive_start_point, self.Y, self.positive_start_point),
                "vector_C": mdc.vec3(self.positive_start_point, self.negative_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.X, self.negative_start_point, self.positive_start_point)
            },

            "direction_11": {
                "vector_A": mdc.vec3(self.positive_start_point, self.negative_start_point, self.Y),
                "vector_C": mdc.vec3(self.positive_start_point, self.negative_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.positive_start_point, self.X, self.positive_start_point)
            },

            "direction_12": {
                "vector_A": mdc.vec3(self.Y, self.negative_start_point, self.positive_start_point),
                "vector_C": mdc.vec3(self.positive_start_point, self.negative_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.positive_start_point, self.negative_start_point, self.X)
            },

            # back bottom left corner
            "direction_13": {
                "vector_A": mdc.vec3(self.X, self.positive_start_point, self.negative_start_point),
                "vector_C": mdc.vec3(self.negative_start_point, self.positive_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.negative_start_point, self.Y, self.negative_start_point),
            },

            "direction_14": {
                "vector_A": mdc.vec3(self.negative_start_point, self.X, self.negative_start_point),
                "vector_C": mdc.vec3(self.negative_start_point, self.positive_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.negative_start_point, self.positive_start_point, self.Y),
            },

            "direction_15": {
                "vector_A": mdc.vec3(self.negative_start_point, self.positive_start_point, self.X),
                "vector_C": mdc.vec3(self.negative_start_point, self.positive_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.Y, self.positive_start_point, self.negative_start_point),
            },

            # back bottom right corner
            "direction_16": {
                "vector_A": mdc.vec3(self.positive_start_point, self.Y, self.negative_start_point),
                "vector_C": mdc.vec3(self.positive_start_point, self.positive_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.X, self.positive_start_point, self.negative_start_point),
            },

            "direction_17": {
                "vector_A": mdc.vec3(self.positive_start_point, self.positive_start_point, self.Y),
                "vector_C": mdc.vec3(self.positive_start_point, self.positive_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.positive_start_point, self.X, self.negative_start_point),
            },

            "direction_18": {
                "vector_A": mdc.vec3(self.Y, self.positive_start_point, self.negative_start_point),
                "vector_C": mdc.vec3(self.positive_start_point, self.positive_start_point, self.negative_start_point),
                "vector_B": mdc.vec3(self.positive_start_point, self.positive_start_point, self.X),
            },

            # back upper left corner
            "direction_19": {
                "vector_A": mdc.vec3(self.negative_start_point, self.Y, self.positive_start_point),
                "vector_C": mdc.vec3(self.negative_start_point, self.positive_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.X, self.positive_start_point, self.positive_start_point),
            },

            "direction_20": {
                "vector_A": mdc.vec3(self.negative_start_point, self.positive_start_point, self.Y),
                "vector_C": mdc.vec3(self.negative_start_point, self.positive_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.negative_start_point, self.X, self.positive_start_point),
            },

            "direction_21": {
                "vector_A": mdc.vec3(self.Y, self.positive_start_point, self.positive_start_point),
                "vector_C": mdc.vec3(self.negative_start_point, self.positive_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.negative_start_point, self.positive_start_point, self.X),
            },

            # back upper right corner
            "direction_22": {
                "vector_A": mdc.vec3(self.X, self.positive_start_point, self.positive_start_point),
                "vector_C": mdc.vec3(self.positive_start_point, self.positive_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.positive_start_point, self.Y, self.positive_start_point),
            },

            "direction_23": {
                "vector_A": mdc.vec3(self.positive_start_point, self.X, self.positive_start_point),
                "vector_C": mdc.vec3(self.positive_start_point, self.positive_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.positive_start_point, self.positive_start_point, self.Y),
            },

            "direction_24": {
                "vector_A": mdc.vec3(self.positive_start_point, self.positive_start_point, self.X),
                "vector_C": mdc.vec3(self.positive_start_point, self.positive_start_point, self.positive_start_point),
                "vector_B": mdc.vec3(self.Y, self.positive_start_point, self.positive_start_point),
            },
        }

        self.depth = {
            "direction_1": self.depth * mdc.Z,
            "direction_2": self.depth * mdc.X,
            "direction_3": self.depth * mdc.Y,
            "direction_4": self.depth * mdc.Z,
            "direction_5": self.depth * -mdc.X,
            "direction_6": self.depth * mdc.Y,
            "direction_7": self.depth * -mdc.Z,
            "direction_8": self.depth * mdc.X,
            "direction_9": self.depth * mdc.Y,
            "direction_10": self.depth * -mdc.Z,
            "direction_11": self.depth * -mdc.X,
            "direction_12": self.depth * mdc.Y,
            "direction_13": self.depth * mdc.Z,
            "direction_14": self.depth * mdc.X,
            "direction_15": self.depth * -mdc.Y,
            "direction_16": self.depth * mdc.Z,
            "direction_17": self.depth * -mdc.X,
            "direction_18": self.depth * -mdc.Y,
            "direction_19": self.depth * -mdc.Z,
            "direction_20": self.depth * mdc.X,
            "direction_21": self.depth * -mdc.Y,
            "direction_22": self.depth * -mdc.Z,
            "direction_23": self.depth * -mdc.X,
            "direction_24": self.depth * -mdc.Y,
        }

    def manufacturing_time_calculation(self, triangle):
        manufacturing_time = self.max_manufacturing_time * (triangle.volume() / self.max_volume)
        if self.dir in ["direction_2", "direction_3", "direction_5", "direction_6", "direction_8",
                        "direction_9", "direction_11", "direction_12",  "direction_14", "direction_15",
                        "direction_17", "direction_18", "direction_21", "direction_23", "direction_24",]:
            manufacturing_time += self.manufacturing_time_side_supplement
        if self.dir in ["direction_1", "direction_4", "direction_13", "direction_16"]:
            manufacturing_time += self.manufacturing_time_bottom_supplement
        return manufacturing_time

    def transformation(self):
        _triangular_blind_step_primitive = [mdc.Segment(self.triangular_vectors[self.dir]["vector_A"],
                                                        self.triangular_vectors[self.dir]["vector_B"]),
                                            mdc.Segment(self.triangular_vectors[self.dir]["vector_B"],
                                                        self.triangular_vectors[self.dir]["vector_C"]),
                                            mdc.Segment(self.triangular_vectors[self.dir]["vector_C"],
                                                        self.triangular_vectors[self.dir]["vector_A"])],

        _triangular_blind_step = mdc.extrusion(self.depth[self.dir], mdc.flatsurface(_triangular_blind_step_primitive))
        _manufacturing_time = round(self.manufacturing_time_calculation(_triangular_blind_step), 4)

        return _triangular_blind_step, _manufacturing_time
