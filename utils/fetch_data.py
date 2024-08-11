import re
from datetime import datetime,timedelta, date
from utils.req_functions import *
from utils.bdd_functions import *

today = date.today()

def fetch_companies_info() :
    companies_dict = {}
    for i in range(1,3) :
        url = f'https://www.boursorama.com/bourse/actions/cotations/page-{i}?quotation_az_filter%5Bmarket%5D=1rPCAC'
        bsObj = request_url(url)
        if bsObj :
            if bsObj.find('tbody', class_='c-table__body') :    
                table = bsObj.find('tbody', class_='c-table__body') 
                companies = table.find_all('tr')
                for cie in companies :
                    cie_details = cie.find('a')
                    name = cie_details['title']
                    id_tag = cie_details['href']
                    if id_tag : 
                        match = re.search(r'/cours/([^/]+)/', id_tag)
                        if match :
                            id = match.group(1)
                            companies_dict[name] = id
    if companies_dict :
        return companies_dict
    
    

    
    
def fetch_history(companie_id) :
    
    dict_result_history = {}
    date_reference = datetime(1970, 1, 1)

# Ajouter le nombre de jours souhaité à la date de référence

    day_list = []
    opening_list = []
    highest_list = []
    lowest_list = []
    closing_list = []
    volume_list = []

    url = f'https://www.boursorama.com/bourse/action/graph/ws/GetTicksEOD?symbol={companie_id}&length=3650&period=1&guid='
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
        
        if day_list and opening_list and highest_list and lowest_list and closing_list and volume_list :
            dict_result_history['Day'] = day_list
            dict_result_history['Opening'] = opening_list
            dict_result_history['Highest'] = highest_list
            dict_result_history['Lowest'] = lowest_list
            dict_result_history['Closing'] = closing_list
            dict_result_history['Volume'] = volume_list
            return dict_result_history