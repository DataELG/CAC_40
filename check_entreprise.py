import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
from bs4 import BeautifulSoup
import re
import sqlalchemy as sa
from sqlalchemy import create_engine, MetaData, text
import pyodbc 
import os



def fetch_url(url, headers=None, timeout=10, max_retries=3, backoff_factor=0.3):
    # Créer une session pour maintenir les connexions ouvertes et gérer les retries
    session = requests.Session()
    
    # Configurer les retries avec gestion de l'attente exponentielle
    retry = Retry(
        total=max_retries,
        read=max_retries,
        connect=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504]
    )
    
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    # Ajouter des en-têtes par défaut si non spécifiés
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
    
    try:
        # Effectuer la requête
        response = session.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Vérifier si le statut est 200 (OK)
        return BeautifulSoup(response.content, 'html.parser') # Retourner le contenu de la réponse
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")
        return None
    
def  insert_data(table_name) :

    pwd = os.getenv('PASSWORD_SQL')
    driver = os.getenv('DRIVER')
    params = f"Driver={{{driver}}};Server=tcp:servercac40.database.windows.net,1433;Database=cac40;Uid=CloudSAf5a7adf6;Pwd={pwd};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
    engine_azure = create_engine(conn_str,echo=True) 
    try:
        with engine_azure.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Connexion réussie !")
    except Exception as e:
        print(f"Erreur lors de la connexion : {e}")
        
    # cursor = connection_string.cursor()
    # cursor.execute("SELECT * FROM COMPANIES") 
    # row = cursor.fetchone() 
    # while row:
    #     print (row) 
    #     row = cursor.fetchone()
    # cursor.close()
    # connection_string.close()
    
insert_data('test')

cie_list = []
for i in range(1,3) :
    url = f'https://www.boursorama.com/bourse/actions/cotations/page-{i}?quotation_az_filter%5Bmarket%5D=1rPCAC'
    bsObj = fetch_url(url)
    if bsObj :
        if bsObj.find('tbody', class_='c-table__body') :    
            table = bsObj.find('tbody', class_='c-table__body') 
            companies = table.find_all('tr')
            for cie in companies :
                cie_details = cie.find('a')
                name = cie_details['title']
                id_tag = cie_details['href']
                cie_list.append(name)
                if id_tag : 
                    match = re.search(r'/cours/([^/]+)/', id_tag)
                    if match :
                        id = match.group(1)
                        print(id)  
print(len(cie_list))
print(sorted(cie_list))