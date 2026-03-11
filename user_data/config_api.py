from flask import Flask, request, jsonify, send_from_directory
import os
import json
import time
import threading

app = Flask(__name__, static_folder='.', static_url_path='')

CONFIG_PATH = os.environ.get('CONFIG_PATH', '/freqtrade/user_data/config.json')
CONFIG_LOCK = threading.Lock()

def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(data):
    with CONFIG_LOCK:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    return send_from_directory('.', 'config_manager.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    try:
        config = load_config()
        return jsonify({"status": "success", "data": config}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/config', methods=['POST'])
def update_config():
    try:
        config_data = request.get_json()
        if not config_data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        
        save_config(config_data)
        return jsonify({"status": "success", "message": "Configuration saved successfully"}), 200
    except json.JSONDecodeError as e:
        return jsonify({"status": "error", "message": f"Invalid JSON: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/config/validate', methods=['POST'])
def validate_config():
    try:
        config_data = request.get_json()
        required_fields = ['exchange', 'pairlists']
        missing = [f for f in required_fields if f not in config_data]
        
        if missing:
            return jsonify({"status": "error", "message": f"Missing required fields: {', '.join(missing)}"}), 400
        
        return jsonify({"status": "success", "message": "Configuration is valid"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "freqtrade-config-api"}), 200

@app.route('/api/v1/save_config', methods=['POST'])
def save_config_legacy():
    try:
        config_data = request.get_data(as_text=True)
        json_obj = json.loads(config_data)
        save_config(json_obj)
        return jsonify({"status": "success", "message": "Configuration saved successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=False)
