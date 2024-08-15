from datetime import datetime, timedelta
import requests
import json
import pandas as pd

## Test 1
# a = datetime.datetime.now() -  datetime.datetime(1970, 1, 1)
# print(a.days)

## Test 2
#json_cointreau = 'https://www.boursorama.com/bourse/action/graph/ws/GetTicksEOD?symbol=1rPRCO&length=5&period=-1&guid='

## Trouver la date 
# Date de référence
date_reference = datetime(1970, 1, 1)

# Ajouter le nombre de jours souhaité à la date de référence
# date_result = date_reference + timedelta(days=19821)
# date_formatee = date_result.strftime("%Y-%m-%d") # Reformatage

# print("Date correspondante:", date_formatee)

day_list = []
opening_list = []
highest_list = []
lowest_list = []
closing_list = []
volume_list = []

#url = "https://www.boursorama.com/bourse/action/graph/ws/GetTicksEOD?symbol=1rPRCO&length=30&period=0&guid="
url = 'https://www.boursorama.com/bourse/action/graph/ws/GetTicksEOD?symbol=1rPRCO&length=3650&period=1&guid='
response = requests.get(url)
if response.status_code == 200:
    response_json = response.json()
    data = response_json['d']['QuoteTab']
    for ligne in  data : 
        day = ligne['d']
        day_clean = date_reference + timedelta(days=day)
        day_formatee = day_clean.strftime("%Y-%m-%d")
        day_list.append(day_formatee)
        opening_list.append(ligne['o'])
        highest_list.append(ligne['h'])
        lowest_list.append(ligne['l'])
        closing_list.append(ligne['c'])
        volume_list.append(ligne['v'])
    # print(len(data['d']['QuoteTab']))
    # print(data['d']['QuoteTab'][20]['d'])
else:
    print("Erreur lors de la requête à l'API:", response.status_code)
    
df_month = pd.DataFrame({'Day' : day_list,
    'Opening' : opening_list,
    'Highest' : highest_list,
    'Lowest' : lowest_list,
    'Closing'  : closing_list,
    'Volume' : volume_list
})

print(df_month)
#df_month.to_csv('/Users/manu/Desktop/SUP/Cac40/Results/10Years_Cointreau.csv', index=False)
    
# Interpretation JSON 
# d = day
# o  = opening
# h = highest
# l = lowest
# c = closing
# v = volume