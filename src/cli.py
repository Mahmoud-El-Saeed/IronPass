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
    print("input Site Name like (Google - github) not (Google.com - Github.com)")
    while True:
        site = input("Site Name: ").strip()
        if site:
            return site
        print("Site name cannot be empty.")

def input_UserName() -> str : 
    while True:
        site = input("User Name: ").strip()
        if site:
            return site
        print("Site name cannot be empty.")

def input_Password() -> str | None:
    while True:
        tries = 0
        password = ""
        while tries < 5:
            password = getpass.getpass("Password: ").strip()
            confirm_password = getpass.getpass("Confirm Password: ").strip()
            if confirm_password == password:
                break
            else:
                tries += 1
                print(f"Password doesn't match. Attempts left: { 5 - tries}")
                print()
        if confirm_password != password :
            return None
        
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
                return password

def Show_Options() -> str : 

    print("\n=== Main Menu ===")
    print("1. Generate new password")
    print("2. Show password")
    print("3. Show All passwords")
    print("4. Delete password")
    print("5. Add Password")
    print("6. Exit")
    print()
    choice = input("Select option: ").strip()
    return choice

def inputMasterPass() -> str:
    password = getpass.getpass("Master Password: ").strip()
    return password    

