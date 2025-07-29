"""
Password Manager (IronPass)

A secure and user-friendly password management system with the following features:

- Automatically detects first-time use:
    - Prompts the user to create a master password (that allows you to access all password).
    - Stores the master password as a secure hash.
- Requires the master password on every launch:
    - Verifies input by comparing hashes.
    - Prevents access to stored data without correct authentication.
- Generates strong, random passwords with a random length (greater than 15 characters).
- Allows saving passwords associated with unique name IDs (e.g., "email", "github").
- Encrypts and stores all saved passwords.
- Decrypts passwords securely upon request using the stored encryption key.
- Stores all data in a local database.
- Supports two interfaces:
    - Command-Line Interface (CLI)
    - Graphical User Interface (GUI)
"""
import sys
from src import *


def main():
    iron_pass = IronPass()
    if "--gui" in sys.argv:
        iron_pass.Start_Gui()
    else:
        iron_pass.Start_Cli()

if __name__ == "__main__":
    main()