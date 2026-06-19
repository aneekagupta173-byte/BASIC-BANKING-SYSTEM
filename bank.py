import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "practice.txt")


def check_balance():
    account_number = input("Enter your account number: ")
    with open(DATA_FILE, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) < 2:
                continue
            account = parts[0].strip()
            balance = parts[-1].strip()
            if account == account_number:
                print(f"Your balance is: {balance}")
                return
    print("Account number not found.")
    

def open_account():
    account_number = input("Enter a new account number: ")
    initial_balance = input("Enter initial balance: ")
    name = input("Enter your name: ")
    with open(DATA_FILE, "a") as file:
        file.write(f"{account_number},{name},{initial_balance}\n")
    print("Account opened successfully.")


def money():
    print("DO YOU WANT TO CREDIT OR DEBIT?")
    choice = int(input("Enter 'credit' = 1 or 'debit' = 2: "))
    if choice == 1:
        account_number = input("Enter your account number: ")
        amount = float(input("Enter amount to credit: "))
        updated = False
        with open(DATA_FILE, "r") as file:
            lines = file.readlines()
        with open(DATA_FILE, "w") as file:
            for line in lines:
                account, name, balance = line.strip().split(",")
                if account == account_number:
                    new_balance = float(balance) + amount
                    file.write(f"{account},{name},{new_balance}\n")
                    print(f"Amount credited. New balance is: {new_balance}")
                    updated = True
                else:
                    file.write(line)
        if not updated:
            print("Account number not found.")
    elif choice == 2:
        account_number = input("Enter your account number: ")
        amount = float(input("Enter amount to debit: "))
        updated = False
        with open(DATA_FILE, "r") as file:
            lines = file.readlines()
        with open(DATA_FILE, "w") as file:
            for line in lines:
                account, name, balance = line.strip().split(",")
                if account == account_number:
                    if float(balance) >= amount:
                        new_balance = float(balance) - amount
                        file.write(f"{account},{name},{new_balance}\n")
                        print(f"Amount debited. New balance is: {new_balance}")
                    else:
                        print("Insufficient funds.")
                        file.write(line)
                    updated = True
                else:
                    file.write(line)
        if not updated:
            print("Account number not found.")
    else:
        print("Invalid choice. Please enter 'credit' or 'debit'.")

print("Welcome to the Banking System")
print("How can we help you today?")

while True: 
    fun = int(input("Enter 'check balance' = 1 , 'open account' = 2, or 'credit/debit' = 3: "))
    if fun == 1:
        check_balance()
    elif fun == 2:
        open_account()
    elif fun == 3:
        money()
    a = input("Do you want to continue? (yes =1/no = 2): ")
    if a == '2':
        print("Thank you for using our banking system. Goodbye!")
        break
