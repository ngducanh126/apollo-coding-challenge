import sqlite3
import os

DATABASE = 'vehicles.db'

def get_db():
    db_path = os.path.abspath(DATABASE)
    print(f"Using database at: {db_path}") 

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with get_db() as db:
        cursor = db.cursor()  # Create a cursor explicitly
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
        db.commit()  # Commit changes explicitly

if __name__ == "__main__":
    init_db()
    print("Database initialized.")