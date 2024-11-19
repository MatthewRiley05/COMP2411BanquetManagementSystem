import datetime
import sqlite3

def createNewBanquet(id : int, name : str, date_time : str, address : str, location : str, quota : int, available : int, first_name : str, last_name : str, remarks, cursor):
    try:
        datetime.date.fromisoformat(datetime)
    except ValueError:
        raise ValueError("Incorrect date format, should be 'YYYY-MM-DD")
    
    try:
        sqliteConnection = sqlite3.connect('banquetDatabase.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("INSERT INTO Banquet VALUES ({id}, {name}, {date_time}, {address}, {location}, {quota}, {available}, {first_name}, {last_name}, {remarks})")
        print("Created a new banquet. ID: {id}, Name: {name}")
    except Exception:
        if (None in (id, name, date_time, address, location, quota, available, first_name, last_name)):
            print("Value of all arguments (except remarks) must not be None .")
        if (available != 0 or 1):
            print("Value of 'available' must be 0 (false) or 1 (true).")
