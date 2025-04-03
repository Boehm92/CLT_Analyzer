from data_generator.scripts.geometric_primitives.PowerOutlet import PowerOutlet
from data_generator.scripts.geometric_primitives.Door import Door
from data_generator.scripts.geometric_primitives.Window import Window
from data_generator.scripts.geometric_primitives.TransportConnector import TransportConnector
from data_generator.scripts.geometric_primitives.ElectricalCabinet import ElectricalCabinet
from data_generator.scripts.geometric_primitives.ElecticalWire import ElectricalWire
from data_generator.scripts.geometric_primitives.XFitConnector import XFitConnector


class MachiningFeature:
    def __init__(self, machining_feature_id, cltWall):
        self.machining_feature_id = machining_feature_id
        self._cltWall = cltWall
        self.machining_feature = [PowerOutlet, Door, Window, TransportConnector, ElectricalCabinet, ElectricalWire,
                                  XFitConnector]

    def create(self,):
        return self.machining_feature[self.machining_feature_id](self._cltWall).transformation()
