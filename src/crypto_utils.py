import secrets
import base64
from argon2.low_level import hash_secret_raw, Type
from cryptography.fernet import Fernet

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
    return Key
def GetKeyBase64(key: bytes) -> str :
    """
    Convert a key From Hex/bytes To Base64
    And return it as string
    """
    Sqlcipher_pass = base64.b64encode(key).decode()
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
    

    