from app.server import app
from app.db import init_db, get_db
import json
import logging
from unittest.mock import patch
import sqlite3

class TestVehicleAPI:
    """
    Test suite for the Vehicle API.
    """

    def setup_method(self):
        """
        Set up the test client and in-memory database before each test.
        """
        app.config['TESTING'] = True
        app.config['DEBUG'] = True  
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB

        # logging
        app.logger.setLevel(logging.DEBUG) 
        for handler in app.logger.handlers:
            handler.setLevel(logging.DEBUG)

        self.client = app.test_client()

        with app.app_context():
            init_db()

        self.example_vehicle = {
            "vin": "1HGCM82633A123459",
            "manufacturer_name": "Honda",
            "description": "Reliable sedan",
            "horse_power": 150,
            "model_name": "Accord",
            "model_year": 2020,
            "purchase_price": 25000.50,
            "fuel_type": "Gasoline"
        }

    def teardown_method(self):
        """
        Clean up the database after each test.
        """
        with app.app_context():
            db = get_db()
            db.execute("DELETE FROM vehicles")
            db.commit()

    def test_add_vehicle_success(self):
        """
        Test POST /vehicle with valid data.
        """
        response = self.client.post(
            '/vehicle',
            data=json.dumps(self.example_vehicle),
            content_type='application/json'
        )
        assert response.status_code == 201
        
        # Check if the returned vehicle data matches the example vehicle
        vehicle_data = response.json
        assert vehicle_data["vin"] == self.example_vehicle["vin"]
        assert vehicle_data["manufacturer_name"] == self.example_vehicle["manufacturer_name"]
        assert vehicle_data["description"] == self.example_vehicle["description"]
        assert vehicle_data["horse_power"] == self.example_vehicle["horse_power"]
        assert vehicle_data["model_name"] == self.example_vehicle["model_name"]
        assert vehicle_data["model_year"] == self.example_vehicle["model_year"]
        assert vehicle_data["purchase_price"] == self.example_vehicle["purchase_price"]
        assert vehicle_data["fuel_type"] == self.example_vehicle["fuel_type"]


    def test_get_vehicle_by_vin_not_found(self):
        response = self.client.get('/vehicle/00000000000000000')
        assert response.status_code == 404
        assert response.json['error'] == "Vehicle not found"

    def test_get_vehicle_by_vin_success(self):
        # add the vehicle to the database
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')

        # fetch the vehicle by VIN
        response = self.client.get(f'/vehicle/{self.example_vehicle["vin"]}')
        assert response.status_code == 200  
        assert response.json["vin"] == self.example_vehicle["vin"]
        assert response.json["manufacturer_name"] == self.example_vehicle["manufacturer_name"]  # Verify other fields

    def test_get_vehicle_by_invalid_vin(self):
        # VIN that does not conform to the correct format
        response = self.client.get('/vehicle/INVALID_VIN')
        assert response.status_code == 400 
        assert response.json['error'] == 'VIN format is not valid'

    def test_get_all_vehicles_mocked_empty_result(self):
        """
        Test GET /vehicle with a mocked empty database result.
        """
        with patch('app.db.get_db') as mock_get_db:
            mock_cursor = mock_get_db.return_value.cursor.return_value
            mock_cursor.fetchall.return_value = []
            mock_cursor.description = []

            response = self.client.get('/vehicle')
            assert response.status_code == 200
            assert response.json == []
 

    def test_get_all_vehicles_no_body(self):
        """
        Test GET /vehicle with no request body.
        """
        # Add a sample vehicle for context
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')

        response = self.client.get('/vehicle')
        assert response.status_code == 200  # OK
        # print('vehicle got back is ', response.json)
        assert response.json[0]["vin"] == "1HGCM82633A123457"


    def test_get_all_vehicles_with_body(self):
        """
        Test GET /vehicle with a request body included.
        """
        response = self.client.get(
            '/vehicle',
            data=json.dumps({"unexpected_field": "unexpected_value"}),
            content_type='application/json'
        )
        assert response.status_code == 422 
        assert "Request body is not allowed in GET request" in response.json.get("error", "")


    def test_get_all_vehicles_malformed_body(self):
        """
        Test GET /vehicle with a malformed JSON body.
        """
        response = self.client.get(
            '/vehicle',
            data="INVALID_JSON",
            content_type='application/json'
        )
        assert response.status_code == 422
        assert "Request body is not allowed in GET request" in response.json.get("error", "")

    def test_get_all_vehicles_empty_body(self):
        """
        Test GET /vehicle with an empty body.
        """
        response = self.client.get(
            '/vehicle',
            data="",
            content_type='application/json'
        )
        assert response.status_code == 200 


    def test_add_vehicle_missing_fields(self):
        invalid_vehicle = self.example_vehicle.copy()
        del invalid_vehicle["model_name"] 

        response = self.client.post(
            '/vehicle',
            data=json.dumps(invalid_vehicle),
            content_type='application/json'
        )
        assert response.status_code == 422 
        assert "model_name" in response.json["error"]  


    def test_add_vehicle_duplicate_vin(self):
        # Add the vehicle once
        self.client.post(
            '/vehicle',
            data=json.dumps(self.example_vehicle),
            content_type='application/json'
        )

        # adding the same vehicle again
        response = self.client.post(
            '/vehicle',
            data=json.dumps(self.example_vehicle),
            content_type='application/json'
        )
        assert response.status_code == 409 
        assert "Vehicle with VIN" in response.json.get("error", "")


    def test_add_vehicle_invalid_json(self):
        """
        Test POST /vehicle with invalid JSON in the request body.
        """
        response = self.client.post(
            '/vehicle',
            data="not-a-json-string",
            content_type='application/json'
        )
        assert response.status_code == 400  

    def test_post_vehicle_mocked_db_error(self):
        """
        mocked database error during vehicle insertion.
        """
        with patch('app.server.get_db') as mock_get_db:
            mock_conn = mock_get_db.return_value
            mock_conn.execute.side_effect = sqlite3.Error("Mocked database insertion error")

            vehicle_data = self.example_vehicle.copy()
            response = self.client.post(
                '/vehicle',
                data=json.dumps(vehicle_data),
                content_type='application/json'
            )
            assert response.status_code == 500
            assert "Database error" in response.json.get("error", "")

    def test_put_vehicle_without_json(self):
        """
        Test PUT without application/json Content-Type.
        """
        response = self.client.put(
            '/vehicle/1HGCM82633A123456',
            data="plain text",
            content_type='text/plain'
        )
        assert response.status_code == 400
        assert "Content-Type must be application/json" in response.json.get("error", "")

    def test_put_vehicle_mocked_db_error(self):
        """
        mocked database error during update.
        """
        with patch('app.server.get_db') as mock_get_db:
            mock_conn = mock_get_db.return_value
            mock_conn.execute.side_effect = sqlite3.Error("Mocked database update error")

            updated_data = self.example_vehicle.copy()
            updated_data["description"] = "Updated description"
            response = self.client.put(
                f'/vehicle/{self.example_vehicle["vin"]}',
                data=json.dumps(updated_data),
                content_type='application/json'
            )
            assert response.status_code == 500
            assert "Database error" in response.json.get("error", "")

    def test_add_vehicle_invalid_field_types(self):
        invalid_vehicle = self.example_vehicle.copy()
        invalid_vehicle["horse_power"] = "not-an-integer"

        response = self.client.post(
            '/vehicle',
            data=json.dumps(invalid_vehicle),
            content_type='application/json'
        )
        assert response.status_code == 422 
        assert "horse_power must be convertible to int" in response.json.get("error", "")


    def test_add_vehicle_missing_vin(self):
        """
        Test POS with VIN missing in the request body.
        """
        invalid_vehicle = self.example_vehicle.copy()
        del invalid_vehicle["vin"]

        response = self.client.post(
            '/vehicle',
            data=json.dumps(invalid_vehicle),
            content_type='application/json'
        )
        assert response.status_code == 422


    def test_add_vehicle_null_attributes(self):
        invalid_vehicle = {
            "vin": None, 
            "manufacturer_name": "Honda",
            "description": "Reliable sedan",
            "horse_power": 150,
            "model_name": "Accord",
            "model_year": 2020,
            "purchase_price": 25000.50,
            "fuel_type": "Gasoline"
        }

        response = self.client.post(
            '/vehicle',
            data=json.dumps(invalid_vehicle),
            content_type='application/json'
        )
        assert response.status_code == 422 


    def test_add_vehicle_extra_fields_new_json(self):
        new_vehicle_with_extra_field = {
            "vin": "1HGCM82633A123456",
            "manufacturer_name": "Ford",
            "description": "A reliable SUV",
            "horse_power": 240,
            "model_name": "Explorer",
            "model_year": 2022,
            "purchase_price": 35000.99,
            "fuel_type": "Gasoline",
            "extra_field": "Unexpected field"  # extra unexpected field
        }

        response = self.client.post(
            '/vehicle',
            data=json.dumps(new_vehicle_with_extra_field),
            content_type='application/json'
        )
        assert response.status_code == 422  


    def test_add_vehicle_edge_values(self):
        """
        edge case values.
        """
        edge_case_vehicle = {
            "vin": "1HGCM82633A123456", 
            "manufacturer_name": "EdgeManufacturer",
            "description": "EdgeDescription",
            "horse_power": 0,  
            "model_name": "EdgeModel",  
            "model_year": 1900,  
            "purchase_price": 0.0,  
            "fuel_type": "Diesel"
        }

        response = self.client.post(
            '/vehicle',
            data=json.dumps(edge_case_vehicle),
            content_type='application/json'
        )
        assert response.status_code == 201  

    def test_add_vehicle_empty_string_fields(self):
        """
        Test POST /vehicle with empty strings for string fields.
        """
        invalid_vehicle = {
            "vin": "1HGCM82633A123456",
            "manufacturer_name": "", 
            "description": "A valid description",
            "horse_power": 150,
            "model_name": "",
            "model_year": 2020,
            "purchase_price": 25000.50,
            "fuel_type": ""
        }

        response = self.client.post(
            '/vehicle',
            data=json.dumps(invalid_vehicle),
            content_type='application/json'
        )
        assert response.status_code == 422 
        assert "manufacturer_name must be a non-empty string" in response.json["error"]
        assert "model_name must be a non-empty string" in response.json["error"]
        assert "fuel_type must be a non-empty string" in response.json["error"]


    def test_add_vehicle_negative_numeric_fields(self):
        invalid_vehicle = {
            "vin": "1HGCM82633A123456",
            "manufacturer_name": "EdgeManufacturer",
            "description": "EdgeDescription",
            "horse_power": -10,  
            "model_name": "EdgeModel",
            "model_year": -1900,  
            "purchase_price": -1000.0, 
            "fuel_type": "Diesel"
        }

        response = self.client.post(
            '/vehicle',
            data=json.dumps(invalid_vehicle),
            content_type='application/json'
        )
        assert response.status_code == 422  
        assert "horse_power must be greater than or equal to 0" in response.json["error"]



    def test_post_vehicle_vin_case_insensitive(self):
        # Add a vehicle with an uppercase VIN
        vehicle_uppercase_vin = self.example_vehicle.copy()
        vehicle_uppercase_vin["vin"] = "1HGCM82633A123456"

        response = self.client.post(
            '/vehicle',
            data=json.dumps(vehicle_uppercase_vin),
            content_type='application/json'
        )
        assert response.status_code == 201 

        # add a vehicle with the same VIN in lowercase
        vehicle_lowercase_vin = self.example_vehicle.copy()
        vehicle_lowercase_vin["vin"] = "1hgcm82633a123456"

        response = self.client.post(
            '/vehicle',
            data=json.dumps(vehicle_lowercase_vin),
            content_type='application/json'
        )
        assert response.status_code == 409  
        assert f'VIN {vehicle_lowercase_vin["vin"]} already exists' in response.json.get("error", "")

    def test_update_vehicle_mismatched_vin(self):
        """
        Test PUT /vehicle/{vin} with mismatched VIN in URL and request body.
        """
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')

        # Change VIN in the request body
        updated_data = self.example_vehicle.copy()
        updated_data["vin"] = "1HGCM82633A123455"  # Mismatched VIN
        response = self.client.put(
            f'/vehicle/{self.example_vehicle["vin"]}', 
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        assert response.status_code == 422  
        assert "VIN in request body must match VIN in URL" in response.json.get("error", "")


    def test_put_vehicle_vin_case_insensitive(self):
        # Add a vehicle with an uppercase VIN
        vehicle_uppercase_vin = self.example_vehicle.copy()
        vehicle_uppercase_vin["vin"] = "1HGCM82633A123456"

        self.client.post(
            '/vehicle',
            data=json.dumps(vehicle_uppercase_vin),
            content_type='application/json'
        )

        # Update the vehicle using the lowercase version of the same VIN
        updated_data = vehicle_uppercase_vin.copy()
        updated_data["description"] = "Updated description"

        response = self.client.put(
            '/vehicle/1hgcm82633a123456', 
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        assert response.status_code == 200  
        assert response.json["description"] == "Updated description"

    def test_update_vehicle_success(self):
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')

        # Update the vehicle
        updated_data = self.example_vehicle.copy()
        updated_data["description"] = "Updated description"
        response = self.client.put(
            f'/vehicle/{self.example_vehicle["vin"]}',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        assert response.status_code == 200  
        assert response.json["description"] == "Updated description"  


    def test_update_vehicle_not_found(self):
        updated_data = {
            "vin": "1HGCM82633A123457",
            "manufacturer_name": "Honda",
            "description": "Reliable sedan",
            "horse_power": 150,
            "model_name": "Accord",
            "model_year": 2020,
            "purchase_price": 25000.50,
            "fuel_type": "Gasoline"
        }
        
        response = self.client.put(
            '/vehicle/1HGCM82633A123457',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        assert response.status_code == 404
        assert response.json.get('error') == 'Vehicle not found'
 

    def test_update_vehicle_invalid_data(self):
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')

        updated_data = self.example_vehicle.copy()
        updated_data.pop("description")
        
        response = self.client.put(
            f'/vehicle/{self.example_vehicle["vin"]}',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        assert response.status_code == 422
        assert 'Missing fields' in response.json.get('error')
 


    def test_update_vehicle_invalid_json(self):
        response = self.client.put(
            f'/vehicle/{self.example_vehicle["vin"]}',
            data="INVALID_JSON",
            content_type='application/json'
        )
        assert response.status_code == 400
        assert response.json.get('error') == 'Invalid JSON format'


    def test_put_vehicle_without_json(self):
        response = self.client.put(
            '/vehicle/1HGCM82633A123456',
            data="plain text instead of JSON",
            content_type='text/plain'
        )
        assert response.status_code == 400  
        assert "Content-Type must be application/json" in response.json.get("error", "")

    def test_update_vehicle_extra_fields(self):
        """
        Test PUT /vehicle/{vin} with extra fields in the request body.
        """
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')

        # Add extra fields to the request body
        updated_data = self.example_vehicle.copy()
        updated_data["extra_field"] = "Extra data"

        response = self.client.put(
            f'/vehicle/{self.example_vehicle["vin"]}',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        assert response.status_code == 422
        assert "Unexpected fields" in response.json.get("error", "")


    def test_update_vehicle_invalid_field_types(self):
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')

        # Use invalid field types
        updated_data = self.example_vehicle.copy()
        updated_data["horse_power"] = "not-an-integer"
        updated_data["purchase_price"] = "not-a-float"

        response = self.client.put(
            f'/vehicle/{self.example_vehicle["vin"]}',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        assert response.status_code == 422
        assert "horse_power must be convertible to int" in response.json.get("error", "")
        assert "purchase_price must be convertible to float" in response.json.get("error", "")
        
    def test_delete_vehicle_not_found(self):
        response = self.client.delete('/vehicle/11111111111111111')
        assert response.status_code == 404  

    def test_delete_vehicle_invalid_vin_format(self):
        response = self.client.delete('/vehicle/123') 
        assert response.status_code == 400  


    def test_delete_vehicle_success(self):
        # add the vehicle to the database
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')
        # delete the vehicle
        response = self.client.delete(f'/vehicle/{self.example_vehicle["vin"]}')
        assert response.status_code == 204  

    def test_delete_vehicle_with_body(self):
        """
        Test DELETE /vehicle/{vin} with a request body included.
        """
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')

        # Try to delete the vehicle with an unexpected request body
        response = self.client.delete(
            f'/vehicle/{self.example_vehicle["vin"]}',
            data=json.dumps({"unexpected_field": "unexpected_value"}),
            content_type='application/json'
        )
        assert response.status_code == 422  

    def test_delete_vehicle_case_insensitive_vin(self):
        """
        Test DELETE /vehicle/{vin} with a VIN in a different case (case-insensitive match).
        """
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')

        response = self.client.delete(f'/vehicle/{self.example_vehicle["vin"].lower()}')
        assert response.status_code == 204   #success


    def test_delete_vehicle_database_error(self):
        """
        Test DELETE /vehicle/{vin} when a database error occurs.
        """
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')

        # Simulate a database error
        with patch('app.server.get_db', side_effect=Exception("Simulated database error")):
            response = self.client.delete(f'/vehicle/{self.example_vehicle["vin"]}')
            assert response.status_code == 500
