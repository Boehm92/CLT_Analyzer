import madcad as mdc


class Cube:
    def __init__(self, side_length, position):
        self.side_length = side_length
        self.position = position

    def transform(self):
        return mdc.brick(width=mdc.vec3(self.side_length)).transform(self.position)
