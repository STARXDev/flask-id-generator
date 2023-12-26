import unittest
import json
import base64
from io import BytesIO
from api import app  # Make sure to import your Flask app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_generate_id_uuid(self):
        response = self.app.get('/generate-id?type=uuid&count=1')
        self.assertEqual(response.status_code, 200)
        # Add more assertions here to check the content of the response

    def test_encrypt_decrypt(self):
        test_data = {"data": "Test String"}
        encrypt_response = self.app.post('/encrypt', data=json.dumps(test_data), content_type='application/json')
        self.assertEqual(encrypt_response.status_code, 200)

        encrypted_data = json.loads(encrypt_response.data)
        decrypt_response = self.app.post('/decrypt', data=json.dumps(encrypted_data), content_type='application/json')
        self.assertEqual(decrypt_response.status_code, 200)

        decrypted_data = json.loads(decrypt_response.data)
        self.assertEqual(decrypted_data['decrypted'], test_data['data'])

    def test_file_encryption_decryption(self):
        # Simulate a file upload for encryption
        test_file = (BytesIO(b"Test file content"), 'test.txt')
        encrypt_response = self.app.post('/encrypt-file', data={'file': test_file}, content_type='multipart/form-data')
        self.assertEqual(encrypt_response.status_code, 200)

        encrypted_data = json.loads(encrypt_response.data)
        self.assertIn('encrypted_file', encrypted_data)

        # Simulate sending the encrypted data to the decrypt endpoint
        encrypted_file = BytesIO(base64.b64decode(encrypted_data['encrypted_file']))
        decrypt_data = {
            'file': (encrypted_file, 'test.txt'),
            'encrypted_aes_key': encrypted_data['encrypted_aes_key'],
            'encrypted_iv': encrypted_data['encrypted_iv']
        }
        decrypt_response = self.app.post('/decrypt-file', data=decrypt_data, content_type='multipart/form-data')
        self.assertEqual(decrypt_response.status_code, 200)

        # Read the decrypted file content and compare with original
        decrypted_file = decrypt_response.data
        self.assertEqual(decrypted_file, b"Test file content")


if __name__ == '__main__':
    unittest.main()
