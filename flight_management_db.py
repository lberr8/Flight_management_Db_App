import sqlite3, pprint

# create database called Flight_maganement_db
# # This line creates a connection to an SQLite database file named 'Flight_Management'. If the file doesn't already exist, SQLite will create it. 
# The connection is stored in the variable 'conn'.

DATABASE_FILE = "Flight_Management"

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
        "CREATE TABLE IF NOT EXISTS flights (flight_no TEXT, departure_date TEXT, departure_time INTEGER, departure_gate TEXT, destination TEXT, arrival_date TEXT, arrival_time INTEGER, arrival_gate TEXT, no_passengers INTEGER, captain TEXT, first_officer TEXT, flight_status TEXT, passenger_classes TEXT) STRICT",
        "CREATE TABLE IF NOT EXISTS pilots (pilot_id TEXT, rank TEXT, licence_no INTEGER, licence_valid INTEGER, status TEXT, flying_hours REAL) STRICT"
        "CREATE TABLE IF NOT EXISTS employees (employee_id TEXT, first_name TEXT, last_name TEXT, date_of_birth TEXT, phone INTEGER, email TEXT, street TEXT, town TEXT, post_code TEXT, salary INTEGER) STRICT"
        "CREATE TABLE IF NOT EXISTS destinations (destination_id INTEGER, name TEXT, country TEXT, street TEXT, city TEXT, postcode TEXT)"
    ]

    for statement in create_statements:
        cursor.execute(statement)


# function to drop tables
def drop_tables(cursor):
    pass


def initialise_table_data(cursor, conn):
    flights_data = ""
    pilots_data = ""
    employees_data = ""
    destinations_data = ""

    for flight_data in flights_data:
        cursor.execute(f"INSERT INTO flights VALUES({flight_data})")

    for pilot_data in pilots_data:
        cursor.execute(f"INSERT INTO flights VALUES({pilot_data})")

    for employee_data in employees_data:
        cursor.execute(f"INSERT INTO flights VALUES({employee_data})")

    for destination_data in destinations_data:
        cursor.execute(f"INSERT INTO flights VALUES({destination_data})")

    conn.commit()


db_conn = sqlite3.connect(DATABASE_FILE)
print("Database has been created")

cursor = db_conn.cursor()
create_tables(cursor)
initialise_table_data(cursor, db_conn)

results = cursor.execute("SELECT * FROM flights")
# for row in cursor:
#     print("flight_no = ", row[0]) etc
# or
# all_flights = results.fetchall()
# or
#pprint.pprint(all_flights)





# ref panoto recording