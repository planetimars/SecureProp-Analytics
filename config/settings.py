import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    print(f"\nGenerated new encryption key: {ENCRYPTION_KEY}")
    print("Add this to your .env file!\n")

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
BASE_URL = 'https://example.com'