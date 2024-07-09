from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
load_dotenv()


def encode_password(password):
    key = os.getenv('ENCRYPTION_KEY')
    cipher_suite = Fernet(key.encode())
    return cipher_suite.encrypt(password.encode()).decode()   

def verify_password(encrypted_password, password):
    key = os.getenv('ENCRYPTION_KEY')
    cipher_suite = Fernet(key.encode())
    return cipher_suite.decrypt(encrypted_password.encode()).decode() == password

password = "root"
password = encode_password(password)
print(password)