import sqlite3, pprint
import csv

# create database called Flight_maganement_db
# # This line creates a connection to an SQLite database file named 'Flight_Management'. If the file doesn't already exist, SQLite will create it. 
# The connection is stored in the variable 'conn'.

DATABASE_FILE = "flight_management"

# conn.execute("DROP TABLE IF EXISTS flights")
# print("Table flights created successfully")

# conn.execute("DROP TABLE IF EXISTS pilots")
# print("Table pilots created successfully")

# conn.execute("DROP TABLE IF EXISTS destination")
# print("Table destination created successfully")

# dates: YYYY-MM-DD ?
# time: HHMM
# or date time can be recorded as 'YYYY-MM-DD HH:MM:SS' TEXT
# passenger_classes: first, business, economy - multiple answers in field possible
# flight_status: on-time, delayed, cancelled
# boarding_status: boarding, not_boarding
# boolean can be recorded as integer with 1 representing true. 
def create_tables(cursor):
    create_statements = [
        # "CREATE TABLE IF NOT EXISTS flights (flight_no INTEGER, departure_date TEXT, departure_gate INTEGER, dest_id INTEGER, arrival_date TEXT, arrival_gate INTEGER, no_passengers INTEGER, captain INTEGER, first_officer INTEGER, flight_status TEXT, passenger_classes TEXT) STRICT",
        # "CREATE TABLE IF NOT EXISTS pilots (pilot_id INTEGER, first_name TEXT, last_name TEXT, dob TEXT, license_no INTEGER, license_valid INTEGER, rank TEXT, phone_no INTEGER, email TEXT) STRICT"
        "CREATE TABLE IF NOT EXISTS addresses (address_id INTEGER, street TEXT, city TEXT, postcode TEXT, country TEXT) STRICT"
        # "CREATE TABLE IF NOT EXISTS destinations (dest_id INTEGER, name TEXT, country TEXT, address_id INTEGER) STRICT"
    ]

    for statement in create_statements:
        cursor.execute(statement)


# function to drop tables
def drop_tables(cursor):
    pass


def initialise_table_data(cursor, conn):
    

    # for flight_data in flights_data:
    #     cursor.execute(f"INSERT INTO flights VALUES({flight_data})")

    # for pilot_data in pilots_data:
    #     cursor.execute(f"INSERT INTO flights VALUES({pilot_data})")

    with open('addresses.csv', 'r') as addresses_data:
        csv_reader = csv.reader(addresses_data)
        next(csv_reader)

        for address_data in csv_reader:
            cursor.execute("""INSERT INTO addresses 
                           (address_id, street, city, postcode, country)
                           VALUES(?, ?, ?, ?, ?)""", address_data)

    # for destination_data in destinations_data:
    #     cursor.execute(f"INSERT INTO flights VALUES({destination_data})")

    conn.commit()


db_conn = sqlite3.connect(f"{DATABASE_FILE}.db")
print("Database has been created")

cursor = db_conn.cursor()
create_tables(cursor)
initialise_table_data(cursor, db_conn)

results = cursor.execute("SELECT * FROM addresses")
# for row in cursor:
#     print("flight_no = ", row[0]) etc
# or
# all_flights = results.fetchall()
# or
# pprint.pprint(all_flights)
pprint.pprint(results.fetchall())





# ref panoto recording