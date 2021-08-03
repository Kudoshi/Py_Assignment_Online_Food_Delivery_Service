#BRENDEN TAN POH GUAN - TP061596
#CHAN HONG WEI - TP

import os
import time
import datetime

'''
The simple food delivery online service system is coded using the concept of front-end and back-end.
The front-end is constructed in a page-like format that handles display, navigations, some validations and userinput
The back-end is where the underlying logic of the page resides. 

---------------------------------------------------------------------------------------------------------------------

The system is splitted into 4 regions:

1. Utility - Support functions to help the coding of the system.(e.g. clearConsole,u_constructButton)
2. db utility - Support functions that aids in coding the logic part of the page. (e.g. db_searchRecord)
3. db logic - The main logic behind the pages. Handles all the logic and some input validations. 
4. page - Handles display, navigations, sometimes validation and user input. 
          Simple short logic will sometime exist in this part. 
'''

#Receive - RC | Return - RT
# region Utility

def clearConsole():
    '''
    Clear console. Only works on terminal.
    Else it will next line to simulate clear
    '''
    print('\n'*200)
    time.sleep(0.1)
    cmd = "clear"
    if os.name in ('dos', 'nt'):
        cmd = "cls cmd"

    os.system(cmd)
    time.sleep(0.1)
    print("="*70)


def setupDB():
    '''
    Loads required files if haven't exist and clears temporary files
    '''
    #Creates file if not found
    requiredFiles = ["Accounts.txt", "Beverage.txt", "Western.txt", "Dessert.txt", "Local.txt",
                     "Order.txt", "Cart.txt"]
    for file in requiredFiles:
        with open(file, 'a') as f:
            continue
    #Empty the cart
    with open("Cart.txt", "w") as f:
        f.close()

def u_insertLine(symbol='_', nextLine= True,length = 70):
    '''
    Generate a line of default length 70. Able to specify whether to have next line at the top
    '''
    if nextLine:
        print('\n'+symbol*length)
    else:
        print(symbol*length)
def u_insertHeader(header, backButton = True):
    '''
    # Prints button
    # RC: Columnt Amt (max 3), 2D buttonList [[buttonTitle, buttonName],[]], resolution(default 70 spaces)
    # MoveleftAmt = how much to the left from the centre aligned
    '''

    if backButton:
        print('[BACK] Back')
        print(header.center(70,' '))
    else:
        print('\n'+header.center(70,' '))

    print('_'*70+'\n')

def u_constructButton(columnAmt, buttonlist,moveLeftAmt=9, resolution=70):
    '''
    Calculates position to put button using grid calculation method.
    The resolution is first divided based on columnAmt to get the grid size
    The grid size is then divided into 2 to get the middle align.
    Then move slightly left from middle based on moveLeftAmt
    '''
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
def u_popup(message, transitionSec = 4, nextLineAmt = 4):
    '''
    Generates an empty page containing the message. After a few transition sec it then returns control to the caller.
    Able to specify how many next line at the top of the message (nextLineAmt)
    '''
    clearConsole()
    print('\n'*nextLineAmt)
    print(message.center(70,' '))
    time.sleep(transitionSec)


# RC: 1D list RT: string
def list_ToSingleString(list):
    '''
    Converts a 1D list into a string format of (var1;var2;var3;var4) and return the string
    '''
    string = ''
    for i in range(0, len(list), 1):

        if i == (len(list) - 1):
            string = string + str(list[i]) + '\n'
        else:
            string = string + str(list[i]) + ';'

    return string

# endregion

#region DATABASE
#---------UTILITY----------

#RT 2D list
def db_returnList(fileName):
    '''
    Returns a 2D list based on the filename given.
    Return format: [[xx,xx,xx],[],[]]
    '''
    list = []
    with open(fileName, 'r') as file:
        for line in file:
            list.append(line.strip().split(';'))

    return list

#RC: 2d list
def db_overwriteRecord(fileName, list):
    '''
    Receives a 2D list, converts the 1D list inside into string. Then overwrite into the file.
    Generally used to overwrite food items when items are modified.
    '''
    with open(fileName, 'w') as file:
        for smallList in list:
            file.write(list_ToSingleString(smallList))

