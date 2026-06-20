import os  # import the os module for path operations

DATA_FILE = os.path.join(os.path.dirname(__file__), "practice.txt")  # path to the data file inside the same folder
import os  # duplicate import (harmless) kept to preserve original order
import tkinter as tk  # import tkinter with alias tk for GUI
from tkinter import messagebox  # import messagebox for popup dialogs

DATA_FILE = os.path.join(os.path.dirname(__file__), "practice.txt")  # ensure DATA_FILE is set (redefined)

root = tk.Tk()  # create the main application window
root.title("Banking System")  # set the window title
root.geometry("420x320")  # set the default window size


def show_frame(frame):  # function to switch visible frames
    for f in (home_frame, check_frame, open_frame, money_frame, transfer_frame):  # iterate all frames
        f.pack_forget()  # hide each frame
    frame.pack(fill="both", expand=True)  # show the requested frame


# Frames
home_frame = tk.Frame(root, padx=10, pady=10)  # main menu frame
check_frame = tk.Frame(root, padx=10, pady=10)  # check-balance frame
open_frame = tk.Frame(root, padx=10, pady=10)  # open-account frame
money_frame = tk.Frame(root, padx=10, pady=10)  # credit/debit frame
transfer_frame = tk.Frame(root, padx=10, pady=10)  # transfer frame

# --- Home ---
tk.Label(home_frame, text="Welcome to the Banking System", font=("Arial", 14)).pack(pady=8)  # title label
tk.Button(home_frame, text="1 - Check Balance", width=20, command=lambda: show_frame(check_frame)).pack(pady=4)  # button to go to check frame
tk.Button(home_frame, text="2 - Open Account", width=20, command=lambda: show_frame(open_frame)).pack(pady=4)  # button to go to open frame
tk.Button(home_frame, text="3 - Credit/Debit", width=20, command=lambda: show_frame(money_frame)).pack(pady=4)  # button to go to money frame
tk.Button(home_frame, text="4 - Transfer Money", width=20, command=lambda: show_frame(transfer_frame)).pack(pady=4)  # button to go to transfer frame
tk.Label(home_frame, text="").pack(pady=6)  # spacer label

# --- Check Balance Frame ---
tk.Label(check_frame, text="Check Balance", font=("Arial", 12)).pack(pady=6)  # heading for check frame
tk.Label(check_frame, text="Enter Account Number").pack()  # label for account number input
check_acc_entry = tk.Entry(check_frame)  # entry widget to input account number
check_acc_entry.pack(pady=4)  # place the entry in the layout
check_result = tk.Label(check_frame, text="")  # label to show results or messages
check_result.pack(pady=4)  # place the result label

def check_balance_action():  # action invoked when checking balance
    acc = check_acc_entry.get().strip()  # read account number from entry and trim whitespace
    if not acc:  # if no value provided
        check_result.config(text="Enter an account number")  # prompt user
        return  # stop processing
    try:
        with open(DATA_FILE, "r") as f:  # open the data file for reading
            for line in f:  # iterate each line (account record)
                parts = line.strip().split(",")  # split CSV fields
                if parts and parts[0].strip() == acc:  # match account number
                    check_result.config(text=f"Balance: {parts[-1].strip()}")  # show the balance
                    return  # done
        check_result.config(text="Account number not found.")  # not found message
    except FileNotFoundError:
        check_result.config(text="Data file not found.")  # show file-missing message

tk.Button(check_frame, text="Check", command=check_balance_action).pack(pady=4)  # button to trigger balance check
tk.Button(check_frame, text="Back", command=lambda: show_frame(home_frame)).pack()  # back to home


# --- Open Account Frame ---
tk.Label(open_frame, text="Open Account", font=("Arial", 12)).pack(pady=6)  # heading for open account
tk.Label(open_frame, text="Account number").pack()  # label for account field
open_acc_entry = tk.Entry(open_frame)  # entry for new account number
open_acc_entry.pack()  # place account entry
tk.Label(open_frame, text="Name").pack()  # label for name field
open_name_entry = tk.Entry(open_frame)  # entry for name
open_name_entry.pack()  # place name entry
tk.Label(open_frame, text="Initial balance").pack()  # label for balance field
open_bal_entry = tk.Entry(open_frame)  # entry for initial balance
open_bal_entry.pack()  # place balance entry

