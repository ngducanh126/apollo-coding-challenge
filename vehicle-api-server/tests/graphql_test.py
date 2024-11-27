import pytest
import json
from app.graphql_server import app
from app.db import init_db, get_db

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        # Initialize the database before test
        with app.app_context():
            init_db()
            db = get_db()
            db.execute("DELETE FROM vehicles")  # Clear the table
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
