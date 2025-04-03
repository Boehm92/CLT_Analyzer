import os
import numpy as np
import madcad as mdc
from geometric_primitives.base_primitive import CltWall
from utils.MachiningFeature import MachiningFeature
from utils.CsgOperation import CsgOperation
from utils.MachiningFeatureLabels import MachiningFeatureLabels


class DataGenerator:
    def __init__(self, config):
        self.cad_data_generation_start_cycle = config.cad_data_generation_start_cycle
        self.cad_data_generation_end_cycles = config.cad_data_generation_end_cycles
        self.target_directory = config.target_directory
        self.select_machining_feature_id_random = config.select_machining_feature_id_random
        self.machining_feature_id = config.machining_feature_id
        self.machining_config = eval(config.machining_config)
        np.random.seed(config.random_generation_seed)

    def generate(self):
        for _model_id in range(self.cad_data_generation_start_cycle, self.cad_data_generation_end_cycles):
            _machining_feature_id_list = []
            _machining_feature_list = []
            _manufacturing_time = 0
            _cltWall = CltWall()
            _new_cad_model = _cltWall.transform()

            for _machining_feature_id, _count in self.machining_config:
                try:
                    for _ in range(_count):
                        _machining_feature, _machining_feature_time = \
                            MachiningFeature(_machining_feature_id, _cltWall).create()

                        if _machining_feature_time <= 0:
                            raise ValueError("Manufacturing time is zero or below.")

                        _manufacturing_time += _machining_feature_time
                        _new_cad_model = CsgOperation(_new_cad_model, _machining_feature).difference()
                        _new_cad_model.mergeclose()
                        _new_cad_model = mdc.segmentation(_new_cad_model)

                        _machining_feature_id_list.append(_machining_feature_id)
                        _machining_feature_list.append(_machining_feature)

                except Exception as e:
                    print(f"[⚠] Feature-ID {_machining_feature_id} nicht alle anwendbar für Modell {_model_id}")

            mdc.write(_new_cad_model, os.path.join(os.getenv(self.target_directory), f"{_model_id}.stl"))

            labels = MachiningFeatureLabels(_machining_feature_list, _model_id, self.target_directory,
                                            _machining_feature_id_list)
            labels.write_vertices_file()
            labels.write_bounding_box_file()
            labels.write_manufacturing_time_file(_manufacturing_time)

            print(f"✔ Created CAD model {_model_id} with features: {_machining_feature_id_list}")

            del _new_cad_model
            del _machining_feature_id_list
