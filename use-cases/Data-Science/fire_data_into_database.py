import requests
import random
import string
import argparse

post_url = "http://127.0.0.1:5000/vehicle"

manufacturers = ["Toyota", "Honda", "Ford", "Chevrolet", "Nissan", "BMW", "Mercedes-Benz", "Volkswagen", "Hyundai", "Kia"]
models = {
    "Toyota": ["Corolla", "Camry", "RAV4"],
    "Honda": ["Civic", "Accord", "CR-V"],
    "Ford": ["F-150", "Explorer", "Mustang"],
    "Chevrolet": ["Silverado", "Malibu", "Equinox"],
    "Nissan": ["Altima", "Rogue", "Sentra"],
    "BMW": ["X5", "3 Series", "5 Series"],
    "Mercedes-Benz": ["C-Class", "E-Class", "GLE"],
    "Volkswagen": ["Golf", "Passat", "Tiguan"],
    "Hyundai": ["Elantra", "Santa Fe", "Tucson"],
    "Kia": ["Sportage", "Sorento", "Optima"]
}
fuel_types = ["Gasoline", "Diesel", "Electric", "Hybrid"]

# Generate random VIN
def generate_vin():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=17))

# Generate good random data into the DB
def feed_good_data():
    manufacturer = random.choice(manufacturers)
    model_name = random.choice(models[manufacturer])

    for _ in range(10):
        data = {
        "vin": generate_vin(),
        "manufacturer_name": manufacturer,
        "description": f"A reliable {manufacturer} {model_name} vehicle",
        "horse_power": random.randint(100, 400),
        "model_name": model_name,
        "model_year": random.randint(2000, 2025),
        "purchase_price": round(random.uniform(15000, 50000), 2),
        "fuel_type": random.choice(fuel_types)
        }
        response = requests.post(post_url, json=data)
        if response.status_code == 201:
            print("Successfully added vehicle")
        else:
            print("Failed to add vehicle")

# Generate data with missing values and duplicates into the DB  - THIS IS CURRENTLY NOT WORKING BECAUSE THE API DOES NOT ALLOW MISSING OR DUPLICATE VINS
# def feed_bad_data():
#     data = [
#         {
#             "vin": generate_vin(),
#             "manufacturer_name": random.choice(manufacturers),
#             "description": "A reliable car",  # No missing value here
#             "horse_power": random.randint(100, 400),  # Valid value
#             "model_name": random.choice(["Corolla", "Civic", "F-150", "Accord", "Camry"]),
#             "model_year": random.randint(2000, 2025),  # Valid value
#             "purchase_price": round(random.uniform(15000, 50000), 2),  # Valid value
#             "fuel_type": random.choice(fuel_types),
#         },
#         {
#             "vin": generate_vin(),
#             "manufacturer_name": None,  # Missing manufacturer name
#             "description": "Missing manufacturer",  # Missing value example
#             "horse_power": random.randint(100, 400),
#             "model_name": random.choice(["Golf", "Passat"]),
#             "model_year": random.randint(2000, 2025),
#             "purchase_price": round(random.uniform(15000, 50000), 2),
#             "fuel_type": random.choice(fuel_types),
#         },
#         {
#             "vin": generate_vin(),
#             "manufacturer_name": "Toyota",
#             "description": "Duplicate vehicle",
#             "horse_power": random.randint(100, 400),
#             "model_name": "Corolla",
#             "model_year": 2020,
#             "purchase_price": 25000.50,
#             "fuel_type": "Gasoline",
#         },  # Duplicate data
#         {
#             "vin": generate_vin(),
#             "manufacturer_name": "Toyota",
#             "description": "Duplicate vehicle",
#             "horse_power": random.randint(100, 400),
#             "model_name": "Corolla",
#             "model_year": 2020,
#             "purchase_price": 25000.50,
#             "fuel_type": "Gasoline",
#         },  # Duplicate data
#     ]
    
#     for this_data in data:
#         response = requests.post(post_url, json=data)
#         if response.status_code == 201:
#             print("Successfully added bad vehicle")
#         else:
#             print("Failed to add bad vehicle")


def get_valid_argument():
    while True:
        print("Please provide a valid argument ('good' or 'bad'):")
        user_input = input("Type of data to fire: ").strip().lower()
        if user_input in ["good", "bad"]:
            return user_input
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    feed_good_data()