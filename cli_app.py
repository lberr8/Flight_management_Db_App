from plane_image import plane_art

print(plane_art)
print("Welcome to the Flight Management Database Application")

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
        pass
    elif choice == "3":
        # Update Flight Information
        print("You have chosen: 3 - Update Flight Information")
        pass
    elif choice == "4":
        # Assign Pilot to Flight
        print("You have chosen:  4 - Assign Pilot to Flight")
        pass
    elif choice == "5":
        # View Pilot Schedule
        print("You have chosen: 5 - View Pilot Schedule")
        pass
    elif choice == "6":
        # View Destination Information
        print("You have chosen: 6 - View Destination Information")
        pass
    elif choice == "7":
        # Update Destination Information
        print("You have chosen: 7 - Update Destination Information")
        pass
    elif choice == "8":
        print("You have chosen to exit. Goodbye!")
        exit()


choice = print_menu()
initial_menu_loop(choice)

def add_new_flight(cursor, conn):
    # ask for each attribute
    # check correct data type had been entered
    # insert record into database
    # display full record when data entry has been completed using select statement to prove it has been entered (WHERE flight_no = x)

    print("You have chosen: 1 - Add New Flight")

    flight_no = input("Please input the flight number: ")
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

    cursor.execute(f"INSERT INTO flights VALUES({flight_no, departure_date, departure_gate, destination, arrival_date, arrival_gate, no_passengers, captain, first_officer}, 'on-time', 0)")
    
    pass

def view_flights_by_criteria():
    # display menu of criteria to add
    # add criteria to select statment
    # there could be a varying amount of criteria, so maybe add criteria to list, then use this list to populate select statement?
    # display result of select statment
    pass

def update_flight_info():
    # ask which flight and present list of possible flight_no
    # present menu of what the person can change
    # allow one thing to be changed at once
    # go back to menu - do you want to change anything else? Y continue in this menu
    # if no, do you want to change info on another flight? Y - Present list of flight nos again
    # N - go back to main menu
    # at end display updated record
    pass

def assign_pilot_to_flight():
    # ask which pilot from presented list of pilots in table
    # ask which flight from presented list of flights in table
    # check pilot is available
    # if available, add pilot to flight and print update record
    # if not say pilot cannot be assigned and ask if they want to assign another pilot
    pass

def view_pilot_schedule():
     # ask which pilot from presented list of pilots in table
     # display pilot_id, flight_no, flight_dest, departure_date and arrival_date and times
    pass

def view_destination_info():
    # ask which destination from list of valid desitination ids or if want all to be displayed
    pass

def update_destination_info():
    # ask which destination from list
    # add destination as an option?
    # present menu of destination fields that can be modified
    # check type
    # similar flow to update flight above
    pass