import sqlite3
from plane_image import plane_art
from prettytable import PrettyTable


def print_menu():
    choice = input("""Please select an option:
        1 - Add New Flight
        2 - View Flights by Criteria
        3 - Update Flight Information
        4 - Assign Pilot to Flight
        5 - View Pilot Schedule
        6 - View Destination Information
        7 - Update Destination Information 
        8 - Quit\n""")
    
    return choice

def initial_menu_loop(choice):
    
    while not choice.isdigit() or (int(choice) < 1 or int(choice) > 8):
        print("Please enter a number between 1 and 8. ")
        choice = print_menu()

    if choice == "1":
        # Add New Flight
        add_new_flight(cursor, conn)
        
        pass
    elif choice == "2":
        # View Flights by Criteria
        print("You have chosen: 2 - View Flights by Criteria")
        view_flights_by_criteria(cursor)
        pass
    elif choice == "3":
        # Update Flight Information
        print("You have chosen: 3 - Update Flight Information")
        update_flight_info(cursor)
        pass
    elif choice == "4":
        # Assign Pilot to Flight
        print("You have chosen:  4 - Assign Pilot to Flight")
        assign_pilot_to_flight(cursor)
        pass
    elif choice == "5":
        # View Pilot Schedule
        print("You have chosen: 5 - View Pilot Schedule")
        view_pilot_schedule(cursor)
        pass
    elif choice == "6":
        # View Destination Information
        print("You have chosen: 6 - View Destination Information")
        view_destination_info(cursor)
    elif choice == "7":
        # Update Destination Information
        print("You have chosen: 7 - Update Destination Information")
        update_destination_info(cursor)
    elif choice == "8":
        print("You have chosen to exit. Goodbye!")
        exit()

def display_results():
    column_names = [x[0] for x in cursor.description]
    rows = cursor.fetchall()

    display_table = PrettyTable(column_names)
    for row in rows:
        display_table.add_row(row)
    print(display_table)

def add_new_flight(cursor, conn):
    # ask for each attribute
    # check correct data type had been entered
    # insert record into database
    # display full record when data entry has been completed using select statement to prove it has been entered (WHERE flight_no = x)

    print("You have chosen: 1 - Add New Flight")

    # flight_no = cursor.execute("SELECT MAX(flight_no) FROM flights").fetchall()
    # print(flight_no)
    
    # input("Please input the flight number: ")
    # do a check here to make sure the flight number is unique

    departure_date = input("Please enter a departure date in the format YYYY-MM-DD HH:MM:SS: ")
    # check date is not in the past and it is of correct format

    departure_gate = input("Please enter departure gate: ")
    # all flight are starting from the same airport so we know what the gate number would be from

    destination = input("Please enter a destination: ")
    # Need to check if this destination is in the destination table and add if not?

    arrival_date = input("Please enter an arrival date in the format YYYY-MM-DD HH:MM:SS: ")
    # check arrival date is not before departure data and that it is in the correct format
    
    arrival_gate = input("Please enter the arrival gate: ")
    # this is dependent on the destination airport

    no_passengers = input("Please enter the number of passengers: ")
    # This would depend on the type of airplane and the number of tickets booked, but we do not have these tables for simplificaiton

    captain = input("Please enter the pilot_id of the captain: ")
    # maybe display a list of available pilots
    
    first_officer = input("Please enter the pilot_id of the first officer: ")
    # maybe display list of available pilots

    # Note - all flights are initially added as on-time and not-boarding

    cursor.execute(f"""INSERT INTO flights 
                   VALUES({flight_no, departure_date, departure_gate, destination, arrival_date, arrival_gate, no_passengers, captain, first_officer}, 'on-time', 0)""")
    cursor.execute("""INSERT INTO destinations(dest_id, name, no_of_gates) 
                        VALUES(?, ?, ?)""", [11,'Josep Tarradellas Barcelona–El Prat Airport [BCN]', 23])
    cursor.execute("""SELECT * from destinations""")
    print("\nDisplaying destinations information after adding Barcelona airport:")
    display_results()
    conn.commit()
    pass
############################################################################################################################################################################################################

def view_flights_by_criteria(cursor):
    # display menu of criteria to add
    # add criteria to select statment
    # there could be a varying amount of criteria, so maybe add criteria to list, then use this list to populate select statement?
    # display result of select statment
    pass

###########################################################################################################################################################################################################

