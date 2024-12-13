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
        print("Poll created successfully!")

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

        print("Poll Results:")
        for option_text, votes in options:
            percentage = (votes / float(total_votes)) * 100 if total_votes > 0 else 0
            print(f"{option_text}: {votes} votes ({percentage:.2f}%)")

    def get_poll(self, poll_id):
        """ Fetch a poll and its options """
        self.cursor.execute("SELECT question FROM polls WHERE id = ?", (poll_id,))
        question = self.cursor.fetchone()
        
        if question:
            print(f"Poll: {question[0]}")
            self.cursor.execute("""
            SELECT id, option_text FROM poll_options WHERE poll_id = ?""", (poll_id,))
            options = self.cursor.fetchall()
            for option_id, option_text in options:
                print(f"{option_id}. {option_text}")
        else:
            print("Poll not found!")

    def close(self):
        """ Close the database connection """
        self.conn.close()
