import requests
import time
import re

class ExchangeRateAPI:
    def __init__(self):
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"
        self.session = requests.Session()
        self.cached_rates = {}
        self.last_fetch = 0
    
    def get_rates(self, base_currency="EUR"):
        current_time = time.time()
        if base_currency in self.cached_rates and current_time - self.last_fetch < 3600:
            return self.cached_rates[base_currency]
        
        try:
            url = f"{self.base_url}{base_currency}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.cached_rates[base_currency] = data['rates']
                self.last_fetch = current_time
                return data['rates']
            else:
                print(f"API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error fetching exchange rates: {e}")
            return None
    
    def convert_price(self, price_text, from_currency="EUR", to_currency="USD"):
        if not price_text or price_text == 'N/A':
            return {'original': price_text, 'converted': 'N/A', 'rate': None}
        
        try:
            import re
            price_match = re.search(r'([\d,]+)', price_text.replace('.', ''))
            if not price_match:
                return {'original': price_text, 'converted': 'N/A', 'rate': None}
            
            price = float(price_match.group(1).replace(',', ''))
            
            rates = self.get_rates(from_currency)
            if not rates or to_currency not in rates:
                return {'original': price_text, 'converted': 'N/A', 'rate': None}
            
            rate = rates[to_currency]
            converted = price * rate
            
            return {
                'original': price_text,
                'original_value': price,
                'converted_value': round(converted, 2),
                'converted': f"{round(converted, 2):,} {to_currency}",
                'rate': rate,
                'from': from_currency,
                'to': to_currency
            }
            
        except Exception as e:
            print(f"Conversion error: {e}")
            return {'original': price_text, 'converted': 'N/A', 'rate': None}