import math
import numpy as np
import madcad as mdc


class SixSidePassage:
    def __init__(self):
        self.dir = np.random.choice(["direction_1", "direction_2", "direction_3"])
        self.radius = np.random.uniform(1, 2.25)
        self.Cx = np.random.uniform(0.5 + self.radius, 9.5 - self.radius)
        self.Cy = np.random.uniform(0.5 + self.radius, 9.5 - self.radius)
        self.depth = 10.0002
        self.negative_start_point = -0.0001

        self.max_volume = 526
        self.max_manufacturing_time = 1.75
        self.manufacturing_time_side_supplement = 0.16

        self.six_side_vectors = {
            # top side
            "direction_1": {
                "vector_A": mdc.vec3(self.Cx + self.radius * math.cos(math.radians(-240)),
                                     self.Cy + self.radius * math.sin(math.radians(-240)), self.negative_start_point),
                "vector_B": mdc.vec3(self.Cx + self.radius * math.cos(math.radians(-300)),
                                     self.Cy + self.radius * math.sin(math.radians(-300)), self.negative_start_point),
                "vector_C": mdc.vec3(self.Cx + self.radius, self.Cy, self.negative_start_point),
                "vector_D": mdc.vec3(self.Cx + self.radius * math.cos(math.radians(-60)),
                                     self.Cy + self.radius * math.sin(math.radians(-60)), self.negative_start_point),
                "vector_E": mdc.vec3(self.Cx + self.radius * math.cos(math.radians(-120)),
                                     self.Cy + self.radius * math.sin(math.radians(-120)), self.negative_start_point),
                "vector_F": mdc.vec3(self.Cx - self.radius, self.Cy, self.negative_start_point),
            },
            # front side
            "direction_2": {
                "vector_A": mdc.vec3(self.Cx - self.radius, self.negative_start_point, self.Cy),
                "vector_B": mdc.vec3(self.Cx + self.radius * math.cos(math.radians(-120)),
                                     self.negative_start_point, self.Cy + self.radius * math.sin(math.radians(-120))),
                "vector_C": mdc.vec3(self.Cx + self.radius * math.cos(math.radians(-60)),
                                     self.negative_start_point,
                                     self.Cy + self.radius * math.sin(math.radians(-60))),
                "vector_D": mdc.vec3(self.Cx + self.radius, self.negative_start_point, self.Cy),
                "vector_E": mdc.vec3(self.Cx + self.radius * math.cos(math.radians(-300)), self.negative_start_point,
                                     self.Cy + self.radius * math.sin(math.radians(-300))),
                "vector_F": mdc.vec3(self.Cx + self.radius * math.cos(math.radians(-240)), self.negative_start_point,
                                     self.Cy + self.radius * math.sin(math.radians(-240))),
            },
            # right side
            "direction_3": {
                "vector_A": mdc.vec3(self.negative_start_point, self.Cx + self.radius * math.cos(math.radians(-240)),
                                     self.Cy + self.radius * math.sin(math.radians(-240))),
                "vector_B": mdc.vec3(self.negative_start_point, self.Cx + self.radius * math.cos(math.radians(-300)),
                                     self.Cy + self.radius * math.sin(math.radians(-300))),
                "vector_C": mdc.vec3(self.negative_start_point, self.Cx + self.radius, self.Cy),
                "vector_D": mdc.vec3(self.negative_start_point, self.Cx + self.radius * math.cos(math.radians(-60)),
                                     self.Cy + self.radius * math.sin(math.radians(-60))),
                "vector_E": mdc.vec3(self.negative_start_point, self.Cx + self.radius * math.cos(math.radians(-120)),
                                     self.Cy + self.radius * math.sin(math.radians(-120))),
                "vector_F": mdc.vec3(self.negative_start_point, self.Cx - self.radius, self.Cy)},
        }

        self.depth = {
            "direction_1": self.depth * mdc.Z,
            "direction_2": self.depth * mdc.Y,
            "direction_3": self.depth * mdc.X,
        }

    def manufacturing_time_calculation(self, six_side_passage):
        manufacturing_time = self.max_manufacturing_time * (six_side_passage.volume() / self.max_volume)
        if self.dir in ["direction_2", "direction_3"]:
            manufacturing_time += self.manufacturing_time_side_supplement
        return manufacturing_time

    def transformation(self):
        _six_side_passage_primitive = [mdc.Segment(self.six_side_vectors[self.dir]["vector_A"],
                                                   self.six_side_vectors[self.dir]["vector_B"]),
                                       mdc.Segment(self.six_side_vectors[self.dir]["vector_B"],
                                                   self.six_side_vectors[self.dir]["vector_C"]),
                                       mdc.Segment(self.six_side_vectors[self.dir]["vector_C"],
                                                   self.six_side_vectors[self.dir]["vector_D"]),
                                       mdc.Segment(self.six_side_vectors[self.dir]["vector_D"],
                                                   self.six_side_vectors[self.dir]["vector_E"]),
                                       mdc.Segment(self.six_side_vectors[self.dir]["vector_E"],
                                                   self.six_side_vectors[self.dir]["vector_F"]),
                                       mdc.Segment(self.six_side_vectors[self.dir]["vector_F"],
                                                   self.six_side_vectors[self.dir]["vector_A"])],

        _six_side_passage = mdc.extrusion(self.depth[self.dir], mdc.flatsurface(_six_side_passage_primitive))
        _manufacturing_time = round(self.manufacturing_time_calculation(_six_side_passage), 4)

        return _six_side_passage, _manufacturing_time
