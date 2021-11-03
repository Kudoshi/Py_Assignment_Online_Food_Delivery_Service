#BRENDEN TAN POH GUAN - TP061596
#CHAN HONG WEI - TP060647

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
2. Database - Support functions that aids in coding the logic part of the page. (e.g. db_searchRecord)
3. Db Page logic - The main logic behind the pages. Handles all the logic and some input validations. 
4. Pages - Handles display, navigations, sometimes validation and user input. 
          Simple short logic will sometime exist in this part. The page is further split into a few section.
'''

#Receive - RC | Return - RT
# region Utility

def clearConsole():
    '''
    Clear console. Only works on terminal.
    Else it will next line to simulate clear
    '''
    print('\n'*200) #Due to errors in the pycharm output window. So just in case
    time.sleep(0.1) #Someimtes will have error with the display. So sleep the time for awhile for display to load or sometihng

    cmd = "clear" #dfault value - WIndows defualt clear cmd
    if os.name in ('dos', 'nt'): #if your os name is mac or linux
        cmd = "cls cmd" #change the cmd to this <-- cz linux or mac might cls cmd

        #WIndows clear cmd - clear, linux/mac - cls cmd

    os.system(cmd) #call clear cmd
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
def u_popup(message, transitionSec = 2, nextLineAmt = 4):
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

#region Database
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
        print(index)

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
#Page resolution is set as 70

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
    Used by login page to login. Returns True or False indicating success operation

    '''
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
        #Increases food quantity if already in cart
        if cart[i][0] == foodID and overwriteQuantity == False:
            cart[i][3] = str(int(cart[i][3]) + int(quantity))
            foundInCart = True

        #Used by modify cart to directly overwrite quantity value
        elif cart[i][0] == foodID and overwriteQuantity == True:
            cart[i][3] = str(quantity)
            foundInCart = True

    # Write the new details into cart.txt if item already in cart
    if foundInCart:
        with open("Cart.txt", "w") as file:
            lineCount = 0
            for line in cart:
                lineCount += 1
                if lineCount == 1:
                    file.write(line[0]+"\n")
                else:
                    # If quantity is 0 then do not write. Removes it from cart
                    if int(line[3]) == 0:
                        continue
                    file.write(f"{line[0]};{line[1]};{line[2]};{line[3]}\n")
        return True

    #Stops the function when it is called by modify cart to modify item quantity only.
    if fileName == None:
        return False

    #Add new item into cart if not in cart yet
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
------------------------------
Pages are split into 6 sections:
1. Customer Page
2. Admin Page
3. Guest Page
4. Register and Login Page
5. Exit and Main Page
6. Program Start
'''
#region Customer Page
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
                print("-"*70)
                for foodItem in range(6,len(orderRecord),1):
                    foodDetails = orderRecord[foodItem].strip().split(">")
                    print("{:<9}{:<40}{:<15}{:<7}".format(foodDetails[0],foodDetails[1],foodDetails[2],foodDetails[3]))

                u_insertLine("_",False)
                u_insertLine("x")
                print("\n\n\n")

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
            u_popup("ORDERED SUCCESSFULLY")
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
            if quantity == "BACK":
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

#endregion

#region Admin Page
def pg_adminAdd3(cat_name_price):
    while True:
        clearConsole()
        u_insertHeader(f"COMFIRM ADD TO '{cat_name_price[0]}'")
        print(f"\n", " " * 18, f"new item name  : {cat_name_price[1]} \n", " " * 18,
              f"new item price : RM {cat_name_price[2]}")

        print("\n\n" + " " * 8 + "[CONFIRM] to confirm" + " " * 16 + "[REDO] to re-enter")
        print(" " * 8 + "   [BACK] to back\n")
        print("-" * 70)

        uinput_comfirmation = input("Select your option : ")
        if uinput_comfirmation.upper() == "CONFIRM":
            newid_index = db_getNewID(cat_name_price[0] + ".txt")
            newlist = [newid_index[0], cat_name_price[1], cat_name_price[2]]
            list1 = []
            with open(cat_name_price[0] + ".txt", "r") as readfile:
                for data in readfile:
                    list1.append(data.strip().split(";"))
            list1.insert(int(newid_index[1]), newlist)
            db_overwriteRecord(cat_name_price[0] + ".txt", list1)
            u_popup("[SUCCESS] item added")
            break
        elif uinput_comfirmation.upper() == "REDO":
            return True
        elif uinput_comfirmation.upper() == "BACK":
            break
        else:
            u_popup("Please enter a proper value")
            continue

def pg_adminAdd2(category):
    '''
    Page to insert new name and price
    '''
    while True:
        clearConsole()
        u_insertHeader(f"ADD TO {category}")
        uinput_newname = input(" " * 22 + "new item name  : ")
        if uinput_newname.upper() == "BACK":
            break
        if ';' in uinput_newname or '>' in uinput_newname:
            u_popup("Do not insert ';' and '>' within item name")
            continue

        uinput_newprice = input(" " * 22 + "new item price : RM ")
        if uinput_newprice.lower() == "back":
            break

        try:
            check_price = round(float(uinput_newprice), 2)
            check_price = "{:,.2f}".format(check_price)
        except:
            u_popup("Please enter a proper value")
            continue

        cat_name_price = [category, uinput_newname, check_price]
        redo = pg_adminAdd3(cat_name_price)
        if redo:
            continue
        else:
            break

def pg_adminAdd1():
    '''
    Select food category to add page
    '''
    while True:
        clearConsole()
        u_insertHeader("ADD")
        print("Select Category".center(70, " "))
        print("\n", " " * 26, "[1]    Local")
        print(" " * 27, "[2]    Western")
        print(" " * 27, "[3]    Dessert")
        print(" " * 27, "[4]    Beverage")
        print(" " * 24, "[BACK]    Back\n")
        print("\n", "=" * 70)

        uinput_cat = input("Enter your selection: ")
        if uinput_cat == "1":
            selected_cat = "Local"
        elif uinput_cat == "2":
            selected_cat = "Western"
        elif uinput_cat == "3":
            selected_cat = "Dessert"
        elif uinput_cat == "4":
            selected_cat = "Beverage"
        elif uinput_cat.upper() == "BACK":
            break
        else:
            u_popup("Please insert a proper value")
            continue

        pg_adminAdd2(selected_cat)

def pg_adminModify3(cat_list, foodidx, uinput_modifiedname, checked_price, category):
    '''
    Confirm the modification to item page
    '''
    while True:
        clearConsole()
        u_insertHeader(f"Confirm to MODIFY '{cat_list[foodidx][0]}'")
        print(" " * 20, f"initial name  : {cat_list[foodidx][1]}")
        print(" " * 20, f"initial price : RM {cat_list[foodidx][2]}\n")
        print(" " * 24, f"new name  : {uinput_modifiedname}")
        print(" " * 24, f"new price : RM {checked_price}\n")
        print("_" * 70, "\n")
        print("Select an Option".center(70, " "))
        print("\n" + " " * 8 + "[CONFIRM] to confirm" + " " * 16 + "[REDO] to re-enter")
        print(" " * 8 + "   [BACK] to back\n")
        print("=" * 70)
        uinput_decision = input("Input your decision : ")

        if uinput_decision.upper() == "BACK":
            return True
        elif uinput_decision.upper() == "REDO":
            return True
        elif uinput_decision.upper() == "CONFIRM":
            cat_list[foodidx].pop(1)
            cat_list[foodidx].insert(1, uinput_modifiedname)
            cat_list[foodidx].pop(2)
            cat_list[foodidx].insert(2, checked_price)
            db_overwriteRecord(category + ".txt", cat_list)
            u_popup("[SUCCESS] item modified")
            return False
        else:
            u_popup("Please enter a proper value")

def pg_adminModify(cat_list, foodidx,category):
    '''
    Confirm to modify food item
    '''
    while True:
        clearConsole()
        u_insertHeader(f"MODIFY {cat_list[foodidx][1]}")
        uinput_modifiedname = input(" " * 23 + "new name  : ")

        # Validation check
        if ';' in uinput_modifiedname or '>' in uinput_modifiedname:
            u_popup("[ERROR] invalid symbol ';' or '>'")
            continue

        if uinput_modifiedname.upper() == "BACK":
            break
        uinput_modifiedprice = input(" " * 23 + "new price : RM ")
        if uinput_modifiedprice.upper() == "BACK":
            break

        try:
            check_price = float(uinput_modifiedprice)
            check_price = "{:,.2f}".format(check_price)
        except:
            u_popup("[ERROR] insert proper price")
            continue

        redo = pg_adminModify3(cat_list, foodidx, uinput_modifiedname, check_price, category)

        if redo:
            continue
        elif not redo:
            return True
        else:
            break

def pg_adminDelete(cat_list, foodidx, category):
    '''
    Delete selected food item and confirm to delete
    '''
    while True:
        clearConsole()
        print("\n" + f"Confirm to delete '{cat_list[foodidx][1]}'".center(70, " "))
        print("\n" + " " * 8 + "[CONFIRM] to confirm" + " " * 16 + "[BACK] to back")
        uinput_confirmation = input("\nInput your decision : ")
        if uinput_confirmation.upper() == "BACK":
            return True
        elif uinput_confirmation.upper() == "CONFIRM":
            location = 0
            for findidx in cat_list:
                if cat_list[foodidx][0] in findidx:
                    break
                else:
                    location += 1
            cat_list.pop(location)
            with open(f"{category}" + ".txt", "w") as overwritefile:
                for overwriteitem in cat_list:
                    overwritefile.write(f"{overwriteitem[0]};{overwriteitem[1]};{overwriteitem[2]}\n")
            u_popup("[SUCCESS] item deleted")
            break
        else:
            u_popup("Please insert a proper value")
            continue

def pg_adminModify2(category, foodid):
    '''
    Ask user whether to modify or delete the food item
    '''
    while True:
        clearConsole()
        u_insertHeader(foodid)
        cat_list = []
        with open(category + ".txt", "r") as readfile:
            for appendtolist in readfile:
                cat_list.append(appendtolist.strip().split(";"))

        foodidx = 0
        for food in cat_list:
            if foodid in food:
                break
            else:
                foodidx += 1

        print(" " * 20, f"Original Name  : {cat_list[foodidx][1]}")
        print(" " * 20, f"Original Price : RM {cat_list[foodidx][2]}\n")
        print("_" * 70)

        print("\n\n" + " " * 8 + " [DELETE] to delete" + " " * 15 + "[MODIFY] to modify")
        print(" " * 8 + "   [BACK] to back\n")
        print("-" * 70)


        uinput_selection = input("Input your decision : ")
        if uinput_selection.upper() == "DELETE":
            cnt = pg_adminDelete(cat_list, foodidx, category)
            if cnt:
                continue
            else:
                break


        elif uinput_selection.upper() == "MODIFY":
            pagebreak = pg_adminModify(cat_list, foodidx,category)
            if pagebreak:
                break
            else:
                continue
        elif uinput_selection.upper() == "BACK":
            break
        else:
            u_popup("Please enter a proper value")
            continue

def pg_adminModify1():
    '''
    Display all records of food item that can be modified and ask for food id to be modifeied
    '''
    while True:
        clearConsole()
        db_displayAllFoodRecord()
        uinput_itemtochange = input("Input Food ID to delete / modify: ")

        try:
            if uinput_itemtochange.upper() == "BACK":
                break
            elif uinput_itemtochange[0].upper() == "L":
                category = "Local"
            elif uinput_itemtochange[0].upper() == "W":
                category = "Western"
            elif uinput_itemtochange[0].upper() == "D":
                category = "Dessert"
            elif uinput_itemtochange[0].upper() == "B":
                category = "Beverage"
            else:
                u_popup("[ERROR] Food ID invalid")
                continue
        except:
            u_popup("[ERROR] Food ID invalid")
            continue

        if db_searchRecord(category + ".txt", uinput_itemtochange):
            pg_adminModify2(category, uinput_itemtochange)
        elif not db_searchRecord(category + ".txt", uinput_itemtochange):
            u_popup("[ERROR] Food ID invalid")
            continue

def pg_adminDisplay():
    while True:
        clearConsole()
        u_insertHeader("DISPLAY")
        print("Select to display".center(70, " "))
        print("\n" + " " * 24, "[1]    All categories")
        print(" " * 24, "[2]    ALL food item")
        print(" " * 24, "[3]    Order list")
        print(" " * 24, "[4]    Payment list")
        print(" " * 21, "[BACK]    Back\n")
        print("_" * 70)
        uinput_display = input("Input your decision : ")

        if uinput_display == "1":
            clearConsole()
            u_insertHeader("ALL CATEGORIES", False)
            print(" " * 28, "1. LOCAL")
            print(" " * 28, "2. WESTERN")
            print(" " * 28, "3. DESSERT")
            print(" " * 28, "4. BEVERAGE\n")
            print("_" * 70)
            print("\n" + "[ENTER] to back".center(70, " "))
            input(" ")
            continue

        elif uinput_display == "2":
            clearConsole()
            db_displayAllFoodRecord()
            print("[ENTER] to back".center(70, " ") + "\n")
            input("")
            continue

        elif uinput_display == "3":
            clearConsole()
            u_insertHeader("ORDER LIST", False)
            print("\n")
            orderlist = []
            with open("order.txt", "r") as readOrder:
                for orderdetails in readOrder:
                    orderlist.append(orderdetails.strip().split(";"))

            for fooddetails in orderlist:
                print("#" * 70)
                print(f"Order ID      : {fooddetails[0]}")
                print(f"Customer Name : {fooddetails[1]}")
                print(f"Total Ordered : {fooddetails[5]}\n\n")
                print("{:<8} {:<45} {:<5} {:<9}".format("FOODID", "FOOD NAME", "QTY", "PRICE(RM)"))
                print("{:<8} {:<45} {:<5} {:<9}".format("_" * 6, "_" * 43, "_" * 3, "_" * 9))

                for foodID_name_price in fooddetails[6:]:
                    food = foodID_name_price.split(">")
                    print("{:<8} {:<45} {:<5} {:<9}".format(food[0], food[1], food[3], food[2]))

                print("\n" + "=" * 70)
                print("\n\n\n\n")

            print("[ENTER] to Back".center(70, " "))
            input("")

        elif uinput_display == "4":
            clearConsole()
            u_insertHeader("PAYMENT LIST", False)
            print("\n")
            paymentlist = []
            with open("order.txt", "r") as readOrder:
                for orderdetails in readOrder:
                    paymentlist.append(orderdetails.strip().split(";"))

            for paymentdetails in paymentlist:
                print(f"Order ID      : {paymentdetails[0]}")
                print(f"Customer Name : {paymentdetails[1]}")
                print(f"Total Fee     : RM {paymentdetails[2]}")
                print(f"Address       : {paymentdetails[3]}")
                print(f"Date & Time   : {paymentdetails[4]}\n\n\n")

            print("[ENTER] to Back")
            input("")


        elif uinput_display.upper() == "BACK":
            break
        else:
            u_popup("Please insert a proper value")
            continue

def pg_adminSearch_order():
    while True:
        clearConsole()
        u_insertHeader("SEARCH 'CUSTOMER ORDER'")
        try:
            uinput_orderid = input("Input Order ID to search : ")
            if uinput_orderid.upper() == "BACK":
                break
            search = db_searchRecord("Order.txt", uinput_orderid, True)

            print("\n\n" + "*" * 70)
            print(f"\nOrder ID      : {search[0]}")
            print(f"Customer Name : {search[1]}")
            print(f"Total Ordered : {search[5]}\n\n")
            print("{:<8} {:<45} {:<5} {:<9}".format("FOODID", "FOOD NAME", "QTY", "PRICE(RM)"))
            print("{:<8} {:<45} {:<5} {:<9}".format("_" * 6, "_" * 43, "_" * 3, "_" * 9))

            for foodID_name_price in search[6:]:
                food = foodID_name_price.split(">")
                print("{:<8} {:<45} {:<5} {:<9}".format(food[0], food[1], food[3], food[2]))
            print("\n" + "*" * 70 + "\n\n")

        except:
            u_popup("[ERROR] Order ID does not exist")
            continue

        print("Select".center(70, " "), "\n")
        print(" " * 9 + "[REDO] to re-search" + " " * 16 + "[BACK] to back" + "\n")
        print("-" * 70)
        uinput_selection = input("Input a value : ")

        if uinput_selection.upper() == "REDO":
            continue
        elif uinput_selection.upper() == "BACK":
            break
        else:
            u_popup("INSERT PROPER VALUE", 1.5)
            continue


def pg_adminSearch_payment():
    while True:
        clearConsole()
        u_insertHeader("SEARCH 'Customer Payment'")

        try:
            uinput_orderid = input("Input Order ID to search : ")
            if uinput_orderid.upper() == "BACK":
                break
            search = db_searchRecord("Order.txt", uinput_orderid, True)

            print(f"\n\nOrder ID      : {search[0]}")
            print(f"Customer Name : {search[1]}")
            print(f"Total Fee     : RM {search[2]}")
            print(f"Address       : {search[3]}")
            print(f"Date & Time   : {search[4]}\n\n\n")

        except:
            u_popup("[ERROR] Order ID does not exist")
            continue

        print("-" * 70)
        print("\n" + "Select".center(70, " "), "\n")
        print(" " * 9 + "[REDO] to re-search" + " " * 16 + "[BACK] to back" + "\n")
        print("-" * 70)
        uinput_selection = input("Input a value : ")

        if uinput_selection.upper() == "REDO":
            continue
        elif uinput_selection.upper() == "BACK":
            break
        else:
            u_popup("[ERROR] input proper value")

def pg_adminSearch():
    while True:
        clearConsole()
        u_insertHeader("SEARCH")
        print("Select to search".center(70, " "), "\n")
        print(" " * 24, "[1]  Customer Order")
        print(" " * 24, "[2]  Customer Payment\n")
        print("_" * 70)
        uinput_search = input("Input your decision : ")

        if uinput_search.upper() == "BACK":
            break
        elif uinput_search == "1":
            pg_adminSearch_order()
        elif uinput_search == "2":
            pg_adminSearch_payment()
        else:
            u_popup("[ERROR] Please input proper value")
            continue

def pg_adminMain():
    while True:
        clearConsole()
        u_insertHeader("ADMIN MAIN PAGE")
        print("Select to".center(70, " "))
        print("\n" + " " * 26, "[1]    Add New Item")
        print(" " * 26, "[2]    Modify Menu")
        print(" " * 26, "[3]    Display")
        print(" " * 26, "[4]    Search")
        print(" " * 23, "[BACK]    Back\n")
        print("\n", "=" * 70)

        uinput_cat = input("Enter your selection: ")
        if uinput_cat == "1":
            pg_adminAdd1()
        elif uinput_cat == "2":
            pg_adminModify1()
        elif uinput_cat == "3":
            pg_adminDisplay()
        elif uinput_cat == "4":
            pg_adminSearch()
        elif uinput_cat.upper() == "BACK":
            break
        else:
            u_popup("Please insert a proper value")
            continue

#endregion

#region Guest Page
def pg_guest():
    while True:
        clearConsole()
        u_insertHeader("LOGIN AS GUEST")
        db_displayAllFoodRecord()

        print("REGISTER AN ACCOUNT TO PLACE ORDER".center(70, " "), "\n")
        print(" " * 9 + "[REGISTER] to register" + " " * 16 + "[BACK] to back" + "\n")
        print("-" * 70)
        uinput_selection = input("Input a value : ")

        if uinput_selection.upper() == "REGISTER":
            pg_register()
            break
        elif uinput_selection.upper() == "BACK":
            break
        else:
            u_popup("[ERROR] input proper value")
            continue
#endregion

#region Register and Login Page
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
        '''
        User login / admin login page
        Admin account is set and cannot be created
        Admin - username: Admin password: SystemAdmin123
        '''
        clearConsole()
        #Display
        u_insertHeader("LOGIN", False)

        username = input(" "*20+ "Username: ")
        password = input(" "*20+ "Password: ")

        u_insertLine()

        #Check for admin
        if username == 'Admin' and password == 'SystemAdmin123':
            pg_adminMain()
            break

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
#endregion

#region Exit and Main Page
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
        elif decision == 'GUEST':
            pg_guest()
        else:
            u_popup("[ERROR] INVALID INPUT DECISION!", 1.5)

# endregion

#region Program Start
#PROGRAM STARTS HERE
clearConsole()

setupDB()
pg_main()

# u_constructButton(3, [["RETURN", "Return"],["HOME","To Home"],["PAY","Payment"],["HELLO","Hello to you"],["ADDRESS", "Address"]])






#endregion
#endregion