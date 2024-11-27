import sqlite3
from flask import g

DATABASE = 'vehicles.db'

def get_db():
    """
    Get a database connection, reuse it if already opened.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  
    return db

def init_db():
    """
    Initialize the vehicles table in the database.
    """
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS vehicles (
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

def close_db(exception=None):
    """
    Close the database connection after each request.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
