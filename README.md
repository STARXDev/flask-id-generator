Flask ID Generator API

This project is a Flask web application designed to generate different types of identifiers (IDs). It offers a simple API for generating UUIDs, random numeric IDs, random alphanumeric strings, and hexadecimal strings. It's useful for learning Flask basics and as a tool for generating unique identifiers for various purposes.

Features:

-Generate UUIDs.

-Generate random numeric IDs.

-Generate random alphanumeric strings.

-Generate random hexadecimal strings.

Installation:

To set up the project locally, follow these steps:

Clone the Repository

bash
Copy code
git clone https://github.com/your-username/flask-id-generator.git
Navigate to the Project Directory

bash
Copy code
cd flask-id-generator
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Usage
Run the application using the following command:

bash
Copy code
python app.py
After starting the server, it will be accessible at http://localhost:5000.

API Endpoints

Generate ID:

Endpoint:

/generate-id
Method: GET
Parameters:
type: Type of ID to generate (uuid, numeric, string, wep). Default is uuid.
count: Number of IDs to generate. Default is 1, maximum is 1000.
Example request to generate 5 alphanumeric strings:

bash

Copy code
http://localhost:5000/generate-id?type=string&count=5

Contributing

If you wish to contribute to this project, feel free to fork the repository and submit pull requests. You can also open issues for bugs or feature suggestions.

License

This project is licensed under the MIT License - see the LICENSE file for details.