#RC: id,returnRecord | RT: T/F or 1D list
def db_searchRecord(fileName, id, returnRecord = False): #returnRecord: True - return record if got | False - return True False
    '''
    Searches a file (2D format) and checks whether the specified ID exists.
    Can return True or the entire details if returnRecord is True
    '''
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
    '''
    Deletes the record based on id
    It searches the file and turns it into 2D list. Removes it from the list and then overwrite the file.
    '''
    #Get the list first
    list = db_returnList(fileName)
    if db_searchRecord(fileName, id):
        # print(db_searchRecord(fileName,id, returnRecord=True))
        list.remove(db_searchRecord(fileName,id, returnRecord=True))

    db_overwriteRecord(fileName, list)

#RT: list[ID ,indexInList]
def db_getNewID(fileName):
    '''
    Generates a new ID and where to insert in the list for food or order based on the fileName given.
    Format: Food - X001 | Order - 123456
    '''
    #Get code
    if fileName == "Beverage.txt":
        codeID = 'B'
    elif fileName == "Dessert.txt":
        codeID = 'D'
    elif fileName == "Local.txt":
        codeID = 'L'
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

    #Order code
    if fileName == "Order.txt":
        return [str(gapNumber).zfill(6),index]
    #Food code
    return [codeID+str(gapNumber).zfill(3), index]

#RC: 1d list
def db_appendRecord(fileName, list):
    '''
    Append a 1D list without caring about ID into the file
    '''
    with open(fileName, 'a') as file:
        file.write(list_ToSingleString(list))

# endregion

#region Db Page Logics
#-----------PAGE LOGICS------------
#Resolution of 70 spaces
def db_displayFoodRecord(fileName, category):
    '''
    Displays a food category. Has a header based on the category param given.
    '''
    print(f'{category}'.center(70))
    print("-"*70)
    print("{:<10}{:<45}{:<15}".format('Food ID','Food Name', 'Price'))
    print("-"*70)
    foodList = db_returnList(fileName)
    for food in foodList:
        print("{:<10}{:<45}{:<15}".format(food[0], food[1], f"RM {float(food[2]):.2f}"))

    print('_'*70)

def db_displayAllFoodRecord():
    '''
    Displays ALL food category.
    Goes through the food category and prints them all out using the db_displayFoodRecord function
    '''
    print(" " * 24, f"ALL FOOD ITEM\n")
    foodCategory = [["Local.txt", "LOCAL"], ["Western.txt", "WESTERN"],
                    ["Dessert.txt", "DESSERT"], ["Beverage.txt", "BEVERAGE"]]

    for element in foodCategory:
        db_displayFoodRecord(element[0],element[1])
        print('\n')

def db_registerAccount(username, password): #return false if can't register
    '''
    Used by register page to register user account
    Performs simple search to check whether record exist.
    Returns True or False to indicate success operation
    '''
    #Checks if value exist
    if db_searchRecord("Accounts.txt", username):
        return False

    account = [username,password]
    db_appendRecord('Accounts.txt', account)
    return True


def db_loginAccount(username,password):
    '''
    Used by login page to login. Checks admin login or user login. Returns True or False indicating success operation
    Checks for ADMIN login with:
    username - admin | password - SystemAdmin123

    '''
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

def db_addToCart(fileName, foodID, quantity, overwriteQuantity = False): #fileName None for pg_cartModify
    '''
    Adds food item to cart.
    If foodID already exist in cart, it increases quantity. Else it creates new record in cart.
    Performs simple check on whether food id exist and inserts the food details into the cart file.
    OverwriteQuantity - Used for modification of cart to overwrite the food quantity.
    '''
    # Check existing cart
    cart = db_returnList("Cart.txt")
    foundInCart = False
    for i in range(1, len(cart), 1):
        if cart[i][0] == foodID and overwriteQuantity == False:
            cart[i][3] = str(int(cart[i][3]) + int(quantity))
            foundInCart = True
        elif cart[i][0] == foodID and overwriteQuantity == True:
            cart[i][3] = str(quantity)
            foundInCart = True

    # Add into existing cart
    if foundInCart:
        with open("Cart.txt", "w") as file:
            lineCount = 0
            for line in cart:
                print(line)

                lineCount += 1
                if lineCount == 1:
                    file.write(line[0]+"\n")
                else:
                    if int(line[3]) == 0: #If quantity is 0 then do not write
                        continue
                    file.write(f"{line[0]};{line[1]};{line[2]};{line[3]}\n")
        return True

    if fileName == None: #If fileName is None (for when adding to existing cart only)
        return False
    itemDetail = db_searchRecord(fileName, foodID, True)
    if itemDetail != False:
        itemDetail.append(str(quantity))
        db_appendRecord("Cart.txt", itemDetail)
        return True
    else:
        return False

