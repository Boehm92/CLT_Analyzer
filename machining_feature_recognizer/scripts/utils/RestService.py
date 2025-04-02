import os
import base64
import numpy as np
from flask_cors import CORS
from flask import Flask, request, jsonify

class RestService:
    def __init__(self, machining_feature_recognizer):
        self.machining_feature_recognizer = machining_feature_recognizer
        self.app = Flask(__name__)
        CORS(self.app)  # 🔹 Allow all origins
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/processstlmodel', methods=['POST'])
        def process_stl_model():
            try:
                os.remove(os.path.join(os.getenv('TEST_DATA'), "processed/mfr_data.pt"))
                os.remove(os.path.join(os.getenv('TEST_DATA'), "processed/pre_filter.pt"))
                os.remove(os.path.join(os.getenv('TEST_DATA'), "processed/pre_transform.pt"))
                os.remove(os.path.join(os.getenv('TEST_DATA'), "received.stl"))
            except FileNotFoundError:
                print('graph test data could not be found.')
            except Exception as e:
                print(f'graph test data could not be deleted: {e}')

            try:
                if not request.is_json:
                    return jsonify({"error": "Invalid JSON format"}), 400

                data = request.get_json()

                if "stl_base64" not in data:
                    return jsonify({"error": "Missing 'stl_base64' key in request"}), 400

                _stl_as_base64_string = data["stl_base64"]
                self.create_and_write_stl_file(_stl_as_base64_string)

                _response = self.machining_feature_recognizer.test()

                if _response is None:
                    print("🚨 Model did not return predictions")
                    return jsonify({"error": "Model failed to return predictions"}), 500

                if isinstance(_response, np.ndarray):
                    _response = _response.tolist()

                return jsonify(_response), 200

            except Exception as e:
                print(f"🚨 Critical server error: {str(e)}")
                return jsonify({"error": f"Critical server error: {str(e)}"}), 500

    def create_and_write_stl_file(self, stl_as_base64_string):
        _stl_file_path = "received.stl"
        absolute_stl_file_path = self.get_absolute_stl_file_path(_stl_file_path)
        _stl_bytes = base64.b64decode(stl_as_base64_string)

        with open(absolute_stl_file_path, 'wb') as stl_file:
            stl_file.write(_stl_bytes)

    def get_absolute_stl_file_path(self, file_name):
        path = os.getenv('TEST_DATA')
        return os.path.join(path, file_name)