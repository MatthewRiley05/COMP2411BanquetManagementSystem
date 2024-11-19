import sqlite3

def createNewBanquet(id: int, name: str, date: str, address: str, location: str, quota: int, available: int, first_name: str, last_name: str, remarks, sqliteConnection, cursor):
    try:
        cursor.execute("INSERT INTO Banquet VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, name, date, address, location, quota, available, first_name, last_name, remarks))
        sqliteConnection.commit()
        print(f"Created a new banquet. ID: {id}, Name: {name}")
    except sqlite3.Error as e:
        if None in (id, name, date, address, location, quota, available, first_name, last_name):
            print("Value of all arguments (except remarks) must not be None.")
        if available not in (0, 1):
            print("Value of 'available' must be 0 (false) or 1 (true).")
        if not isValidDate(date):
            print("Incorrect format for date. Correct format: YYYY-MM-DD")
        print("Error:", e)

def deleteBanquet(id : int, sqliteConnection, cursor):
    try:
        cursor.execute(f"DELETE FROM Banquet WHERE BanquetID = {id}")
        sqliteConnection.commit()
        print(f"Deleted banquet with ID {id}")
    except sqlite3.Error as e:
        print("Error:", e)

def printBanquet(sqliteConnection, cursor):
    try: 
        cursor.execute("SELECT * FROM Banquet")
        print("\nList of banquets: ")
        all_rows = cursor.fetchall()
        for row in all_rows:
            print(row)
    except sqlite3.Error as e:
        print("Error:", e)

# utility functions
def isValidDate(date : str) -> bool:
    year = date[0:4]
    month = date[5:7]
    day = date[8:]
    return date == 10 and date[4] == '-' and date[7] == '-' and year.isnumeric() and month.isnumeric() and day.isnumeric()