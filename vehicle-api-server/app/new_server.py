from flask import Flask, jsonify, request
from .new_db import get_db, init_vehicles_table, init_manufacturers_table
import sqlite3
import re
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from flask_cors import CORS


app = Flask(__name__)
CORS(app) 


@app.before_request
def before_request():
    init_manufacturers_table()
    init_vehicles_table()


@app.teardown_appcontext
def teardown_appcontext(exception):
    pass

@app.route('/vehicle', methods=['GET'])
def get_vehicle():
    try:
        db = get_db()
        data = db.execute('select * from vehicles ').fetchall()
        return jsonify([dict(row) for row in data]) , 200
    except:
        return jsonify({'error' : 'server error'}) ,500
    
@app.route('/vehicle/manufacturer', methods=['GET'])
def get_vehicle_and_manufacturer():
    try:
        db = get_db()
        data = db.execute('''select v.description, v.fuel_type, m.name from vehicles v 
                            left join manufacturers m
                            on v.manufacturer_name = m.name
                          ''').fetchall()
        return jsonify([dict(row) for row in data]) , 200
    except:
        return jsonify({'error' : 'server error'}) ,500



@app.route('/vehicle' , methods=['POST'])
def post_vehicle():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Malformed JSON body"}), 400
    data = request.get_json()
    try:
        db = get_db()
        db.execute('''
                   insert into vehicles values
                    (?,?,?,?,?,?,?,?)
                   ''' , (data['vin'], data['manufacturer_name'] , data['description'], data['horse_power'],
                        data['model_name'] , data['model_year'] , data['purchase_price'] , data['fuel_type']))
        db.commit()
        return jsonify(data), 201
    except sqlite3.Error as error:
        return jsonify({'error' : 'db error'}), 500
    except Exception as error:
        return jsonify({'error' : 'server unexpected error'}), 500

@app.route('/manufacturer', methods=['GET'])
def get_manufacturer():
    try:
        db = get_db()
        data = db.execute('select * from manufacturers ').fetchall()
        return jsonify([dict(row) for row in data]) , 200
    except:
        return jsonify({'error' : 'server error'}) ,500
    

@app.route('/manufacturer' , methods=['POST'])
def post_manufacturer():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Malformed JSON body"}), 400

    try:
        db = get_db()
        db.execute('insert into manufacturers values (?,?)' , (data['name'], data['headquarters']))
        db.commit()
        return jsonify(data), 201
    except sqlite3.Error as error:
        return jsonify({'error' : 'db error'}), 500
    except Exception as error:
        return jsonify({'error' : 'server unexpected error'}), 500