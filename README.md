API Server
Clone the Repository
First, clone the repository to your local machine: git clone <repository-url> Replace <repository-url> with the URL of your project repository.

REST API Setup
Navigate to the vehicle-api-server/ directory: cd vehicle-api-server/

Create a virtual environment: python -m venv venv

Activate the virtual environment:

Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate
Install the required dependencies: pip install -r requirements.txt

Start the REST API server: In the vehicle-api-server/ directory, run: python restAPI_run.py

The REST API server will be up and running at port 5000. You can access it in your browser at: http://127.0.0.1:5000/vehicle

GraphQL API Setup
Ensure you are in the vehicle-api-server/ directory: cd vehicle-api-server/

Activate the virtual environment you created during the REST API setup:

Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate
Start the GraphQL API server: In the vehicle-api-server/ directory, run: python graphql_run.py
The GraphQL server will be up and running at port 5001. You can access and test queries at: http://127.0.0.1:5001/graphql
