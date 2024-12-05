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
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
limiter = Limiter(get_remote_address, app=app)

REQUIRED_FIELDS = ["vin","manufacturer_name", "description", "horse_power",
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

    # Reject GET requests with any body data
    if request.content_length and request.content_length > 0:
        logger.error("GET request must not include a request body")
        return jsonify({'error': 'Request body is not allowed in GET request'}), 422

    # per_page = int(request.args.get('per_page', 3))
    # page = int(request.args.get('page', 1))
    # offset = (page-1) * per_page

    try:
        db = get_db()
        cursor = db.execute("SELECT * FROM vehicles ",)
        vehicles = [dict(row) for row in cursor.fetchall()]
        return jsonify(vehicles), 200
    except sqlite3.Error as e:
        logger.error('Database error')
        return jsonify({"error": "Internal server error. Please try again later."}), 500
    except Exception as e:
        logger.error('Unexpected server error')
        return jsonify({"error": "Internal server error. Please try again later."}), 500


@app.route('/vehicle', methods=['POST'])
@limiter.limit("100/minute")
def add_vehicle():
    logger.debug('Received POST request')

    # Ensure Content-Type is application/json
    if not request.is_json:
        logger.error('Content-Type must be application/json')
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    try:
        data = request.get_json()
    except:
        logger.error('Error parsing JSON data')
        return jsonify({'error': 'Invalid JSON format'}), 400

    # Validate VIN
    if not validate_vin(data.get('vin')):
        logger.error('Invalid VIN format provided')
        return jsonify({'error': 'Invalid VIN format'}), 422

    # Ensure required fields are present
    missing_fields = find_missing_fields(data, REQUIRED_FIELDS)
    if missing_fields:
        logger.error(f'Missing required fields: {missing_fields}')
        return jsonify({'error': f'Missing fields: {missing_fields}'}), 422

    # Check for unexpected fields
    unexpected_fields = [field for field in data if field not in REQUIRED_FIELDS]
    if unexpected_fields:
        logger.error(f'Unexpected fields provided: {unexpected_fields}')
        return jsonify({'error': f'Unexpected fields: {unexpected_fields}'}), 422

    # Validate field types
    field_errors = get_field_errors(data)
    if field_errors:
        logger.error(f'Field validation errors: {field_errors}')
        return jsonify({'error': f'Error validate fields: {field_errors}'}), 422

    try:
        db = get_db()

        # Check if the VIN already exists
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

        logger.info(f'Successfully added vehicle with VIN: {data["vin"]}')
        return jsonify(data), 201

    except sqlite3.Error as e:
        logger.error(f'Database error: {e}')
        return jsonify({'error': 'Database error'}), 500

    except Exception as e:
        logger.error(f'Server error: {e}')
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/vehicle/<vin>', methods=['GET'])
@limiter.limit("100/minute")  
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
        return jsonify({'error': 'Internal server error'}), 500
    

@app.route('/vehicle/<vin>', methods=['PUT'])
@limiter.limit("100/minute")
def update_vehicle(vin):
    logger.debug(f'Received PUT request for VIN: {vin}')

    # Ensure Content-Type is application/json
    if not request.is_json:
        logger.error('Content-Type must be application/json')
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    try:
        data = request.get_json()
    except Exception as e:
        logger.error(f'Error parsing JSON data: {e}')
        return jsonify({'error': 'Invalid JSON format'}), 400
    
    # Validate VIN
    if not validate_vin(data.get('vin')):
        logger.error('Invalid VIN format provided')
        return jsonify({'error': 'Invalid VIN format'}), 422
    
    # Ensure VIN in the URL matches VIN in the request body (case-insensitive)
    if data.get('vin').lower() != vin.lower():
        logger.error('VIN in request body does not match VIN in URL (case-insensitive)')
        return jsonify({'error': 'VIN in request body must match VIN in URL (case-insensitive)'}), 422

    # Validate required fields and types
    missing_fields = find_missing_fields(data, REQUIRED_FIELDS)
    if missing_fields:
        logger.error(f'Missing required fields: {missing_fields}')
        return jsonify({'error': f'Missing fields: {missing_fields}'}), 422

    # Check for unexpected fields
    unexpected_fields = [field for field in data if field not in REQUIRED_FIELDS]
    if unexpected_fields:
        logger.error(f'Unexpected fields provided: {unexpected_fields}')
        return jsonify({'error': f'Unexpected fields: {unexpected_fields}'}), 422

    field_errors = get_field_errors(data)
    if field_errors:
        logger.error(f'Field validation errors: {field_errors}')
        return jsonify({'error': field_errors}), 422

    try:
        db = get_db()

        # Check if vehicle exists
        cursor = db.execute('SELECT * FROM vehicles WHERE vin = ?', (vin,))
        if not cursor.fetchone():
            logger.error(f'No vehicle found with VIN: {vin}')
            return jsonify({'error': 'Vehicle not found'}), 404

        # Update vehicle
        db.execute('''
            UPDATE vehicles
            SET manufacturer_name = ?, description = ?, horse_power = ?, 
                model_name = ?, model_year = ?, purchase_price = ?, fuel_type = ?
            WHERE vin = ?
        ''', (data['manufacturer_name'], data['description'], data['horse_power'],
              data['model_name'], data['model_year'], data['purchase_price'], 
              data['fuel_type'], vin))
        db.commit()

        logger.info(f'Successfully updated vehicle with VIN: {vin}')
        return jsonify(data), 200

    except sqlite3.Error as e:
        logger.error(f'Database error: {e}')
        return jsonify({'error': 'Database error'}), 500

    except Exception as e:
        logger.error(f'Server error: {e}')
        return jsonify({'error': 'Server error'}), 500

@app.route('/vehicle/<vin>', methods=['DELETE'])
@limiter.limit("10/minute") 
def delete_vehicle(vin):
    logger.debug(f'Received DELETE request for vehicle with VIN: {vin}')

    # Validate VIN
    if not validate_vin(vin):
        logger.error('Invalid VIN format provided in URL')
        return jsonify({'error': 'Invalid VIN format in URL'}), 400

    # Reject DELETE requests with any body data
    if request.data and len(request.data) > 0:
        logger.error('DELETE request must not include a request body')
        return jsonify({'error': 'Request body is not allowed in DELETE request'}), 422

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
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/vehicle/<vin>' , methods=['PATCH'])
def patch_vehicle(vin):
    #validate vin
    if not validate_vin(vin):
        return jsonify({'error':{'Error validating vin '}}),400

    #data sent is json
    if not request.is_json:
        logger.error('Content-Type must be application/json')
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    try:
        data = request.get_json()
    except Exception as e:
        logger.error(f'Error parsing JSON data: {e}')
        return jsonify({'error': 'Invalid JSON format'}), 400
    
    # if no fields are provided for update
    if not data:
        return jsonify({'error': 'No fields to update'}), 400
    
    #vin in url matches vin sent in json
    if not (data['vin'].lower() == vin.lower()):
        return jsonify({'error':'vin does not matches vin in url'}),400

    #validate fields
    error_fields = get_field_errors(data)
    if error_fields:
        return jsonify({'error':'Error field'}), 422
    
    #CONSTRUCT THE SET CLAUSE AND PARAMS
    set_clauses = []
    params = []
    for field,value in data.items():
        if field != 'vin':
            set_clauses.append(f'{field} = ?')
            params.append(value)
    set_clauses = ','.join(set_clauses)   #convert to string and get rid of trailing comma
    params.append(data['vin'])

    try:
        query = f'update vehicles set {set_clauses} where vin = ?'
        db = get_db()
        cursor = db.execute(query, params)
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'VIN not found'}), 404
        return jsonify({'message': 'Vehicle updated successfully'}), 200

    except sqlite3.Error as err:
        return jsonify({'error':'Database error'}),500
    except Exception as err:
        return jsonify({'error':'Internal server error'}),500
    

