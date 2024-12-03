from flask import Flask, g
from strawberry.flask.views import GraphQLView
import strawberry
from .db import get_db, init_db
from flask_cors import CORS
import sqlite3
from typing import Optional


app = Flask(__name__)
CORS(app)

with app.app_context():
    init_db()

@app.teardown_appcontext
def teardown(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Define the Vehicle type
@strawberry.type
class Vehicle:
    vin: str
    manufacturer_name: str
    description: str
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: float
    fuel_type: str

# resolver to get all vehicles
def resolve_vehicles(manufacturer_name: Optional[str] = None, model_year: Optional[int] = None) -> list[Vehicle]:
    try:
        db = get_db()
        query = "SELECT * FROM vehicles WHERE 1=1"
        params = []

        if manufacturer_name:
            query += " AND manufacturer_name = ?"
            params.append(manufacturer_name)

        if model_year:
            query += " AND model_year = ?"
            params.append(model_year)
        vehicles = db.execute(query, params).fetchall()
        return [
            Vehicle(
                vin=vehicle["vin"],
                manufacturer_name=vehicle["manufacturer_name"],
                description=vehicle["description"],
                horse_power=vehicle["horse_power"],
                model_name=vehicle["model_name"],
                model_year=vehicle["model_year"],
                purchase_price=vehicle["purchase_price"],
                fuel_type=vehicle["fuel_type"],
            )
            for vehicle in vehicles
        ]
    except Exception as e:
        raise ValueError(f"Error fetching vehicles: {e}")

# Resolver for fetching a vehicle by VIN
def resolve_vehicle(vin: str) -> Vehicle:
    try:
        db = get_db()
        vehicle = db.execute("SELECT * FROM vehicles WHERE vin = ?", (vin,)).fetchone()
        if vehicle:
            return Vehicle(
                vin=vehicle["vin"],
                manufacturer_name=vehicle["manufacturer_name"],
                description=vehicle["description"],
                horse_power=vehicle["horse_power"],
                model_name=vehicle["model_name"],
                model_year=vehicle["model_year"],
                purchase_price=vehicle["purchase_price"],
                fuel_type=vehicle["fuel_type"],
            )
        raise ValueError(f"Vehicle with VIN '{vin}' not found.")
    except Exception as e:
        raise ValueError(f"Error fetching vehicles: {e}")

# Resolver for creating a vehicle
def resolve_create_vehicle(
    vin: str,
    manufacturer_name: str,
    description: str,
    horse_power: int,
    model_name: str,
    model_year: int,
    purchase_price: float,
    fuel_type: str,
) -> Vehicle:
    db = get_db()
    # Validate VIN format
    if not validate_vin(vin):
        raise ValueError("Invalid VIN format provided.")

    existing_vehicle = db.execute('SELECT vin FROM vehicles WHERE vin = ?', (vin,)).fetchone()
    if existing_vehicle:
        raise ValueError(f"Vehicle with VIN '{vin}' already exists.")

    # Validate required fields
    required_fields = {
        "manufacturer_name": str,
        "description": str,
        "horse_power": int,
        "model_name": str,
        "model_year": int,
        "purchase_price": float,
        "fuel_type": str
    }

    for field, field_type in required_fields.items():
        value = locals().get(field)
        if value is None or not isinstance(value, field_type):
            raise ValueError(f"Field '{field}' must be of type {field_type.__name__} and cannot be null.")
        if isinstance(value, (int, float)) and value < 0:
            raise ValueError(f"Field '{field}' must be non-negative.")

    # Insert new vehicle
    try:
        db.execute(
            """INSERT INTO vehicles (vin, manufacturer_name, description, horse_power, 
            model_name, model_year, purchase_price, fuel_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (vin, manufacturer_name, description, horse_power, model_name, model_year, purchase_price, fuel_type),
        )
        db.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error: {e}")

    return Vehicle(
        vin=vin,
        manufacturer_name=manufacturer_name,
        description=description,
        horse_power=horse_power,
        model_name=model_name,
        model_year=model_year,
        purchase_price=purchase_price,
        fuel_type=fuel_type,
    )

# Resolver for updating a vehicle
def resolve_update_vehicle(
    vin: str,
    manufacturer_name: str,
    description: str,
    horse_power: int,
    model_name: str,
    model_year: int,
    purchase_price: float,
    fuel_type: str,
) -> Vehicle:
    db = get_db()

    # Validate VIN format
    if not validate_vin(vin):
        raise ValueError("Invalid VIN format provided.")

    existing_vehicle = db.execute("SELECT * FROM vehicles WHERE vin = ?", (vin,)).fetchone()
    if not existing_vehicle:
        raise ValueError(f"Vehicle with VIN '{vin}' not found.")

    # Validate required fields
    required_fields = {
        "manufacturer_name": str,
        "description": str,
        "horse_power": int,
        "model_name": str,
        "model_year": int,
        "purchase_price": float,
        "fuel_type": str
    }

    for field, field_type in required_fields.items():
        value = locals().get(field)
        if value is None or not isinstance(value, field_type):
            raise ValueError(f"Field '{field}' must be of type {field_type.__name__} and cannot be null.")
        if isinstance(value, (int, float)) and value < 0:
            raise ValueError(f"Field '{field}' must be non-negative.")

    # Update vehicle
    try:
        db.execute(
            """UPDATE vehicles SET manufacturer_name = ?, description = ?, horse_power = ?, 
            model_name = ?, model_year = ?, purchase_price = ?, fuel_type = ? WHERE vin = ?""",
            (manufacturer_name, description, horse_power, model_name, model_year, purchase_price, fuel_type, vin),
        )
        db.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error: {e}")

    return Vehicle(
        vin=existing_vehicle["vin"],  # Return the original VIN's casing
        manufacturer_name=manufacturer_name,
        description=description,
        horse_power=horse_power,
        model_name=model_name,
        model_year=model_year,
        purchase_price=purchase_price,
        fuel_type=fuel_type,
    )

def validate_vin(vin):
    if not vin or len(vin) != 17:
        return False
    if not vin.isalnum():
        return False
    return True

# Resolver for deleting a vehicle
def resolve_delete_vehicle(vin: str) -> bool:
    db = get_db()

    # Validate VIN format
    if not validate_vin(vin):
        raise ValueError("Invalid VIN format provided.")

    try:
        result = db.execute("SELECT * FROM vehicles WHERE vin = ?", (vin,)).fetchone()
        if not result:
            raise ValueError(f"Vehicle with this VIN not found.")
        
        # Delete the vehicle
        db.execute("DELETE FROM vehicles WHERE vin = ?", (vin,))
        db.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error: {e}")

    return True


# Define Query and Mutation classes
@strawberry.type
class Query:
    vehicles: list[Vehicle] = strawberry.field(resolver=resolve_vehicles)
    vehicle: Vehicle = strawberry.field(resolver=resolve_vehicle)

@strawberry.type
class Mutation:
    create_vehicle: Vehicle = strawberry.mutation(resolver=resolve_create_vehicle)
    update_vehicle: Vehicle = strawberry.mutation(resolver=resolve_update_vehicle)
    delete_vehicle: bool = strawberry.mutation(resolver=resolve_delete_vehicle)

schema = strawberry.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema, graphiql=True),
)

if __name__ == "__main__":
    app.run(debug=True)
