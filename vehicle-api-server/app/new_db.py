import sqlite3
import os

DATABASE = 'vehicles2.db'

def get_db():
    db_path = os.path.abspath(DATABASE)
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def init_vehicles_table():
    with get_db() as db:
        cursor = db.cursor()  
        cursor.execute('''CREATE TABLE IF NOT EXISTS vehicles (
            vin TEXT PRIMARY KEY COLLATE NOCASE,
            manufacturer_name TEXT NOT NULL,
            description TEXT NOT NULL,
            horse_power INTEGER NOT NULL,
            model_name TEXT NOT NULL,
            model_year INTEGER NOT NULL,
            purchase_price REAL NOT NULL,
            fuel_type TEXT NOT NULL,
            foreign key (manufacturer_name) references manufacturers(name) )
        ''')
        db.commit()  

def init_manufacturers_table():
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('''
                   create table if not exists manufacturers (
                       name text primary key,
                       headquarters text not null
                       )
                   
                   ''')
        db.commit()

if __name__ == '__main__':
    init_manufacturers_table()
    init_vehicles_table()