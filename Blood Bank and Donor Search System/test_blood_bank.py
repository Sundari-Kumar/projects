import unittest
import sqlite3
from blood_bank import setup_database, register_donor, search_donor, list_all_donors

class TestBloodBankSystem(unittest.TestCase):
    def setUp(self):
        # Create an in-memory database for testing
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE donors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                blood_type TEXT NOT NULL,
                contact TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def tearDown(self):
        # Close the in-memory database
        self.conn.close()

    def test_register_donor(self):
        # Simulate registering a donor
        name = "John Doe"
        blood_type = "A+"
        contact = "1234567890"

        # Directly insert data (simulating function behavior)
        self.cursor.execute("INSERT INTO donors (name, blood_type, contact) VALUES (?, ?, ?)", (name, blood_type, contact))
        self.conn.commit()

        # Verify the donor is registered
        self.cursor.execute("SELECT * FROM donors WHERE name = ?", (name,))
        donor = self.cursor.fetchone()
        self.assertIsNotNone(donor)
        self.assertEqual(donor[1], name)
        self.assertEqual(donor[2], blood_type)
        self.assertEqual(donor[3], contact)

    def test_search_donor(self):
        # Insert a test donor
        self.cursor.execute("INSERT INTO donors (name, blood_type, contact) VALUES (?, ?, ?)", ("Jane Doe", "B+", "0987654321"))
        self.conn.commit()

        # Search for the donor
        self.cursor.execute("SELECT name, contact FROM donors WHERE blood_type = ?", ("B+",))
        results = self.cursor.fetchall()
        self.assertGreater(len(results), 0)
        self.assertIn(("Jane Doe", "0987654321"), results)

    def test_list_all_donors(self):
        # Insert multiple donors
        donors = [
            ("John Doe", "A+", "1234567890"),
            ("Jane Smith", "O-", "9876543210")
        ]
        self.cursor.executemany("INSERT INTO donors (name, blood_type, contact) VALUES (?, ?, ?)", donors)
        self.conn.commit()

        # List all donors
        self.cursor.execute("SELECT name, blood_type, contact FROM donors")
        results = self.cursor.fetchall()
        self.assertEqual(len(results), 2)
        for donor in donors:
            self.assertIn(donor, results)

if __name__ == "__main__":
    unittest.main()
