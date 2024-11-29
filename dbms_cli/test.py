import unittest
import sqlite3
import commands


class TestBMS(unittest.TestCase):

    def setUp(self):
        """
        Setup the connection to the existing banquetDatabase.db.
        """
        self.connection = sqlite3.connect("banquetDatabase.db")
        self.cursor = self.connection.cursor()

    def tearDown(self):
        """
        Close the database connection after each test.
        """
        self.cursor.close()
        self.connection.close()

    def test_createNewBanquet(self):
        """
        Test creating a new banquet.
        """
        banquet_id = 100
        commands.createNewBanquet(
            banquet_id, "testbanquet", "2024-12-25_18:00", "TestAddress", "TestLocation", 50, 1,
            "TestFirstName", "TestLastName", "TestRemarks", self.connection, self.cursor
        )
        self.cursor.execute(f"SELECT * FROM Banquet WHERE banquetID = {banquet_id}")
        banquet = self.cursor.fetchone()
        self.assertIsNotNone(banquet)
        self.assertEqual(banquet[1], "testbanquet")
        self.assertEqual(banquet[5], 50)
        self.cursor.execute(f"DELETE FROM Banquet WHERE banquetID = {banquet_id}")
        self.connection.commit()

    def test_deleteBanquet(self):
        banquet_id = 100
        self.cursor.execute(
            f"INSERT INTO Banquet (banquetID, name, dateTime, address, location, quota, available, firstNameOfContactStaff, lastNameOfContactStaff, remarks) "
            f"VALUES ({banquet_id}, 'deletebanquet', '2024-12-25_18:00', 'TestAddress', 'TestLocation', 50, 1, 'FirstName', 'LastName', 'Remarks')"
        )
        self.connection.commit()
        commands.deleteBanquet(banquet_id, self.connection, self.cursor)
        self.cursor.execute(f"SELECT * FROM Banquet WHERE banquetID = {banquet_id}")
        banquet = self.cursor.fetchone()
        self.assertIsNone(banquet)

    def test_editBanquet(self):
        banquet_id = 10003
        self.cursor.execute(
            f"INSERT INTO Banquet (banquetID, name, dateTime, address, location, quota, available, firstNameOfContactStaff, lastNameOfContactStaff, remarks) "
            f"VALUES ({banquet_id}, 'editbanquet', '2024-12-25_18:00', 'TestAddress', 'TestLocation', 50, 1, 'FirstName', 'LastName', 'Remarks')"
        )
        self.connection.commit()
        commands.editBanquet(banquet_id, "name", "updatedbanquet", self.connection, self.cursor)
        self.cursor.execute(f"SELECT name FROM Banquet WHERE banquetID = {banquet_id}")
        banquet_name = self.cursor.fetchone()[0]
        self.assertEqual(banquet_name, "updatedbanquet")
        self.cursor.execute(f"DELETE FROM Banquet WHERE banquetID = {banquet_id}")
        self.connection.commit()

    def test_printAttendee(self):
        email = "test@example.com"
        self.cursor.execute(f"DELETE FROM Attendee WHERE emailAddress = '{email}'")
        self.connection.commit()
        self.cursor.execute(
            f"INSERT INTO Attendee (emailAddress, firstName, lastName, address, password, mobileNumber, type, affiliatedOrganization) "
            f"VALUES ('{email}', 'Firstname', 'Lastname', 'TestAddress', 'password', 12345678, 'staff', 'PolyU')"
        )
        self.connection.commit()
        commands.printAttendee(email, self.cursor)
        self.cursor.execute(f"DELETE FROM Attendee WHERE emailAddress = '{email}'")
        self.connection.commit()

    def test_editAttendee(self):
        email = "testedit@example.com"
        self.cursor.execute(f"DELETE FROM Attendee WHERE emailAddress = '{email}'")
        self.connection.commit()
        self.cursor.execute(
            f"INSERT INTO Attendee (emailAddress, firstName, lastName, address, password, mobileNumber, type, affiliatedOrganization) "
            f"VALUES ('{email}', 'Firstname', 'Lastname', 'TestAddress', 'password', 12345678, 'staff', 'PolyU')"
        )
        self.connection.commit()
        commands.adminEditAttendee(email, "lastName", "UpdatedLastname", self.connection, self.cursor)
        self.cursor.execute(f"SELECT lastName FROM Attendee WHERE emailAddress = '{email}'")
        last_name = self.cursor.fetchone()[0]
        self.assertEqual(last_name, "UpdatedLastname")
        self.cursor.execute(f"DELETE FROM Attendee WHERE emailAddress = '{email}'")
        self.connection.commit()

    def test_generateReport(self):
        commands.generateReport(self.connection, self.cursor)


if __name__ == "__main__":
    unittest.main()
