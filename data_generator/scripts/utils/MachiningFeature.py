from geometric_primitives.PowerOutlet import PowerOutlet
from geometric_primitives.Door import Door
from geometric_primitives.Window import Window
from geometric_primitives.TransportConnector import TransportConnector
from geometric_primitives.ElectricalCabinet import ElectricalCabinet
from geometric_primitives.ElecticalWire import ElectricalWire
from geometric_primitives.XFitConnector import XFitConnector


class MachiningFeature:
    def __init__(self, machining_feature_id, cltWall):
        self.machining_feature_id = machining_feature_id
        self._cltWall = cltWall
        self.machining_feature = [PowerOutlet, Door, Window, TransportConnector, ElectricalCabinet, ElectricalWire,
                                  XFitConnector]

    def create(self,):
        return self.machining_feature[self.machining_feature_id](self._cltWall).transformation()
