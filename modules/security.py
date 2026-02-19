from cryptography.fernet import Fernet
import hashlib
import base64

class SecurityManager:
    def __init__(self, key=None):
        if key:
            self.key = key.encode() if isinstance(key, str) else key
        else:
            self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encrypt_data(self, data):
        if not isinstance(data, bytes):
            data = str(data).encode()
        encrypted = self.cipher.encrypt(data)
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt_data(self, encrypted_data):
        try:
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(decoded)
            return decrypted.decode()
        except:
            return "[DECRYPTION FAILED]"
    
    def hash_data(self, data):
        if not isinstance(data, bytes):
            data = str(data).encode()
        return hashlib.sha256(data).hexdigest()
    
    def get_key(self):
        return self.key.decode()