import sqlite3
import datetime

def adminLogin(username: str, password: str) -> bool:
    try:
        if username == "admin" and password == "admin":
            print("\nLogin successful.")
            return True
        else:
            print("\nLogin failed. Invalid username or password.")
            return False
    except Exception as e:
        print("Error:", e)
        return False
    
def userLogin(emailAddress: str, password: str, sqliteConnection, cursor) -> bool:
    try:
        cursor.execute(f"SELECT * FROM Attendee WHERE EmailAddress = '{emailAddress}' AND Password = '{password}'")
        if cursor.fetchone() is not None:
            print("\nLogin successful.")
            return True
        else:
            print("\nLogin failed. Invalid email address or password.")
            return False
    except sqlite3.Error as e:
        print("Error:", e)
        return False
    
def createNewBanquet(id: int, name: str, date: str, address: str, location: str, quota: int, available: int, first_name: str, last_name: str, remarks, sqliteConnection, cursor):
    try:
        cursor.execute("INSERT INTO Banquet VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (id, name, date, address, location, quota, available, first_name, last_name, remarks))
        sqliteConnection.commit()
        print(f"\nCreated a new banquet. ID: {id}, Name: {name}")
    except sqlite3.Error as e:
        if None in (id, name, date, address, location, quota, available, first_name, last_name):
            print("\nValue of all arguments (except remarks) must not be None.")
        if available not in (0, 1):
            print("\nValue of 'available' must be 0 (false) or 1 (true).")
        if not isValidDate(date):
            print("\nIncorrect format for date. Correct format: YYYY-MM-DD_HH:MM")
        print("\nError:", e)
        
def deleteBanquet(id: int, sqliteConnection, cursor):
    try:
        cursor.execute(f"DELETE FROM Banquet WHERE BanquetID = {id}")
        sqliteConnection.commit()
        print(f"\nDeleted banquet with ID {id}")
    except sqlite3.Error as e:
        print("\nError:", e)
        
def editBanquet(banquetID: int, attributeName: str, newValue, sqliteConnection, cursor):
    try:
        cursor.execute(f"UPDATE Banquet SET {attributeName} = '{newValue}' WHERE BanquetID = {banquetID}")
        sqliteConnection.commit()
        print(f"\nUpdated banquet {banquetID} {attributeName} to {newValue}")
    except sqlite3.Error as e:
        if attributeName not in ("BanquetID", "Name", "DateTime", "Address", "Location", "Quota", "Available", "FirstNameofContactStaff", "LastNameofContactStaff", "Remarks"):
            print("\nInvalid attribute name.")
        if attributeName == "Available" and newValue not in (0, 1):
            print("\nValue of 'available' must be 0 (false) or 1 (true).")
        if attributeName == "DateTime" and not isValidDate(newValue):
            print("\nIncorrect format for date. Correct format: YYYY-MM-DD_HH:MM")
        print("\nError:", e)
        
def printBanquet(cursor):
    try: 
        cursor.execute("SELECT * FROM Banquet")
        print("\nList of banquets: ")
        all_rows = cursor.fetchall()
        for row in all_rows:
            print(row)
    except sqlite3.Error as e:
        print("\nError:", e)
        
def createMeal(banquetID: int, dishName: str, dishType: str, price: float, specialCuisine: str, sqliteConnection, cursor):
    try:
        cursor.execute("INSERT INTO Meal VALUES (?, ?, ?, ?, ?)",
                       (banquetID, dishName, dishType, price, specialCuisine))
        sqliteConnection.commit()
        print(f"\nCreated a new meal. Banquet ID: {banquetID}, Dish Name: {dishName}")
    except sqlite3.Error as e:
        if None in (banquetID, dishName, dishType, price, specialCuisine):
            print("\nValue of all arguments must not be None.")
        if dishType not in ("fish", "chicken", "beef", "vegetarian"):
            print("\nValue of 'disType' must be 'appetizer', 'main course', or 'dessert'.")
        print("\nError:", e)
        
def createAttendee(emailAddress: str, firstName: str, lastName: str, address: str,  password: str, attendeeType: str, mobileNumber: int, affiliatedOrganization: str, sqliteConnection, cursor):
    try:
        cursor.execute("INSERT INTO Attendee VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (emailAddress, firstName, lastName, address, password, attendeeType, mobileNumber, affiliatedOrganization))
        sqliteConnection.commit()
        print(f"\nCreated a new user account. ID: {emailAddress}, Name: {firstName} {lastName}")
    except sqlite3.Error as e:
        if None in (emailAddress, firstName, lastName, address, password, attendeeType, mobileNumber, affiliatedOrganization):
            print("\nValue of all arguments (except remarks) must not be None.")
        if emailAddress.count("@") != 1:
            print("\nInvalid email address.")
        if mobileNumber != 8:
            print("\nMobile number must be 8 digits.")
        if firstName.isnumeric() or lastName.isnumeric():
            print("\nFirst name and last name must not be numeric.")
        if attendeeType not in ("staff", "student", "alumni", "guest"):
            print("\nValue of 'attendeeType' must be 'staff', 'student', 'alumni', or 'guest'.")
        if affiliatedOrganization not in ("PolyU", "SPEED", "HKCC", "Others"):
            print("\nValue of 'affiliatedOrganization' must be 'PolyU', 'SPEED', 'HKCC', or 'Others'.")
        print("\nError:", e)
        
def adminEditAttendee(emailAddress: str, attributeName: str, newValue, sqliteConnection, cursor):
    try:
        cursor.execute(f"UPDATE Attendee SET {attributeName} = '{newValue}' WHERE EmailAddress = '{emailAddress}'")
        sqliteConnection.commit()
        print(f"\nUpdated attendee {emailAddress} {attributeName} to {newValue}")
    except sqlite3.Error as e:
        if attributeName not in ("EmailAddress", "FirstName", "LastName", "Address", "Password", "AttendeeType", "MobileNumber", "AffiliatedOrganization"):
            print("\nInvalid attribute name.")
        if attributeName == "MobileNumber" and newValue != 8 and not newValue.isnumeric():
            print("\nMobile number must be 8 digits.")
        if attributeName == "EmailAddress" and newValue.count("@") != 1:
            print("\nInvalid email address.")
        if attributeName == "AttendeeType" and newValue not in ("staff", "student", "alumni", "guest"):
            print("\nValue of 'attendeeType' must be 'staff', 'student', 'alumni', or 'guest'.")
        if attributeName == "AffiliatedOrganization" and newValue not in ("PolyU", "SPEED", "HKCC", "Others"):
            print("\nValue of 'affiliatedOrganization' must be 'PolyU', 'SPEED', 'HKCC', or 'Others'.")
        print("\nError:", e)
        
def editAttendee(emailAddress: str, password: str, attributeName: str, newValue, sqliteConnection, cursor):
    try:
        cursor.execute(f"UPDATE Attendee SET {attributeName} = '{newValue}' WHERE EmailAddress = '{emailAddress}' AND Password = '{password}'")
        sqliteConnection.commit()
        print(f"\nUpdated Attendee with email address {emailAddress}. Changed {attributeName} to {newValue}")
    except sqlite3.Error as e:
        if attributeName not in ("EmailAddress", "FirstName", "LastName", "Address", "Password", "Type", "MobileNumber", "AffiliatedOrganization"):
            print("\nInvalid attribute name.")
        if attributeName == "MobileNumber" and newValue != 8 and not newValue.isnumeric():
            print("\nNew mobile number must be a number.")
        if attributeName == "EmailAddress" and newValue.count("@") != 1:
            print("\nInvalid email address.")
        if attributeName == "AttendeeType" and newValue not in ("staff", "student", "alumni", "guest"):
            print("\nValue of 'attendeeType' must be 'staff', 'student', 'alumni', or 'guest'.")
        if attributeName == "AffiliatedOrganization" and newValue not in ("PolyU", "SPEED", "HKCC", "Others"):
            print("\nValue of 'affiliatedOrganization' must be 'PolyU', 'SPEED', 'HKCC', or 'Others'.")
        print("\nError:", e)
        
def printAttendee(emailAddress, cursor):
    try: 
        if emailAddress == "all":
            cursor.execute("SELECT * FROM Attendee")
            print("\nList of attendees: ")
            all_rows = cursor.fetchall()
            for row in all_rows:
                print(row)
        else:
            cursor.execute(f"SELECT * FROM Attendee WHERE EmailAddress = '{emailAddress}'")
            print("\nList of attendees: ")
            all_rows = cursor.fetchall()
            for row in all_rows:
                print(row)
    except sqlite3.Error as e:
        print("\nError:", e)
        
# Utility functions
def isValidDate(date: str) -> bool:
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d_%H:%M')
        return True
    except ValueError:
        return False
    
def isInDatabase(emailAddress: str, cursor) -> bool:
    try:
        cursor.execute(f"SELECT * FROM Attendee WHERE EmailAddress = '{emailAddress}'")
        if cursor.fetchone() is not None:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print("Error:", e)
        return False