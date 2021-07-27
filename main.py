import os
import time
#TODO: must make sure all files are there. Ensure files exist first

#Receive - RC | Return - RT

# region Utility
def clearConsole():
    cmd = "clear"
    if os.name in ('dos', 'nt'):
        cmd = "cls"

    os.system(cmd)
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
#UTILITY
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

#RT: new ID
def db_getNewID(fileName):
    list = db_returnList(fileName)
    gapNumber = -1
    print(list[0])
    # if gapNumber < int(list[0]):
    #     gapNumber = line

    return gapNumber

print(db_getNewID("Beverage.txt"))



#RC: 1d list
def db_appendRecord(fileName, list): #append one dimensional list without the id

    with open(fileName, 'a') as file:
        file.write(list_ToSingleString(list))

#for each string available write into the file


#-----------END UTILITY------------
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

db_displayAllFoodRecord()
    #TODO do
def db_registerAccount(username, password): #return false if can't register
    # ADMIN CHECK
    if username == "admin":
        return False

    #Checks if value exist
    if db_searchRecord("Accounts.txt", username):
        return False

    account = [username,password]
    db_addRecord('Accounts.txt', account)
    return True

# endregion
def main():
    print("hey")

#
# if __name__ == '__main__':
#     main()