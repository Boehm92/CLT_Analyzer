import os
import time
import numpy as np
import madcad as mdc
from geometric_primitives.base_primitive import CltWall
from utils.MachiningFeature import MachiningFeature
from utils.MachiningFeatureLabels import MachiningFeatureLabels

def run_single_model(args):
    model_id, config = args
    start_time = time.time()  # ⏱️ Startzeit für Benchmarking

    base_path = os.getenv(config.target_directory)
    np.random.seed(config.random_generation_seed + model_id)

    _machining_feature_id_list = []
    _machining_feature_list = []
    _manufacturing_time = 0

    try:
        # Basiswand erzeugen
        _cltWall = CltWall()
        _new_cad_model = _cltWall.transform()

        # Zufällige Features konfigurieren
        _machining_config = [(0, np.random.randint(0, 8)),
                             (1, np.random.randint(0, 2)),
                             (2, np.random.randint(0, 4)),
                             (3, np.random.randint(1, 7)),
                             (4, np.random.randint(0, 3)),
                             (5, np.random.choice([0, 0, 0, 0, 1, 2, 3, 4, 5])),
                             (6, np.random.randint(0, 9)),]
                             # (2, np.random.randint(0, 4)),
                             # (3, np.random.randint(1, 7)),
                             # (4, np.random.randint(0, 3)),
                             # (5, np.random.choice([0, 0, 0, 0, 1, 2, 3, 4, 5])),
                             # (6, np.random.randint(4, 9))]

        generated_features = []
        generated_ids = []

        for feature_id, count in _machining_config:
            for _ in range(count):
                try:
                    feature, m_time = MachiningFeature(feature_id, _cltWall).create()
                    if m_time <= 0:
                        raise ValueError("Manufacturing time is zero or negative.")
                    _manufacturing_time += m_time
                    generated_features.append(feature)
                    generated_ids.append(feature_id)
                except Exception as e:
                    print(f"[⚠] Fehler beim Erzeugen von Feature {feature_id} für Modell {model_id}: {e}")

        # Feature sukzessive subtrahieren
        valid_features = []
        valid_ids = []
        for i, feature in enumerate(generated_features):
            try:
                _new_cad_model = mdc.difference(_new_cad_model, feature)
                valid_features.append(feature)
                valid_ids.append(generated_ids[i])
            except Exception as e:
                print(f"[⚠] CSG-Differenz fehlgeschlagen (Modell {model_id}, Feature-ID {generated_ids[i]}): {e}")

        # Finales Modell verarbeiten
        _new_cad_model.mergeclose()
        _new_cad_model = mdc.segmentation(_new_cad_model)

        # Speichern
        model_path = os.path.join(base_path, f"{model_id}.stl")
        mdc.write(_new_cad_model, model_path)

        # Labels schreiben
        labels = MachiningFeatureLabels(valid_features, model_id, config.target_directory, valid_ids)
        labels.write_vertices_file()
        labels.write_bounding_box_file()
        labels.write_manufacturing_time_file(_manufacturing_time)

        elapsed = round(time.time() - start_time, 2)  # ⏱️ Zeit stoppen
        print(f"✔ Modell {model_id} erstellt mit {len(valid_features)} Features: {valid_ids} ({elapsed} Sek.)")

    except Exception as e:
        elapsed = round(time.time() - start_time, 2)
        print(f"[⛔] Schwerwiegender Fehler bei Modell {model_id} ({elapsed} Sek.): {e}")