def validate_vin(vin):
    if not vin or len(vin) != 17:
        return False
    if not vin.isalnum():
        return False
    return True


def find_missing_fields(data, required_fields):
    missing_fields = [field for field in required_fields if field not in data]
    return missing_fields


def get_field_errors(data):
    """
    Validate the fields (ONLY checks fields that are present in the data)
    Checks for correct type and checks to ensure all fields are non-empty and numeric fields are greater than or equal to 0 
    This allows for flexibility when we validate a POST and PUT request when we want to validate all fields,
    and also for validating a PATCH request that only sends some fields it wants to update.
    """
    field_types = {
        "manufacturer_name": str,
        "description": str,
        "horse_power": int,
        "model_name": str,
        "model_year": int,
        "purchase_price": float,
        "fuel_type": str
    }
    
    errors = []

    for field, expected_type in field_types.items():
        if field in data:
            value = data[field]
            try:
                # Convert to the expected type to validate
                if expected_type == int:
                    value = int(value)
                    if value < 0:
                        errors.append(f"{field} must be greater than or equal to 0")
                elif expected_type == float:
                    value = float(value)
                    if value < 0:
                        errors.append(f"{field} must be greater than or equal to 0")
                elif expected_type == str:
                    if not isinstance(value, str):
                        raise ValueError(f"{field} must be a string")
                    if not value.strip():
                        errors.append(f"{field} must be a non-empty string")
                else:
                    raise ValueError(f"Unsupported type: {expected_type}")
            except ValueError:
                errors.append(f"{field} must be convertible to {expected_type.__name__}")
    
    return errors


if __name__ == '__main__':
    app.run(debug=True)
