import sqlite3
import csv

def create_tables(cursor):
    create_statements = [
        """CREATE TABLE IF NOT EXISTS flights (flight_no INTEGER PRIMARY KEY AUTOINCREMENT, departure_date TEXT, departure_gate INTEGER CHECK(departure_gate < 21), 
        arrival_date TEXT CHECK(arrival_date > departure_date), no_passengers INTEGER, captain INTEGER, first_officer INTEGER, flight_status TEXT, 
        FOREIGN KEY (captain) REFERENCES pilots (pilot_id) ON UPDATE SET NULL ON DELETE SET NULL,
        FOREIGN KEY (first_officer) REFERENCES pilots (pilot_id) ON UPDATE SET NULL ON DELETE SET NULL)""",
        """CREATE TABLE IF NOT EXISTS pilots (pilot_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, dob TEXT, license_no INTEGER, license_valid INTEGER, 
        rank TEXT, phone_no INTEGER, email TEXT, address_id INTEGER,
        FOREIGN KEY (address_id) REFERENCES addresses (address_id) ON UPDATE SET NULL ON DELETE SET NULL)""",
        """CREATE TABLE IF NOT EXISTS addresses (address_id INTEGER PRIMARY KEY, street TEXT, city TEXT, postcode TEXT NOT NULL, country TEXT NOT NULL)""",
        """CREATE TABLE IF NOT EXISTS destinations (dest_id INTEGER PRIMARY KEY, name TEXT, dest_code TEXT, address_id INTEGER, no_of_gates INTEGER,
        FOREIGN KEY (address_id) REFERENCES addresses (address_id) ON UPDATE SET NULL ON DELETE SET NULL)""",
        """CREATE TABLE IF NOT EXISTS arrival_gates (dest_id INTEGER, gate_id INTEGER, flight_no INTEGER, PRIMARY KEY(dest_id, gate_id, flight_no),
        FOREIGN KEY (dest_id) REFERENCES destinations (dest_id) ON UPDATE SET NULL ON DELETE SET NULL,
        FOREIGN KEY (flight_no) REFERENCES flights (flight_no) ON UPDATE SET NULL ON DELETE SET NULL)""",
        """CREATE TABLE IF NOT EXISTS passenger_classes (class_id TEXT PRIMARY KEY, name TEXT)""",
        """CREATE TABLE IF NOT EXISTS flight_class_details (class_id TEXT, flight_no INTEGER, PRIMARY KEY(class_id, flight_no),
        FOREIGN KEY (class_id) REFERENCES passenger_classes (class_id) ON UPDATE SET NULL ON DELETE SET NULL,
        FOREIGN KEY (flight_no) REFERENCES flights (flight_no) ON UPDATE SET NULL ON DELETE SET NULL)"""
    ]

    for statement in create_statements:
        cursor.execute(statement)


def drop_table(cursor, table_name):
    cursor.execute(f'DROP TABLE {table_name}')
    print(f"\n{table_name} has been deleted")


def initialise_table_data(cursor, conn):
    # 1 - addresses
    try:
        with open('data_files/addresses.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                cursor.execute("""INSERT INTO addresses 
                            (address_id, street, city, postcode, country)
                            VALUES(?, ?, ?, ?, ?)""", row)
            
            print("Addresses table has been created and initialised with data")
    except FileNotFoundError:
        print(f"\nFile not found: data_files/addresses.csv")

    
    # 2 - destinations
    try:
        with open('data_files/destinations.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                cursor.execute("""INSERT INTO destinations
                            (dest_id, name, dest_code, address_id, no_of_gates) 
                            VALUES(?, ?, ?, ?, ?)""", row)
                
            print("Destinations table has been created and initialised with data")
    except FileNotFoundError:
        print(f"\nFile not found: data_files/destinations.csv")

    # 3 - pilots
    try:
        with open('data_files/pilots.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                cursor.execute("""INSERT INTO pilots
                            (pilot_id, first_name, last_name, dob, license_no, license_valid, rank, phone_no, email, address_id) 
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", row)
                
            print("Pilots table has been created and initialised with data")
    except FileNotFoundError:
        print(f"\nFile not found: data_files/pilots.csv")

    # 4 - flights    
    try:
        with open('data_files/flights.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                cursor.execute("""INSERT INTO flights
                            (flight_no, departure_date, departure_gate, arrival_date, no_passengers, captain, first_officer, flight_status) 
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", row)
                
            print("Flights table has been created and initialised with data")
    except FileNotFoundError:
        print(f"\nFile not found: data_files/flights.csv")

    # 5 - arrival_gates
    try:
        with open('data_files/arrival_gates.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                cursor.execute("""INSERT INTO arrival_gates
                            (dest_id, gate_id, flight_no) 
                            VALUES(?, ?, ?)""", row)
                
            print("arrival_gates table has been created and initialised with data")
    except FileNotFoundError:
        print(f"\nFile not found: data_files/arrival_gates.csv")

    # 6 - passenger classes
    try:
        with open('data_files/passenger_classes.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                cursor.execute("""INSERT INTO passenger_classes
                            (class_id, name) 
                            VALUES(?, ?)""", row)
                
            print("passenger_classes table has been created and initialised with data")
    except FileNotFoundError:
        print(f"\nFile not found: data_files/passenger_classes.csv")

    # 7 - flight class details
    try:
        with open('data_files/flight_class_details.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                cursor.execute("""INSERT INTO flight_class_details
                            (class_id, flight_no) 
                            VALUES(?, ?)""", row)
                
            print("flight_class_details table has been created and initialised with data")
    except FileNotFoundError:
        print(f"\nFile not found: data_files/flight_class_details.csv")
    
    conn.commit()

if __name__ == "__main__":

    # create database called Flight_maganement_db
    # # This line creates a connection to an SQLite database file named 'flight_management'. If the file doesn't already exist, SQLite will create it. 
    # The connection is stored in the variable 'db_conn'.
    DATABASE_FILE = "flight_management"

    db_conn = sqlite3.connect(f"{DATABASE_FILE}.db")
    print("Database has been created")

    cursor = db_conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;") # enable foreign key safety features

    create_tables(cursor)
    initialise_table_data(cursor, db_conn)
    # drop_table(cursor, 'addresses') # drop table example

    db_conn.close()
