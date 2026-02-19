import requests
import time

class GeocodingAPI:
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SecureProp-Analytics/1.0'
        })
    
    def get_coordinates(self, address_text):
        if not address_text:
            return None
        
        cities = {
            'TIRANE': 'Tirana',
            'TIRANA': 'Tirana',
            'DURRES': 'Durrës',
            'VLORE': 'Vlorë',
            'SHKODER': 'Shkodër',
            'FIER': 'Fier',
            'ELBASAN': 'Elbasan'
        }
        
        city_found = 'Tirana'
        upper_text = address_text.upper()
        
        for alb_city, eng_city in cities.items():
            if alb_city in upper_text:
                city_found = eng_city
                break
        
        words = address_text.split()
        if len(words) > 3:
            search_text = ' '.join(words[:3])
        else:
            search_text = address_text
        
        search_query = f"{search_text}, {city_found}, Albania"
        
        params = {
            'q': search_query,
            'format': 'json',
            'limit': 1
        }
        
        try:
            print(f"Searching: {search_query}")
            response = self.session.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    return {
                        'lat': data[0]['lat'],
                        'lon': data[0]['lon'],
                        'display_name': data[0]['display_name']
                    }
                else:
                    print(f"No results")
            else:
                print(f"API error: {response.status_code}")
                
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(1)
        return None