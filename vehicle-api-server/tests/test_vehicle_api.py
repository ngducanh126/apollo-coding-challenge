from app.server import app
from app.db import init_db, get_db
import json
import logging

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

        # Configure logging
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

    def setup_method(self):
        """
        Set up the test client before each test.
        """
        self.client = app.test_client()
        self.example_vehicle = {
            "vin": "1HGCM82633A123457",
            "manufacturer_name": "Honda",
            "description": "Reliable sedan",
            "horse_power": 150,
            "model_name": "Accord",
            "model_year": 2020,
            "purchase_price": 25000.50,
            "fuel_type": "Gasoline"
        }

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
        """
        Test GET /vehicle/{vin} with a non-existing VIN.
        """
        response = self.client.get('/vehicle/INVALID_VIN')
        assert response.status_code == 400  # Expecting 400 due to invalid VIN format

    def test_get_vehicle_by_vin_success(self):
        """
        Test GET /vehicle/{vin} with an existing VIN.
        """
        # First, add the vehicle to the database
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')

        # Now, fetch the vehicle by VIN
        response = self.client.get(f'/vehicle/{self.example_vehicle["vin"]}')
        assert response.status_code == 200  
        assert response.json["vin"] == self.example_vehicle["vin"]
        assert response.json["manufacturer_name"] == self.example_vehicle["manufacturer_name"]  # Verify other fields

    def test_get_vehicle_by_invalid_vin(self):
        """
        Test GET /vehicle/{vin} with an invalid VIN format.
        """
        # Testing with a VIN that does not conform to the correct format
        response = self.client.get('/vehicle/INVALID_VIN')
        assert response.status_code == 400  


    def test_update_vehicle_success(self):
        """
        Test PUT /vehicle/{vin} to update an existing vehicle.
        """
        # Add a vehicle first
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')

        # Update the vehicle
        updated_data = self.example_vehicle.copy()
        updated_data["description"] = "Updated description"
        response = self.client.put(
            f'/vehicle/{self.example_vehicle["vin"]}',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        assert response.status_code == 200  # Expecting 200 OK
        assert response.json["description"] == "Updated description"  


    def test_update_vehicle_not_found(self):
        """
        Test PUT /vehicle/{vin} with a non-existing VIN.
        """
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
        
        # Try updating a non-existing vehicle
        response = self.client.put(
            '/vehicle/1HGCM82633A123457',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        assert response.status_code == 404  # Expecting 404 Not Found
        # assert "Vehicle not found" in response.json["error"]

    def test_update_vehicle_invalid_data(self):
        """
        Test PUT /vehicle/{vin} with invalid (missing) data.
        """
        # Add a vehicle first
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')

        # Try updating with missing required fields
        updated_data = self.example_vehicle.copy()
        updated_data.pop("description")
        
        response = self.client.put(
            f'/vehicle/{self.example_vehicle["vin"]}',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        assert response.status_code == 422  


    def test_delete_vehicle_not_found(self):
        """
        Test DELETE /vehicle/{vin} when the vehicle does not exist.
        """
        response = self.client.delete('/vehicle/11111111111111111')
        assert response.status_code == 404  

    def test_delete_vehicle_invalid_vin_format(self):
        """
        Test DELETE /vehicle/{vin} with a malformed VIN (too short).
        """
        response = self.client.delete('/vehicle/123') 
        assert response.status_code == 400  


    def test_delete_vehicle_success(self):
        """
        Test DELETE /vehicle/{vin} when the vehicle exists.
        """
        # add the vehicle to the database
        self.client.post('/vehicle', data=json.dumps(self.example_vehicle), content_type='application/json')

        # Now, delete the vehicle
        response = self.client.delete(f'/vehicle/{self.example_vehicle["vin"]}')
        assert response.status_code == 204  