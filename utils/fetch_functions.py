import re
from datetime import date
from utils.req_functions import *
from utils.bdd_functions import *
from utils.date_functions import *


def fetch_new_companies(companies_table, session) :
    '''
    Fetch a list of company IDs added to the database today.

    Arguments
    ----------
    companies_table : SQLAlchemy Table object
        The table object representing the companies in the database.
    session : SQLAlchemy session object
        The session object used to execute the query in the database.

    Returns
    ----------
    result_list : list
        A list of company IDs (BOURSORAMA_CIE_ID) for companies added today.
    '''
    stmt = select(companies_table.c.BOURSORAMA_CIE_ID).where(companies_table.c.ENTRY_DATE == date.today())
    result = session.execute(stmt)
    result_list = [row[0] for row in result]
    return result_list


def fetch_active_CAC40_cie(companies_table, session) :
    '''
    Fetch a list of currently active CAC40 companies.

    Arguments
    ----------
    companies_table : SQLAlchemy Table object
        The table object representing the companies in the database.
    session : SQLAlchemy session object
        The session object used to execute the query in the database.

    Returns
    ----------
    result_list : list
        A list of active company IDs (BOURSORAMA_CIE_ID) for companies currently in the CAC40.
    '''
    stmt = select(companies_table.c.BOURSORAMA_CIE_ID).where(companies_table.c.EXIT_DATE.is_(None))
    result = session.execute(stmt)
    result_list = [row[0] for row in result]
    return result_list


def fetch_all_CAC40_cie(companies_table, session) :
    '''
    Fetch a list of all CAC40 companies, both active and historical.

    Arguments
    ----------
    companies_table : SQLAlchemy Table object
        The table object representing the companies in the database.
    session : SQLAlchemy session object
        The session object used to execute the query in the database.

    Returns
    ----------
    result_list : list
        A list of company IDs (BOURSORAMA_CIE_ID) for all companies that have been part of the CAC40 index,
        including both active and historical members.
    '''
    stmt = select(companies_table.c.BOURSORAMA_CIE_ID)
    result = session.execute(stmt)
    result_list = [row[0] for row in result]
    return result_list


def fetch_companies_info() :
    '''
    Get list of companies part of CAC40
    
    Returns
    ----------  
    dict 
        dictionnary {companie_name : boursorama_companie_ID} 
    '''
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
    
    
def fetch_history_data(boursorama_cie_ID) :
    '''
    Arguments
    ----------
    boursorama_cie_ID : str 
        Found in COMPANIES table  
        
    Returns
    ----------  
    dict 
        a dictionnary of 3 year-history by day
    '''
    url = f'https://www.boursorama.com/bourse/action/graph/ws/GetTicksEOD?symbol={boursorama_cie_ID}&length=1095&period=1&guid='
    
    dict_result_history = {}
        
    day_list = []
    opening_list = []
    highest_list = []
    lowest_list = []
    closing_list = []
    volume_list = []

    response = requests.get(url)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json['d']['QuoteTab']
        for ligne in  data : 
            day = ligne['d']
            day_formatee = get_date(day) 
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



def fetch_streaming_data(boursorama_cie_ID) :
    '''
    Arguments
    ----------
    boursorama_cie_ID : str 
        Found in COMPANIES table  
        
    Returns
    ----------  
    dict 
        a dictionnary of streaming data
    '''
    
    url = f'https://www.boursorama.com/bourse/action/graph/ws/GetTicksEOD?symbol={boursorama_cie_ID}&length=1&period=0&guid='
    
    dict_streaming = {}
    
    response = requests.get(url)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json['d']['QuoteTab'][-1]
        date = decode_datetime(str(data['d']))
        dict_streaming['Day'] = date
        dict_streaming['Opening'] = data['o']
        dict_streaming['Highest'] = data['h']
        dict_streaming['Lowest'] = data['l']
        dict_streaming['Closing'] = data['c']
        dict_streaming['Volume'] = data['v']
        return dict_streaming


def fetch_today_history(boursorama_cie_ID) :
    '''
    Arguments
    ----------
    boursorama_cie_ID : str 
        Found in COMPANIES table  
        
    Returns
    ----------  
    dict 
        a dictionnary of the recalculed (by boursorama) data of the day 
    '''

    url = f'https://www.boursorama.com/bourse/action/graph/ws/GetTicksEOD?symbol={boursorama_cie_ID}&length=1&period=0&guid='

        
    dict_result_history = {}

    response = requests.get(url)
    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
        data = response_json['d']['qd']
        day = data['d']
        day_formatee = get_date(day)
        dict_result_history['Day'] = day_formatee
        dict_result_history['Opening'] = data['o']
        dict_result_history['Highest'] = data['h']
        dict_result_history['Lowest'] = data['l']
        dict_result_history['Closing'] = data['c']
        dict_result_history['Volume'] = data['v']
        return dict_result_history
