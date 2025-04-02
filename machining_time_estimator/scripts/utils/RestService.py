import os
import base64
import numpy as np
from flask_cors import CORS
from flask import Flask, request, jsonify

class RestService:
    def __init__(self, machining_feature_localizer):
        self.machining_feature_localizer = machining_feature_localizer
        self.app = Flask(__name__)
        CORS(self.app)  # 🔹 Allow all origins
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/processstlmodel', methods=['POST'])
        def process_stl_model():
            try:
                # Entferne alte Dateien
                try:
                    os.remove(os.path.join(os.getenv('TEST_DATA'), "processed/mte_data.pt"))
                    os.remove(os.path.join(os.getenv('TEST_DATA'), "processed/pre_filter.pt"))
                    os.remove(os.path.join(os.getenv('TEST_DATA'), "processed/pre_transform.pt"))
                    os.remove(os.path.join(os.getenv('TEST_DATA'), "received.stl"))
                except FileNotFoundError:
                    print('Graph test data could not be found.')
                except Exception as e:
                    print(f'Graph test data could not be deleted: {e}')

                # Validierung des Requests
                if not request.is_json:
                    return jsonify({"error": "Invalid JSON format"}), 400

                data = request.get_json()

                if "stl_base64" not in data:
                    return jsonify({"error": "Missing 'stl_base64' key in request"}), 400

                _stl_as_base64_string = data["stl_base64"]
                self.create_and_write_stl_file(_stl_as_base64_string)

                _response = self.machining_feature_localizer.test()

                if _response is None:
                    print("🚨 Model did not return predictions")
                    return jsonify({"error": "Model failed to return predictions"}), 500

                _response = self.convert_numpy_types(_response)

                return jsonify(_response), 200

            except Exception as e:
                print(f"🚨 Critical server error: {str(e)}")
                return jsonify({"error": f"Critical server error: {str(e)}"}), 500

    def convert_numpy_types(self, obj):
        """
        Konvertiere rekursiv alle numpy-Typen in native Python-Typen.
        """
        if isinstance(obj, dict):
            return {k: self.convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_numpy_types(i) for i in obj]
        elif isinstance(obj, (np.float32, np.float64, float, np.int32, np.int64, int)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            try:
                return float(obj)
            except:
                return str(obj)
        return obj

    def create_and_write_stl_file(self, stl_as_base64_string):
        _stl_file_path = "received.stl"
        absolute_stl_file_path = self.get_absolute_stl_file_path(_stl_file_path)
        _stl_bytes = base64.b64decode(stl_as_base64_string)

        with open(absolute_stl_file_path, 'wb') as stl_file:
            stl_file.write(_stl_bytes)

    def get_absolute_stl_file_path(self, file_name):
        path = os.getenv('TEST_DATA')
        return os.path.join(path, file_name)
