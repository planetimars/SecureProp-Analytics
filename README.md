# SecureProp Analytics

Një analizues i të dhënave të pasurive të paluajtshme me fokus sigurinë, që nxjerr të dhëna nga Century21 Albania dhe i pasuron ato me konvertim valutor.

## Arkitektura
- **scraper.py** - Merr të dhënat e pronave nga Century21 Albania
- **security.py** - Enkripton të dhënat sensitive duke përdorur Fernet (AES)
- **exchange_api.py** - Konverton EUR në USD përmes ExchangeRate-API
- **main.py** - Orkestron të gjithë pipeline-in

## Rrjedha e të Dhënave
1. Scraper nxjerr listimet e pronave → të dhëna të papërpunuara
2. Moduli i sigurisë enkripton adresat
3. Exchange API konverton çmimet nga EUR në USD
4. Të dhënat përfundimtare ruhen në JSON me fusha të enkriptuara

## Teknologjitë e Përdorura
- **Python 3.13** - Gjuha e programimit
- **Requests** - Për HTTP requests gjatë web scraping
- **BeautifulSoup4** - Për parsing të HTML
- **Cryptography** - Për enkriptimin Fernet (AES)
- **ExchangeRate-API** - Për konvertimin e valutave
- **python-dotenv** - Për menaxhimin e variablave të mjedisit

## Enkriptimi
- Përdor Fernet (enkriptim simetrik AES)
- Çelësat ruhen në .env (asnjëherë të commit-uara)
- Adresat enkriptohen para se të ruhen në JSON

## Udhëzime për Setup dhe Ekzekutim

1. **Klononi repository-n**
   ```bash
   git clone https://github.com/planetimars/SecureProp-Analytics.git
   cd SecureProp-Analytics