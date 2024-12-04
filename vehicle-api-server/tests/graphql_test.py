from unittest import TestCase
from unittest.mock import patch
import sqlite3
import json
from app.graphql_server import app


class TestVehicleGraphQLAPI(TestCase):
    def setUp(self):
        """
        in-memory database before each test.
        """
        app.config['TESTING'] = True
        app.config['DEBUG'] = True

        self.client = app.test_client()
        self.test_db = sqlite3.connect(':memory:')
        self.test_db.row_factory = sqlite3.Row

        cursor = self.test_db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS vehicles (
            vin TEXT PRIMARY KEY COLLATE NOCASE,
            manufacturer_name TEXT NOT NULL,
            description TEXT NOT NULL,
            horse_power INTEGER NOT NULL,
            model_name TEXT NOT NULL,
            model_year INTEGER NOT NULL,
            purchase_price REAL NOT NULL,
            fuel_type TEXT NOT NULL
        )''')
        cursor.execute('''INSERT INTO vehicles (vin, manufacturer_name, description, horse_power, 
                        model_name, model_year, purchase_price, fuel_type)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                        ("1HGCM82633A123456", "Toyota", "Test Vehicle", 200, "Camry", 2020, 25000.0, "Gas"))
        self.test_db.commit()

        # patch `get_db` 
        self.get_db_patcher = patch('app.graphql_server.get_db', return_value=self.test_db)
        self.mock_get_db = self.get_db_patcher.start()

    def tearDown(self):
        self.get_db_patcher.stop()  
        self.test_db.close()  

    def test_create_vehicle(self):
        query = '''
        mutation {
            createVehicle(
                vin: "2HGCM82633A654321",
                manufacturerName: "Honda",
                description: "Another Test Vehicle",
                horsePower: 180,
                modelName: "Civic",
                modelYear: 2021,
                purchasePrice: 22000.0,
                fuelType: "Gas"
            ) {
                vin
                manufacturerName
                description
            }
        }
        '''
        response = self.client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "errors" not in data
        assert data["data"]["createVehicle"]["vin"] == "2HGCM82633A654321"
        assert data["data"]["createVehicle"]["manufacturerName"] == "Honda"

    def test_query_vehicle(self):
        query = '''
        query {
            vehicle(vin: "1HGCM82633A123456") {
                vin
                manufacturerName
                description
            }
        }
        '''
        response = self.client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "errors" not in data
        assert data["data"]["vehicle"]["vin"] == "1HGCM82633A123456"
        assert data["data"]["vehicle"]["manufacturerName"] == "Toyota"
        assert data["data"]["vehicle"]["description"] == "Test Vehicle"

    def test_query_vehicles_by_manufacturer_and_year(self):
        query = '''
        query {
            vehicles(manufacturerName: "Toyota", modelYear: 2020) {
                vin
                manufacturerName
                modelYear
            }
        }
        '''
        response = self.client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "errors" not in data
        vehicles = data["data"]["vehicles"]
        assert len(vehicles) > 0
        for vehicle in vehicles:
            assert vehicle["manufacturerName"] == "Toyota"
            assert vehicle["modelYear"] == 2020

    def test_update_vehicle_success(self):
        query = '''
        mutation {
            updateVehicle(
                vin: "1HGCM82633A123456",
                manufacturerName: "Updated Toyota",
                description: "Updated Test Vehicle",
                horsePower: 220,
                modelName: "Updated Camry",
                modelYear: 2021,
                purchasePrice: 26000.0,
                fuelType: "Hybrid"
            ) {
                vin
                manufacturerName
                description
            }
        }
        '''
        response = self.client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "errors" not in data
        assert data["data"]["updateVehicle"]["vin"] == "1HGCM82633A123456"
        assert data["data"]["updateVehicle"]["manufacturerName"] == "Updated Toyota"
        assert data["data"]["updateVehicle"]["description"] == "Updated Test Vehicle"

    def test_delete_vehicle_success(self):
        query = '''
        mutation {
            deleteVehicle(vin: "1HGCM82633A123456")
        }
        '''
        response = self.client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "errors" not in data
        assert data["data"]["deleteVehicle"] is True

    def test_update_vehicle_not_found(self):
        query = '''
        mutation {
            updateVehicle(
                vin: "NONEXISTENTVIN",
                manufacturerName: "Test",
                description: "Test",
                horsePower: 100,
                modelName: "Test",
                modelYear: 2021,
                purchasePrice: 20000.0,
                fuelType: "Gas"
            ) {
                vin
            }
        }
        '''
        response = self.client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "errors" in data


    def test_update_vehicle_invalid_input(self):
        query = '''
        mutation {
            updateVehicle(
                vin: "1HGCM82633A123456",
                manufacturerName: "",
                description: "Test Vehicle",
                horsePower: -10,
                modelName: "Test",
                modelYear: 2021,
                purchasePrice: -20000.0,
                fuelType: "Gas"
            ) {
                vin
            }
        }
        '''
        response = self.client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "errors" in data

    def test_delete_vehicle_not_found(self):
        query = '''
        mutation {
            deleteVehicle(vin: "NONEXISTENTVIN")
        }
        '''
        response = self.client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "errors" in data


    def test_delete_vehicle_case_insensitive(self):
        query = '''
        mutation {
            deleteVehicle(vin: "1hgcm82633a123456")
        }
        '''
        response = self.client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "errors" not in data
        assert data["data"]["deleteVehicle"] is True
