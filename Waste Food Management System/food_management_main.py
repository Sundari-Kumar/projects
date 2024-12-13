import time
from food_management_system import FoodDonationSystem

def main():
    system = FoodDonationSystem()

    # Add some food items to the system
    system.add_food_item("Rice", 100)
    system.add_food_item("Wheat", 50)
    system.add_food_item("Vegetables", 30)

    while True:
        print("\nWaste Food Management and Donation System")
        print("1. View Available Food Items for Donation")
        print("2. Donate a Food Item")
        print("3. View All Food Items Status")
        print("4. Exit")
        
        choice = raw_input("Enter your choice: ")

        if choice == '1':
            system.view_available_food()
        elif choice == '2':
            try:
                food_id = int(raw_input("Enter Food Item ID to donate: "))
                system.donate_food(food_id)
            except ValueError:
                print("Invalid input. Please enter a valid Food Item ID.")
        elif choice == '3':
            system.view_food_status()
        elif choice == '4':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")
        
        time.sleep(2)  # Adding a brief pause before next action.

    system.close()

if __name__ == "__main__":
    main()