def update_flight_info(cursor):
    # ask which flight and present list of possible flight_no
    # present menu of what the person can change
    # allow one thing to be changed at once
    # go back to menu - do you want to change anything else? Y continue in this menu
    # if no, do you want to change info on another flight? Y - Present list of flight nos again
    # N - go back to main menu
    # at end display updated record
    pass
    print("\nFlight no. 1009 has been delayed: it's status and departure time will be updated")
    cursor.execute("""UPDATE flights SET departure_date = '2025-04-27 19:05', arrival_date = '2025-04-27 23:05', flight_status = 'delayed'
                    WHERE flight_no = 1009""")

    print("\nDelayed flight no 1010 has been cancelled and will be updated")
    cursor.execute("""UPDATE flights SET flight_status = 'cancelled'
                    WHERE flight_no = 1010""")

    print("\nArrival gate for flight 1008 has changed to 7 and will be updated")
    cursor.execute("""UPDATE arrival_gates SET gate_id = 7
                    WHERE flight_no = 1008""")

    conn.commit()

    print("\n\nDisplaying updated flight schedule:")
    cursor.execute("""SELECT flights.flight_no, destinations.name AS destination, flights.departure_date, flights.departure_gate, 
                        flights.arrival_date, arrival_gates.gate_id, flights.flight_status FROM flights
                        JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                        JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                        """)
    display_results()

#####################################################################################################################################################################################################

def assign_pilot_to_flight(cursor):
    # ask which pilot from presented list of pilots in table
    # ask which flight from presented list of flights in table
    # check pilot is available
    # if available, add pilot to flight and print update record
    # if not say pilot cannot be assigned and ask if they want to assign another pilot
    cursor.execute("""SELECT flights.flight_no, destinations.name AS destination, flights.departure_date, flights.arrival_date, pilots.pilot_id, 
                        pilots.first_name, pilots.last_name, pilots.rank FROM flights
                        JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                        JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                        JOIN pilots
                        WHERE (pilots.pilot_id = flights.captain OR pilots.pilot_id = flights.first_officer)
                        ORDER BY flights.flight_no, pilots.rank
                        """)
    display_results()
    flight_no = input("Which flight do you want to assign/re-assign pilot to? Enter flight number from above table: ")
    max_flight_no = cursor.execute("SELECT MAX(flight_no) FROM flights").fetchone()[0]
    
    # check user input is valid
    while not flight_no.isdigit() or (int(flight_no) < 1001 or int(flight_no) > max_flight_no):
        flight_no = input(f"Please enter a number between 1001 and {max_flight_no}: ")

    # ask which pilot from list of pilots with valid license
    # future improvement when have more time: add check that departure dates don't conflict
    cursor.execute(f"""SELECT pilot_id, first_name, last_name, rank, license_no, license_valid FROM pilots
                   WHERE  pilots.license_valid = 1""")
    print()
    display_results()
    pilot_choice = input(f"\nPlease enter the pilot_id from the table above for the pilot that you want to assign to flight {flight_no}: ")

    max_pilot_id = cursor.execute("SELECT MAX(pilot_id) FROM pilots").fetchone()[0]
    
    # check user input is valid
    # future impprovement when have more time: check entry valid as may not include all numbers from 1 - 10
    while not pilot_choice.isdigit() or (int(pilot_choice) < 1 or int(pilot_choice) > max_pilot_id):
        pilot_choice = input(f"Please enter a number between 1 and {max_pilot_id}: ")

    # get rank of chosen pilot
    pilot_rank = cursor.execute("SELECT rank FROM pilots WHERE pilot_id = ?", (pilot_choice,)).fetchone()[0]
    if pilot_rank == 'captain':
        flights_attribute = 'captain'
    else:
        flights_attribute = 'first_officer'

    # assign pilot to flight
    cursor.execute(f"""UPDATE flights SET {flights_attribute} = ? WHERE flight_no = ?""",(pilot_choice, flight_no) )
    print(f"\nFlight schedule updated for flight_no {flight_no}: ")
    cursor.execute("""SELECT flights.flight_no, destinations.name AS destination, flights.departure_date, flights.arrival_date, pilots.pilot_id, 
                        pilots.first_name, pilots.last_name, pilots.rank FROM flights
                        JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                        JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                        JOIN pilots
                        WHERE (pilots.pilot_id = flights.captain OR pilots.pilot_id = flights.first_officer) AND flights.flight_no = ?
                        """, (flight_no,))
    display_results()

    # conn.commit()

##########################################################################################################################################################################################################

