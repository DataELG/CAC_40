import requests
from datetime import datetime, timedelta

# boursorama_cie_ID = ''
# url = f'https://www.boursorama.com/bourse/action/graph/ws/GetTicksEOD?symbol=1rPSU&length=1&period=0&guid='
# response = requests.get(url)
# if response.status_code == 200:
#     response_json = response.json()
#     data = response_json['d']['QuoteTab']

    
# def get_date(date) :
#     date_reference = datetime(1970, 1, 1)
#     day_clean = date_reference + timedelta(days=date)
#     #day_formatee = day_clean.strftime("%Y-%m-%d")
#     return day_clean

# print(get_date(19948))

from datetime import datetime, timedelta

def decode_datetime(date_str):
    # Extraction des parties de la chaîne
    year = int("20" + date_str[:2])  # "24" -> 2024
    month = int(date_str[2:4])       # "08" -> Août
    day = int(date_str[4:6])         # "13" -> 13
    time_in_minutes = int(date_str[6:10])  # "1057" -> 1057 minutes depuis minuit

    # Calcul de l'heure et des minutes à partir des minutes écoulées depuis minuit
    hours = time_in_minutes // 60   # Calcul du nombre d'heures
    minutes = time_in_minutes % 60  # Calcul des minutes restantes

    return datetime(year, month, day, hours, minutes) 

# Exemple d'utilisation
date_str = "2408131057"
decoded_date = decode_datetime(date_str)
print(decoded_date)
