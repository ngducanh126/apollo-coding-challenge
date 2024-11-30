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
        return jsonify({"error": "Unexpected database error"}),500
    except Exception as e:
        logger.error('unexpected server error')
        return jsonify({'error':'unexpected server error'}), 500

@app.route('/vehicle', methods=['POST'])
@limiter.limit("1000/minute") 
def add_vehicle():
    logger.debug('Sending post request')
    db = get_db()
    try:
        data = request.get_json()
    except:
        logger.error('Error POSTing a vehicle because data sent is not json')
        return jsonify({'error' : 'data sent is not json'}), 400
    
    # valdiate vin
    if len(data['vin']) != 17:
        logger.error('Error POSTing vehicle because of invalid vin')
        return jsonify({'error' : 'vin not valid'}), 400
    
    #required fields
    required_fields = ["manufacturer_name", "description", "horse_power",
                       "model_name", "model_year", "purchase_price", "fuel_type"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logger.error('Missing fields when POSTing a vehicle')
        return jsonify({'error ' :'missing fields'}), 422
    
    try:
        db.execute(''' 
                   insert into vehicles (vin, manufacturer_name, description, horse_power, model_name, model_year, purchase_price, fuel_type)
                    values (?,?,?,?,?,?,?,?)
                   
                   ''', (data['vin'],data['manufacturer_name'],data['description'],data['horse_power'], data['model_name'], data['model_year'], data['purchase_price'], data['fuel_type']))
        db.commit()
        logger.info('Successfully POSTed vehicle')
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
    logger.debug('Fetching a vehicle with VIN ')
    if len(vin) != 17:
        logger.error('Invalid vin')
        return jsonify({'error' : 'Vin is not valid'}) , 400
    db = get_db()
    try:
        cursor = db.execute('select * from vehicles where vin = ? limit 1' , (vin,))
        data = dict(cursor.fetchone())
        if not data:
            logger.error('VIN not found')
            return jsonify({'error' :'not found'}), 404
        logger.info("Successfuly fetched vehicle with vin ")
        return jsonify(data), 200
    except sqlite3.Error as e:
        logger.error('Database error when fetching vehicle with vin ')
        return jsonify({'error' : 'database error'}), 500
    except Exception as e:
        logger.error('Server error when fetching vehicle with vin ')
        return jsonify({'error' : 'server error'}), 500
    


@app.route('/vehicle/<vin>', methods=['PUT'])
@limiter.limit("5/minute") 
def update_vehicle(vin):
    logger.debug('Sending a PUT request')
    if len(vin) != 17:
        return jsonify({'error' : 'VIN not valid'}), 400
    try:
        data = request.get_json()
    except:
        return jsonify({'error' : 'Data sent is not json. Error'}), 400
    
    #required fields
    required_fields = ["manufacturer_name", "description", "horse_power",
                       "model_name", "model_year", "purchase_price", "fuel_type"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logger.error('Missing fields when PUTing a vehicle')
        return jsonify({'error' :'missing fields'}), 422
    
    try:
        db = get_db()
        cursor = db.execute('select * from vehicles where vin = ? limit 1' , (vin,))
        vehicle_fetched = cursor.fetchone()
        if not vehicle_fetched:
            return jsonify({'error' : 'VIN not found'}), 404
        db.execute('''
                            update vehicles
                            set manufacturer_name = ? , description = ?, horse_power = ?,
                            model_name = ? , model_year = ?, purchase_price = ?, fuel_type = ?
                            ''', (data['manufacturer_name'], data['description'], data['horse_power'],
                                  data['model_name'], data['model_year'], data['purchase_price'] , data['fuel_type']))
        db.commit()
        return jsonify(data), 200

    except sqlite3.Error as e:
        return jsonify({'error' : 'database error'}), 500
    except Exception as e:
        return jsonify({'error' : 'server error'}), 500


@app.route('/vehicle/<vin>', methods=['DELETE'])
@limiter.limit("5/minute") 
def delete_vehicle(vin):
    if len(vin) != 17:
        return jsonify({'error' : 'invalid vin'}), 400
    try:
        db = get_db()
        cursor = db.execute('select * from vehicles where vin = ?' , (vin,))
        vehicle_fetched = cursor.fetchone()
        if not vehicle_fetched:
            return jsonify({'error' : 'no vehicle found with this vin'}), 404
        db.execute('delete from vehicles where vin = ?', (vin,))
        db.commit()
        return '', 204
    except sqlite3.Error as e:
        return jsonify({'error' : 'database error'}), 500
    except Exception as e:
        return jsonify({'error' : 'server error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