def view_pilot_schedule(cursor):
     # ask which pilot from presented list of pilots with valid license in table
    cursor.execute("""SELECT pilot_id, first_name, last_name, rank, license_no, license_valid FROM pilots WHERE license_valid = 1""")
    display_results()
    pilot_choice = input("\nPlease enter the pilot_id for the pilot's schedule that you want to view: ")
    max_pilot_id = cursor.execute("SELECT MAX(pilot_id) FROM pilots").fetchone()[0]
    
    # check user input is valid
    while not pilot_choice.isdigit() or (int(pilot_choice) < 1 or int(pilot_choice) > max_pilot_id):
        pilot_choice = input(f"Please enter a number between 1 and {max_pilot_id}: ")
    print(pilot_choice)

    # get rank of chosen pilot
    pilot_rank = cursor.execute("SELECT rank FROM pilots WHERE pilot_id = ?", (pilot_choice,)).fetchone()[0]
    if pilot_rank == 'captain':
        flights_attribute = 'flights.captain'
    else:
        flights_attribute = 'flights.first_officer'

    print(f"\nDisplaying schedule for pilot with pilot_id {pilot_choice}:")
    cursor.execute(f"""SELECT pilots.pilot_id, CONCAT(pilots.first_name, ' ',pilots.last_name) AS name, flights.flight_no, destinations.name AS destination, 
               flights.departure_date, flights.departure_gate, flights.arrival_date, arrival_gates.gate_id, flights.flight_status FROM flights
                      JOIN arrival_gates ON flights.flight_no = arrival_gates.flight_no
                      JOIN destinations ON arrival_gates.dest_id = destinations.dest_id
                      JOIN pilots ON pilots.pilot_id = {flights_attribute}
                      WHERE pilots.pilot_id = ?
                      """, (pilot_choice,))
    display_results()

##########################################################################################################################################################################################################

def view_destination_info(cursor):
    print("\nDisplaying destinations information:")
    cursor.execute("""SELECT destinations.dest_id, destinations.name, destinations.dest_code,
                   addresses.street, addresses.city, addresses.postcode, addresses.country, destinations.no_of_gates FROM destinations
                   JOIN addresses ON destinations.address_id = addresses.address_id""")
    display_results()

############################################################################################################################################################################################################

def update_destination_info(cursor):
    # ask which destination is to be updated
    cursor.execute("SELECT dest_id, name, dest_code, no_of_gates FROM destinations")
    display_results()
    dest_id = input("\nWhich destination do you want update?  Enter a dest_id from the list above: ")
    max_dest_id = cursor.execute("SELECT MAX(dest_id) FROM destinations").fetchone()[0]
    
    # check user input is valid
    while not dest_id.isdigit() or (int(dest_id) < 1 or int(dest_id) > max_dest_id):
        dest_id = input(f"Please enter a number between 1 and {max_dest_id}: ")

    # display chosen destination information and ask which attribute is to be updated
    cursor.execute("SELECT dest_id, name, dest_code, no_of_gates FROM destinations WHERE dest_id = ?", (dest_id))
    print("\nSelected destination:")
    display_results()
    update_choice = input("""Which attribute do you want to update:
                          1 - Name
                          2 - destination code
                          3 - number of gates
                          Enter a number between 1 and 3: """)
    
    # check user input is valid
    while not update_choice.isdigit() or (int(update_choice) < 1 or int(update_choice) > 3):
        dest_id = input("Please enter a number between 1 and 3: ")

    dest_attributes = {'1':'name', '2':'destination code', '3': 'number of gates'}
    col_names = {'1':'name', '2':'dest_code', '3': 'no_of_gates'}

    # get information to be updated
    updated_entry = input(f"""You have chosen to update {dest_attributes[update_choice]}.  Please enter the updated information: """)

    print(f"\nUpdating {dest_attributes[update_choice]} for destination with dest_id {dest_id}:")
    cursor.execute(f"""UPDATE destinations SET {col_names[update_choice]} = ?
                WHERE dest_id = ?""", (updated_entry, dest_id))
    cursor.execute("""SELECT * from destinations""")
    print("\nDisplaying destinations information after update:")
    display_results()
    conn.commit()
            
##############################################################################################################################################################################################
# main entry point to application

if __name__ == "__main__":
    conn = sqlite3.connect('flight_management.db')
    cursor = conn.cursor()

    print(plane_art)
    print("Welcome to the Flight Management Database Application")
    choice = print_menu()
    initial_menu_loop(choice)

    response = input("would you like to return to the main menu? (y/n): ")
    while response.lower() == 'y':
        choice = print_menu()
        initial_menu_loop(choice)
        response = input("would you like to return to the main menu? (y/n): ")

    print("Exiting Flight Management Application.....")
    
    conn.close()
    