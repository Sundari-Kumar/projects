import sqlite3

class PollingSystem:
    def __init__(self):
        self.conn = sqlite3.connect('polling_system.db')
        self.cursor = self.conn.cursor()
        self._setup_db()

    def _setup_db(self):
        """ Create the tables for polling system """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS polls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL
        )""")
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS poll_options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            poll_id INTEGER,
            option_text TEXT NOT NULL,
            votes INTEGER DEFAULT 0,
            FOREIGN KEY (poll_id) REFERENCES polls(id)
        )""")
        self.conn.commit()

    def create_poll(self, question, options):
        """ Create a poll with options """
        self.cursor.execute("INSERT INTO polls (question) VALUES (?)", (question,))
        poll_id = self.cursor.lastrowid

        for option in options:
            self.cursor.execute("INSERT INTO poll_options (poll_id, option_text) VALUES (?, ?)", (poll_id, option))
        
        self.conn.commit()

    def vote(self, poll_id, option_id):
        """ Cast a vote for a specific option in a poll """
        self.cursor.execute("SELECT votes FROM poll_options WHERE id = ?", (option_id,))
        result = self.cursor.fetchone()
        if result:
            new_vote_count = result[0] + 1
            self.cursor.execute("UPDATE poll_options SET votes = ? WHERE id = ?", (new_vote_count, option_id))
            self.conn.commit()
            print("Vote successfully casted!")
        else:
            print("Invalid option ID!")

    def view_poll_results(self, poll_id):
        """ View the results of a poll with percentages """
        self.cursor.execute("""
        SELECT option_text, votes FROM poll_options WHERE poll_id = ?""", (poll_id,))
        options = self.cursor.fetchall()

        total_votes = sum([votes for _, votes in options])

        print("\nPoll Results:")
        for option_text, votes in options:
            percentage = (votes / float(total_votes)) * 100 if total_votes > 0 else 0
            print("{0}: {1} votes ({2:.2f}%)".format(option_text, votes, percentage))

    def get_poll(self, poll_id):
        """ Fetch a poll and its options """
        self.cursor.execute("SELECT question FROM polls WHERE id = ?", (poll_id,))
        question = self.cursor.fetchone()
        
        if question:
            print("\nPoll: {0}".format(question[0]))
            self.cursor.execute("""
            SELECT id, option_text FROM poll_options WHERE poll_id = ?""", (poll_id,))
            options = self.cursor.fetchall()
            for option_id, option_text in options:
                print("{0}. {1}".format(option_id, option_text))
        else:
            print("Poll not found!")

    def close(self):
        """ Close the database connection """
        self.conn.close()


def main():
    system = PollingSystem()

    # Create a new poll
    system.create_poll("What is your favorite programming language?", ["Python", "Java", "Ruby", "C++"])

    while True:
        print("\nMenu:")
        print("1. Vote on the poll")
        print("2. View poll results")
        print("3. Exit")

        choice = raw_input("Enter your choice (1/2/3): ")

        if choice == "1":
            poll_id = 1  # In this case, we have a single poll, but you can modify to handle multiple polls
            system.get_poll(poll_id)
            option_id = int(raw_input("Enter the option number you want to vote for: "))
            system.vote(poll_id, option_id)

        elif choice == "2":
            poll_id = 1  # Same as above
            system.view_poll_results(poll_id)

        elif choice == "3":
            print("Exiting system.")
            break

        else:
            print("Invalid choice. Please try again.")

    system.close()

if __name__ == "__main__":
    main()
