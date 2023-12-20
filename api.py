from flask import Flask, request, jsonify
import uuid
import random
import string

# Initialize the Flask application
app = Flask(__name__)

# Define a route with the path '/generate-id' accessible via GET requests
@app.route('/generate-id', methods=['GET'])
def generate_id():
    # Retrieve 'type' and 'count' from request arguments with default values
    id_type = request.args.get('type', 'uuid')
    count = min(int(request.args.get('count', 1)), 1000)

    # Generate UUIDs if id_type is 'uuid'
    if id_type == 'uuid':
        return jsonify([str(uuid.uuid4()) for _ in range(count)])
    # Generate random numeric IDs if id_type is 'numeric'
    elif id_type == 'numeric':
        return jsonify([str(random.randint(100000000000, 999999999999)) for _ in range(count)])
    # Generate random alphanumeric strings if id_type is 'string'
    elif id_type == 'string':
        return jsonify([''.join(random.choices(string.ascii_letters + string.digits, k=12)) for _ in range(count)])
    # Generate random hexadecimal strings if id_type is 'wep'
    elif id_type == 'wep':
        return jsonify([''.join(random.choices('0123456789ABCDEF', k=26)) for _ in range(count)])
    # Return an error for invalid id types
    else:
        return jsonify({"error": "Invalid id type"}), 400

# Run the Flask application in debug mode if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
