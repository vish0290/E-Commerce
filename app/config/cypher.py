from passlib.hash import pbkdf2_sha256
from os import environ
from dotenv import load_dotenv

load_dotenv()
secret = environ.get('ENCRYPT_KEY')
def hash_password(password):
    password += secret
    return pbkdf2_sha256.hash(password)

def verify_password(stored_password, provided_password):
    provided_password += secret
    return pbkdf2_sha256.verify(provided_password, stored_password)
