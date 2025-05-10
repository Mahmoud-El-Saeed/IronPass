import secrets
import base64
from argon2.low_level import hash_secret_raw, Type
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
import string

def GenSalt() -> bytes :
    """
    That is Generate Salt for Firt time
    And return it 
    """
    Salt = secrets.token_bytes(32)
    with open("salt.bin","wb") as file:
        file.write(Salt)
    return Salt
def GetSalt() -> bytes :
    """
    That is return salt from file that stored before
    """
    with open("salt.bin","rb") as file:
        Salt = file.read()
    return Salt   
def GenKey(MasterPass :str,Salt: bytes) -> bytes :
    """
    That generate a key by argon Algorithm
    And return a key
    """
    Key = hash_secret_raw(
        secret=MasterPass.encode(),  
        salt=Salt,         
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,              
        type=Type.ID                     
    )
    Sqlcipher_pass = base64.b64encode(Key)
    return Sqlcipher_pass
def Encrypt_Password(password: str,key: bytes) -> bytes :
    """
    That is Encrypt a password 
    And return it Encrypted 
    """
    Cipher = Fernet(key)
    EnPassword = Cipher.encrypt(password.encode())
    return EnPassword    
def Decrypt_Password(encrypt_Password: bytes,key: bytes) -> str :
    """
    That is decrypt a password 
    And return The Orginal Password 
    """
    Cipher = Fernet(key)
    password = Cipher.decrypt(encrypt_Password)
    return password.decode()    
def Generate_Password() -> str:
    choices = string.ascii_letters + string.digits +string.punctuation
    while True:
        password = "".join(secrets.choice(choices) for i in range(secrets.choice(range(20,41))))
        if ( any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password)>=3
            and any(c in string.punctuation for c in password)):
            break
    return password 
def GenToke(MasterPassword: str) -> str:
    ph = PasswordHasher()
    hased = ph.hash(MasterPassword)
    return hased
def verify_MasterPass(currentPassword: str,StoredPassword: str) -> bool:
    ph = PasswordHasher()
    try :
        return ph.verify(StoredPassword,currentPassword)    
    except:
        return False