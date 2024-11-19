import sqlite3
 
try:
   
    sqliteConnection = sqlite3.connect('banquetDatabase.db')
    cursor = sqliteConnection.cursor()
    print('DB Init')
 
    query = 'select sqlite_version();'
    cursor.execute(query)
 
    result = cursor.fetchall()
    print('SQLite Version is {}'.format(result))
 
    cursor.close()
 
except sqlite3.Error as error:
    print('Error occurred - ', error)
 
finally:
   
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection closed')