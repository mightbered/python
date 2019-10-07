#ATM System
#Update databases in two functions for insurance
#Create Find Function for easy indexing
def find(string, char):
    indices = []
    for i in range(0, len(string)):
        if string[i] == char:
            indices.append(i)
    return indices

#Initialize databases
f = open("database.txt", "r")
data = f.readlines()
nameDatabase = {}
balDatabase = {}
pinDatabase = []

for i in range(0, len(data)):
    #Remove newlines
    data[i] = data[i].strip()
    
    #First line in text file was used as a comment
    if i == 0:
        pass
    else:
        indices = find(data[i], ":")
        
        #Format is NAME:PIN:BAL, start at 0, end at first ":"  
        name = data[i][:indices[0]]

        #For PIN, start at first ":" + 1, end at second ":"
        pin = data[i][indices[0] + 1: indices[1]]

        #For balance, start at second ":" + 1, end at end
        bal = data[i][indices[1] + 1:]

        #Append to dictionaries and list
        nameDatabase[pin] = name
        balDatabase[pin] = bal
        pinDatabase.append(pin)

#Create login function
def login():
    print("*** ATM MACHINE ***")
    
    #Loop made to ensure user is inputting correct info
    while True:
        pin = input("Enter your PIN: ")
        if pin in nameDatabase:
            print("PIN found... loggin in")
            name = nameDatabase[pin]
            bal = balDatabase[pin]
            print("\n" * 1)
            break
        else:
            print("PIN not found.")
    #Returning account details of entered PIN
    return name, pin, bal

#Create menu function
def menu(name):
    print("Welcome {}!".format(name))
    print("What would you like to do?")
    print("1. Balance Inquiry")
    print("2. Withdraw")
    print("3. Deposit")
    print("4. Change PIN")
    print("5. Transfer Funds")
    print("6. Exit")
    while True:
        option = input("Enter selection: ")

        #Ensuring user is inputing within choices
        if option not in range(1, 7) and len(option) > 1:
            print("Error. Please enter a valid selection. ")
        else:
            print("\n" * 9)
            return option

#Create action function
def action(option, name, pin, bal):
    pin = pin
    if option == "1":
        print("BALANCE INQUIRY")
        print("Current balance is {}.".format(bal))
        redo(name, pin)
    elif option == "2":
        print("WITHDRAW")
        print("Current balance is {}.".format(bal))
        if int(bal) <= 500:
            print("Account within minimum balance, cannot withdraw.")
            redo(name, pin)
        else:
            while True:
                withdraw = int(input("Enter amount: "))
                if withdraw > int(bal):
                    print("Error. Amount higher than balance.")
                else:
                    bal = int(bal) -  withdraw
                    balDatabase[pin] = str(bal)
                    print("Your account is now {}.".format(bal))
                    redo(name, pin)
    elif option == "3":
        print("DEPOSIT")
        print("Current balance is {}.".format(bal))
        deposit = int(input("Enter amount: "))
        bal = int(bal) + deposit
        balDatabase[pin] = str(bal)
        print("Your account is now {}.".format(bal))
        redo(name, pin)
    elif option == "4":
        print("CHANGE PIN")
        while True:
            oldpin = input("Enter old PIN: ")
            if oldpin == pin:
                print("Changing PIN for {}".format(nameDatabase[oldpin]))
                while True:
                    newpin = input("Enter new PIN: ")
                    verpin = input("Verify PIN: ")
                    
                    #Removing old PIN from database
                    if oldpin in pinDatabase:
                        pinDatabase.remove(oldpin)
                    
                    #Verifying if PIN is not another user's PIN and PIN is numerical
                    if int(newpin.isdigit()) and newpin == verpin and newpin not in pinDatabase:
                        nameDatabase[newpin] = nameDatabase.pop(oldpin)
                        balDatabase[newpin] = balDatabase.pop(oldpin)
                        pin = newpin
                        print("Change successful!!!")
                        redo(name, pin)
                    else:
                        print("Error. Either PIN is not numerical or PIN does not match or PIN exists.")
            else:
                print("Incorrect PIN.")
    elif option == "5":
        print("TRANSFER FUNDS")
        while True:
            transferAcc = input("Enter account name: ")
            if transferAcc.lower() in nameDatabase[pin].lower():
                    print("Error. Your are transfering to your own account.")
            else:
                for i in nameDatabase:
                    if transferAcc.lower() in nameDatabase[i].lower():
                        print("Account found!")
                        print("{}".format(nameDatabase[i]))
                        while True:
                            confirm = input("Is this the account? (Y/N) ")
                            if confirm.lower() == "y":
                                while True:
                                    transferAmt = int(input("Enter amount: "))
                                    if transferAmt > int(balDatabase[pin]):
                                        print("Error. Amount larger than balance")
                                    else:
                                        balDatabase[i] = transferAmt + int(balDatabase[i])
                                        balDatabase[pin] = int(balDatabase[pin]) - transferAmt
                                        balDatabase[i] = str(balDatabase[i])
                                        balDatabase[pin] = str(balDatabase[pin])
                                        print("Transfer Successful!!!")
                                        print("Your current balance is now {}.".format(balDatabase[pin]))
                                        redo(name, pin)
                    
                print("Account not found!!!")
    elif option == "6":
        print("\n" * 9)
        print("Exiting...")
        #Update databases
        f = open("database.txt", "w")
        f.write("#FORMAT NAME:PIN:BAL\n")
        for i in nameDatabase:
            f.write("{}:{}:{}\n".format(nameDatabase[i], i, balDatabase[i]))
        f.close()
        main()

#Create redo function
def redo(name, pin):
    while True:
        choice = input("Return to the main menu? (Y/N) ")
        if choice.lower() in ["y","n"]:
            if choice.lower() == "y":
                print("\n" * 4)
                option = menu(name)
                action(option, name, pin, bal)
            elif choice.lower() == "n":
                #Update databases
                f = open("database.txt", "w")
                f.write("#FORMAT NAME:PIN:BAL\n")
                for i in nameDatabase:
                    f.write("{}:{}:{}\n".format(nameDatabase[i], i, balDatabase[i]))
                f.close()
                main()
        else:
            print("Error. Please enter a valid answer.")

#Creating main function
def main():
    name, pin, bal = login()
    option = menu(name)
    action(option, name, pin, bal)

main()

