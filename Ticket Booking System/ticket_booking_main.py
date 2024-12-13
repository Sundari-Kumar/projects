from ticket_booking_system import TicketBookingSystem

def main():
    system = TicketBookingSystem()

    while True:
        print("\nTicket Booking System Menu:")
        print("1. Add Event")
        print("2. View Events")
        print("3. Book Ticket")
        print("4. Exit")
        
        choice = raw_input("Enter your choice: ")

        if choice == "1":
            event_name = raw_input("Enter event name: ")
            available_seats = int(raw_input("Enter available seats: "))
            ticket_price = float(raw_input("Enter ticket price: "))
            system.add_event(event_name, available_seats, ticket_price)

        elif choice == "2":
            system.view_events()

        elif choice == "3":
            system.view_events()  # Display available events
            event_id = int(raw_input("Enter event ID to book tickets: "))
            num_tickets = int(raw_input("Enter number of tickets to book: "))
            system.book_ticket(event_id, num_tickets)

        elif choice == "4":
            print("Exiting system.")
            break

        else:
            print("Invalid choice. Please try again.")

    system.close()

if __name__ == "__main__":
    main()
