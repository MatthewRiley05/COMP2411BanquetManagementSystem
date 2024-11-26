import sqlite3
import commands

loggedInUserEmail = None

def commandListAdmin(command, sqliteConnection, cursor):
    
    commandParsed = command.split(" ")
    
    match commandParsed[0]:
        case "commandList":
            print('\nAdmin commands: commandList, createNewBanquet, deleteBanquet, editBanquet, printBanquet, printAttendee, editAttendee, printRegisters, generateReport')
            
        case "createNewBanquet":
            if len(commandParsed) != 11:
                print('\nIncorrect number of parameters (Expected 11). Command format: createNewBanquet [BanquetID] [Name] [DateTime] [Address] [Location] [Quota] [Available] [FirstNameofContactStaff] [LastNameofContactStaff] [Remarks]')
                return
            commands.createNewBanquet(commandParsed[1], commandParsed[2], commandParsed[3], commandParsed[4], commandParsed[5], commandParsed[6], commandParsed[7], commandParsed[8], commandParsed[9], commandParsed[10], sqliteConnection, cursor)
            
            for _ in range(4):
                dishName = input('\nEnter dish name: ')
                dishType = input('Enter meal type (e.g. beef, pork, chicken, fish, vegetarian): ')
                price = float(input('Enter price: '))
                specialCuisine = input('Enter special cuisine: ')
                commands.createMeal(commandParsed[1], dishName, dishType, price, specialCuisine, sqliteConnection, cursor)
                
        case "deleteBanquet":
            if len(commandParsed) != 2:
                print('\nInccorect number of parameters (Expected 2). Command format: deleteBanquet [BanquetID]')
                return
            commands.deleteBanquet(commandParsed[1], sqliteConnection, cursor)
            
        case "editBanquet":
            if len(commandParsed) != 4:
                print('\nIncorrect number of parameters (Expected 4). Command format: editBanquet [BanquetID] [AttributeName] [NewValue]')
                return
            commands.editBanquet(commandParsed[1], commandParsed[2], commandParsed[3], sqliteConnection, cursor)
            
        case "printBanquet":
            if len(commandParsed) != 2:
                print('\nIncorrect number of parameters (Expected 2). Command format: printBanquet [BanquetID]')
                return
            commands.printBanquet(commandParsed[1], cursor)
            
        case "printAttendee":
            if len(commandParsed) != 2:
                print('\nIncorrect number of parameters (Expected 2). Command format: printAttendee [Email]')
                return
            commands.printAttendee(commandParsed[1], cursor)
            
        case "editAttendee":
            if len(commandParsed) != 4:
                print('\nIncorrect number of parameters (Expected 4). Command format: editAttendee [Email] [AttributeName] [NewValue]')
                return
            commands.adminEditAttendee(commandParsed[1], commandParsed[2], commandParsed[3], sqliteConnection, cursor)
            
        case "printRegisters":
            if len(commandParsed) != 2:
                print('\nIncorrect number of parameters (Expected 2). Command format: printRegisters [BanquetID]')
                return
            commands.printRegisters(commandParsed[1], cursor)
        
        case "generateReport":
            if len(commandParsed) != 1:
                print('\nIncorrect number of parameters (Expected 1). Command format: generateReport')
                return
            commands.generateReport(sqliteConnection, cursor)
        case _:
            print('\nInvalid command. Please enter a valid command.')
            
def commandListUser(command, sqliteConnection, cursor):
    
    global loggedInUserEmail
    
    commandParsed = command.split(" ")
    
    match commandParsed[0]:
        case "commandList":
            print('\nUser commands: commandList, printBanquet, printAttendee, editAttendee, registerBanquet, deregisterBanquet, printRegisters')
            
        case "printBanquet":
            if len(commandParsed) != 2:
                print('\nIncorrect number of parameters (Expected 2). Command format: printBanquet [BanquetID]')
                return
            commands.printBanquet(commandParsed[1], cursor)
            
        case "printAttendee":
            if len(commandParsed) != 1:
                print('\nIncorrect number of parameters (Expected 2). Command format: printAttendee')
                return
            commands.printAttendee(loggedInUserEmail, cursor)
            
        case "editAttendee":
            if len(commandParsed) != 5:
                print('\nIncorrect number of parameters (Expected 5). Command format: editAttendee [Email] [Password] [AttributeName] [NewValue]')
                return
            commands.editAttendee(commandParsed[1], commandParsed[2], commandParsed[3], commandParsed[4], sqliteConnection, cursor)
            
        case "registerBanquet":
            if len(commandParsed) != 7:
                print('\nIncorrect number of parameters (Expected 7). Command format: registerBanquet [emailAddress] [Password] [BanquetID] [MealChoice] [DrinkChoice] [Remarks]')
                return
            commands.registerBanquet(loggedInUserEmail, commandParsed[2], commandParsed[3], commandParsed[4], commandParsed[5], commandParsed[6], sqliteConnection, cursor)
            
        case "deregisterBanquet":
            if len(commandParsed) != 4:
                print('\nIncorrect number of parameters (Expected 4). Command format: deregisterBanquet [emailAddress] [Password] [BanquetID]')
                return
            commands.deregisterBanquet(loggedInUserEmail, commandParsed[2], commandParsed[3], sqliteConnection, cursor)
            
        case "searchRegisters":
            if len(commandParsed) != 3:
                print('\nIncorrect number of parameters (Expected 3). Command format: searchRegisters [attributeName] [attributeValue]')
                return
            commands.searchRegisters(loggedInUserEmail, commandParsed[1], commandParsed[2], cursor)
            
        case "editRegisters":
            if len(commandParsed) != 4:
                print('\nIncorrect number of parameters (Expected 5). Command format: editRegisters [emailAddress] [banquetID] [attributeName] [NewValue]')
                return
            commands.editRegisters(loggedInUserEmail, commandParsed[1], commandParsed[2], commandParsed[3], sqliteConnection, cursor)
            
        case _:
            print('\nInvalid command. Please enter a valid command.')
            
def newAccount(command, sqliteConnection, cursor):
    commandParsed = command.split(" ")
    match commandParsed[0]:
        case "createAttendee":
            if len(commandParsed) != 9:
                print('\nIncorrect number of parameters (Expected 9). Command format: createAttendee [emailAddress] [firstName] [lastName] [address] [password] [attendeeType] [mobileNumber] [affiliatedOrganization]')
                return
            commands.createAttendee(commandParsed[1], commandParsed[2], commandParsed[3], commandParsed[4], commandParsed[5], commandParsed[6], commandParsed[7], commandParsed[8], sqliteConnection, cursor)
            
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
    
    role = input('\nEnter your role (Admin/User): ')
    if role.lower() == 'admin':
        userName = input('\nEnter your username: ')
        password = input('Enter your password: ')
        if commands.adminLogin(userName, password):
            commandListAdmin('commandList', sqliteConnection, cursor)
            
    elif role.lower() == 'user':
        global loggedInUserEmail
        email = input('\nEnter your email: ')
        if commands.isInDatabase(email, cursor):
            loggedInUserEmail = email
            password = input('Enter your password: ')
            if commands.userLogin(email, password, sqliteConnection, cursor):
                commandListUser('commandList', sqliteConnection, cursor)
        else:
            try:
                loggedInUserEmail = email
                createAttendee = input('\nUser not found. Create an account to continue: ')
                newAccount(createAttendee, sqliteConnection, cursor)
            except Exception as e:
                print(f'\nAn error occurred: {e}. Exiting the program...')
                return
            
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