def open_account_action():  # action to create a new account
    acc = open_acc_entry.get().strip()  # get account number
    name = open_name_entry.get().strip()  # get name
    bal = open_bal_entry.get().strip()  # get initial balance
    if not acc or not name or not bal:  # validate inputs
        messagebox.showinfo("Input needed", "Fill all fields")  # show info dialog
        return  # abort
    try:
        float(bal)  # validate that balance is a number
    except ValueError:
        messagebox.showerror("Error", "Initial balance must be a number")  # show error if invalid
        return
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)  # ensure directory exists
    with open(DATA_FILE, "a") as f:  # append the new record to the data file
        f.write(f"{acc},{name},{bal}\n")  # write CSV line without extra blank lines
    messagebox.showinfo("Success", "Account opened successfully")  # confirmation dialog
    open_acc_entry.delete(0, tk.END)  # clear account entry
    open_name_entry.delete(0, tk.END)  # clear name entry
    open_bal_entry.delete(0, tk.END)  # clear balance entry
    show_frame(home_frame)  # return to the home frame

tk.Button(open_frame, text="Open Account", command=open_account_action).pack(pady=6)  # button to open account
tk.Button(open_frame, text="Back", command=lambda: show_frame(home_frame)).pack()  # back button


# --- Money Frame ---
tk.Label(money_frame, text="Credit / Debit", font=("Arial", 12)).pack(pady=6)  # heading for money operations
tk.Label(money_frame, text="Account number").pack()  # label for account input
money_acc_entry = tk.Entry(money_frame)  # entry for account to operate on
money_acc_entry.pack()  # place account entry
tk.Label(money_frame, text="Amount").pack()  # label for amount input
money_amount_entry = tk.Entry(money_frame)  # entry for amount
money_amount_entry.pack()  # place amount entry
mode_var = tk.IntVar(value=1)  # variable to select credit (1) or debit (2)
tk.Radiobutton(money_frame, text="Credit", variable=mode_var, value=1).pack()  # credit option
tk.Radiobutton(money_frame, text="Debit", variable=mode_var, value=2).pack()  # debit option
money_result = tk.Label(money_frame, text="")  # label to show results/messages
money_result.pack(pady=4)  # place result label

def money_action():  # perform credit or debit
    acc = money_acc_entry.get().strip()  # read account
    amt_text = money_amount_entry.get().strip()  # read amount text
    if not acc or not amt_text:  # validate inputs
        money_result.config(text="Fill account and amount")  # prompt user
        return
    try:
        amount = float(amt_text)  # parse amount as float
    except ValueError:
        money_result.config(text="Amount must be a number")  # show error
        return
    updated = False  # flag to track whether an account was updated
    try:
        with open(DATA_FILE, "r") as f:  # read all lines from data file
            lines = f.readlines()
    except FileNotFoundError:
        money_result.config(text="Data file not found.")  # if file missing, show message
        return
    with open(DATA_FILE, "w") as f:  # reopen file for writing (we will rewrite all lines)
        for line in lines:  # iterate existing records
            parts = line.strip().split(",")  # split CSV fields
            if len(parts) < 3:  # if record doesn't have expected fields
                f.write(line)  # write it back unchanged
                continue  # skip processing
            account = parts[0].strip()  # existing account number
            name = parts[1].strip()  # existing name
            balance = float(parts[-1].strip())  # existing balance as float
            if account == acc:  # found matching account
                if mode_var.get() == 1:  # credit mode
                    balance += amount  # add amount
                    money_result.config(text=f"Credited. New balance: {balance}")  # show new balance
                else:  # debit mode
                    if balance >= amount:  # check funds
                        balance -= amount  # subtract amount
                        money_result.config(text=f"Debited. New balance: {balance}")  # show new balance
                    else:
                        money_result.config(text="Insufficient funds")  # show insufficient message
                        f.write(line)  # write original line back
                        continue  # skip writing updated line
                f.write(f"{account},{name},{balance}\n")  # write updated record
                updated = True  # mark updated
            else:
                f.write(line)  # write non-matching record unchanged
    if not updated:
        money_result.config(text="Account number not found.")  # no account matched
    else:
        money_acc_entry.delete(0, tk.END)  # clear account entry
        money_amount_entry.delete(0, tk.END)  # clear amount entry

