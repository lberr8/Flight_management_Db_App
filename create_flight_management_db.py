import sqlite3, pprint
import csv

# create database called Flight_maganement_db
# # This line creates a connection to an SQLite database file named 'Flight_Management'. If the file doesn't already exist, SQLite will create it. 
# The connection is stored in the variable 'conn'.

DATABASE_FILE = "flight_management"

def create_tables(cursor):
    create_statements = [
        "CREATE TABLE IF NOT EXISTS flights (flight_no INTEGER, departure_date TEXT, departure_gate INTEGER, arrival_date TEXT, no_passengers INTEGER, captain INTEGER, first_officer INTEGER, flight_status TEXT) STRICT",
        "CREATE TABLE IF NOT EXISTS pilots (pilot_id INTEGER, first_name TEXT, last_name TEXT, dob TEXT, license_no INTEGER, license_valid INTEGER, rank TEXT, phone_no INTEGER, email TEXT, address_id INTEGER) STRICT",
        "CREATE TABLE IF NOT EXISTS addresses (address_id INTEGER, street TEXT, city TEXT, postcode TEXT, country TEXT) STRICT",
        "CREATE TABLE IF NOT EXISTS destinations (dest_id INTEGER, name TEXT, address_id INTEGER, no_of_gates INTEGER) STRICT",
        "CREATE TABLE IF NOT EXISTS arrival_gates (dest_id INTEGER, gate_id INTEGER, flight_no INTEGER) STRICT",
        "CREATE TABLE IF NOT EXISTS passenger_classes (class_id TEXT, name TEXT) STRICT",
        "CREATE TABLE IF NOT EXISTS flight_class_details (class_id TEXT, flight_no INTEGER) STRICT"
    ]

    for statement in create_statements:
        cursor.execute(statement)


# function to drop tables
def drop_table(cursor, table_name):
    cursor.execute(f'DROP TABLE {table_name}')
    print(f"\n{table_name} has been deleted")


def initialise_table_data(cursor, conn):
    # 1 - addresses
    with open('data_files\\addresses.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            cursor.execute("""INSERT INTO addresses 
                           (address_id, street, city, postcode, country)
                           VALUES(?, ?, ?, ?, ?)""", row)
        
        print("Addresses table has been created and initialised with data")

    
    # 2 - destinations
    with open('data_files\\destinations.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            cursor.execute("""INSERT INTO destinations
                        (dest_id, name, address_id, no_of_gates) 
                        VALUES(?, ?, ?, ?)""", row)
            
        print("Destinations table has been created and initialised with data")

    # 3 - pilots
    with open('data_files\\pilots.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            cursor.execute("""INSERT INTO pilots
                        (pilot_id, first_name, last_name, dob, license_no, license_valid, rank, phone_no, email, address_id) 
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", row)
            
        print("Pilots table has been created and initialised with data")

    # 4 - flights    
    with open('data_files\\flights.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            cursor.execute("""INSERT INTO flights
                        (flight_no, departure_date, departure_gate, arrival_date, no_passengers, captain, first_officer, flight_status) 
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", row)
            
        print("Flights table has been created and initialised with data")

    # 5 - arrival_gates
    with open('data_files\\arrival_gates.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            cursor.execute("""INSERT INTO arrival_gates
                        (dest_id, gate_id, flight_no) 
                        VALUES(?, ?, ?)""", row)
            
        print("arrival_gates table has been created and initialised with data")

    # 6 - passenger classes
    with open('data_files\\passenger_classes.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            cursor.execute("""INSERT INTO passenger_classes
                        (class_id, name) 
                        VALUES(?, ?)""", row)
            
        print("passenger_classes table has been created and initialised with data")

    # 7 - flight class details
    with open('data_files\\flight_class_details.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            cursor.execute("""INSERT INTO flight_class_details
                        (class_id, flight_no) 
                        VALUES(?, ?)""", row)
            
        print("flight_class_details table has been created and initialised with data")

    
    conn.commit()

if __name__ == "__main__":

    db_conn = sqlite3.connect(f"{DATABASE_FILE}.db")
    print("Database has been created")
    # db_conn.execute('PRAGMA foreign_keys = ON') # enable foreign key safety features

    cursor = db_conn.cursor()
    create_tables(cursor)
    initialise_table_data(cursor, db_conn)
    drop_table(cursor,'addresses')





# ref panoto recording