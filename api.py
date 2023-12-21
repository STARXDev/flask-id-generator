from flask import Flask, request, jsonify, send_file
import uuid
import random
import string
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import io

app = Flask(__name__)

# Retrieve the key from an environment variable
fernet_key = os.environ.get('SECRET_KEY')
if not fernet_key:
    raise ValueError("No secret key set for encryption")

cipher_suite = Fernet(fernet_key)

def aes_encrypt(key, iv, data):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()

def aes_decrypt(key, iv, data):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()

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

@app.route('/encrypt-file', methods=['POST'])
def encrypt_file_route():
    if 'file' not in request.files:
        return "No file provided", 400

    file = request.files['file']
    aes_key = os.urandom(32)  # AES key must be either 16, 24, or 32 bytes long
    iv = os.urandom(16)       # IV must be 16 bytes long for AES

    encrypted_file = aes_encrypt(aes_key, iv, file.read())
    encrypted_io = io.BytesIO(encrypted_file)
    encrypted_io.seek(0)

    return send_file(encrypted_io, as_attachment=True, attachment_filename='encrypted_file')

@app.route('/decrypt-file', methods=['POST'])
def decrypt_file_route():
    if 'file' not in request.files:
        return "No file provided", 400

    file = request.files['file']
    aes_key = os.urandom(32)  # Same AES key length as encryption
    iv = os.urandom(16)       # Same IV length as encryption

    decrypted_file = aes_decrypt(aes_key, iv, file.read())
    decrypted_io = io.BytesIO(decrypted_file)
    decrypted_io.seek(0)

    return send_file(decrypted_io, as_attachment=True, attachment_filename='decrypted_file')

if __name__ == '__main__':
    app.run(debug=True)
