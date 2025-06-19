import argparse
from multiprocessing import Pool, cpu_count
from DataGenerator import run_single_model

_parser = argparse.ArgumentParser(description='Base configuration of the synthetic data generator')
_parser.add_argument('--target_directory',
                     dest='target_directory', default='TRAINING_DATASET_SOURCE', type=str,
                     help='The variable TRAINING_DATASET_SOURCE is an environment variable used '
                          'to access the training and test CAD data in the CAFR framework.')
_parser.add_argument('--cad_data_generation_start_cycle',
                     dest='cad_data_generation_start_cycle', type=int, default=24001,
                     help='Start ID of the data generation process.')
_parser.add_argument('--cad_data_generation_end_cycles',
                     dest='cad_data_generation_end_cycles', type=int, default=56655,
                     help='End ID of the data generation process (non-inclusive).')
_parser.add_argument('--machining_config',
                     dest='machining_config',
                     type=str,
                     default="""[(0, np.random.randint(0, 10)),
                                (1, np.random.randint(1, 2)),
                                (2, np.random.randint(1, 3)),
                                (3, np.random.randint(1, 10)),
                                (4, np.random.randint(1, 2)),
                                (5, np.random.randint(1, 6)),
                                (6, np.random.randint(1, 9))]""",
                     help='Machining feature config: (ID, count)')
_parser.add_argument('--random_generation_seed',
                     dest='random_generation_seed', type=int, default=42,
                     help='Random seed for consistent generation.')

if __name__ == '__main__':
    _config = _parser.parse_args()

    model_ids = list(range(_config.cad_data_generation_start_cycle, _config.cad_data_generation_end_cycles))
    num_workers = 18

    print(f"🔧 Starte parallele Datengenerierung mit {num_workers} Prozessen ...")

    with Pool(num_workers) as pool:
        pool.map(run_single_model, [(model_id, _config) for model_id in model_ids])

    print("✅ Datengenerierung abgeschlossen.")
