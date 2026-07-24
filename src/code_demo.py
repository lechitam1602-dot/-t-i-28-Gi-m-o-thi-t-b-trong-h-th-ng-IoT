import json
import logging
import os
import hmac
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "../results/logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

DEVICES_FILE = os.path.join(BASE_DIR, "../data/devices.json")

def load_devices():
    """Hàm nạp danh sách thiết bị từ file devices.json"""
    if os.path.exists(DEVICES_FILE):
        with open(DEVICES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@app.route('/telemetry', methods=['POST'])
def receive_telemetry():
    data = request.get_json()
    
    if not data:
        msg = "[REJECTED] Dữ liệu gửi lên không đúng định dạng JSON."
        logging.warning(msg)
        return jsonify({"status": "error", "message": "Payload không hợp lệ"}), 400

    device_id = data.get("device_id")
    value = data.get("value")
    token = data.get("token")
    client_hmac = data.get("hmac") 

    devices = load_devices()

    if not device_id or device_id not in devices:
        msg = f"[SPOOF DETECTED] Từ chối: device_id '{device_id}' GIẢ MẠO hoặc KHÔNG TỒN TẠI trong danh sách!"
        logging.warning(msg)
        return jsonify({"status": "rejected", "reason": "Thiết bị giả mạo / Không tồn tại"}), 401

    device_info = devices[device_id]

    if token and token != device_info.get("token"):
        msg = f"[SPOOF DETECTED] Từ chối: Token không đúng cho thiết bị '{device_id}'. (Token nhận được: '{token}')"
        logging.warning(msg)
        return jsonify({"status": "rejected", "reason": "Token không hợp lệ"}), 403

    if client_hmac:
        secret_key = device_info.get("secret_key", "").encode('utf-8')
        message = f"{device_id}:{value}".encode('utf-8')
        expected_hmac = hmac.new(secret_key, message, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(expected_hmac, client_hmac):
            msg = f"[SPOOF DETECTED] Từ chối: Chữ ký HMAC không khớp cho thiết bị '{device_id}'."
            logging.warning(msg)
            return jsonify({"status": "rejected", "reason": "Chữ ký HMAC không hợp lệ"}), 403

    msg = f"[SUCCESS] Nhận dữ liệu HỢP LỆ từ '{device_id}': value = {value}"
    logging.info(msg)
    return jsonify({"status": "success", "message": "Dữ liệu hợp lệ đã được chấp nhận"}), 200

if __name__ == '__main__':
    print(">>> Server API Flask đang chạy tại http://127.0.0.1:5000/telemetry")
    app.run(host='0.0.0.0', port=5000, debug=True)
