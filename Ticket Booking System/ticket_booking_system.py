import sqlite3

class TicketBookingSystem:
    def __init__(self):
        # Initialize the database connection
        self.conn = sqlite3.connect("ticket_booking.db")
        self.cursor = self.conn.cursor()

        # Create the events table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT NOT NULL,
                available_seats INTEGER NOT NULL,
                ticket_price REAL NOT NULL
            )
        """)
        self.conn.commit()

    def add_event(self, event_name, available_seats, ticket_price):
        # Add an event to the database
        self.cursor.execute("""
            INSERT INTO events (event_name, available_seats, ticket_price)
            VALUES (?, ?, ?)
        """, (event_name, available_seats, ticket_price))
        self.conn.commit()

    def view_events(self):
        # Display all events in the database
        self.cursor.execute("SELECT * FROM events")
        events = self.cursor.fetchall()
        if events:
            for event in events:
                print("ID: {}, Name: {}, Available Seats: {}, Ticket Price: ${}".format(
                    event[0], event[1], event[2], event[3]
                ))
        else:
            print("No events available.")

    def book_ticket(self, event_id, num_tickets):
        # Book tickets for an event if enough available seats
        self.cursor.execute("SELECT available_seats FROM events WHERE event_id = ?", (event_id,))
        result = self.cursor.fetchone()
        if result:
            available_seats = result[0]
            if num_tickets <= available_seats:
                new_seats = available_seats - num_tickets
                self.cursor.execute("""
                    UPDATE events SET available_seats = ? WHERE event_id = ?
                """, (new_seats, event_id))
                self.conn.commit()
                print("{} tickets successfully booked!".format(num_tickets))
            else:
                print("Not enough available seats for this event.")
        else:
            print("Event not found.")

    def process_payment(self, amount):
        # Simulate payment processing
        print("Processing payment of ${}...".format(amount))
        return True  # Simulating a successful payment

    def close(self):
        # Close the database connection
        self.conn.close()


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
