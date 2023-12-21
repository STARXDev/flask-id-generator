Flask ID Generator API

This project is a Flask web application designed to generate different types of identifiers (IDs). It offers a simple API for generating UUIDs, random numeric IDs, random alphanumeric strings, and hexadecimal strings. Additionally, it includes encryption and decryption functionalities, both for strings and larger files like audio recordings. It's useful for learning Flask basics and as a tool for generating unique identifiers and securely handling data encryption for various purposes.

Features:

-Generate UUIDs.

-Generate random numeric IDs.

-Generate random alphanumeric strings.

-Generate random hexadecimal strings.

-Encrypt and decrypt strings securely.

-Encrypt and decrypt files securely.

Installation:

To set up the project locally, follow these steps:

-Clone the Repository

git clone https://github.com/your-username/flask-id-generator.git
Navigate to the Project Directory

cd flask-id-generator
Install Dependencies

pip install -r requirements.txt

Usage:
Run the application using the following command:

python app.py

After starting the server, it will be accessible at http://localhost:5000.

API Endpoints

-Generate ID:

API Endpoints:

Generate ID:

Endpoint: /generate-id

Method: GET
Parameters:
type: Type of ID to generate (uuid, numeric, string, wep). Default is uuid.
count: Number of IDs to generate. Default is 1, maximum is 1000.

Example Request: Generate 5 alphanumeric strings:
http://localhost:5000/generate-id?type=string&count=5

Encrypt Data:

Endpoint: /encrypt
Method: POST
Body: JSON object with a data field containing the string to be encrypted.
Example Request: Encrypt a string:
Use a tool like curl or Postman to POST a JSON object {"data": "your_string_to_encrypt"} to http://localhost:5000/encrypt.

Decrypt Data:

Endpoint: /decrypt
Method: POST
Body: JSON object with a data field containing the encrypted string.
Example Request: Decrypt a string:
Use a tool like curl or Postman to POST a JSON object {"data": "encrypted_string_here"} to http://localhost:5000/decrypt.

Local Testing for data encryption:

Testing Encryption:
To encrypt the string "Hello, Dream Keeper!", use the following curl command:


curl -X POST http://127.0.0.1:5000/encrypt -H "Content-Type: application/json" -d "{\"data\":\"Hello, Dream Keeper!\"}"

You'll receive a response with the encrypted version of this string, which will look like a random string of characters.

Testing Decryption:
To decrypt an encrypted string, use the curl command with the encrypted data:

curl -X POST http://127.0.0.1:5000/decrypt -H "Content-Type: application/json" -d "{\"data\":\"encrypted_string_here\"}"
Replace encrypted_string_here with the actual encrypted string you received. The response should give you back the original string.


Encrypt File:

Endpoint: /encrypt-file
Method: POST
Form Data:
file: The file to be encrypted.

Usage: Use a tool like curl or Postman to POST the file to http://localhost:5000/encrypt-file. The response will be the encrypted file.

Decrypt File:
Endpoint: /decrypt-file
Method: POST
Form Data:
file: The encrypted file to be decrypted.

Usage: Use a tool like curl or Postman to POST the encrypted file to http://localhost:5000/decrypt-file. The response will be the decrypted file.

Secure Key and IV Management in Real-World Scenarios:
For production environments, it's essential to securely manage the encryption keys and IVs used for file encryption and decryption. This involves:

Storing Keys and IVs: Store the encryption keys and IVs in a secure database or a managed service like AWS KMS or Azure Key Vault. Each key and IV should be associated with a unique identifier for the file or user.

Retrieving Keys for Decryption: When decrypting a file, retrieve the corresponding key and IV from the secure storage using the file's unique identifier.

Ensuring Security: Implement robust security measures to protect the key storage, including access controls, encryption in transit, and regular security audits.


Contributing

If you wish to contribute to this project, feel free to fork the repository and submit pull requests. You can also open issues for bugs or feature suggestions.

License

This project is licensed under the MIT License - see the LICENSE file for details.