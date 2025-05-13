import getpass
import re

PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{9,}$'

def input_New_MasterPass() -> str | None : 
    print("Enter a Master Passwor or (Q)uit for exit")
    while True:
        master_password = getpass.getpass("Master Password: ").strip()
        if master_password.lower() in ['q',"quit"]:
            print("Exiting...")
            return 
        if not re.match(PASSWORD_PATTERN,master_password):
            print(
                "Password must be at least 9 characters long and\n"
                "contain uppercase letters, lowercase letters,\n"
                "digits, and special characters."
                )

            continue
        confirm_password = getpass.getpass("Confirm Password: ").strip()
        if master_password == confirm_password:
            return master_password
        else:
            print("Password doesn't match.")
            print()

def input_SiteName() -> str : 
    while True:
        site = input("Site Name: ").strip()
        if site:
            return site
        print("Site name cannot be empty.")

def input_Password() -> str | None:
    while True:
        password = getpass.getpass("Password: ").strip()
        if not re.match(PASSWORD_PATTERN, password):
            check = input(
                "The password is weak.\n"
                "You must change it.\n"
                "Do you want to save it anyway? (Y)es or (N)o: ").strip().lower()
            
            if check not in ["y", "yes"]:
                print("Good, go change it on the website and return again.")
                return None  
            else:
                print("Warning: You're saving a weak password!")
        tries = 0
        max_tries = 5
        while tries < max_tries:
            confirm_password = getpass.getpass("Confirm Password: ").strip()
            if confirm_password == password:
                return password
            else:
                tries += 1
                print(f"Password doesn't match. Attempts left: {max_tries - tries}")
                print()
        print("Too many failed attempts. Please try again later.")
        return None

def Show_Options() -> str : 

    print("\n=== Main Menu ===")
    print("1. Generate new password")
    print("2. Retrieve password")
    print("3. Delete password")
    print("4. Add Password")
    print("5. Exit")
    print()
    choice = input("Select option: ").strip()
    return choice

def inputMasterPass() -> str:
    password = getpass.getpass("Master Password: ").strip()
    return password    

