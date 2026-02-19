# SecureProp Analytics

A security-focused real estate data analyzer that scrapes Century21 Albania and enriches data with currency conversion.

## Features
- Web scraping of property listings from Century21 Albania
- AES encryption for sensitive address data
- Live currency conversion (EUR to USD) using ExchangeRate-API
- JSON data export with encrypted fields

## Architecture
- `scraper.py` - Handles all web scraping logic
- `security.py` - Manages encryption/decryption of sensitive data
- `exchange_api.py` - Integrates with exchange rate API
- `main.py` - Orchestrates the entire pipeline

## Setup
```bash
# Clone repository
git clone https://github.com/yourusername/secureprop-analytics.git
cd secureprop-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the scraper
python main.py