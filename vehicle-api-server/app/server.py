from flask import Flask, jsonify, request
from app.db import get_db, init_db, close_db
import sqlite3
from marshmallow import Schema, fields, ValidationError
import re
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from flask_cors import CORS


# Setup Logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    handlers=[
        logging.StreamHandler(), 
        logging.FileHandler("app.log"),  
    ]
)

# Create a logger instance
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) 
limiter = Limiter(get_remote_address, app=app)

@app.before_request
def before_request():
    init_db()
    logger.info("Request received for vehicle data")

@app.teardown_appcontext
def teardown_appcontext(exception):
    close_db(exception)
    if exception:
        logger.error(f"An error occurred: {exception}")
    else:
        logger.info("Request processed successfully")

@app.route('/vehicle', methods=['GET'])
@limiter.limit("100/hour")  
def get_all_vehicles():
    logger.debug("Fetching all vehicles")
    db = get_db()

    # # Default pagination parameters
    # page = int(request.args.get('page', 1))
    # page_size = int(request.args.get('page_size', 10))
    # offset = (page - 1) * page_size

    # cursor = db.execute(
    #     "SELECT * FROM vehicles LIMIT ? OFFSET ?", (page_size, offset)
    # )

    cursor = db.execute(
        "SELECT * FROM vehicles"
    )
    vehicles = [dict(row) for row in cursor.fetchall()]
    logger.info(f"Found {len(vehicles)} vehicles")

    return jsonify(vehicles), 200


@app.route('/vehicle', methods=['POST'])
@limiter.limit("1000/minute") 
def add_vehicle():
    logger.debug("Adding a new vehicle")
    if not request.is_json:
        logger.error("Request must be JSON")
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    required_fields = ["vin", "manufacturer_name", "description", "horse_power",
                       "model_name", "model_year", "purchase_price", "fuel_type"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        logger.warning(f"Missing fields: {missing_fields}")
        return jsonify({"error": "Missing fields", "missing": missing_fields}), 422

    # Validate VIN 
    if len(data.get("vin", "")) != 17:
        logger.error(f"Invalid VIN length for {data.get('vin')}")
        return jsonify({"error": "VIN must be exactly 17 characters long"}), 400

    db = get_db()
    try:
        db.execute(''' 
            INSERT INTO vehicles (vin, manufacturer_name, description, horse_power, model_name, model_year, purchase_price, fuel_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data["vin"], data["manufacturer_name"], data["description"], data["horse_power"],
              data["model_name"], data["model_year"], data["purchase_price"], data["fuel_type"]))
        logger.info(f"Vehicle {data['vin']} added successfully")
        db.commit()
    except sqlite3.IntegrityError:
        logger.error(f"Vehicle with VIN {data['vin']} already exists")
        return jsonify({"error": "Vehicle with this VIN already exists"}), 422

    # Returning the created vehicle details including the unique VIN
    return jsonify({
        "vin": data["vin"],
        "manufacturer_name": data["manufacturer_name"],
        "description": data["description"],
        "horse_power": data["horse_power"],
        "model_name": data["model_name"],
        "model_year": data["model_year"],
        "purchase_price": data["purchase_price"],
        "fuel_type": data["fuel_type"]
    }), 201


@app.route('/vehicle/<vin>', methods=['GET'])
@limiter.limit("5/minute")  
def get_vehicle(vin):
    logger.debug(f"Fetching vehicle with VIN: {vin}")
    # Validate VIN format (17 alphanumeric characters excluding I, O, Q)
    if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin):
        logger.error(f"Invalid VIN format: {vin}")
        return jsonify({"error": "Invalid VIN format"}), 400  # Return 400 for invalid VIN format

    db = get_db()
    cursor = db.execute("SELECT * FROM vehicles WHERE vin = ?", (vin,))
    vehicle = cursor.fetchone()

    if not vehicle:
        logger.error(f"Vehicle with VIN {vin} not found")
        return jsonify({"error": "Vehicle not found"}), 404  # Return 404 if the vehicle is not found

    return jsonify(dict(vehicle)), 200  # Return the vehicle if found

@app.route('/vehicle/<vin>', methods=['PUT'])
@limiter.limit("5/minute") 
def update_vehicle(vin):
    logger.debug(f"Received PUT request to update vehicle with VIN: {vin}")
    if not request.is_json:
        logger.error("Request must be JSON")
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    required_fields = ["manufacturer_name", "description", "horse_power",
                       "model_name", "model_year", "purchase_price", "fuel_type"]

    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logger.warning(f"Missing fields: {missing_fields}")
        return jsonify({"error": "Missing fields", "missing": missing_fields}), 422

    db = get_db()
    
    # Check if the vehicle exists
    cursor = db.execute("SELECT * FROM vehicles WHERE vin = ?", (vin,))
    vehicle = cursor.fetchone()

    if not vehicle:
        logger.error(f"Vehicle with VIN {vin} not found")
        return jsonify({"error": "Vehicle not found"}), 404  # Return 404 if the vehicle doesn't exist

    # Update the vehicle in the database
    db.execute('''
        UPDATE vehicles
        SET manufacturer_name = ?, description = ?, horse_power = ?, 
            model_name = ?, model_year = ?, purchase_price = ?, fuel_type = ?
        WHERE vin = ?
    ''', (data["manufacturer_name"], data["description"], data["horse_power"],
          data["model_name"], data["model_year"], data["purchase_price"], data["fuel_type"], vin))
    db.commit()

    logger.info(f"Vehicle with VIN {vin} updated successfully")

    # Return the updated vehicle
    return jsonify({
        "vin": vin,
        "manufacturer_name": data["manufacturer_name"],
        "description": data["description"],
        "horse_power": data["horse_power"],
        "model_name": data["model_name"],
        "model_year": data["model_year"],
        "purchase_price": data["purchase_price"],
        "fuel_type": data["fuel_type"]
    }), 200


@app.route('/vehicle/<vin>', methods=['DELETE'])
@limiter.limit("5/minute") 
def delete_vehicle(vin):
    logger.debug(f"Deleting vehicle with VIN: {vin}")
    # Validate VIN format (17 characters long, alphanumeric)
    if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin):
        logger.error(f"Invalid VIN format: {vin}")
        return jsonify({"error": "Invalid VIN format"}), 400  # Return 400 Bad Request for invalid VIN format

    db = get_db()
    
    # Check if the vehicle exists in the database
    cursor = db.execute("SELECT * FROM vehicles WHERE vin = ?", (vin,))
    if not cursor.fetchone():
        logger.error(f"Vehicle with VIN {vin} not found")
        return jsonify({"error": "Vehicle not found"}), 404  # Return 404 if vehicle is not found

    # Delete the vehicle
    db.execute("DELETE FROM vehicles WHERE vin = ?", (vin,))
    db.commit()

    logger.info(f"Vehicle with VIN {vin} deleted successfully")
    return '', 204  # Return 204 No Content when deletion is successful


if __name__ == '__main__':
    app.run(debug=True)