def db_cartCheckout(totalPrice, address, foodQuantity):
    '''
    Used by cartcheckout page to write the cart details into the order history file.
    Format: orderID;username;totalPrice;address;dateTime;foodQuantity;foodID>foodName>price>quantity(foodRepeats)
    '''
    cartList = db_returnList("Cart.txt")
    idInfo = db_getNewID("Order.txt")
    dateTime = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M")
    orderRecord = f"{idInfo[0]};{cartList[0][0]};{totalPrice:.2f};{address};{dateTime};{str(foodQuantity)}"
    for i in range(1, len(cartList), 1):
        orderRecord += f";{cartList[i][0]}>{cartList[i][1]}>{float(cartList[i][2]):.2f}>{cartList[i][3]}"

    with open("Order.txt", "a") as file:
        file.write(orderRecord + '\n')

    with open("Cart.txt", "w") as file:  # Clear cart
        file.write(f"{cartList[0][0]}\n")
# endregion

#region Pages
'''
------------PAGES--------------
All pages are displayed in a consistent format:
- Back button with page header
- Content
- Buttons 
- User input decision
'''
def pg_custOrderHistory():
    while True:
        clearConsole()
        orderList = db_returnList("Order.txt")
        cartList = db_returnList("Cart.txt")
        #Display
        u_insertHeader("ORDER HISTORY")
        print(f"Customer: {cartList[0][0]}\n\n".center(70))
        u_insertLine("x")
        #Display order history
        for orderRecord in orderList:
            if orderRecord[1] == cartList[0][0]:
                print(f"Order ID: {orderRecord[0]}".center(70))
                u_insertLine("-")
                print(f"CUSTOMER: {orderRecord[1]}".center(70))
                print(f"Total Price: {orderRecord[2]}".center(70))
                print(f"Address:".center(70))
                print(f"{orderRecord[3]}".center(70))
                print(f"Date Time Ordered: {orderRecord[4]}".center(70))
                print(f"Item Quantity: {orderRecord[5]}".center(70))
                print(" ")
                u_insertLine("-", False)
                print("{:<9}{:<40}{:<12}{:<10}".format("Food ID","Food Items","Price","Quantity"))
                for foodItem in range(6,len(orderRecord),1):
                    foodDetails = orderRecord[foodItem].strip().split(">")
                    print("{:<9}{:<40}{:<15}{:<7}".format(foodDetails[0],foodDetails[1],foodDetails[2],foodDetails[3]))

                u_insertLine("_",False)
                u_insertLine("x")
                print("\n\n")

        u_constructButton(1,[["BACK", "Back"]])
        decision = input("Input your decision: ").upper()
        if decision == "BACK":
            break
        else:
            u_popup("INVALID INPUT DECISION",1.5)

def pg_cartCheckout():
    while True:
        clearConsole()
        cartList = db_returnList("Cart.txt")
        totalQuantity = 0
        totalPrice = 0

        #Display
        u_insertHeader("CHECKOUT")
        print("{:<45}{:<15}{:<10}".format("Food Items", "Price", "Quantity"))
        u_insertLine('-', False)
        #Display cart content

        for i in range(1, len(cartList), 1):
            totalQuantity += int(cartList[i][3])
            totalPrice += float(cartList[i][2]) * float(cartList[i][3])
            print("{:<45}{:<18}{:<7}".format(cartList[i][1], f'RM {float(cartList[i][2]):.2f}', cartList[i][3]))

        u_insertLine("_", False)
        print(f"Customer: {cartList[0][0]}\n".center(70))
        print(f"Total Food Items: {totalQuantity}".center(70))
        print(f"Total: RM {totalPrice:.2f}\n".center(70))

        #Handle user input
        address = input("Address location: ")
        print(" ")

        u_constructButton(2, [["PAY","Pay"],["RETYPE","Retype Address"]])

        decision = input("Input your decision: ").upper()
        if decision == "PAY":
            #Address validation
            if ">" in address or ";" in address:
                u_popup("INVALID SYMBOL (;,>) DETECTED IN ADDRESS",1.5)
                continue

            #Pay
            db_cartCheckout(totalPrice, address,totalQuantity)
            u_popup("ORDERED SUCESSFULLY")
            break
        elif decision == "BACK":
            break
        elif decision == "RETYPE":
            continue
        else:
            u_popup("INVALID INPUT DECISION",1.5)



