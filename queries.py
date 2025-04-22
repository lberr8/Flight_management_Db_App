import sqlite3
from prettytable import PrettyTable

conn = sqlite3.connect('flight_management.db')
cursor = conn.cursor()

def display_results():
    column_names = [x[0] for x in cursor.description]
    rows = cursor.fetchall()

    display_table = PrettyTable(column_names)
    for row in rows:
        display_table.add_row(row)
    print(display_table)

###	Flight Retrieval: Retrieve flights based on multiple criteria, such as destination, status, or departure date.

print("\nDisplaying information for all flights that with a status of 'on-time'")
cursor.execute("SELECT * FROM flights WHERE flight_status = 'on-time' ORDER BY departure_date")
display_results()

print("\nDisplaying information for all flights that with a departure date of 2025-04-25")
cursor.execute("SELECT * FROM flights WHERE departure_date LIKE '2025-04-25%'")
display_results()

print("\nDisplaying information for flights where destination is LA")
cursor.execute("""SELECT flights.flight_no, destinations.name, flights.departure_date, flights.arrival_date FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      WHERE destinations.name LIKE '%LAX%'""")
display_results()


print("\nDisplaying information for flights where destination is LA, flight status is on-time that depart before 25/04/2025")
cursor.execute("""SELECT flights.flight_no, destinations.name, flights.departure_date, flights.arrival_date, flights.flight_status FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      WHERE destinations.name LIKE '%LAX%' AND flights.flight_status = 'on-time' AND flights.departure_date < '2025-04-25'""")
display_results()

### Schedule Modification: Update flight schedules (e.g., change departure time or status)
print("\nDisplaying information for flight schedule before change")
cursor.execute("""SELECT flights.flight_no, destinations.name AS destination, flights.departure_date, flights.departure_gate, flights.arrival_date, arrival_gates.gate_id, flights.flight_status FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      """)
display_results()

print("\nFlight no. 1009 has been delayed: it's status and departure time will be updated")
cursor.execute("""UPDATE flights SET departure_date = '2025-04-27 19:05', arrival_date = '2025-04-27 23:05', flight_status = 'delayed'
                  WHERE flight_no = 1009""")

print("\nDelayed flight no 1010 has been cancelled and will be updated")
cursor.execute("""UPDATE flights SET flight_status = 'cancelled'
                  WHERE flight_no = 1010""")

print("\nDeparture gate for flight 1008 has changed to 7 and will be updated")
cursor.execute("""UPDATE arrival_gates SET gate_id = 7
                  WHERE flight_no = 1008""")

conn.commit()

print("\n\nDisplaying updated flight schedule:")
cursor.execute("""SELECT flights.flight_no, destinations.name AS destination, flights.departure_date, flights.departure_gate, flights.arrival_date, arrival_gates.gate_id, flights.flight_status FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      """)
display_results()




###	Pilot Assignment: Assign pilots to flights and retrieve information about pilot schedules.
# SELECT destinations.dest_id, destinations.name, 
# SELECT pilots.pilot_id, pilots.first_name, pilots.last_name, flights.flight_no FROM flights, pilots
cursor.execute("""SELECT pilots.pilot_id, pilots.first_name, pilots.last_name, flights.flight_no, destinations.name AS destination, flights.departure_date, flights.departure_gate, flights.arrival_date, arrival_gates.gate_id, flights.flight_status FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      JOIN pilots
                      WHERE pilots.pilot_id = flights.captain OR pilots.pilot_id = flights.first_officer
                      ORDER BY pilots.pilot_id
                      """)
print("\nDisplaying pilot schedule:")
display_results()
###	Destination Management: View and update destination information as required.
# REMOVE DESTINATION TO SHOW DELETION?




### Include additional queries that summarise data, such as the number of flights to each destination or the number of flights assigned to a pilot.

cursor.execute("""SELECT destinations.name AS destination, COUNT(arrival_gates.flight_no) AS 'number of flights' FROM arrival_gates
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      GROUP BY destinations.name
                      """)
print("\nDisplaying number of flights to each destination:")
display_results()

# number of flights assigned to a pilot
cursor.execute("""SELECT pilots.pilot_id, CONCAT(pilots.first_name,' ', pilots.last_name) AS name, pilots.rank, COUNT(flights.flight_no) AS 'number of flights' FROM pilots
                      JOIN flights
                      WHERE pilots.pilot_id = flights.captain OR pilots.pilot_id = flights.first_officer
                      GROUP BY pilots.pilot_id
                      """)
print("\nDisplaying number of flights to assigned to a pilot:")
display_results()