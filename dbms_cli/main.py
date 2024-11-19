import sqlite3
import commands

def commandList(command, cursor):
    commandParsed = command.split(" ")
    match commandParsed[0]:
        case "createNewBanquet":
            if len(commandParsed) != 11:
                print('Invalid number of arguments, Expected 11 arguments, got', len(commandParsed))
                return
            commands.createNewBanquet(commandParsed[1], commandParsed[2], commandParsed[3], commandParsed[4], commandParsed[5], commandParsed[6], commandParsed[7], commandParsed[8], commandParsed[9], commandParsed[10], cursor)

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