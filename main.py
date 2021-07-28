import os
import time
#Receive - RC | Return - RT
# region Utility

def clearConsole():
    print('\n'*200)
    time.sleep(0.1)
    cmd = "clear"
    if os.name in ('dos', 'nt'):
        cmd = "cls"

    os.system(cmd)
    time.sleep(0.1)
    print("="*70)


def setupDB():
    #Create files if not exist yet
    requiredFiles = ["Accounts.txt", "Beverage.txt", "Western.txt", "Dessert.txt", "Local.txt",
                     "Order.txt", "Payment.txt", "Cart.txt"]
    for file in requiredFiles:
        with open(file, 'a') as f:
            continue
    #TODO Load data into at launch
    #Empty the cart
    with open("Cart.txt", "w") as f:
        f.close()

# Prints button
# RC: Columnt Amt (max 3), 2D buttonList [buttonTitle, buttonName], resolution(pagesize)
# MoveleftAmt = how much to the left from the centre aligned
def u_insertLine(symbol='_', nextLine= True,length = 70):
    if nextLine:
        print('\n'+symbol*length)
    else:
        print(symbol*length)
def u_insertHeader(header, backButton = True):
    if backButton:
        print('[BACK] Back')

    print('\n'+header.center(70,' '))
    print('_'*70+'\n')

def u_constructButton(columnAmt, buttonlist,moveLeftAmt=9, resolution=70):
    gridSize = int(resolution / columnAmt)
    leftPadding = int((gridSize / 2) - moveLeftAmt)
    col = 0
    text = ''
    buttonsCnt = 0

    for buttons in buttonlist:
        buttonsCnt += 1
        col += 1
        text += ' ' * leftPadding + f"[{buttons[0]}] {buttons[1]}"

        textLength = len(text) - (gridSize * (col - 1))
        # Add remaining spaces of the grid
        if textLength <= gridSize:
            remainingSpace = gridSize - textLength
            text += ' ' * remainingSpace
        # Prints the text and reset the var
        if col % columnAmt == 0 or buttonsCnt == len(buttonlist):
            print(text+'\n')
            text = ''
            col = 0


#RC: message, transitionSec, nxtLineAmt
def u_popup(message, transitionSec, nextLineAmt):
    clearConsole()
    print('\n'*nextLineAmt)
    print(message.center(70,' '))
    time.sleep(transitionSec)


# RC: 1D list RT: string
def list_ToSingleString(list):
    string = ''
    for i in range(0, len(list), 1):

        if i == (len(list) - 1):
            string = string + str(list[i]) + '\n'
        else:
            string = string + str(list[i]) + ';'

    return string

# endregion

#region DATABASE
#------UTILITY--------

#RT 2D list
def db_returnList(fileName):
    list = []
    with open(fileName, 'r') as file:
        for line in file:
            list.append(line.strip().split(';'))

    return list

#RC: 2d list
def db_overwriteRecord(fileName, list):
    with open(fileName, 'w') as file:
        for smallList in list:
            file.write(list_ToSingleString(smallList))

#RC: id,returnRecord | RT: T/F or 1D list
def db_searchRecord(fileName, id, returnRecord = False): #returnRecord: True - return record if got | False - return True False
    #Search and extract record based on id
    record = False
    with open(fileName, "r") as file:
        for line in file:
            _record = line.strip().split(";")
            if _record[0] == id:
                record = _record
                break

    #Check if id exist
    if record != False:
        #return record or True
        if returnRecord:
            return record
        else:
            return True
    else: #record not found
        return False

#RC: id
def db_deleteRecord(fileName, id):
    #Get the list first
    list = db_returnList(fileName)
    if db_searchRecord(fileName, id):
        # print(db_searchRecord(fileName,id, returnRecord=True))
        list.remove(db_searchRecord(fileName,id, returnRecord=True))

    db_overwriteRecord(fileName, list)

#RT: list[ID ,indexInList]
def db_getNewID(fileName):
    #Get code
    if fileName == "Beverage.txt":
        codeID = 'B'
    elif fileName == "Cart.txt":
        codeID = 'C'
    elif fileName == "Dessert.txt":
        codeID = 'D'
    elif fileName == "Local.txt":
        codeID = 'L'
    elif fileName == "Order.txt":
        codeID = 'R'
    elif fileName == "Western.txt":
        codeID = 'W'

    #Get auto-increment id and the index of the gap
    list = db_returnList(fileName)
    gapNumber = 1
    index = 0
    for records in list:
        if gapNumber == int(records[0][1:]):
            gapNumber += 1
        else:
            break
        index += 1
    print(index)
    return [codeID+str(gapNumber).zfill(3), index]

#RC: 1d list
def db_appendRecord(fileName, list): #append one dimensional list without the id

    with open(fileName, 'a') as file:
        file.write(list_ToSingleString(list))

#for each string available write into the file


#-----------PAGE LOGICS------------
#Resolution of 70 spaces
def db_displayFoodRecord(fileName, category):
    print(" "*27, f"{category}")
    print("="*70)
    print("{:<10}{:<40}{:<20}".format('Food ID','Food Name', 'Price'))
    print("-"*70)
    foodList = db_returnList(fileName)
    for food in foodList:
        print("{:<10}{:<40}{:<20}".format(food[0], food[1], 'RM '+str(food[2])))
    print('='*70)

def db_displayAllFoodRecord():
    print(" " * 24, f"ALL FOOD ITEM\n")
    foodCategory = [["Local.txt", "LOCAL"], ["Western.txt", "WESTERN"],
                    ["Dessert.txt", "DESSERT"], ["Beverage.txt", "BEVERAGE"]]

    for element in foodCategory:
        db_displayFoodRecord(element[0],element[1])
        print('\n')

def db_registerAccount(username, password): #return false if can't register
    # ADMIN CHECK
    #Checks if value exist
    if db_searchRecord("Accounts.txt", username):
        return False

    account = [username,password]
    db_appendRecord('Accounts.txt', account)
    return True


def db_loginAccount(username,password):
    #Check admin credentials
    if username == 'admin' and password == 'SystemAdmin123':
        print("Admin page")
        #to admin page

    #Check user login credentials
    account = db_searchRecord('Accounts.txt', username, True)
    if account != False and account[1] == password:
        return True
    else:
        return False

# endregion

#region Pages
def pg_login():
    while True:
        clearConsole()
        u_insertHeader("LOGIN", False)

        username = input(" "*20+ "Username: ")
        password = input(" "*20+ "Password: ")

        print('\n')
        print("-"*70)

        login = db_loginAccount(username,password)
        if login:
            clearConsole()
            #To customer page
            time.sleep(4)
            break
        else:
            clearConsole()
            u_popup('[ERROR] INCORRECT USERNAME OR PASSWORD', 4, 4)
            break

def pg_main():
    while True:
        clearConsole()
        u_insertHeader("MAIN MENU", False)
        u_constructButton(1, [["LOGIN", 'Login'], ["REGISTER", "Register"],
                              ['GUEST', 'View as Guest'], ['EXIT', 'Exit']])
        u_insertLine()
        decision = input("Input your decision: ").upper()

        if decision == "LOGIN":
            pg_login()
        else:
            print("Input proper value please")
            time.sleep(1)

# endregion

pg_main()

#
# if __name__ == '__main__':
#     main()