import sqlite3

try :
    sqliteConnection = sqlite3.connect('banquetDatabase.db')
    print("Database connected successfully")
    
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)