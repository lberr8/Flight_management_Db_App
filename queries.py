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

### SQL queries for part 2 of the coursework
###	1. Flight Retrieval: Retrieve flights based on multiple criteria, such as destination, status, or departure date.
### a. status = on-time

print("\nDisplaying information for all flights that with a status of 'on-time'")
cursor.execute("SELECT * FROM flights WHERE flight_status = 'on-time' ORDER BY departure_date")
display_results()

### b. departure date
print("\nDisplaying information for all flights that with a departure date of 2025-04-25")
cursor.execute("SELECT * FROM flights WHERE departure_date LIKE '2025-04-25%'")
display_results()

### c. destination
print("\nDisplaying information for flights where destination is LA")
cursor.execute("""SELECT flights.flight_no, destinations.name, flights.departure_date, flights.arrival_date FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      WHERE destinations.name LIKE '%LAX%'""")
display_results()

### d. multiple criteria at once: destination, flight status and departure date
print("\nDisplaying information for flights where destination is LA, flight status is on-time that depart before 25/04/2025")
cursor.execute("""SELECT flights.flight_no, destinations.name, flights.departure_date, flights.arrival_date, flights.flight_status FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      WHERE destinations.name LIKE '%LAX%' AND flights.flight_status = 'on-time' AND flights.departure_date < '2025-04-25'""")
display_results()

################################################################################################################################################################################################################

### 2. Schedule Modification: Update flight schedules (e.g., change departure time or status)

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

#####################################################################################################################################################################################################################################################################

###	3. Pilot Assignment: Assign pilots to flights and retrieve information about pilot schedules.
### a. Assign pilots to flights
print("\nDisplaying pilot information before change:")
cursor.execute("""SELECT flights.flight_no, destinations.name AS destination, flights.departure_date, flights.arrival_date, pilots.pilot_id, pilots.first_name, pilots.last_name, pilots.rank FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      JOIN pilots
                      WHERE pilots.pilot_id = flights.captain OR pilots.pilot_id = flights.first_officer
                      ORDER BY flights.flight_no
                      """)
display_results()

print("\nPilots with pilot_id 3 and pilot_id 6 have had their licenses renewed and can now be assigned to flight 1008")
cursor.execute("""UPDATE pilots SET license_valid = 1
                  WHERE pilot_id = 3""")
cursor.execute("""UPDATE pilots SET license_valid = 1
                  WHERE pilot_id = 6""")
print("\nPilots' licenses updated: ")
cursor.execute("""SELECT pilot_id, first_name, last_name, license_no, license_valid, rank FROM pilots""")
display_results()

cursor.execute("""UPDATE flights SET captain = 3, first_officer = 6
                  WHERE flight_no = 1008""")
print("\nFlight schedule updated for flight_no 1008: ")
cursor.execute("""SELECT flights.flight_no, destinations.name AS destination, flights.departure_date, flights.arrival_date, pilots.pilot_id, pilots.first_name, pilots.last_name, pilots.rank FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      JOIN pilots
                      WHERE (pilots.pilot_id = flights.captain OR pilots.pilot_id = flights.first_officer) AND flights.flight_no = 1008
                      ORDER BY flights.flight_no
                      """)
display_results()

conn.commit()

### bi. Retrieve information about pilot schedules (all ranks)
cursor.execute("""SELECT pilots.pilot_id, pilots.first_name, pilots.last_name, flights.flight_no, destinations.name AS destination, flights.departure_date, flights.departure_gate, flights.arrival_date, arrival_gates.gate_id, flights.flight_status FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      JOIN pilots
                      WHERE pilots.pilot_id = flights.captain OR pilots.pilot_id = flights.first_officer
                      ORDER BY pilots.pilot_id
                      """)
print("\nDisplaying flight schedules for all pilots:")
display_results()

### bii. Retrieve information about pilot schedules (captains only)
cursor.execute("""SELECT pilots.pilot_id, pilots.first_name, pilots.last_name, flights.flight_no, destinations.name AS destination, flights.departure_date, flights.departure_gate, flights.arrival_date, arrival_gates.gate_id, flights.flight_status FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      JOIN pilots ON pilots.pilot_id = flights.captain
                      ORDER BY pilots.pilot_id
                      """)
print("\nDisplaying flight schedules for captains:")
display_results()

### biii. Retrieve information about pilot schedules (first officer only)
cursor.execute("""SELECT pilots.pilot_id, pilots.first_name, pilots.last_name, flights.flight_no, destinations.name AS destination, flights.departure_date, flights.departure_gate, flights.arrival_date, arrival_gates.gate_id, flights.flight_status FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      JOIN pilots ON pilots.pilot_id = flights.first_officer
                      ORDER BY pilots.pilot_id
                      """)
print("\nDisplaying flight schedules for first officers:")
display_results()

### biv. Retrieve information about a pilot schedule by name
cursor.execute("""SELECT pilots.pilot_id, CONCAT(pilots.first_name, ' ',pilots.last_name) AS name, flights.flight_no, destinations.name AS destination, flights.departure_date, flights.departure_gate, flights.arrival_date, arrival_gates.gate_id, flights.flight_status FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      JOIN pilots ON pilots.pilot_id = flights.captain
                      WHERE pilots.first_name = 'Sophie' AND pilots.last_name = 'Turner'
                      """)
print("\nDisplaying flight schedule for pilot Sarah Turner:")
display_results()

############################################################################################################################################################################################################################################################################################
###	4. Destination Management: View and update destination information as required.

### a. view destination information
print("\nDisplaying destinations information:")
cursor.execute("""SELECT * from destinations""")
display_results()

### b. update destination information
### bi. update number of gates for dest_id 3 and correct display error in name
print("\nUpdating airport name and number of gates for destination with dest_id 3:")
cursor.execute("""UPDATE destinations SET no_of_gates = 32, name = 'Hartsfield-Jackson Atlanta International Airport (ATL)'
               WHERE dest_id = 3""")
cursor.execute("""SELECT * from destinations""")
print("\nDisplaying destinations information after update:")
display_results()
conn.commit()

### bii. add new destination, then delete it
cursor.execute("""INSERT INTO destinations(dest_id, name, no_of_gates) 
                        VALUES(?, ?, ?)""", [11,'Josep Tarradellas Barcelona–El Prat Airport [BCN]', 23])
cursor.execute("""SELECT * from destinations""")
print("\nDisplaying destinations information after adding Barcelona airport:")
display_results()
conn.commit()

cursor.execute("DELETE FROM destinations WHERE dest_id = 11")
cursor.execute("""SELECT * from destinations""")
print("\nDisplaying destinations information after removing Barcelona airport:")
display_results()
conn.commit()


###############################################################################################################################################################################################################################################################################################
### 5. Include additional queries that summarise data, such as the number of flights to each destination or the number of flights assigned to a pilot.
### a. summarising the number of flights to each destination
cursor.execute("""SELECT destinations.name AS destination, COUNT(arrival_gates.flight_no) AS 'number of flights' FROM arrival_gates
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      GROUP BY destinations.name
                      """)
print("\nDisplaying number of flights to each destination:")
display_results()

## b. summarising the number of flights assigned to a pilot
cursor.execute("""SELECT pilots.pilot_id, CONCAT(pilots.first_name,' ', pilots.last_name) AS name, pilots.rank, COUNT(flights.flight_no) AS 'number of flights' FROM pilots
                      JOIN flights
                      WHERE pilots.pilot_id = flights.captain OR pilots.pilot_id = flights.first_officer
                      GROUP BY pilots.pilot_id
                      """)
print("\nDisplaying number of flights to assigned to a pilot:")
display_results()

