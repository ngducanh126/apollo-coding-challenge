import requests
import json

data = {
            "vin": "111111111111111",
            "manufacturer_name": "Honda",
            "description": "Reliable sedan",
            "horse_power": 150,
            "model_name": "Accord",
            "model_year": 2020,
            "purchase_price": 25000.50,
            "fuel_type": "Gasoline"
        }
response = requests.post("http://127.0.0.1:5002/vehicle", json=data)
data = {
            "name" : "Honda",
            "headquarters" : "Japan"
        }
response = requests.post("http://127.0.0.1:5002/manufacturer", json=data)


# GET
response_vehicles = requests.get("http://127.0.0.1:5002/vehicle")
response_manufacterers = requests.get("http://127.0.0.1:5002/manufacturer")
vehicles = response_vehicles.json()
manufacturers = response_manufacterers.json()
print('vehicles is ', vehicles)
print('manufacturers is ', manufacturers)

# GET
response_v_and_m = requests.get("http://127.0.0.1:5002/vehicle/manufacturer")
data = response_v_and_m.json()
print('v and m ', data)