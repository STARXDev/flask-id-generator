from flask import Flask, request, jsonify, send_file
import uuid
import random
import string
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import io
import base64

app = Flask(__name__)

# Load RSA keys from environment variable paths
PRIVATE_KEY_PATH = os.environ.get('PRIVATE_KEY_PATH')
PUBLIC_KEY_PATH = os.environ.get('PUBLIC_KEY_PATH')

def load_private_key(path_to_private_key):
    with open(path_to_private_key, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

def load_public_key(path_to_public_key):
    with open(path_to_public_key, "rb") as key_file:
        return serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

private_key = load_private_key(PRIVATE_KEY_PATH)
public_key = load_public_key(PUBLIC_KEY_PATH)

def rsa_encrypt(public_key, data):
    return public_key.encrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

def rsa_decrypt(private_key, data):
    return private_key.decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

def aes_encrypt(key, iv, data):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()

def aes_decrypt(key, iv, data):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()

@app.route('/get-public-key', methods=['GET'])
def get_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as key_file:
        return key_file.read()

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
        aes_key = os.urandom(32)  # AES key must be either 16, 24, or 32 bytes long
        iv = os.urandom(16)       # IV must be 16 bytes long for AES

        encrypted_data = aes_encrypt(aes_key, iv, data.encode())
        encrypted_aes_key = rsa_encrypt(public_key, aes_key)
        encrypted_iv = rsa_encrypt(public_key, iv)

        return jsonify({
            "encrypted_data": base64.b64encode(encrypted_data).decode(),
            "encrypted_aes_key": base64.b64encode(encrypted_aes_key).decode(),
            "encrypted_iv": base64.b64encode(encrypted_iv).decode()
        })
    return jsonify({"error": "No data provided"}), 400

@app.route('/decrypt', methods=['POST'])
def decrypt_data():
    encrypted_data = request.json.get('encrypted_data', '')
    encrypted_aes_key = request.json.get('encrypted_aes_key', '')
    encrypted_iv = request.json.get('encrypted_iv', '')

    if encrypted_data and encrypted_aes_key and encrypted_iv:
        aes_key = rsa_decrypt(private_key, base64.b64decode(encrypted_aes_key))
        iv = rsa_decrypt(private_key, base64.b64decode(encrypted_iv))
        decrypted_data = aes_decrypt(aes_key, iv, base64.b64decode(encrypted_data))

        return jsonify({"decrypted": decrypted_data.decode()})
    return jsonify({"error": "Required data missing"}), 400

@app.route('/encrypt-file', methods=['POST'])
def encrypt_file_route():
    if 'file' not in request.files:
        return "No file provided", 400

    file = request.files['file']
    aes_key = os.urandom(32)
    iv = os.urandom(16)

    encrypted_file = aes_encrypt(aes_key, iv, file.read())
    encrypted_aes_key = rsa_encrypt(public_key, aes_key)
    encrypted_iv = rsa_encrypt(public_key, iv)

    encrypted_io = io.BytesIO(encrypted_file)
    encrypted_io.seek(0)

    return jsonify({
        "encrypted_file": base64.b64encode(encrypted_io.read()).decode(),
        "encrypted_aes_key": base64.b64encode(encrypted_aes_key).decode(),
        "encrypted_iv": base64.b64encode(encrypted_iv).decode()
    })

@app.route('/decrypt-file', methods=['POST'])
def decrypt_file_route():
    if 'file' not in request.files or 'encrypted_aes_key' not in request.form or 'encrypted_iv' not in request.form:
        return "Required data missing", 400

    file = request.files['file']
    encrypted_aes_key = base64.b64decode(request.form['encrypted_aes_key'])
    encrypted_iv = base64.b64decode(request.form['encrypted_iv'])

    aes_key = rsa_decrypt(private_key, encrypted_aes_key)
    iv = rsa_decrypt(private_key, encrypted_iv)

    decrypted_file = aes_decrypt(aes_key, iv, file.read())
    decrypted_io = io.BytesIO(decrypted_file)
    decrypted_io.seek(0)

    return send_file(decrypted_io, as_attachment=True, download_name='decrypted_file')

if __name__ == '__main__':
    app.run(debug=True)