tk.Button(money_frame, text="Apply", command=money_action).pack(pady=6)  # apply button for money ops
tk.Button(money_frame, text="Back", command=lambda: show_frame(home_frame)).pack()  # back to home


tk.Label(transfer_frame, text="Transfer Money", font=("Arial", 12)).pack(pady=6)  # heading for transfer frame
tk.Label(transfer_frame, text="From Account").pack()  # label for source account
transfer_from_entry = tk.Entry(transfer_frame)
transfer_from_entry.pack()
tk.Label(transfer_frame, text="To Account").pack()  # label for destination account
transfer_into_entry = tk.Entry(transfer_frame) 
transfer_into_entry.pack()
tk.Label(transfer_frame, text="Amount").pack()  # label for transfer amount
transfer_amount_entry = tk.Entry(transfer_frame)
transfer_amount_entry.pack()
transfer_result = tk.Label(transfer_frame, text="")  # label to show transfer results
transfer_result.pack()



def transfer_action():  # action to transfer money between accounts
    from_acc = transfer_from_entry.get().strip()  # source account
    to_acc = transfer_into_entry.get().strip()  # destination account
    amt_text = transfer_amount_entry.get().strip()  # amount to transfer
    if not from_acc or not to_acc or not amt_text:  # validate inputs
        transfer_result.config(text="Fill all fields")  # prompt user
        return
    try:
        amount = float(amt_text)  # parse amount as float
    except ValueError:
        transfer_result.config(text="Amount must be a number")  # show error
        return
    updated_from = False  # flag for source account update
    updated_to = False  # flag for destination account update
    try:
        with open(DATA_FILE, "r") as f:  # read all lines from data file
            lines = f.readlines()
    except FileNotFoundError:
        transfer_result.config(text="Data file not found.")  # if file missing, show message
        return
    new_lines = []
    source_balance = None          
    for line in lines:  # iterate existing records
        if not line.strip():  # preserve blank lines if any
            new_lines.append(line)
            continue
        parts = line.strip().split(",")  # split CSV fields
        if len(parts) < 3:  # if record doesn't have expected fields
            new_lines.append(line)
            continue
        account = parts[0].strip()  # existing account number
        name = parts[1].strip()  # existing name
        balance = float(parts[-1].strip())  # existing balance as float
        if account == from_acc:  # found source account
            if balance < amount:  # check funds
                transfer_result.config(text="Insufficient funds in source account")  # show insufficient message
                return
            balance -= amount  # subtract amount for transfer
            source_balance = balance
            updated_from = True  # mark source updated
            new_lines.append(f"{account},{name},{balance}\n")  # write updated source record
        elif account == to_acc:  # found destination account
            balance += amount  # add amount for transfer
            updated_to = True  # mark destination updated
            new_lines.append(f"{account},{name},{balance}\n")  # write updated destination record
        else:
            new_lines.append(line)  # write unchanged record
    if not updated_from or not updated_to:  # ensure both ends exist
        transfer_result.config(text="Source or destination account not found.")
        return
    with open(DATA_FILE, "w") as f:  # overwrite file with updated records
        f.writelines(new_lines)
    transfer_result.config(text=f"Transferred {amount}. New source balance: {source_balance}")
    transfer_from_entry.delete(0, tk.END)
    transfer_into_entry.delete(0, tk.END)
    transfer_amount_entry.delete(0, tk.END)
tk.Button(transfer_frame, text="Transfer", command=transfer_action).pack(pady=6)  # button to trigger transfer
tk.Button(transfer_frame, text="Back", command=lambda: show_frame(home_frame)).pack()  # back to home
# show home frame and start
show_frame(home_frame)  # display the home screen initially
root.mainloop()  # start the GUI event loop

