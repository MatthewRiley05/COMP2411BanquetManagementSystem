import sqlite3

def commandList(command, cursor):
    commandLower = command.lower()
    match commandLower:
        case "print tables":
            print("Printing tables...")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                if not table_name.startswith('sqlite'):
                    print(f'\nTable: {table_name}')

def initDatabase():
    try:
        sqliteConnection = sqlite3.connect('banquetDatabase.db')
        cursor = sqliteConnection.cursor()
        print('Banquet Management System has been initialized')
        return sqliteConnection, cursor
    except sqlite3.Error as error:
        print('Error:', error)
        return None, None

def main():
    sqliteConnection, cursor = initDatabase()
    if cursor is None:
        return

    while True:
        command = input('Enter a command: ')
        if command.lower() == 'exit':
            print('Exiting the program...')
            break
        commandList(command, cursor)

    cursor.close()
    sqliteConnection.close()

if __name__ == "__main__":
    main()