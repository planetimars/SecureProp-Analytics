import sys
import time
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import ENCRYPTION_KEY, USER_AGENT
from modules.scraper import RealEstateScraper
from modules.security import SecurityManager
from modules.exchange_api import ExchangeRateAPI

def main():
    print("=" * 60)
    print("CENTURY21 ALBANIA - WITH CURRENCY CONVERSION")
    print("=" * 60)
    
    scraper = RealEstateScraper(USER_AGENT)
    security = SecurityManager(ENCRYPTION_KEY)
    exchange = ExchangeRateAPI()
    
    property_links = scraper.get_property_links("https://www.century21albania.com/")
    property_links = property_links[:5]
    
    all_properties = []
    
    for i, url in enumerate(property_links, 1):
        print(f"\n--- Property {i} ---")
        
        property_data = scraper.scrape_property(url)
        
        if property_data:
            print(f"Title: {property_data['title'][:70]}...")
            print(f"Original price: {property_data['price']}")
            
            conversion = exchange.convert_price(property_data['price'], "EUR", "USD")
            property_data['price_usd'] = conversion['converted']
            property_data['exchange_rate'] = conversion['rate']
            
            if conversion['rate']:
                print(f"USD price: {conversion['converted']} (Rate: {conversion['rate']})")
            else:
                print("Could not convert price")
            
            if property_data['location']:
                property_data['encrypted_address'] = security.encrypt_data(property_data['location'])
            
            all_properties.append(property_data)
        
        time.sleep(1)
    
    filename = f"century21_with_usd_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_properties, f, indent=2, ensure_ascii=False)
    
    print(f"\n Saved {len(all_properties)} properties with USD prices to {filename}")
    print("=" * 60)

if __name__ == "__main__":
    main()