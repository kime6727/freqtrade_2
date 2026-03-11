from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

CONFIG_PATH = os.environ.get('CONFIG_PATH', '/freqtrade/user_data/config.json')

@app.route('/api/v1/save_config', methods=['POST'])
def save_config():
    try:
        config_data = request.get_data(as_text=True)
        
        json_obj = json.loads(config_data)
        
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(json_obj, f, indent=4, ensure_ascii=False)
        
        return jsonify({"status": "success", "message": "Configuration saved successfully"}), 200
    except json.JSONDecodeError as e:
        return jsonify({"status": "error", "message": f"Invalid JSON: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
