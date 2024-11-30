from flask import Flask, jsonify, request, g
from app.db import get_db, init_db
import sqlite3
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

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) 
limiter = Limiter(get_remote_address, app=app)

REQUIRED_FIELDS = ["manufacturer_name", "description", "horse_power",
                   "model_name", "model_year", "purchase_price", "fuel_type"]

with app.app_context():
    init_db()
    logger.info("Database initialized.")

@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/vehicle', methods=['GET'])
@limiter.limit("100/hour")  
def get_all_vehicles():
    logger.debug("Fetching all vehicles")
    try:
        db = get_db()
        cursor = db.execute("SELECT * FROM vehicles")
        vehicles = [dict(row) for row in cursor.fetchall()]
        return jsonify(vehicles), 200
    except sqlite3.Error as e:
        logger.error('Database error')
        return jsonify({"error": "Internal server error. Please try again later."}), 500
    except Exception as e:
        logger.error('unexpected server error')
        return jsonify({"error": "Internal server error. Please try again later."}), 500

@app.route('/vehicle', methods=['POST'])
@limiter.limit("1000/minute") 
def add_vehicle():
    logger.debug('Sending post request')
    try:
        data = request.get_json()
    except:
        logger.error('Error POSTing a vehicle because data sent is not json')
        return jsonify({'error' : 'data sent is not json'}), 400
    
    # valdiate vin
    if not validate_vin(data.get('vin')):
        logger.error('Invalid VIN format provided')
        return jsonify({'error': 'Invalid VIN format'}), 422
    
    # make sure there are no missing fields
    missing_fields = find_missing_fields(data, REQUIRED_FIELDS)
    if missing_fields:
        logger.error(f'Missing required fields: {missing_fields}')
        return jsonify({'error': f'Missing fields: {missing_fields}'}), 422
    
    # Validate field types for provided fields
    field_errors = validate_field_types(data)
    if field_errors:
        logger.error(f'Field validation errors: {field_errors}')
        return jsonify({'error': field_errors}), 422
    
    try:
        db = get_db()

        # Check if the VIN already exists in the database
        cursor = db.execute('SELECT vin FROM vehicles WHERE vin = ?', (data['vin'],))
        existing_vehicle = cursor.fetchone()

        if existing_vehicle:
            logger.error(f'VIN already exists: {data["vin"]}')
            return jsonify({'error': f'Vehicle with VIN {data["vin"]} already exists'}), 409

        # Insert new vehicle
        db.execute(''' 
            INSERT INTO vehicles (vin, manufacturer_name, description, horse_power, 
                                  model_name, model_year, purchase_price, fuel_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['vin'], data['manufacturer_name'], data['description'], 
              data['horse_power'], data['model_name'], data['model_year'], 
              data['purchase_price'], data['fuel_type']))
        db.commit()

        logger.info(f'Successfully added new vehicle with VIN: {data["vin"]}')
        return jsonify(data), 201
    
    except sqlite3.Error as e:
        logger.error('Database error when trying to POST a vehicle')
        return jsonify({'error':'database error'}), 500

    except Exception as e:
        logger.error('Server error when trying to POST a vehicle')
        return jsonify({'error' : 'server error'}), 500


@app.route('/vehicle/<vin>', methods=['GET'])
@limiter.limit("5/minute")  
def get_vehicle(vin):
    logger.debug(f'Fetching a vehicle with VIN: {vin}')

    # Validate VIN
    if not validate_vin(vin):
        logger.error('Invalid VIN format ')
        return jsonify({'error': 'VIN format is not valid'}), 400
    
    try:
        db = get_db()
        cursor = db.execute('SELECT * FROM vehicles WHERE vin = ? LIMIT 1', (vin,))
        row = cursor.fetchone()
        if not row:
            logger.error(f'VIN not found: {vin}')
            return jsonify({'error': 'Vehicle not found'}), 404
        data = dict(row)
        logger.info(f'Successfully fetched vehicle with VIN: {vin}')
        return jsonify(data), 200
    
    except sqlite3.Error as e:
        logger.error(f'Database error when fetching vehicle with VIN {vin}: {e}')
        return jsonify({'error': 'Database error'}), 500

    except Exception as e:
        logger.error(f'Server error when fetching vehicle with VIN {vin}: {e}')
        return jsonify({'error': 'Server error'}), 500
    

@app.route('/vehicle/<vin>', methods=['PUT'])
@limiter.limit("5/minute") 
def update_vehicle(vin):
    logger.debug(f'Received PUT request for vehicle with VIN: {vin}')

    # Validate VIN
    if not validate_vin(vin):
        logger.error('Invalid VIN format in URL ')
        return jsonify({'error': 'Invalid VIN format in URL'}), 400
    
    try:
        data = request.get_json()
    except Exception as e:
        logger.error(f'Error parsing JSON for PUT request: {e}')
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    # make sure there are no missing fields
    missing_fields = find_missing_fields(data, REQUIRED_FIELDS)
    if missing_fields:
        logger.error(f'Missing required fields: {missing_fields}')
        return jsonify({'error': f'Missing fields: {missing_fields}'}), 422
    
    # Validate field types for provided fields
    field_errors = validate_field_types(data)
    if field_errors:
        logger.error(f'Field validation errors: {field_errors}')
        return jsonify({'error': field_errors}), 422
    
    # Ensure VIN in the request body matches VIN in the URL
    if data['vin'] != vin:
        logger.error('VIN in request body does not match VIN in URL')
        return jsonify({'error': 'VIN in request body must match VIN in URL'}), 422
    
    try:
        db = get_db()
        # Check if vehicle exists 
        cursor = db.execute('SELECT * FROM vehicles WHERE vin = ? LIMIT 1', (vin,))
        if cursor.fetchone() is None:
            logger.error(f'No vehicle found with VIN: {vin}')
            return jsonify({'error': 'Vehicle not found'}), 404
        
        db.execute('''
                    update vehicles
                    set manufacturer_name = ? , description = ?, horse_power = ?,
                    model_name = ? , model_year = ?, purchase_price = ?, fuel_type = ?
                    ''', (data['manufacturer_name'], data['description'], data['horse_power'],
                        data['model_name'], data['model_year'], data['purchase_price'] , data['fuel_type']))
        db.commit()

        logger.info(f'Successfully updated vehicle with VIN: {vin}')
        return jsonify(data), 200

    except sqlite3.Error as e:
        logger.error(f'Database error while updating vehicle with VIN {vin}: {e}')
        return jsonify({'error': 'Database error'}), 500

    except Exception as e:
        logger.error(f'Server error while updating vehicle with VIN {vin}: {e}')
        return jsonify({'error': 'Server error'}), 500


@app.route('/vehicle/<vin>', methods=['DELETE'])
@limiter.limit("5/minute") 
def delete_vehicle(vin):
    logger.debug(f'Received DELETE request for vehicle with VIN: {vin}')

    # Validate VIN
    if not validate_vin(vin):
        logger.error('Invalid VIN format provided in URL')
        return jsonify({'error': 'Invalid VIN format in URL'}), 400
    
    try:
        db = get_db()

        # Try to delete the vehicle
        cursor = db.execute('DELETE FROM vehicles WHERE vin = ?', (vin,))
        db.commit()

        if cursor.rowcount == 0:  # if no rows were deleted
            logger.error(f'No vehicle found with VIN: {vin}')
            return jsonify({'error': 'No vehicle found with this VIN'}), 404

        logger.info(f'Successfully deleted vehicle with VIN: {vin}')
        return '', 204
    
    except sqlite3.Error as e:
        logger.error(f'Database error while deleting vehicle with VIN {vin}: {e}')
        return jsonify({'error': 'Database error'}), 500

    except Exception as e:
        logger.error(f'Server error while deleting vehicle with VIN {vin}: {e}')
        return jsonify({'error': 'Server error'}), 500


def validate_vin(vin):
    if not vin or len(vin) != 17:
        return False
    if not vin.isalnum():
        return False
    return True


def find_missing_fields(data, required_fields):
    missing_fields = [field for field in required_fields if field not in data]
    return missing_fields


def validate_field_types(data):
    """
    Validate the types of fields.
    ONLY checks fields that are present in the data. 
    This allows for flexiblity when we validate a POST and PUT request when we want to validate all fields,
    and also for validating a PATCH request that only sends some fields it wants to update
    
    Expected types:
    - manufacturer_name: string
    - description: string
    - horse_power: integer
    - model_name: string
    - model_year: integer
    - purchase_price: decimal (float or int)
    - fuel_type: string
    """
    field_types = {
        "manufacturer_name": str,
        "description": str,
        "horse_power": int,
        "model_name": str,
        "model_year": int,
        "purchase_price": (float, int),
        "fuel_type": str
    }
    
    errors = []

    for field, expected_type in field_types.items():
        if field in data:
            if not isinstance(data[field], expected_type):
                errors.append(f"{field} must be of type {expected_type.__name__}")

    return errors


if __name__ == '__main__':
    app.run(debug=True)