def pg_cartModify():
    while True:
        clearConsole()
        cartList = db_returnList("Cart.txt")

        #Display
        u_insertHeader("MODIFY CART")

        print("{:<9}{:<40}{:<12}{:<10}".format("Food ID","Food Items","Price","Quantity"))
        u_insertLine('-', False)
        for i in range(1, len(cartList), 1):
            print("{:<9}{:<40}{:<15}{:<7}".format(cartList[i][0], cartList[i][1], f"RM {float(cartList[i][2]):.2f}", cartList[i][3]))
        u_insertLine("_", False)
        print("Input Food ID to modify\n".center(70))

        #Handle input
        inputID = input("Food ID: ").upper()
        if inputID == "BACK":
            break
        try:
            quantity = input("Quantity: ").upper()
            if inputID == "BACK":
                break
            quantity = int(quantity)
        except:
            u_popup("PLEASE INPUT NUMBERS ONLY", 1.5)
            continue

        isAdded = db_addToCart(None, inputID, quantity, True)
        if isAdded == False:
            u_popup("INVALID FOOD ID/DECISION",1.5)
        else:
            u_popup("ITEM MODIFIED SUCCESSFULLY",1.5)
            break


def pg_cart():
    while True:
        clearConsole()
        cartList = db_returnList("Cart.txt")
        totalQuantity = 0
        totalPrice = 0

        # Check if cart is empty
        if len(cartList) == 1:
            u_popup("CART IS EMPTY", 1.5)
            break

        #Display
        u_insertHeader("CART")
        print("{:<45}{:<15}{:<10}".format("Food Items","Price","Quantity"))
        u_insertLine('-',False)

        #Display cart content
        for i in range(1,len(cartList),1):
            totalQuantity += int(cartList[i][3])
            totalPrice+= float(cartList[i][2])*float(cartList[i][3])
            print("{:<45}{:<18}{:<7}".format(cartList[i][1], f'RM {float(cartList[i][2]):.2f}', cartList[i][3]))

        u_insertLine("_",False)
        print(f"Total Food Items: {totalQuantity}".center(70))
        print(f"Total: RM {totalPrice:.2f}\n".center(70))
        u_constructButton(2, [['MODIFY', 'Modify Cart'],['CHECKOUT', 'Proceed To Checkout']],13)

        #Handle user input
        decision = input("Input your decision: ").upper()

        if decision == "MODIFY":
            pg_cartModify()
        elif decision == "CHECKOUT":
            pg_cartCheckout()
            break
        elif decision == "BACK":
            break
        else:
            u_popup("INVALID INPUT DECISION", 1.5)

def pg_custMenuItems(fileName, categoryHeader):
    while True:
        clearConsole()
        #Display
        u_insertHeader("MENU")
        db_displayFoodRecord(fileName, categoryHeader)
        print("Input Food ID to add to cart\n".center(70))
        #Handle input
        decision = input("Input your decision: ").upper()
        if decision == "BACK":
            break
        if db_searchRecord(fileName,decision) == False:
            u_popup("FOOD ID NOT FOUND",1.5)
            continue

        #Quantity
        try:
            quantity = int(input("Please input quantity: "))
            if quantity <= 0:
                raise ValueError
        except:
            u_popup("INVALID VALUE ENTERED",1.5)
            continue



        #Add to cart
        isSuccessful = db_addToCart(fileName, decision, quantity)
        if isSuccessful:
            u_popup("ITEM ADDED TO CART", 1)
            continue
        else:
            u_popup("FOOD ITEM NOT FOUND", 1.5)
            continue

