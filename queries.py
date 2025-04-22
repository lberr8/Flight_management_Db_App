import sqlite3, pprint

from prettytable import PrettyTable

conn = sqlite3.connect('flight_management.db')

###	Flight Retrieval: Retrieve flights based on multiple criteria, such as destination, status, or departure date.

print("\nDisplaying information for all flights that with a status of 'on-time'")
cursor = conn.execute("SELECT * FROM flights WHERE flight_status = 'on-time' ORDER BY departure_date")
for row in cursor:
    print(row)


print("\nDisplaying information for all flights that with a departure date of 2025-04-25")
cursor = conn.execute("SELECT * FROM flights WHERE departure_date LIKE '2025-04-25%'")
for row in cursor:
    print(row)

print("\nDisplaying information for flights where destination is LA")
cursor = conn.cursor()
cursor.execute("""SELECT flights.flight_no, destinations.name, flights.departure_date, flights.arrival_date FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      WHERE destinations.name LIKE '%LAX%'""")
# for row in cursor:
#     print(row)

column_names = [x[0] for x in cursor.description]
rows = cursor.fetchall()
print("printing rows", rows)

display_table = PrettyTable(column_names)
for row in rows:
     display_table.add_row(row)
print(display_table)

print("\nDisplaying information for flights where destination is LA, flight status is on-time that depart before 25/04/2025")


### Schedule Modification: Update flight schedules (e.g., change departure time or status).
###	Pilot Assignment: Assign pilots to flights and retrieve information about pilot schedules.
# SELECT destinations.dest_id, destinations.name, 
# SELECT pilots.pilot_id, pilots.first_name, pilots.last_name, flights.flight_no FROM flights, pilots


###	Destination Management: View and update destination information as required.




### Include additional queries that summarise data, such as the number of flights to each destination or the number of flights assigned to a pilot.



# results = cursor.execute("SELECT * FROM addresses")
# # for row in cursor:
# #     print("flight_no = ", row[0]) etc
# # or
# # all_flights = results.fetchall()
# # or
# # pprint.pprint(all_flights)
# pprint.pprint(results.fetchall())