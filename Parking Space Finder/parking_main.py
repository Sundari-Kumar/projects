import time
from parking_system import ParkingSystem

def main():
    system = ParkingSystem()

    # Add some parking spaces to the system
    system.add_parking_space("Car")
    system.add_parking_space("Truck")
    system.add_parking_space("Motorcycle")
    
    while True:
        print("\nParking System")
        print("1. View Available Parking Spaces")
        print("2. Book a Parking Space")
        print("3. View All Parking Spaces Status")
        print("4. Exit")
        
        choice = raw_input("Enter your choice: ")

        if choice == '1':
            system.view_available_spaces()
        elif choice == '2':
            try:
                space_id = int(raw_input("Enter Parking Space ID to book: "))
                system.book_parking_space(space_id)
            except ValueError:
                print("Invalid input. Please enter a valid Parking Space ID.")
        elif choice == '3':
            system.view_parking_status()
        elif choice == '4':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")
        
        time.sleep(2)  # Adding a brief pause before next action.

    system.close()

if __name__ == "__main__":
    main()