def pg_custMenuCategory():
    while True:
        clearConsole()
        u_insertHeader("MENU")
        print("CATEGORY".center(70)+"\n")
        u_constructButton(1, [['LOCAL', 'Local Food'],['WESTERN','Western Food'],
                              ['DESSERT','Dessert'],["BEVERAGE","Beverage"]])
        u_insertLine()
        print("Select Menu Category".center(70))
        decision = input("\nInput your decision: ").upper()

        if decision == "LOCAL":
            pg_custMenuItems("Local.txt","Local Food")
        elif decision == "WESTERN":
            pg_custMenuItems("Western.txt","Western Food")
        elif decision == "DESSERT":
            pg_custMenuItems("Dessert.txt","Dessert")
        elif decision == "BEVERAGE":
            pg_custMenuItems("Beverage.txt","Beverage")
        elif decision == "BACK":
            break
        else:
            u_popup("INVALID INPUT DECISION",1.5)


def pg_custMain():
    while True:
        clearConsole()
        #Display
        u_insertHeader("SPIDERMAN ONLINE FOOD SERVICES", False)
        print(f"Welcome, {db_returnList('Cart.txt')[0][0]}\n".center(70))
        u_constructButton(1,[['MENU','Menu'], ['CART', 'Cart'],
                             ['HISTORY', 'Order History'],['LOGOUT','Log Out']])

        u_insertLine()
        #Handle input
        decision = input("Input your decision: ").upper()
        if decision == 'MENU':
            pg_custMenuCategory()
        elif decision == 'CART':
            pg_cart()
        elif decision == "HISTORY":
            pg_custOrderHistory()
        elif decision == 'LOGOUT':
            with open("Cart.txt", "w") as f:
                f.close()
            break
        else:
            u_popup("[ERROR] INVALID INPUT DECISION",1.5)

def pg_register():
    while True:
        clearConsole()
        #Display
        u_insertHeader("REGISTER", True)
        username = input(" " * 20 + "Username: ")
        password = input(" " * 20 + "Password: ")
        u_insertLine()
        u_constructButton(2, [["SUBMIT", "Submit"], ["RETYPE","Retype"]])

        #Handle input
        decision = input("Input your decision: ").upper()
        if decision == "SUBMIT":
            #Validation check
            if "admin" in username:
                u_popup("INVALID USERNAME", 1.5)
                continue
            elif ">" in username or ";" in username:
                u_popup("USERNAME CONTAINS INVALID SYMBOL", 1.5)
                continue

            #Register account
            isSuccessful = db_registerAccount(username, password)
            if isSuccessful:
                u_popup("REGISTERED SUCCESSFUL",2)
                break
            else:
                u_popup("USERNAME ALREADY EXIST",2)
        elif decision == "RETYPE":
            continue
        elif decision == "BACK":
            break
        else:
            u_popup("INVALID INPUT DECISION", 1.5)

def pg_login():
    while True:
        clearConsole()
        #Display
        u_insertHeader("LOGIN", False)

        username = input(" "*20+ "Username: ")
        password = input(" "*20+ "Password: ")

        u_insertLine()
        #Handle input
        login = db_loginAccount(username,password)
        if login:
            clearConsole()
            #Clear cart and write username to cart
            with open("Cart.txt",'w') as file:
                file.write(username+'\n')
            pg_custMain()
            break
        else:
            clearConsole()
            u_popup('[ERROR] INCORRECT USERNAME OR PASSWORD', 1.5)
            break
def pg_exit():
    clearConsole()
    u_popup("THANK YOU FOR USING OUR SERVICE")
    exit()
def pg_main():
    while True:
        clearConsole()
        u_insertHeader("WELCOME TO SPIDERMAN ONLINE FOOD DELIVERY SERVICES", False)

        u_constructButton(1, [["LOGIN", 'Login'], ["REGISTER", "Register"],
                              ['GUEST', 'View as Guest'], ['EXIT', 'Exit']])
        u_insertLine()
        decision = input("Input your decision: ").upper()

        if decision == "LOGIN":
            pg_login()
        elif decision == "REGISTER":
            pg_register()
        elif decision == "EXIT":
            pg_exit()
            break
        else:
            u_popup("[ERROR] INVALID INPUT DECISION!", 1.5)

# endregion

#PROGRAM STARTS HERE

setupDB()
pg_main()
