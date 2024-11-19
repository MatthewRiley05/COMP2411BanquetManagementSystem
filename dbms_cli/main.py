import sqlite3
import commands

def commandListAdmin(command, sqliteConnection, cursor):
    commandParsed = command.split(" ")
    match commandParsed[0]:
        case "createNewBanquet":
            if len(commandParsed) != 11:
                print('\nInvalid number of arguments, Expected 11 arguments, got', len(commandParsed))
                return
            commands.createNewBanquet(commandParsed[1], commandParsed[2], commandParsed[3], commandParsed[4], commandParsed[5], commandParsed[6], commandParsed[7], commandParsed[8], commandParsed[9], commandParsed[10], sqliteConnection, cursor)
        case "deleteBanquet":
            if len(commandParsed) != 2:
                print('\nInvalid number of arguments, Expected 2 arguments, got', len(commandParsed))
                return
            commands.deleteBanquet(commandParsed[1], sqliteConnection, cursor)
        case "printBanquet":
            if len(commandParsed) != 1:
                print('\nInvalid number of arguments, Expected 1 argument, got', len(commandParsed))
                return
            commands.printBanquet(sqliteConnection, cursor)
        case _:
            print('\nInvalid command. Please enter a valid command.')

def commandListUser(command, sqliteConnection, cursor):
    commandParsed = command.split(" ")
    match commandParsed[0]:
        case "createNewBanquet":
            if len(commandParsed) != 11:
                print('\nInvalid number of arguments, Expected 11 arguments, got', len(commandParsed))
                return
            commands.createNewBanquet(commandParsed[1], commandParsed[2], commandParsed[3], commandParsed[4], commandParsed[5], commandParsed[6], commandParsed[7], commandParsed[8], commandParsed[9], commandParsed[10], sqliteConnection, cursor)
        case "deleteBanquet":
            if len(commandParsed) != 2:
                print('\nInvalid number of arguments, Expected 2 arguments, got', len(commandParsed))
                return
            commands.deleteBanquet(commandParsed[1], sqliteConnection, cursor)
        case "printBanquet":
            if len(commandParsed) != 1:
                print('\nInvalid number of arguments, Expected 1 argument, got', len(commandParsed))
                return
            commands.printBanquet(sqliteConnection, cursor)
        case _:
            print('\nInvalid command. Please enter a valid command.')

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
    
    role = input('\nEnter your role (admin/user): ')
    if role.lower() == 'admin':
        print('\nAdmin commands: createNewBanquet, deleteBanquet, printBanquet')
    elif role.lower() == 'user':
        print('\nUser commands: printBanquet')
    else:
        print('\nInvalid role. Exiting the program...')
        return

    while True:
        command = input('\nEnter a command: ')
        if command.lower() == 'exit':
            print('\nExiting the program...')
            break
        if role.lower() == "admin":
            commandListAdmin(command, sqliteConnection, cursor)
        elif role.lower() == "user":
            commandListUser(command, sqliteConnection, cursor)

    cursor.close()
    sqliteConnection.close()

if __name__ == "__main__":
    main()