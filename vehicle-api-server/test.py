import requests
import json

data = {
            "vin": "11",
            "manufacturer_name": "Honda",
            "description": "Reliable sedan",
            "horse_power": 150,
            "model_name": "Accord",
            "model_year": 2020,
            "purchase_price": 25000.50,
            "fuel_type": "Gasoline"
        }
response = requests.get("http://127.0.0.1:5000/vehicle/1HGCM82633A123456",)
print(response.status_code)
print(response.json())