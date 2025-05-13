import os
from .crypto_utils import *
from .database import *
from .cli import *
from .gui import *
import sys


class IronPass():
    
    def __init__(self):
        if os.path.exists("salt.bin"):
            self.__salt = GetSalt()
            password = self.Verify_MasterPass()
            if password :
                self.__master_password = password
            else:
                self.Exit_Program() 
            self.key = GenKey(self.__master_password,self.__salt)
        else:
            self.__salt = GenSalt()
            self.__master_password = input_New_MasterPass()
            self.key = GenKey(self.__master_password,self.__salt)
        Tokin =  GenTokin(self.__master_password)
        Create_Database(Tokin)
        
    def Verify_MasterPass(self) -> str | None:
        Max_tries = 5
        tries = 0
        while Max_tries> tries:
            curpassword = inputMasterPass()
            if verify_MasterPass(curpassword,GetTokin()):
                return curpassword
            else:
                print(f"Password doesn't match. Attempts left: {Max_tries - tries}")
                tries+=1
        print("The tries is finised!")
        return None
        
    def Generate_New_Password(self):
        while True:
            site_name = input_SiteName()
            password = Generate_Password()
            encrypt_password = Encrypt_Password(password,self.key)
            if Store_Password(site_name,encrypt_password) :
                print(f"The password is stored successfully --> '{password}' ")
                break
            else:
                print("The siteName is already exits")

    def Showing_Password(self):
        site_name =  input_SiteName()
        encrypt_Password = Showing_Password(site_name)
        if encrypt_Password:
            password = Decrypt_Password(encrypt_Password[0],self.key)
            print(f"The password for {site_name} is '{password}' ")
            return
        print(f"That no password for this site {site_name}")

    def Deleting_Password(self):
        siteName = input_SiteName()
        Deleting_Password(siteName)

    def Add_Password(self):
        siteName = input_SiteName()
        password = input_Password()
        if password is None :
            self.Exit_Program()
        else:
            encrypt_Password = Encrypt_Password(password,self.key)
            if Store_Password(siteName,encrypt_Password):
                print(f"The password is stored successfully --> '{password}' ")
                return
            print("The siteName is already exits")

    def Exit_Program(self):
        sys.exit()

    def Start_Cli(self):
        while True:
            choice = Show_Options()
            if choice=="1":
                self.Generate_New_Password()
            elif choice =="2":
                self.Showing_Password()
            elif choice =="3":
                self.Deleting_Password()
            elif choice =="4":
                self.Add_Password()
            elif choice =="5":
                self.Exit_Program()
            else:
                print('Invalid input!!')
    
    
    def Start_Gui(self):
        pass



