import pytest
import json
from app.graphql_server import app
from app.db import init_db, get_db

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        # Initialize the db before test
        with app.app_context():
            init_db()
            db = get_db()
            db.execute("DELETE FROM vehicles")
            db.execute(
                """INSERT INTO vehicles (vin, manufacturer_name, description, horse_power,
                model_name, model_year, purchase_price, fuel_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                ("1HGCM82633A123456", "Toyota", "Test Vehicle", 200, "Camry", 2020, 25000.0, "Gas"),
            )
            db.commit()
        yield client

def test_create_vehicle(client):
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
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "errors" not in data
    assert data["data"]["createVehicle"]["vin"] == "2HGCM82633A654321"
    assert data["data"]["createVehicle"]["manufacturerName"] == "Honda"

def test_query_vehicle(client):
    query = '''
    query {
        vehicle(vin: "1HGCM82633A123456") {
            vin
            manufacturerName
            description
        }
    }
    '''
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "errors" not in data
    assert data["data"]["vehicle"]["vin"] == "1HGCM82633A123456"
    assert data["data"]["vehicle"]["manufacturerName"] == "Toyota"
    assert data["data"]["vehicle"]["description"] == "Test Vehicle"
    

def test_query_vehicles_by_manufacturer_and_year(client):
    query = '''
    query {
        vehicles(manufacturerName: "Toyota", modelYear: 2020) {
            vin
            manufacturerName
            modelYear
        }
    }
    '''
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "errors" not in data
    vehicles = data["data"]["vehicles"]
    assert len(vehicles) > 0
    for vehicle in vehicles:
        assert vehicle["manufacturerName"] == "Toyota"
        assert vehicle["modelYear"] == 2020

def test_update_vehicle_success(client):
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
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "errors" not in data
    assert data["data"]["updateVehicle"]["vin"] == "1HGCM82633A123456"
    assert data["data"]["updateVehicle"]["manufacturerName"] == "Updated Toyota"
    assert data["data"]["updateVehicle"]["description"] == "Updated Test Vehicle"

def test_update_vehicle_not_found(client):
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
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "errors" in data


def test_update_vehicle_invalid_input(client):
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
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "errors" in data


def test_delete_vehicle_success(client):
    query = '''
    mutation {
        deleteVehicle(vin: "1HGCM82633A123456")
    }
    '''
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "errors" not in data
    assert data["data"]["deleteVehicle"] is True

def test_delete_vehicle_not_found(client):
    query = '''
    mutation {
        deleteVehicle(vin: "NONEXISTENTVIN")
    }
    '''
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "errors" in data


def test_delete_vehicle_case_insensitive(client):
    query = '''
    mutation {
        deleteVehicle(vin: "1hgcm82633a123456")
    }
    '''
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "errors" not in data
    assert data["data"]["deleteVehicle"] is True
