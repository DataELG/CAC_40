import requests
from datetime import datetime, timedelta

boursorama_cie_ID = ''
url = f'https://www.boursorama.com/bourse/action/graph/ws/GetTicksEOD?symbol=1rPSU&length=1&period=0&guid='
response = requests.get(url)
if response.status_code == 200:
    response_json = response.json()
    data = response_json['d']['QuoteTab']

    
def get_date(date) :
    date_reference = datetime(1970, 1, 1)
    day_clean = date_reference + timedelta(days=date)
    #day_formatee = day_clean.strftime("%Y-%m-%d")
    return day_clean


from datetime import datetime, timedelta


def decode_datetime(date_str):
    # Extraction des parties de la chaîne
    year = int("20" + date_str[:2])  # "24" -> 2024
    month = int(date_str[2:4])       # "08" -> Août
    day = int(date_str[4:6])         # "12" -> 12
    hour_code = int(date_str[6:8])   # "09" -> heure
    minute_code = int(date_str[8:10])# "97" -> minutes en base 100

    # Décoder l'heure
    base_hour = 4  # Le code 00 correspond à 4h
    hour = base_hour + hour_code  # "09" + 4 = 13h

    # Convertir les minutes de base 100 à base 60
    minute = int(minute_code * 60 / 100)

    # Créer l'objet datetime
    return datetime(year, month, day, hour, minute)

# Exemple d'utilisation
date_str = "2408120541"
decoded_date = decode_datetime(date_str)
print(decoded_date)
