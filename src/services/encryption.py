from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from typing import Optional

class EncryptionService:
    def __init__(self, master_key: Optional[str] = None):
        if master_key:
            self.key = self._derive_key(master_key.encode())
        else:
            self.key = self._get_or_create_key()
        self.cipher_suite = Fernet(self.key)
    
    def _derive_key(self, password: bytes, salt: bytes = b'stable_salt_for_auth_tool') -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def _get_or_create_key(self) -> bytes:
        key_file = 'encryption.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def encrypt(self, plaintext: str) -> str:
        encrypted_data = self.cipher_suite.encrypt(plaintext.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def decrypt(self, encrypted_text: str) -> str:
        encrypted_data = base64.urlsafe_b64decode(encrypted_text.encode())
        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
        return decrypted_data.decode()
    
    def is_valid_encrypted_data(self, encrypted_text: str) -> bool:
        try:
            self.decrypt(encrypted_text)
            return True
        except Exception:
            return False