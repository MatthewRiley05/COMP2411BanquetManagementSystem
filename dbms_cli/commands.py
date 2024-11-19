import sqlite3

def createNewBanquet(id: int, name: str, date: str, address: str, location: str, quota: int, available: int, first_name: str, last_name: str, remarks, cursor):
    try:
        sqliteConnection = sqlite3.connect('banquetDatabase.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("INSERT INTO Banquet VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, name, date, address, location, quota, available, first_name, last_name, remarks))
        sqliteConnection.commit()
        print(f"Created a new banquet. ID: {id}, Name: {name}")
    except Exception as e:
        if None in (id, name, date, address, location, quota, available, first_name, last_name):
            print("Value of all arguments (except remarks) must not be None.")
        if available not in (0, 1):
            print("Value of 'available' must be 0 (false) or 1 (true).")
        if not isValidDate(date):
            print("Incorrect format for date. Correct format: YYYY-MM-DD")
        print("Error:", e)

# util functions
def isValidDate(date : str) -> bool:
    year = date[0:4]
    month = date[5:7]
    day = date[8:]
    return date == 10 and date[4] == '-' and date[7] == '-' and year.isnumeric() and month.isnumeric() and day.isnumeric()