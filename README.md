## Architecture
- **scraper.py** - Fetches property data from Century21 Albania
- **security.py** - Encrypts sensitive data using Fernet (AES)
- **exchange_api.py** - Converts EUR to USD via ExchangeRate-API
- **main.py** - Orchestrates the pipeline

## Data Flow
1. Scraper fetches property listings → raw data
2. Security module encrypts addresses
3. Exchange API converts EUR prices to USD
4. Final data saved to JSON with encrypted fields

## Encryption
- Uses Fernet (symmetric AES encryption)
- Keys stored in .env file (never committed)
- Addresses encrypted before saving to JSON