import os
import numpy as np
import madcad as mdc
# from data_generator.scripts.utils.BinvoxConverter import BinvoxConverter
from geometric_primitives.base_primitive import Cube
from utils.MachiningFeature import MachiningFeature
from utils.CsgOperation import CsgOperation
from utils.MachiningFeatureLabels import MachiningFeatureLabels


class DataGenerator:
    def __init__(self, config):
        self.cad_data_generation_start_cycle = config.cad_data_generation_start_cycle
        self.cad_data_generation_end_cycles = config.cad_data_generation_end_cycles
        self.max_machining_feature_count = config.max_machining_feature_count
        self.target_directory = config.target_directory
        self.select_machining_feature_id_random = config.select_machining_feature_id_random
        self.machining_feature_id = config.machining_feature_id
        np.random.seed(config.random_generation_seed)

    def generate(self):
        for _model_id in range(self.cad_data_generation_start_cycle, self.cad_data_generation_end_cycles):
            _machining_feature_id_list = []
            _machining_feature_list = []
            _manufacturing_time = 0
            _new_cad_model = Cube(10, mdc.vec3(5, 5, 5)).transform()
            _machining_feature_count = np.random.randint(1, (self.max_machining_feature_count + 1))
            _machining_feature, _machining_feature_time = \
                MachiningFeature(0).create()
            try:
                for _ in range(_machining_feature_count):
                    if self.select_machining_feature_id_random:
                        _machining_feature_id = np.random.randint(0, 24)
                    else:
                        _machining_feature_id = self.machining_feature_id

                    _machining_feature, _machining_feature_time = \
                        MachiningFeature(_machining_feature_id).create()
                    if _machining_feature_time <= 0:
                        raise ValueError("Manufacturing time is zero or below.")
                    _manufacturing_time += _machining_feature_time
                    _new_cad_model = CsgOperation(_new_cad_model, _machining_feature).difference()


                    _machining_feature_id_list.append(_machining_feature_id)
                    _machining_feature_list.append(_machining_feature)
                mdc.write(_new_cad_model, os.getenv(self.target_directory) + "/" + str(_model_id) + ".stl")
                MachiningFeatureLabels(_machining_feature_list, _model_id, self.target_directory,
                                       _machining_feature_id_list).write_vertices_file()
                MachiningFeatureLabels(_machining_feature_list, _model_id, self.target_directory,
                                       _machining_feature_id_list).write_bounding_box_file()
                MachiningFeatureLabels(_machining_feature_list, _model_id, self.target_directory,
                                       _machining_feature_id_list).write_manufacturing_time_file(_manufacturing_time)

                print(f"Created CAD model {_model_id} with {_machining_feature_count} machining feature")
                print(f"machining feature: {_machining_feature_id_list}")
            except:
                # We use here a broad exception clause to avoid applying machining feature if not enough surface is
                # available
                print(f"One or more machining feature for the CAD model {_model_id} were not feasible."
                      f"The regarding machining feature had the id {_machining_feature_id}."
                      f" For CAD model {_model_id}, {_} from {_machining_feature_count} have been applied."
                      f" This can happen when not enough surface is available for the CSG difference operation")

            del _new_cad_model
            del _machining_feature_id_list

        # BinvoxConverter(self.target_directory).create_file()
