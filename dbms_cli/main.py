import sqlite3
 
try:
    sqliteConnection = sqlite3.connect('banquetDatabase.db')
    cursor = sqliteConnection.cursor()
    print('Banquet Management System has been initialized')

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print(f'\nTable: {table_name}')
        
        cursor.execute(f'SELECT * FROM {table_name}')
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)

    cursor.close()
 
except sqlite3.Error as error:
    print('Error:', error)