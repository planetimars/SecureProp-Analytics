import requests
from bs4 import BeautifulSoup
import time
import re

class RealEstateScraper:
    def __init__(self, user_agent):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.base_url = "https://www.century21albania.com"
        
        self.location_keywords = {
            'LAPRAKE': 'Laprakë',
            'PASKUQAN': 'Paskuqan',
            'KAMEZ': 'Kamëz',
            'KASHAR': 'Kashar',
            'SAUK': 'Sauk',
            'KODRA E LIQENIT': 'Kodra e Liqenit',
            'BULEVARDI I RI': 'Bulevardi i Ri',
            'ALI DEMI': 'Ali Demi',
            'KOMUNA PARISIT': 'Komuna e Parisit',
            'DURRES': 'Durrës',
            'VLORE': 'Vlorë',
            'SHKODER': 'Shkodër'
        }
    
    def fetch_page(self, url, retries=3):
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    return response.text
            except:
                pass
            time.sleep(2)
        return None
    
    def get_property_links(self, page_url):
        html = self.fetch_page(page_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        property_urls = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/property/' in href:
                if href.startswith('http'):
                    property_urls.append(href)
                else:
                    property_urls.append(self.base_url + href)
        
        return list(set(property_urls))[:10]
    
    def extract_location_from_title(self, title):
        title_upper = title.upper()
        
        for keyword, name in self.location_keywords.items():
            if keyword in title_upper:
                parts = title_upper.split(keyword)[0].strip()
                for word in ['NE', 'TEK', 'PRANE', 'LAGJJA', 'RRUGA']:
                    parts = parts.replace(word, '').strip()
                
                if parts and len(parts) > 2:
                    return f"{parts}, {name}"
                return name
        
        cities = {
            'TIRANE': 'Tirana',
            'TIRANA': 'Tirana',
            'DURRES': 'Durrës',
            'VLORE': 'Vlorë'
        }
        
        for alb, eng in cities.items():
            if alb in title_upper:
                return eng
        
        return "Tirana"
    
    def scrape_property(self, property_url):
        html = self.fetch_page(property_url)
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        
        title = soup.find('h1')
        title_text = title.text.strip() if title else ''
        
        location = self.extract_location_from_title(title_text)
        
        price_match = re.search(r'([\d,]+)\s*[€$]', text)
        price = price_match.group(1) + ' €' if price_match else 'N/A'
        
        rooms_match = re.search(r'(\d+)\+(\d+)', title_text)
        if rooms_match:
            bedrooms = f"{rooms_match.group(1)}+{rooms_match.group(2)}"
        else:
            rooms_match = re.search(r'(\d+)\s*[+]?\s*(\d+)?', title_text)
            bedrooms = rooms_match.group(1) if rooms_match else 'N/A'
        
        area_match = re.search(r'(\d+)\s*m[²2]', text)
        area = area_match.group(1) + ' m²' if area_match else 'N/A'
        
        return {
            'url': property_url,
            'title': title_text,
            'price': price,
            'location': location,
            'bedrooms': bedrooms,
            'area': area,
            'extracted_from': 'title_parsing'
        }