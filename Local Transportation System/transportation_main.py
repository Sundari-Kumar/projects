from transportation_system import TransportationSystem

def main():
    system = TransportationSystem()

    while True:
        print("\nLocal Transportation System Menu:")
        print("1. Add Vehicle")
        print("2. Update Vehicle")
        print("3. Delete Vehicle")
        print("4. Search Vehicle")
        print("5. Exit")
        
        choice = raw_input("Enter your choice: ")

        if choice == "1":
            vehicle_number = raw_input("Enter vehicle number: ")
            vehicle_type = raw_input("Enter vehicle type: ")
            location = raw_input("Enter vehicle location: ")
            status = raw_input("Enter vehicle status (e.g., available, in-use): ")
            system.add_vehicle(vehicle_number, vehicle_type, location, status)

        elif choice == "2":
            vehicle_number = raw_input("Enter vehicle number to update: ")
            vehicle_type = raw_input("Enter new vehicle type (or press Enter to skip): ")
            location = raw_input("Enter new location (or press Enter to skip): ")
            status = raw_input("Enter new status (or press Enter to skip): ")
            system.update_vehicle(vehicle_number, vehicle_type, location, status)

        elif choice == "3":
            vehicle_number = raw_input("Enter vehicle number to delete: ")
            system.delete_vehicle(vehicle_number)

        elif choice == "4":
            vehicle_number = raw_input("Enter vehicle number (or press Enter to skip): ")
            vehicle_type = raw_input("Enter vehicle type (or press Enter to skip): ")
            location = raw_input("Enter vehicle location (or press Enter to skip): ")
            system.search_vehicle(vehicle_number, vehicle_type, location)

        elif choice == "5":
            print("Exiting system.")
            break

        else:
            print("Invalid choice. Please try again.")

    system.close()

if __name__ == "__main__":
    main()
