from geometric_primitives.ORing import ORing
from geometric_primitives.ThroughHole import ThroughHole
from geometric_primitives.BlindHole import BlindHole
from geometric_primitives.TriangularPassage import TriangularPassage
from geometric_primitives.RectangularPassage import RectangularPassage
from geometric_primitives.TriangularPocket import TriangularPocket
from geometric_primitives.RectangularPocket import RectangularPocket
from geometric_primitives.CircularThroughSlot import CircularThroughSlot
from geometric_primitives.TriangularThroughSlot import TriangularThroughSlot
from geometric_primitives.RectangularTroughSlot import RectangularTroughSlot
from geometric_primitives.RectangularBlindSlot import RectangularBlindSlot
from geometric_primitives.CircularEndPocket import CircularEndPocket
from geometric_primitives.TriangularBlindStep import TriangularBlindStep
from geometric_primitives.CircularBlindStep import CircularBlindStep
from geometric_primitives.RectangularBlindStep import RectangularBlindStep
from geometric_primitives.RectangularTroughStep import RectangularTroughStep
from geometric_primitives.TwoSideThroughStep import TwoSideThroughStep
from geometric_primitives.SlantedThroughStep import SlantedThroughStep
from geometric_primitives.Chamfer import Chamfer
from geometric_primitives.Round import Round
from geometric_primitives.VerticalCircularEndBlindSlot import \
    VerticalCircularEndBlindSlot
from geometric_primitives.HorizontalCircularEndBlindSlot import \
    HorizontalCircularEndBlindSlot
from geometric_primitives.SixSidePassage import SixSidePassage
from geometric_primitives.SixSidePocket import SixSidePocket


class MachiningFeature:
    def __init__(self, machining_feature_id):
        self.machining_feature_id = machining_feature_id
        self.machining_feature = [ORing, ThroughHole, BlindHole, TriangularPassage, RectangularPassage,
                                  CircularThroughSlot, TriangularThroughSlot, RectangularTroughSlot,
                                  RectangularBlindSlot, TriangularPocket, RectangularPocket, CircularEndPocket,
                                  TriangularBlindStep, CircularBlindStep, RectangularBlindStep, RectangularTroughStep,
                                  TwoSideThroughStep, SlantedThroughStep, Chamfer, Round, VerticalCircularEndBlindSlot,
                                  HorizontalCircularEndBlindSlot, SixSidePassage, SixSidePocket]

    def create(self):
        return self.machining_feature[self.machining_feature_id]().transformation()
