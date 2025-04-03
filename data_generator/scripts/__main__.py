import argparse
from DataGenerator import DataGenerator

_parser = argparse.ArgumentParser(description='Base configuration of the synthetic data generator')
_parser.add_argument('--target_directory',
                     dest='target_directory', default='TRAINING_DATASET_SOURCE', type=str,
                     help='The variables TRAINING_DATASET_SOURCE is a environment variables used'
                          'to access the training and test cad data in the CAFR framework. The variable is necessary'
                          'for the right saving of the training data')
_parser.add_argument('--cad_data_generation_start_cycle',
                     dest='cad_data_generation_start_cycle', type=int, default=1,
                     help='This value defines with which ID the data generation process starts. This can be important'
                          'if a dataset was already created and has to be increased with additional data. If the'
                          'start number of the data generation cycle then is not adapted, the existing data is just'
                          'overwritten')
_parser.add_argument('--cad_data_generation_end_cycles',
                     dest='cad_data_generation_end_cycles', type=int, default=10,
                     help='This value defines how many cad models with multiple machining feature are '
                          'created.')
_parser.add_argument('--machining_config',
                     dest='machining_config',
                     type=str,
                     default="""[(0, np.random.randint(0, 15)),
                                (1, np.random.randint(1, 3)), 
                                (2, np.random.randint(1, 4)),
                                (3, np.random.randint(1, 15)),
                                (4, np.random.randint(1, 3)),   
                                (5, np.random.randint(1, 10)),   
                                (6, np.random.randint(1, 13)),]""",
                     help='0: PowerOutlet, 1: Door, 2: Window, 3: TransportConnector, 4: ElectricalCabinet,'
                          '5: ElecticalWire, 6: XFitConnector:')
_parser.add_argument('--random_generation_seed',
                     dest='random_generation_seed', type=int, default=42,
                     help='Random seed for generating CAD models')
_parser.add_argument('--select_machining_feature_id_random',
                     dest='select_machining_feature_id_random', type=bool, default=False,
                     help='When true, the machining_feature_id in the Class DataGenerator is selected '
                          'randomly. If false it uses the config value machining_feature_id. Should only'
                          'be true for single machining feature creation.')
_parser.add_argument('--machining_feature_id',
                     dest='machining_feature_id', type=int, default=0,
                     help='This value selects a specific machining feature for the application to the base'
                          'primitive. Can only be used if "select_machining_feature_id_random" is False.'
                          'Should be true for single machining feature creation.')
if __name__ == '__main__':
    _config = _parser.parse_args()
    _data_generator = DataGenerator(_config)
    _data_generator.generate()
