from datetime import datetime, timedelta
import requests
import json
import pandas as pd

# Date de référence
date_reference = datetime(1970, 1, 1)

# Inserer  le time 

day_list = []
opening_list = []
highest_list = []
lowest_list = []
closing_list = []
volume_list = []

url = 'https://www.boursorama.com/bourse/action/graph/ws/GetTicksEOD?symbol=1rPPUB&length=1&period=0&guid='
response = requests.get(url)
if response.status_code == 200:
    response_json = response.json()
    print(response_json)    
    data = response_json['d']['qd']
    day = data['d']
    day_clean = date_reference + timedelta(days=day)
    day_formatee = day_clean.strftime("%Y-%m-%d")
    day_list.append(day_formatee)
    opening_list.append(data['o'])
    highest_list.append(data['h'])
    lowest_list.append(data['l'])
    closing_list.append(data['c'])
    volume_list.append(data['v'])

else:
    print("Erreur lors de la requête à l'API:", response.status_code)
    
df_now = pd.DataFrame({'Day' : day_list,
    'Opening' : opening_list,
    'Highest' : highest_list,
    'Lowest' : lowest_list,
    'Closing'  : closing_list,
    'Volume' : volume_list
})

print(df_now)
#df_month.to_csv('/Users/manu/Desktop/SUP/Cac40/Results/RealTime_Cointreau.csv',index=False)
    
# Interpretation JSON 
# d = day
# o  = opening
# h = highest
# l = lowest
# c = closing
# v = volume