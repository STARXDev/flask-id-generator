from flask import Flask, request, jsonify
import uuid
import random
import string
import os
from cryptography.fernet import Fernet

# Initialize the Flask application
app = Flask(__name__)

# Retrieve the key from an environment variable
key = os.environ.get('SECRET_KEY')
if not key:
    raise ValueError("No secret key set for encryption")

cipher_suite = Fernet(key)

@app.route('/generate-id', methods=['GET'])
def generate_id():
    id_type = request.args.get('type', 'uuid')
    count = min(int(request.args.get('count', 1)), 1000)

    if id_type == 'uuid':
        return jsonify([str(uuid.uuid4()) for _ in range(count)])
    elif id_type == 'numeric':
        return jsonify([str(random.randint(100000000000, 999999999999)) for _ in range(count)])
    elif id_type == 'string':
        return jsonify([''.join(random.choices(string.ascii_letters + string.digits, k=12)) for _ in range(count)])
    elif id_type == 'wep':
        return jsonify([''.join(random.choices('0123456789ABCDEF', k=26)) for _ in range(count)])
    else:
        return jsonify({"error": "Invalid id type"}), 400

@app.route('/encrypt', methods=['POST'])
def encrypt_data():
    data = request.json.get('data', '')
    if data:
        encrypted_data = cipher_suite.encrypt(data.encode())
        return jsonify({"encrypted": encrypted_data.decode()})
    return jsonify({"error": "No data provided"}), 400

@app.route('/decrypt', methods=['POST'])
def decrypt_data():
    data = request.json.get('data', '')
    if data:
        try:
            decrypted_data = cipher_suite.decrypt(data.encode())
            return jsonify({"decrypted": decrypted_data.decode()})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "No data provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
