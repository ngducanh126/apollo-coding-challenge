import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'vehicles.db')

def get_db():
    db_path = os.path.abspath(DATABASE)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    db_path = os.path.abspath(DATABASE)
    if not os.path.exists(db_path):
        print(f"Database at {db_path} does not exist. It will be created.")
    print(f"Using database at: {db_path}")
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
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
        db.commit()