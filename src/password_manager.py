import os
import sys
from PyQt5.QtWidgets import QApplication
from .crypto_utils import *
from .database import *
from .cli import *
from .gui import *
from .gui import MainWindowIRON

class IronPass():
    
    def __init__(self):
        self.key = None
    
    def check_first_time(self) -> bool :
        return not os.path.exists(".salt.bin")
    
    def setup_first_time(self , master_password:str ) -> bool:
        salt = GenSalt()
        tokin = GenTokin(master_password)
        self.key = GenKey(master_password, salt)
        encrypt_tokin = Encrypt_Password(tokin,self.key)
        Create_Database(encrypt_tokin)
        return True
        
    def unlock_app(self , master_password: str) -> bool:
        salt = GetSalt()
        self.key  = GenKey(master_password , salt)
        encrypt_tokin = GetTokin()
        try:
            tokin = Decrypt_Password(encrypt_tokin,self.key)
            return True
        except:
            return False
        # TODO this part i think it doesn't matter because if the password is woring 
        # the try and except do every thing 
        # i will reviewed later
        if tokin and verify_MasterPass(master_password , tokin):
            salt = GetSalt()
            self.key  = GenKey(master_password , salt)
            return True
        return False

    
    
    def add_password(self , site_name , username , password) -> bool:
        if not self.key: return False
        encrypted_pass = Encrypt_Password(password, self.key)
        return Store_Password(site_name, username, encrypted_pass)
    
    def show_password(self,site_name,user_name ):
        if not self.key: return False
        encrypt_Password = Showing_Password(site_name,user_name)
        if not encrypt_Password:
            return False
        password = Decrypt_Password(encrypt_Password[0],self.key)
        return password
    
    def show_All_passwords(self) -> list:
        if not self.key : return []
        
        all_encrypted_password = GetAllPasswords() 
        
        decrypt_Passwords = []
        for password in all_encrypted_password:
            decrypt_Password = Decrypt_Password(password[2] , self.key)
            decrypt_Passwords.append((password[0],password[1],decrypt_Password))
        
        return decrypt_Passwords
        
        
    def delete_password(self, site_name , user_name) -> bool:
        if self.key is None : return False
        return Deleting_Password(site_name , user_name)

    
    

    def Start_Gui(self):

        
        app = QApplication(sys.argv)
        main_win = MainWindowIRON(self)

        if  self.check_first_time():
            main_win.show_first_time_screen()
        else:
            main_win.show_returning_user_screen()

        main_win.show()
        sys.exit(app.exec_())
    
    
    
    
    def Start_Cli(self):
        print("--- IronPass [CLI Mode] ---")
        if self.check_first_time() :
            print("First time setup...")
            master_password =  input_New_MasterPass()
            if not master_password: self.Exit_Program()
            self.setup_first_time(master_password)
            print("Vault created successfully!")
        else:
            TRIES = 0
            while TRIES < 5:
                password = inputMasterPass()
                if self.unlock_app(password):
                    print("Vault unlocked.")
                    break
                else:
                    TRIES += 1
                    print(f"Incorrect password. Attempts left: {5 - TRIES}")
        if not self.key:
                print()
                print("Too many failed attempts. Exiting.")
                self.Exit_Program()
        
        
        # A Main Program
        while True:
            choice = Show_Options()
            if choice not in ["1","2","3","4","5","6"]:
                print('Invalid input!!')
                continue
            elif choice =="1":
                password = Generate_Password()
                site_name = input_SiteName()
                user_name = input_UserName()
                if self.add_password(site_name, user_name,password):
                    print()
                    print("Password Added successfully")
                    print(f"Generated Password: '{password}'")
                else:
                    print()
                    print("The User Name and Site Name are already exits")
            
            elif choice == "2":
                site_name = input_SiteName()
                user_name = input_UserName()
                password = self.show_password(site_name,user_name)
                if not password : 
                    print("The User Name and Site Name NOT exits")
                    continue
                print(f"The Password For {site_name} & {user_name} if '{password}' ")
                    
            
            
            
            elif choice == "3":
                all_password = self.show_All_passwords()
                for i in all_password:
                    print(i)
            
            elif choice == "4":
                site_name = input_SiteName()
                user_name = input_UserName()
                if self.delete_password(site_name,user_name):
                    print("The Password Deleted Successfully")
                else:
                    print("The User Name and Site Name NOT exits")
            
            elif choice == "5":
                site_name = input_SiteName()
                user_name = input_UserName()
                password = input_Password()
                if not password : self.Exit_Program()
                if self.add_password(site_name, user_name,password):
                    print()
                    print("Password Saved successfully")
                    print(f"Password: '{password}'")
                else:
                    print()
                    print("The User Name and Site Name are already exits")
            
            elif choice == "6":
                print("Exit")
                self.Exit_Program()
            
            
            
    def Exit_Program(self):
        print("Exiting IronPass. Goodbye!")
        sys.exit()





