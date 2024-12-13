from atm_system import ATMSystem

def main():
    atm = ATMSystem()
    
    # Uncomment to add new user (this would normally be a one-time action)
    # atm.add_user("Alice", "f12345", 1000)
    
    user = atm.authenticate_user()
    if user:
        while True:
            print("\nATM Menu:")
            print("1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Exit")
            choice = raw_input("Enter choice: ")

            if choice == "1":
                atm.check_balance(user)
            elif choice == "2":
                amount = float(raw_input("Enter amount to deposit: $"))
                atm.deposit(user, amount)
            elif choice == "3":
                amount = float(raw_input("Enter amount to withdraw: $"))
                atm.withdraw(user, amount)
            elif choice == "4":
                print("Exiting ATM system.")
                break
            else:
                print("Invalid choice. Please try again.")

    atm.close()

if __name__ == '__main__':
    main()
