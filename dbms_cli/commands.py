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
        cursor.execute(f"SELECT * FROM Attendee WHERE emailAddress = '{emailAddress}' AND password = '{password}'")
        if cursor.fetchone() is not None:
            print("\nLogin successful.")
            return True
        else:
            print("\nLogin failed. Invalid email address or password.")
            return False
    except sqlite3.Error as e:
        print("Error:", e)
        return False
    
def createNewBanquet(banquetID: int, name: str, dateTime: str, address: str, location: str, quota: int, available: int, firstNameOfContactStaff: str, lastNameOfContactStaff: str, remarks, sqliteConnection, cursor):
    try:
        cursor.execute("INSERT INTO Banquet VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (banquetID, name, dateTime, address, location, quota, available, firstNameOfContactStaff, lastNameOfContactStaff, remarks))
        sqliteConnection.commit()
        print(f"\nCreated a new banquet. ID: {banquetID}, Name: {name}")
    except sqlite3.Error as e:
        if None in (banquetID, name, dateTime, address, location, quota, available, firstNameOfContactStaff, lastNameOfContactStaff):
            print("\nValue of all arguments (except remarks) must not be None.")
        if available not in (0, 1):
            print("\nValue of 'available' must be 0 (false) or 1 (true).")
        if not isValidDate(dateTime):
            print("\nIncorrect format for date. Correct format: YYYY-MM-DD_HH:MM")
        print("\nError:", e)
        
def deleteBanquet(banquetID: int, sqliteConnection, cursor):
    try:
        cursor.execute(f"DELETE FROM Banquet WHERE banquetID = {banquetID}")
        sqliteConnection.commit()
        cursor.execute(f"DELETE FROM Meal WHERE banquetID = {banquetID}")
        sqliteConnection.commit()
        cursor.execute(f"DELETE FROM Registers WHERE banquetID = {banquetID}")
        sqliteConnection.commit()
        print(f"\nDeleted banquet with ID {banquetID}")
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
        
def printBanquet(banquetID, cursor):
    try: 
        if banquetID == 'all':
            cursor.execute("SELECT * FROM Banquet")
            print("\nList of banquets: ")
            all_rows = cursor.fetchall()
            for row in all_rows:
                print(row)
        else:
            cursor.execute(f"SELECT * FROM Banquet WHERE banquetID = {banquetID}")
            print(f"Banquet {banquetID}: ")
            banquet = cursor.fetchone()
            print(banquet)
            cursor.execute(f"SELECT * FROM Meal WHERE banquetID = {banquetID}")
            meals = cursor.fetchall()
            print("\nMeals: ")
            for meal in meals:
                print(meal)
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
        if len(dishName.split()) > 1:
            print("\nDish name must not contain spaces.")
        if dishType not in ("beef", "pork", "chicken", "fish", "vegetarian"):
            print("\nValue of 'dishType' must be 'beef', 'pork', 'chicken', 'fish', 'vegetarian'")
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
        cursor.execute(f"UPDATE Attendee SET {attributeName} = '{newValue}' WHERE emailAddress = '{emailAddress}'")
        sqliteConnection.commit()
        print(f"\nUpdated attendee {emailAddress} {attributeName} to {newValue}")
    except sqlite3.Error as e:
        if attributeName not in ("emailAddress", "firstName", "lastName", "address", "password", "attendeeType", "mobileNumber", "affiliatedOrganization"):
            print("\nInvalid attribute name.")
        if attributeName == "mobileNumber" and newValue != 8 and not newValue.isnumeric():
            print("\nMobile number must be 8 digits.")
        if attributeName == "emailAddress" and newValue.count("@") != 1:
            print("\nInvalid email address.")
        if attributeName == "attendeeType" and newValue not in ("staff", "student", "alumni", "guest"):
            print("\nValue of 'attendeeType' must be 'staff', 'student', 'alumni', or 'guest'.")
        if attributeName == "affiliatedOrganization" and newValue not in ("PolyU", "SPEED", "HKCC", "Others"):
            print("\nValue of 'affiliatedOrganization' must be 'PolyU', 'SPEED', 'HKCC', or 'Others'.")
        print("\nError:", e)
        
def editAttendee(emailAddress: str, password: str, attributeName: str, newValue, sqliteConnection, cursor):
    try:
        cursor.execute(f"UPDATE Attendee SET {attributeName} = '{newValue}' WHERE emailAddress = '{emailAddress}' AND password = '{password}'")
        sqliteConnection.commit()
        print(f"\nUpdated Attendee with email address {emailAddress}. Changed {attributeName} to {newValue}")
    except sqlite3.Error as e:
        if attributeName not in ("emailAddress", "firstName", "lastName", "address", "password", "type", "mobileNumber", "affiliatedOrganization"):
            print("\nInvalid attribute name.")
        if attributeName == "mobileNumber" and newValue != 8 and not newValue.isnumeric():
            print("\nNew mobile number must be a number.")
        if attributeName == "emailAddress" and newValue.count("@") != 1:
            print("\nInvalid email address.")
        if attributeName == "attendeeType" and newValue not in ("staff", "student", "alumni", "guest"):
            print("\nValue of 'attendeeType' must be 'staff', 'student', 'alumni', or 'guest'.")
        if attributeName == "affiliatedOrganization" and newValue not in ("PolyU", "SPEED", "HKCC", "Others"):
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
            cursor.execute(f"SELECT * FROM Attendee WHERE emailAddress = '{emailAddress}'")
            print("\nList of attendees: ")
            all_rows = cursor.fetchall()
            for row in all_rows:
                print(row)
    except sqlite3.Error as e:
        print("\nError:", e)
        
def registerBanquet(emailAddress: str, password: str, banquetID: int, mealChoice: str, drinkChoice: str, remarks: str, sqliteConnection, cursor):
    try:
        cursor.execute(f"SELECT * FROM Attendee WHERE emailAddress = '{emailAddress}' AND password = '{password}'")
        if cursor.fetchone() is None:
            print("\nInvalid email address or password.")
            return
        cursor.execute(f"SELECT * FROM Banquet WHERE banquetID = {banquetID}")
        if cursor.fetchone() is None:
            print("\nInvalid banquet ID.")
            return
        cursor.execute(f"SELECT available FROM Banquet WHERE banquetID = {banquetID}")
        available = cursor.fetchone()[0]
        if available == 0:
            print("\nBanquet is not available.")
        cursor.execute("INSERT INTO Registers VALUES (?, ?, ?, ?, ?)",
                       (emailAddress, banquetID, mealChoice, drinkChoice, remarks))
        sqliteConnection.commit()
        cursor.execute(f"UPDATE Banquet SET quota = quota - 1 WHERE banquetID = {banquetID}")
        sqliteConnection.commit()
        cursor.execute(f"SELECT quota FROM Banquet WHERE banquetID = {banquetID}")
        quota = cursor.fetchone()[0]
        if quota == 0:
            cursor.execute(f"UPDATE Banquet SET AVAILABLE = 0 WHERE banquetID = {banquetID}")
            sqliteConnection.commit()
        print(f"\nRegistered {emailAddress} for banquet {banquetID}")
    except sqlite3.Error as e:
        print("\nError:", e)

def deregisterBanquet(emailAddress: str, password: str, banquetID: int, sqliteConnection, cursor):
    try:
        cursor.execute(f"SELECT * FROM Attendee WHERE emailAddress = '{emailAddress}' AND password = '{password}'")
        if cursor.fetchone() is None:
            print("\nInvalid email address or password.")
            return
        cursor.execute(f"SELECT * FROM Banquet WHERE banquetID = {banquetID}")
        if cursor.fetchone() is None:
            print("\nInvalid banquet ID.")
            return
        cursor.execute(f"SELECT available FROM Banquet WHERE banquetID = {banquetID}")
        available = cursor.fetchone()[0]
        if available == 0:
            print("\nBanquet is not available.")
        cursor.execute(f"DELETE FROM Registers WHERE emailAddress = '{emailAddress}' AND banquetID = {banquetID}")
        sqliteConnection.commit()
        cursor.execute(f"UPDATE Banquet SET quota = quota + 1 WHERE banquetID = {banquetID}")
        sqliteConnection.commit()
        cursor.execute(f"SELECT quota FROM Banquet WHERE banquetID = {banquetID}")
        quota = cursor.fetchone()[0]
        if quota >= 1:
            cursor.execute(f"UPDATE Banquet SET AVAILABLE = 1 WHERE banquetID = {banquetID}")
            sqliteConnection.commit()
        print(f"\nDeregistered {emailAddress} for banquet {banquetID}")
    except sqlite3.Error as e:
        print("\nError:", e)
        
def printRegisters(emailAddress: str, cursor):
    try: 
        if emailAddress == "all":
            cursor.execute("SELECT * FROM Registers")
            print("\nList of registrations: ")
            all_rows = cursor.fetchall()
            for row in all_rows:
                print(row)
        else:
            cursor.execute(f"SELECT * FROM Registers WHERE emailAddress = '{emailAddress}'")
            print("\nList of registrations: ")
            all_rows = cursor.fetchall()
            for row in all_rows:
                print(row)
    except sqlite3.Error as e:
        print("\nError:", e)
        
def searchRegisters(emailAddress, attributeName: str, attributeValue, cursor):
    try:
        query = f"SELECT * FROM Registers WHERE emailAddress = ? AND {attributeName} = ?"
        cursor.execute(query, (emailAddress, attributeValue))
        print("\nList of registrations: ")
        all_rows = cursor.fetchall()
        for row in all_rows:
            print(row)
    except sqlite3.Error as e:
        print("\nError:", e)
        
def editRegisters(emailAddress, banquetID: int, attributeName: str, newValue, sqliteConnection, cursor):
    try:
        if attributeName not in ("emailAddress", "banquetID", "mealChoice", "drinkChoice", "remarks"):
            print("\nInvalid attribute name.")
            return
        elif attributeName == "banquetID":
            print("\nCannot change banquet ID.")
            return
        else:
            cursor.execute(f"UPDATE Registers SET {attributeName} = '{newValue}' WHERE emailAddress = '{emailAddress}' AND banquetID = {banquetID}")
            sqliteConnection.commit()
            print(f"\nUpdated registration for {emailAddress} for banquet {banquetID}. Changed {attributeName} to {newValue}")
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
        cursor.execute(f"SELECT * FROM Attendee WHERE emailAddress = '{emailAddress}'")
        if cursor.fetchone() is not None:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print("Error:", e)
        return False