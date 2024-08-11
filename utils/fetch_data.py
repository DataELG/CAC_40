import re
from requestAPI import *

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