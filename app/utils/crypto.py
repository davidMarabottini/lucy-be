from base64 import urlsafe_b64encode
from hashlib import sha256

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def get_fernet(password: str) -> Fernet:
    """Genera l'istanza Fernet usando PBKDF2 (Molto più sicuro di SHA256)"""
    _SALT = b'\x82\x12\xaf\x19\x04\x11\x8c\x8e\x9f\x1a\x10\x92\xf4\x81\x32\x0b'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=_SALT,
        iterations=100000, # Rende gli attacchi brute-force lentissimi
    )
    key = urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)

def decrypt_db(password: str, input_path: str, output_path: str):
    """Legge il file criptato e lo scrive decriptato in un altro percorso"""
    fernet = get_fernet(password)
    with open(input_path, "rb") as f:
        encrypted_data = f.read()
    
    decrypted_data = fernet.decrypt(encrypted_data)
    
    with open(output_path, "wb") as f:
        f.write(decrypted_data)
        
def encrypt_db(password: str, input_path: str, output_path: str):
    """Funzione atomica per criptare il file. Usata allo shutdown."""
    fernet = get_fernet(password)
    with open(input_path, "rb") as f:
        data = f.read()
    
    encrypted_data = fernet.encrypt(data)
    
    with open(output_path, "wb") as f:
        f.write(encrypted_data)
