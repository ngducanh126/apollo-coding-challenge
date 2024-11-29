from flask import Flask, g
from strawberry.flask.views import GraphQLView
import strawberry
from .db import get_db, init_db
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

with app.app_context():
    init_db()

@app.teardown_appcontext
def teardown(exception):
    pass

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

# Resolver for fetching all vehicles
def resolve_vehicles() -> list[Vehicle]:
    db = get_db()
    vehicles = db.execute("SELECT * FROM vehicles").fetchall()
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

# Resolver for fetching a vehicle by VIN
def resolve_vehicle(vin: str) -> Vehicle:
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
    try:
        db.execute(
            """INSERT INTO vehicles (vin, manufacturer_name, description, horse_power, 
            model_name, model_year, purchase_price, fuel_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (vin, manufacturer_name, description, horse_power, model_name, model_year, purchase_price, fuel_type),
        )
        db.commit()
    except Exception as e:
        raise ValueError(f"Error creating vehicle: {e}")

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
    result = db.execute("SELECT * FROM vehicles WHERE vin = ?", (vin,)).fetchone()
    if not result:
        raise ValueError(f"Vehicle with VIN '{vin}' not found.")
    
    db.execute(
        """UPDATE vehicles SET manufacturer_name = ?, description = ?, horse_power = ?, 
        model_name = ?, model_year = ?, purchase_price = ?, fuel_type = ? WHERE vin = ?""",
        (manufacturer_name, description, horse_power, model_name, model_year, purchase_price, fuel_type, vin),
    )
    db.commit()

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

# Resolver for deleting a vehicle
def resolve_delete_vehicle(vin: str) -> bool:
    db = get_db()
    result = db.execute("SELECT * FROM vehicles WHERE vin = ?", (vin,)).fetchone()
    if not result:
        raise ValueError(f"Vehicle with VIN '{vin}' not found.")
    
    db.execute("DELETE FROM vehicles WHERE vin = ?", (vin,))
    db.commit()
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

# Set up the GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Add the GraphQL endpoint to the Flask app
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema, graphiql=True),
)

if __name__ == "__main__":
    app.run(debug=True)
